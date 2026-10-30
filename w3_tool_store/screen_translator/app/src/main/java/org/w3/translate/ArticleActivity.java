package org.w3.translate;

import android.app.*;
import android.content.*;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Bundle;
import android.text.InputType;
import android.view.*;
import android.widget.*;
import com.google.android.gms.tasks.Tasks;
import com.google.mlkit.common.model.DownloadConditions;
import com.google.mlkit.nl.translate.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.regex.*;

/** Link import and local reading do not need overlay or screen-capture permissions. */
public class ArticleActivity extends Activity {
    private static final int EXPORT=72;
    private static final String[] CODES={"en","zh","ja","th"};
    private final ExecutorService worker=Executors.newSingleThreadExecutor();
    private final AtomicBoolean cancel=new AtomicBoolean();
    private ArticleStore store;
    private LinearLayout root;
    private TextView status;
    private ListView list;
    private Button fetch,translate,stop;
    private Spinner source,display;
    private EditText link;
    private Article article;
    private volatile boolean closed,busy;
    private boolean returnToList;
    private volatile Thread activeWorker;
    private int viewMode=2;
    private long exportId;
    private int exportView;
    private BlockAdapter blocks;
    @Override public void onCreate(Bundle state){
        super.onCreate(state);store=new ArticleStore(this);
        if(state!=null){viewMode=state.getInt("view",2);exportId=state.getLong("exportId");exportView=state.getInt("exportView",2);long id=state.getLong("article");if(id>0){open(id);return;}}
        home(state==null?sharedLink(getIntent()):state.getString("link",sharedLink(getIntent())));
    }
    @Override protected void onNewIntent(Intent i){super.onNewIntent(i);setIntent(i);if(!busy)home(sharedLink(i));}
    private static String sharedLink(Intent i){
        String text=i.getStringExtra(Intent.EXTRA_TEXT);if(text==null)return "";
        Matcher m=Pattern.compile("https://[^\\s<>\"]+",Pattern.CASE_INSENSITIVE).matcher(text);
        return m.find()?m.group():text;
    }
    private void screen(String title){
        root=Ui.column(this,16);root.setBackgroundColor(Ui.BG);setContentView(root);
        root.setOnApplyWindowInsetsListener((v,in)->{root.setPadding(Ui.dp(this,16),in.getSystemWindowInsetTop()+Ui.dp(this,8),Ui.dp(this,16),in.getSystemWindowInsetBottom()+Ui.dp(this,8));return in;});
        TextView heading=Ui.text(this,title,23);Ui.bold(heading);root.addView(heading);
        status=Ui.text(this,"",13);root.addView(status);
    }
    private void ui(Runnable r){runOnUiThread(()->{if(!closed&&!isDestroyed()&&!isFinishing())r.run();});}
    private void message(String text){ui(()->status.setText(text));}
    private void run(Runnable action){busy=true;cancel.set(false);worker.execute(()->{activeWorker=Thread.currentThread();try{if(!cancel.get())action.run();}catch(RuntimeException e){message("ดำเนินการไม่สำเร็จ ตรวจพื้นที่ว่างในเครื่องแล้วลองใหม่");}finally{activeWorker=null;busy=false;ui(()->{if(returnToList&&article!=null){returnToList=false;remember();home("");return;}if(fetch!=null)fetch.setEnabled(true);if(translate!=null)translate.setEnabled(true);if(source!=null)source.setEnabled(true);if(stop!=null)stop.setVisibility(View.GONE);});}});}
    private void home(String incoming){
        article=null;fetch=null;translate=null;source=null;stop=null;
        screen("บทความของฉัน");
        link=new EditText(this);link.setSingleLine(true);link.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_URI);link.setHint("วางลิงก์ HTTPS ของบทความ");link.setText(incoming);root.addView(link);
        fetch=Ui.button(this,"ดึงและบันทึกบทความลงเครื่อง");root.addView(fetch);fetch.setEnabled(!busy);fetch.setOnClickListener(v->importLink());
        root.addView(Ui.text(this,"เก็บข้อความจากหน้านี้พร้อมหัวข้อ ไม่ดึงลิงก์ต่อ ไม่รวมรูป/PDF; เว็บที่ต้องล็อกอินหรือโหลดด้วย JavaScript อาจดึงไม่ครบ",12));
        LinearLayout searchRow=new LinearLayout(this);root.addView(searchRow);
        EditText search=new EditText(this);search.setSingleLine(true);search.setHint("ค้นชื่อ ต้นฉบับ หรือคำแปล");searchRow.addView(search,new LinearLayout.LayoutParams(0,-2,1));
        Button find=Ui.button(this,"ค้น");searchRow.addView(find);find.setOnClickListener(v->loadList(search.getText().toString()));
        list=new ListView(this);list.setDividerHeight(Ui.dp(this,8));root.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        loadList("");
    }
    private void loadList(String query){
        if(busy)return;
        run(()->{try{List<Article> rows=store.list(query);ui(()->{
            status.setText(rows.isEmpty()?"ยังไม่มีบทความที่ตรงกับการค้นหา · บันทึกแล้วเปิดอ่านออฟไลน์ได้":"บันทึกในเครื่อง "+rows.size()+" บทความ · แตะเพื่ออ่าน");
            list.setAdapter(new ArrayAdapter<Article>(this,android.R.layout.simple_list_item_2,android.R.id.text1,rows){
                @Override public View getView(int pos,View old,ViewGroup parent){View v=super.getView(pos,old,parent);Article a=getItem(pos);((TextView)v.findViewById(android.R.id.text1)).setText(a.title);((TextView)v.findViewById(android.R.id.text2)).setText(a.url);return v;}
            });
            list.setOnItemClickListener((p,v,pos,id)->{if(!busy)open(rows.get(pos).id);});
        });}catch(Exception e){message("อ่านรายการไม่ได้ กรุณาตรวจพื้นที่ว่างในเครื่องแล้วเปิดใหม่");}});
    }
    private void importLink(){
        if(busy)return;String input=link.getText().toString();fetch.setEnabled(false);status.setText("กำลังดึงและจัดหัวข้อ…");
        run(()->{try{
            String url=ArticleFetcher.url(input);long existing=store.find(url);
            if(existing>0){ui(()->open(existing));return;}
            Article a=ArticleFetcher.fetch(url);long redirected=store.find(a.url);
            long id=redirected>0?redirected:store.save(a);ui(()->open(id));
        }catch(Exception e){message(e instanceof ArticleFetcher.ReadException&&e.getMessage()!=null?e.getMessage():"บันทึกไม่สำเร็จ ตรวจอินเทอร์เน็ตและพื้นที่ว่าง แล้วลองใหม่");}});
    }
    private void open(long id){
        // Queued after any importing transaction; render only after the full document is loaded.
        worker.execute(()->{try{Article a=store.load(id);int position=store.scroll(id);ui(()->{if(a==null){home("");return;}article=a;reader(position);});}catch(Exception e){message("เปิดบทความไม่ได้ กรุณาลองใหม่");}});
    }
    private void reader(int position){
        fetch=null;translate=null;source=null;stop=null;
        screen("อ่านบทความ");
        LinearLayout actions=new LinearLayout(this);root.addView(actions);
        Button back=Ui.button(this,"รายการ");actions.addView(back,new LinearLayout.LayoutParams(0,-2,1));back.setOnClickListener(v->leaveReader());
        Button toc=Ui.button(this,"สารบัญ");actions.addView(toc,new LinearLayout.LayoutParams(0,-2,1));toc.setOnClickListener(v->contents());
        Button more=Ui.button(this,"เพิ่มเติม");actions.addView(more,new LinearLayout.LayoutParams(0,-2,1));more.setOnClickListener(v->more());
        display=new Spinner(this);display.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"ต้นฉบับ","ไทย","ต้นฉบับคู่ไทย"}));display.setSelection(viewMode);root.addView(display);
        display.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){public void onNothingSelected(AdapterView<?> p){}public void onItemSelected(AdapterView<?> p,View v,int pos,long id){viewMode=pos;if(blocks!=null)blocks.notifyDataSetChanged();}});
        LinearLayout languages=new LinearLayout(this);root.addView(languages);
        source=new Spinner(this);source.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"อังกฤษ → ไทย","จีน → ไทย","ญี่ปุ่น → ไทย","ต้นฉบับไทย"}));
        int selected=Arrays.asList(CODES).indexOf(article.language);source.setSelection(Math.max(0,selected));languages.addView(source,new LinearLayout.LayoutParams(0,-2,1));
        translate=Ui.button(this,"แปล / แปลต่อ");languages.addView(translate);translate.setOnClickListener(v->askTranslate());
        stop=Ui.button(this,"พักการแปล · เก็บส่วนที่แปลแล้ว");root.addView(stop);stop.setVisibility(View.GONE);stop.setOnClickListener(v->pauseTranslation());
        list=new ListView(this);list.setDividerHeight(Ui.dp(this,8));root.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        blocks=new BlockAdapter();list.setAdapter(blocks);list.setSelection(Math.min(position,article.blocks.size()));
        progress("บันทึกแล้ว · อ่านออฟไลน์ได้");
    }
    private void progress(String prefix){status.setText(prefix+" · แปล "+article.translated()+"/"+article.translatable()+" ส่วน");}
    private void askTranslate(){
        if(busy||article==null)return;String code=CODES[source.getSelectedItemPosition()];
        if(code.equals("th")){status.setText("บทความภาษาไทย เลือกดูต้นฉบับได้เลย");return;}
        boolean reset=!code.equals(article.language)&&article.translated()>0;
        new AlertDialog.Builder(this).setTitle(reset?"เปลี่ยนภาษาต้นฉบับและแปลใหม่?":"แปลบทความเป็นไทย?")
            .setMessage((reset?"จะเปลี่ยนคำแปลเดิมของบทความนี้ ต้นฉบับยังอยู่ครบ\n\n":"")+"ตรวจภาษาต้นฉบับที่เลือกก่อนเริ่ม ครั้งแรกอาจดาวน์โหลดชุดภาษาผ่านอินเทอร์เน็ต หลังจากนั้นแปลในเครื่องได้\n\nหากออกจากหน้านี้ การแปลจะพัก และกลับมาแปลต่อได้")
            .setNegativeButton("ไว้ก่อน",null).setPositiveButton("เริ่มแปล",(d,w)->translate(code,reset)).show();
    }
    private void translate(String code,boolean reset){
        translate.setEnabled(false);source.setEnabled(false);stop.setVisibility(View.VISIBLE);progress("กำลังเตรียมชุดภาษา…");Article a=article;
        run(()->{
            Translator t=null;
            try{
                store.language(a.id,code,reset);a.language=code;
                if(reset)for(Article.Block b:a.blocks)b.thai="";
                t=Translation.getClient(new TranslatorOptions.Builder().setSourceLanguage(code).setTargetLanguage("th").build());
                Tasks.await(t.downloadModelIfNeeded(new DownloadConditions.Builder().build()),10,TimeUnit.MINUTES);
                for(int i=0;i<a.blocks.size();i++){
                    if(cancel.get()||closed||Thread.currentThread().isInterrupted())break;
                    Article.Block b=a.blocks.get(i);if(!b.translatable()||!b.thai.isEmpty())continue;
                    StringBuilder translated=new StringBuilder();
                    for(String chunk:Article.chunks(b.original,1500)){
                        if(cancel.get()||closed||Thread.currentThread().isInterrupted())break;
                        if(translated.length()>0)translated.append('\n');
                        translated.append(Tasks.await(t.translate(chunk),90,TimeUnit.SECONDS));
                    }
                    if(cancel.get()||closed||Thread.currentThread().isInterrupted())break;
                    String thai=translated.toString();store.translate(a.id,i,thai);b.thai=thai;
                    ui(()->{if(article==a){progress("กำลังแปลและบันทึก…");blocks.notifyDataSetChanged();}});
                }
                ui(()->{if(article==a){progress(cancel.get()?"พักแล้ว · กดแปลต่อได้":"แปลเสร็จ · เปิดอ่านออฟไลน์ได้");blocks.notifyDataSetChanged();}});
            }catch(Exception e){message("พักการแปลแล้ว ต้นฉบับและคำแปลที่เสร็จยังอยู่ · ตรวจชุดภาษา/อินเทอร์เน็ต แล้วกดแปลต่อ");}
            finally{if(t!=null)t.close();}
        });
    }
    private void contents(){
        List<String> labels=new ArrayList<>();List<Integer> positions=new ArrayList<>();
        for(int i=0;i<article.blocks.size();i++){Article.Block b=article.blocks.get(i);if(b.kind.equals("heading")){String name=viewMode==0||b.thai.isEmpty()?b.original:b.thai;labels.add(String.join("",Collections.nCopies(Math.max(0,b.level-1),"  "))+name);positions.add(i+1);}}
        if(labels.isEmpty()){new AlertDialog.Builder(this).setMessage("หน้านี้ไม่มีหัวข้อที่เว็บระบุไว้ จัดข้อความตามลำดับเดิมแล้ว").setPositiveButton("ตกลง",null).show();return;}
        new AlertDialog.Builder(this).setTitle("สารบัญ").setItems(labels.toArray(new String[0]),(d,w)->list.setSelection(positions.get(w))).setNegativeButton("ปิด",null).show();
    }
    private void more(){
        new AlertDialog.Builder(this).setTitle("บทความนี้").setItems(new String[]{"ส่งออกเป็น Markdown (แบบที่กำลังอ่าน)","เปิดเว็บต้นฉบับ","ลบบทความจากเครื่อง"},(d,w)->{
            if(w==0){exportId=article.id;exportView=viewMode;Intent i=new Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("text/markdown");i.putExtra(Intent.EXTRA_TITLE,article.title.replaceAll("[\\\\/:*?\"<>|]","_").substring(0,Math.min(70,article.title.length()))+".md");try{startActivityForResult(i,EXPORT);}catch(ActivityNotFoundException e){status.setText("ไม่พบแอปเลือกไฟล์สำหรับส่งออก");}}
            if(w==1){try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(article.url)));}catch(ActivityNotFoundException e){status.setText("ไม่พบเบราว์เซอร์");}}
            if(w==2){if(busy){status.setText("กรุณาพักการแปลให้เสร็จก่อนลบบทความ");return;}long id=article.id;new AlertDialog.Builder(this).setTitle("ลบบทความนี้?").setMessage("จะลบต้นฉบับและคำแปลที่บันทึกไว้ในเครื่อง").setNegativeButton("ยกเลิก",null).setPositiveButton("ลบ",(x,y)->run(()->{store.delete(id);ui(()->home(""));})).show();}
        }).show();
    }
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request!=EXPORT)return;long id=exportId;int mode=exportView;exportId=0;
        if(result!=RESULT_OK||data==null||data.getData()==null||id==0)return;Uri uri=data.getData();
        worker.execute(()->{try{Article saved=store.load(id);if(saved==null)throw new IOException();try(OutputStream out=getContentResolver().openOutputStream(uri,"wt")){if(out==null)throw new IOException();out.write(saved.markdown(mode).getBytes(StandardCharsets.UTF_8));}message("ส่งออกเอกสารแล้ว");}catch(Exception e){message("ส่งออกไม่ได้ ต้นฉบับในแอปยังอยู่ กรุณาเลือกตำแหน่งใหม่");}});
    }
    private void remember(){if(article!=null&&list!=null){long id=article.id;int pos=list.getFirstVisiblePosition();worker.execute(()->store.scroll(id,pos));}}
    private void pauseTranslation(){cancel.set(true);Thread t=activeWorker;if(t!=null)t.interrupt();status.setText("กำลังพัก เก็บคำแปลที่เสร็จแล้วไว้ในเครื่อง…");}
    private void leaveReader(){
        if(busy){returnToList=true;pauseTranslation();return;}
        remember();home("");
    }
    @Override public void onBackPressed(){if(article!=null){leaveReader();return;}super.onBackPressed();}
    @Override protected void onPause(){remember();super.onPause();}
    @Override protected void onStop(){if(busy&&article!=null)pauseTranslation();super.onStop();}
    @Override protected void onSaveInstanceState(Bundle out){super.onSaveInstanceState(out);out.putInt("view",viewMode);if(article!=null)out.putLong("article",article.id);if(link!=null)out.putString("link",link.getText().toString());out.putLong("exportId",exportId);out.putInt("exportView",exportView);}
    @Override protected void onDestroy(){closed=true;cancel.set(true);Thread t=activeWorker;if(t!=null)t.interrupt();worker.execute(()->store.close());worker.shutdown();super.onDestroy();}
    private final class BlockAdapter extends BaseAdapter {
        public int getCount(){return article.blocks.size()+1;}
        public Object getItem(int p){return p==0?article:article.blocks.get(p-1);}
        public long getItemId(int p){return p;}
        public View getView(int pos,View recycled,ViewGroup parent){
            LinearLayout card=Ui.column(ArticleActivity.this,12);card.setBackground(Ui.round(0xffffffff,Ui.dp(ArticleActivity.this,12)));
            if(pos==0){TextView title=Ui.text(ArticleActivity.this,article.title,23);Ui.bold(title);card.addView(title);card.addView(Ui.text(ArticleActivity.this,article.url+"\nบันทึก "+android.text.format.DateFormat.format("dd/MM/yyyy HH:mm",article.savedAt),12));card.addView(Ui.text(ArticleActivity.this,article.notice+"\nคำแปลอัตโนมัติ · บล็อกโค้ดคงต้นฉบับ · ตารางจัดเป็นข้อความแยกแถว",12));if(article.language.equals("unknown"))card.addView(Ui.text(ArticleActivity.this,"ตรวจภาษา: เลือกอังกฤษ จีน หรือญี่ปุ่นก่อนแปล",15));return card;}
            Article.Block b=article.blocks.get(pos-1);boolean code=b.kind.equals("code");int size=b.kind.equals("heading")?Math.max(18,27-b.level*2):17;
            String prefix=b.kind.equals("list")?"• ":"";
            if(viewMode!=1||code){TextView text=Ui.text(ArticleActivity.this,prefix+b.original,size);text.setTextIsSelectable(true);if(code)text.setTypeface(Typeface.MONOSPACE);if(b.kind.equals("heading"))Ui.bold(text);card.addView(text);}
            if(viewMode!=0&&!code){TextView thai=Ui.text(ArticleActivity.this,prefix+(b.thai.isEmpty()?"[ยังไม่แปล] "+(viewMode==1?b.original:""):b.thai),size);thai.setTextColor(Ui.GREEN);thai.setTextIsSelectable(true);if(b.kind.equals("heading"))Ui.bold(thai);card.addView(thai);}
            return card;
        }
    }
}
