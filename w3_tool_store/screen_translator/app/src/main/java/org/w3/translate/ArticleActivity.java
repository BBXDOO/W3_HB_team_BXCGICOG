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
    private String website="",section="",query="",filter="";
    private boolean sectionOpen;
    private int listRequest;

    private static final class IndexEntry {
        final String title, detail, kind, status;
        final int accent;
        final Runnable open;

        IndexEntry(String title,String detail,String kind,String status,int accent,Runnable open){
            this.title=title;this.detail=detail;this.kind=kind;this.status=status;this.accent=accent;this.open=open;
        }
    }
    private volatile boolean closed,busy;
    private boolean returnToList;
    private volatile Thread activeWorker;
    private int viewMode=2;
    private long exportId;
    private int exportView;
    private BlockAdapter blocks;
    private boolean editingNote;
    private EditText noteTitle,noteOriginal,noteThai;
    private static final int NOTE_LIMIT=200_000;
    private String[] retainedNote;
    @Override public void onCreate(Bundle state){
        super.onCreate(state);store=new ArticleStore(this);
        retainedNote=(String[])getLastNonConfigurationInstance();
        if(state!=null){
            website=state.getString("website","");section=state.getString("section","");
            sectionOpen=state.getBoolean("sectionOpen");query=state.getString("query","");filter=state.getString("filter","");
            viewMode=state.getInt("view",2);exportId=state.getLong("exportId");exportView=state.getInt("exportView",2);long id=state.getLong("article");if(id>0){open(id);return;}}
        if(state!=null?state.getBoolean("newNote"):getIntent().getBooleanExtra("newNote",false)){
            editNote(null);return;
        }
        home(state==null?sharedLink(getIntent()):state.getString("link",sharedLink(getIntent())));
    }
    @Override protected void onNewIntent(Intent i){super.onNewIntent(i);setIntent(i);if(!busy){website="";sectionOpen=false;query="";filter="";home(sharedLink(i));}}
    private static String sharedLink(Intent i){
        String text=i.getStringExtra(Intent.EXTRA_TEXT);if(text==null)return "";
        Matcher m=Pattern.compile("https://[^\\s<>\"]+",Pattern.CASE_INSENSITIVE).matcher(text);
        return m.find()?m.group():text;
    }
    private void screen(String title){
        root=Ui.column(this,16);root.setBackgroundColor(Ui.BG);setContentView(root);
        root.setOnApplyWindowInsetsListener((v,in)->{root.setPadding(Ui.dp(this,16),in.getSystemWindowInsetTop()+Ui.dp(this,8),Ui.dp(this,16),in.getSystemWindowInsetBottom()+Ui.dp(this,8));return in;});
        TextView heading=Ui.text(this,title,23);Ui.bold(heading);root.addView(heading);
        status=Ui.text(this,"",13);status.setTextColor(Ui.MUTED);root.addView(status);
    }
    private void ui(Runnable r){runOnUiThread(()->{if(!closed&&!isDestroyed()&&!isFinishing())r.run();});}
    private void message(String text){ui(()->status.setText(text));}
    private void run(Runnable action){busy=true;cancel.set(false);worker.execute(()->{activeWorker=Thread.currentThread();try{if(!cancel.get())action.run();}catch(RuntimeException e){message("ดำเนินการไม่สำเร็จ ตรวจพื้นที่ว่างในเครื่องแล้วลองใหม่");}finally{activeWorker=null;busy=false;ui(()->{if(returnToList&&article!=null){returnToList=false;remember();home("");return;}if(fetch!=null)fetch.setEnabled(true);if(translate!=null)translate.setEnabled(true);if(source!=null)source.setEnabled(true);if(stop!=null)stop.setVisibility(View.GONE);});}});}
    private void home(String incoming){
        editingNote=false;article=null;fetch=null;translate=null;source=null;stop=null;
        screen(website.isEmpty()?"สารบัญ":sectionOpen?sectionName(section):website);
        if(website.isEmpty()){
            LinearLayout importPanel=Ui.column(this,8);
            importPanel.setBackground(Ui.surface(this,Ui.PANEL,18,Ui.EDGE));
            link=new EditText(this);link.setSingleLine(true);link.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_URI);link.setHint("วางลิงก์ HTTPS ของบทความ");link.setText(incoming);importPanel.addView(link);
            LinearLayout actions=new LinearLayout(this);importPanel.addView(actions);
            fetch=Ui.button(this,"ดึงและบันทึก");actions.addView(fetch,new LinearLayout.LayoutParams(0,-2,1));
            fetch.setOnClickListener(v->importLink(link.getText().toString()));
            Button bookmark=Ui.button(this,"เก็บลิงก์ไว้อ่าน");actions.addView(bookmark,new LinearLayout.LayoutParams(0,-2,1));
            bookmark.setOnClickListener(v->bookmark());
            Button note=Ui.button(this,"วางข้อความ / Markdown");importPanel.addView(note);
            note.setOnClickListener(v->{if(!busy)editNote(null);});
            Button add=Ui.button(this,"+ เพิ่มเข้าคลัง");root.addView(add);root.addView(importPanel);
            importPanel.setVisibility(incoming.isEmpty()?View.GONE:View.VISIBLE);
            if(!incoming.isEmpty())add.setText("ย่อส่วนเพิ่มเข้าคลัง");
            add.setOnClickListener(v->{
                boolean expand=importPanel.getVisibility()!=View.VISIBLE;
                importPanel.setVisibility(expand?View.VISIBLE:View.GONE);
                add.setText(expand?"ย่อส่วนเพิ่มเข้าคลัง":"+ เพิ่มเข้าคลัง");
            });
        }else{
            TextView path=Ui.text(this,sectionOpen?"สารบัญ / "+website:"สารบัญ / เว็บไซต์",13);
            path.setTextColor(Ui.MUTED);root.addView(path);
            Button up=Ui.button(this,sectionOpen?"กลับไปยัง "+website:"เว็บไซต์ทั้งหมด");
            root.addView(up);up.setOnClickListener(v->leaveIndex());
        }
        LinearLayout searchRow=new LinearLayout(this);root.addView(searchRow);
        EditText search=new EditText(this);search.setSingleLine(true);search.setHint("ค้นชื่อ ลิงก์ หรือเนื้อหา");search.setText(query);
        searchRow.addView(search,new LinearLayout.LayoutParams(0,-2,1));
        Button find=Ui.button(this,"ค้น");searchRow.addView(find);
        list=new ListView(this);list.setDivider(null);list.setDividerHeight(0);
        if(website.isEmpty()){
            Spinner category=new Spinner(this);
            List<String> filters=Arrays.asList("ทุกหมวด","บทความจากลิงก์","คู่มือ","หนังสือ","เกม","อื่น ๆ","บันทึกข้อความ");
            category.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,filters));
            category.setSelection(Math.max(0,filters.indexOf(filter)));
            root.addView(category);
            category.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){
                public void onNothingSelected(AdapterView<?> parent){}
                public void onItemSelected(AdapterView<?> parent,View view,int pos,long id){
                    String selected=pos==0?"":filters.get(pos);
                    if(!selected.equals(filter)){filter=selected;query=search.getText().toString().trim();loadList();}
                }
            });
        }
        root.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        find.setOnClickListener(v->{query=search.getText().toString().trim();loadList();});
        loadList();
    }

    private void leaveIndex(){
        if(sectionOpen)sectionOpen=false;
        else website="";
        home("");
    }

    private static String sectionName(String name){return name.isEmpty()?"ยังไม่จัดหมวด":name;}

    private void loadList(){
        final ListView target=list;
        final int request=++listRequest;
        final String term=query,site=website,selectedSection=section,selectedFilter=filter;
        final boolean inSection=sectionOpen;
        worker.execute(()->{
            try{
                List<Article> rows=store.list(term);
                List<IndexEntry> entries=new ArrayList<>();
                Map<String,Integer> groups=new TreeMap<>();
                for(Article row:rows){
                    if(!selectedFilter.isEmpty()&&!selectedFilter.equals(row.category()))continue;
                    if(site.isEmpty()&&!row.fromScreen()&&!row.fromNote()){
                        groups.merge(row.website(),1,Integer::sum);
                    }else if(site.isEmpty()){
                        entries.add(articleEntry(row));
                    }else if(site.equals(row.website())){
                        if(!inSection)groups.merge(row.webSection,1,Integer::sum);
                        else if(selectedSection.equals(row.webSection))entries.add(articleEntry(row));
                    }
                }
                List<IndexEntry> index=new ArrayList<>();
                groups.forEach((name,count)->index.add(new IndexEntry(site.isEmpty()?name:sectionName(name),
                    count+" หน้า",site.isEmpty()?"เว็บไซต์":"หมวดในเว็บไซต์","",site.isEmpty()?Ui.CYAN:Ui.AMBER,()->{
                        if(site.isEmpty()){website=name;sectionOpen=false;}
                        else{section=name;sectionOpen=true;}
                        home("");
                    })));
                index.addAll(entries);
                ui(()->{
                    if(list!=target||article!=null||request!=listRequest)return;
                    if(!busy)status.setText(index.isEmpty()?"ไม่พบรายการ":site.isEmpty()
                        ?groups.size()+" เว็บไซต์  •  "+entries.size()+" รายการที่บันทึกแยก"
                        :inSection?entries.size()+" หน้าในหมวด":groups.size()+" หมวดในเว็บไซต์");
                    target.setAdapter(new ArrayAdapter<IndexEntry>(this,android.R.layout.simple_list_item_2,android.R.id.text1,index){
                        @Override public View getView(int position,View recycled,ViewGroup parent){
                            return indexCard(getItem(position));
                        }
                    });
                    target.setOnItemClickListener((p,v,pos,id)->{if(!busy)index.get(pos).open.run();});
                });
            }catch(RuntimeException e){
                ui(()->{if(list==target&&request==listRequest)status.setText("อ่านสารบัญไม่ได้ กรุณาลองใหม่");});
            }
        });
    }

    private View indexCard(IndexEntry item){
        LinearLayout frame=Ui.column(this,0);
        frame.setPadding(0,0,0,Ui.dp(this,8));
        LinearLayout card=Ui.column(this,12);
        card.setBackground(Ui.surface(this,Ui.PANEL,17,Ui.EDGE));
        frame.addView(card);
        TextView kind=Ui.text(this,item.kind,12);kind.setTextColor(item.accent);Ui.bold(kind);card.addView(kind);
        TextView title=Ui.text(this,item.title,18);Ui.bold(title);card.addView(title);
        TextView detail=Ui.text(this,item.detail,13);detail.setTextColor(Ui.MUTED);card.addView(detail);
        if(!item.status.isEmpty())card.addView(Ui.text(this,item.status,13));
        return frame;
    }

    private IndexEntry articleEntry(Article row){
        String kind=row.fromNote()?"บันทึกข้อความ":row.fromScreen()?row.category():
            row.linkOnly()?"ลิงก์ไว้อ่าน":"บทความจากเว็บ";
        int accent=row.fromNote()?Ui.VIOLET:row.fromScreen()?Ui.AMBER:Ui.CYAN;
        String date=android.text.format.DateFormat.format("dd/MM/yyyy",row.savedAt).toString();
        String detail=row.fromNote()||row.fromScreen()?"บันทึก "+date:row.url+"\nบันทึก "+date;
        String status=row.linkOnly()?"รอดึงเนื้อหา":"th".equals(row.language)?"ต้นฉบับภาษาไทย":
            row.fromNote()?(row.indexTranslated==0?"เก็บต้นฉบับ":"มีคำแปล"):
            row.indexParts==0?"เก็บต้นฉบับ":row.indexTranslated==0?"ยังไม่แปล":
            row.indexTranslated==row.indexParts?"มีคำแปลครบ":"มีคำแปล "+row.indexTranslated+"/"+row.indexParts+" ส่วน";
        return new IndexEntry(row.title,detail,kind,status,accent,()->open(row.id));
    }

    private void bookmark(){
        if(busy)return;
        String input=link.getText().toString();
        run(()->{try{
            String url=ArticleFetcher.url(input);
            long id=store.find(url);
            if(id==0){
                Article saved=new Article();
                saved.url=url;saved.title=url;saved.language="pending";saved.savedAt=System.currentTimeMillis();
                id=store.save(saved);
            }
            final long savedId=id;
            ui(()->open(savedId));
        }catch(IOException e){message(e.getMessage());}});
    }

    private void importLink(String input){
        if(busy)return;
        if(fetch!=null)fetch.setEnabled(false);
        status.setText("กำลังดึงและจัดหัวข้อ…");
        run(()->{try{
            String url=ArticleFetcher.url(input);
            Article existing=store.load(store.find(url));
            long id=existing!=null&&!existing.linkOnly()?existing.id:store.saveFetched(url,ArticleFetcher.fetch(url));
            ui(()->open(id));
        }catch(Exception e){message(e instanceof ArticleFetcher.ReadException&&e.getMessage()!=null?e.getMessage():"บันทึกไม่สำเร็จ ตรวจอินเทอร์เน็ตและพื้นที่ว่าง แล้วลองใหม่");}});
    }
    private void open(long id){
        LinearLayout target=root;
        // Queued after any importing transaction; render only after the full document is loaded.
        worker.execute(()->{try{Article a=store.load(id);int position=store.scroll(id);ui(()->{if(root!=target)return;if(a==null){home("");return;}if(a.fromNote())editNote(a);else{article=a;reader(position);}});}catch(Exception e){message("เปิดบทความไม่ได้ กรุณาลองใหม่");}});
    }
    private void editNote(Article saved){
        article=saved;editingNote=true;fetch=null;stop=null;list=null;
        screen("วางข้อความ / Markdown");
        noteTitle=new EditText(this);
        noteTitle.setHint("ชื่อบันทึก");noteTitle.setSingleLine(true);
        noteTitle.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(120)});
        root.addView(noteTitle);
        source=new Spinner(this);
        source.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,
            new String[]{"อังกฤษ → ไทย","จีน → ไทย","ญี่ปุ่น → ไทย"}));
        root.addView(source);
        noteOriginal=noteEditor("วางหรือพิมพ์ต้นฉบับ");
        noteThai=noteEditor("คำแปลภาษาไทย · แก้ไขได้");
        Spinner tabs=new Spinner(this);
        tabs.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,
            new String[]{"ต้นฉบับ","คำแปล"}));
        root.addView(tabs);
        root.addView(noteOriginal,new LinearLayout.LayoutParams(-1,0,1));
        root.addView(noteThai,new LinearLayout.LayoutParams(-1,0,1));
        noteThai.setVisibility(View.GONE);
        tabs.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){
            public void onNothingSelected(AdapterView<?> parent){}
            public void onItemSelected(AdapterView<?> parent,View view,int pos,long id){
                noteOriginal.setVisibility(pos==0?View.VISIBLE:View.GONE);
                noteThai.setVisibility(pos==1?View.VISIBLE:View.GONE);
            }
        });
        if(saved!=null){
            noteTitle.setText(saved.title);noteOriginal.setText(saved.blocks.get(0).original);
            noteThai.setText(saved.blocks.get(0).thai);
            source.setSelection(Math.max(0,Arrays.asList(CODES).indexOf(saved.language)));
        }
        LinearLayout actions=new LinearLayout(this);root.addView(actions);
        translate=Ui.button(this,"แปลเป็นไทย");actions.addView(translate,new LinearLayout.LayoutParams(0,-2,1));
        translate.setOnClickListener(v->{
            if(busy)return;
            if(noteThai.length()>0){
                new AlertDialog.Builder(this).setMessage("แทนที่คำแปลที่กำลังแก้ไขด้วยผลแปลใหม่?")
                    .setNegativeButton("ยกเลิก",null).setPositiveButton("แปลใหม่",(d,w)->translateNote(tabs)).show();
            }else translateNote(tabs);
        });
        Button save=Ui.button(this,"บันทึก");actions.addView(save,new LinearLayout.LayoutParams(0,-2,1));
        save.setOnClickListener(v->saveNote(-1));
        LinearLayout fileActions=new LinearLayout(this);root.addView(fileActions);
        Button code=Ui.button(this,"ครอบเป็นบล็อกโค้ด");
        fileActions.addView(code,new LinearLayout.LayoutParams(0,-2,1));
        code.setOnClickListener(v->{
            if(busy)return;
            EditText editor=tabs.getSelectedItemPosition()==0?noteOriginal:noteThai;
            int start=Math.max(0,editor.getSelectionStart()),end=Math.max(0,editor.getSelectionEnd());
            if(start==end){start=0;end=editor.length();}
            String wrapped=NoteMarkdown.codeBlock(editor.getText().subSequence(Math.min(start,end),Math.max(start,end)).toString());
            if(editor.length()-Math.abs(end-start)+wrapped.length()>NOTE_LIMIT){status.setText("ข้อความยาวเกิน 200,000 ตัวอักษร");return;}
            editor.getText().replace(Math.min(start,end),Math.max(start,end),wrapped);
        });
        Button more=Ui.button(this,"ส่งออก / ลบ");
        fileActions.addView(more,new LinearLayout.LayoutParams(0,-2,1));
        more.setOnClickListener(v->{
            if(busy)return;
            String[] options=article==null?new String[]{"ส่งออกต้นฉบับ .md","ส่งออกคำแปล .md"}
                :new String[]{"ส่งออกต้นฉบับ .md","ส่งออกคำแปล .md","ลบบันทึกจากเครื่อง"};
            new AlertDialog.Builder(this).setItems(options,(d,w)->{
                if(w<2){saveNote(w);return;}
                long id=article.id;
                new AlertDialog.Builder(this).setMessage("ลบบันทึกนี้จากเครื่อง?")
                    .setNegativeButton("ยกเลิก",null).setPositiveButton("ลบ",(x,y)->run(()->{
                        store.delete(id);ui(()->home(""));
                    })).show();
            }).show();
        });
        if(retainedNote!=null){
            noteTitle.setText(retainedNote[0]);noteOriginal.setText(retainedNote[1]);noteThai.setText(retainedNote[2]);
            source.setSelection(Integer.parseInt(retainedNote[3]));retainedNote=null;
        }
        status.setText("ต้นฉบับและคำแปลแก้ได้แยกกัน · ช่องละ 200,000 ตัวอักษร");
        root.setFocusableInTouchMode(true);root.requestFocus();
    }

    private EditText noteEditor(String hint){
        EditText editor=new EditText(this);
        editor.setHint(hint);editor.setGravity(Gravity.TOP|Gravity.START);
        editor.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_FLAG_MULTI_LINE|InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS);
        editor.setTypeface(Typeface.MONOSPACE);editor.setTextSize(15);
        editor.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(NOTE_LIMIT)});
        return editor;
    }

    private void saveNote(int exportMode){
        if(busy)return;
        String original=noteOriginal.getText().toString(),thai=noteThai.getText().toString();
        if(original.trim().isEmpty()){status.setText("วางต้นฉบับก่อนบันทึก");return;}
        if(exportMode==1&&thai.trim().isEmpty()){status.setText("เพิ่มคำแปลก่อนส่งออก");return;}
        Article note=new Article();
        note.id=article==null?0:article.id;
        note.url=article==null?"note:"+UUID.randomUUID():article.url;
        note.savedAt=article==null?System.currentTimeMillis():article.savedAt;
        note.title=noteTitle.getText().toString().trim();
        if(note.title.isEmpty())note.title="บันทึกข้อความ";
        note.language=CODES[source.getSelectedItemPosition()];
        Article.Block block=new Article.Block("paragraph",0,original);block.thai=thai;note.blocks.add(block);
        run(()->{
            note.id=store.saveNote(note);
            ui(()->{
                if(!editingNote)return;
                article=note;status.setText("บันทึกแล้ว · เปิดได้จากสารบัญ");
                if(exportMode>=0)exportArticle(note,exportMode);
            });
        });
    }

    private void translateNote(Spinner tabs){
        if(busy)return;
        String input=noteOriginal.getText().toString();
        if(input.trim().isEmpty()){status.setText("วางต้นฉบับก่อนแปล");return;}
        String code=CODES[source.getSelectedItemPosition()];
        EditText originalEditor=noteOriginal,thaiEditor=noteThai;
        String previousThai=thaiEditor.getText().toString();
        source.setEnabled(false);translate.setEnabled(false);
        status.setText("กำลังเตรียมชุดภาษาและแปล…");
        run(()->{
            Translator model=Translation.getClient(new TranslatorOptions.Builder().setSourceLanguage(code).setTargetLanguage("th").build());
            try{
                Tasks.await(model.downloadModelIfNeeded(new DownloadConditions.Builder().build()),10,TimeUnit.MINUTES);
                String translated=NoteMarkdown.translate(input,part->{
                    if(cancel.get())throw new CancellationException();
                    StringBuilder result=new StringBuilder();
                    for(String chunk:Article.chunks(part,1500)){
                        try{
                            if(result.length()>0 && !Character.isWhitespace(result.charAt(result.length()-1)))result.append(' ');
                            result.append(Tasks.await(model.translate(chunk),90,TimeUnit.SECONDS));
                        }catch(Exception error){throw new IllegalStateException(error);}
                    }
                    return result.toString();
                });
                ui(()->{
                    if(!editingNote||noteOriginal!=originalEditor||cancel.get())return;
                    if(!input.contentEquals(originalEditor.getText())||!previousThai.contentEquals(thaiEditor.getText())){
                        status.setText("ข้อความถูกแก้ไขระหว่างแปล · กดแปลใหม่");return;
                    }
                    if(translated.length()>NOTE_LIMIT){status.setText("คำแปลยาวเกิน 200,000 ตัวอักษร · แบ่งต้นฉบับก่อนแปล");return;}
                    thaiEditor.setText(translated);tabs.setSelection(1);status.setText("แปลแล้ว · แก้คำแปลหรือกดบันทึก");
                });
            }catch(Exception error){if(!cancel.get())message("แปลไม่สำเร็จ · ตรวจชุดภาษาและลองอีกครั้ง");}
            finally{model.close();}
        });
    }

    private void reader(int position){
        fetch=null;translate=null;source=null;stop=null;
        screen("อ่านบทความ");
        LinearLayout actions=new LinearLayout(this);root.addView(actions);
        Button back=Ui.button(this,"รายการ");actions.addView(back,new LinearLayout.LayoutParams(0,-2,1));back.setOnClickListener(v->leaveReader());
        Button toc=Ui.button(this,"สารบัญ");actions.addView(toc,new LinearLayout.LayoutParams(0,-2,1));toc.setOnClickListener(v->contents());
        Button more=Ui.button(this,"เพิ่มเติม");actions.addView(more,new LinearLayout.LayoutParams(0,-2,1));more.setOnClickListener(v->more());
        if(!article.fromScreen()){
            Button organize=Ui.button(this,"หมวดในเว็บไซต์"+(article.webSection.isEmpty()?"":" · "+article.webSection));
            root.addView(organize);organize.setOnClickListener(v->chooseWebSection(organize));
        }
        if(article.linkOnly()){
            toc.setVisibility(View.GONE);
            root.addView(Ui.text(this,article.url,15));
            fetch=Ui.button(this,"ดึงเนื้อหาเพื่ออ่านและแปล");root.addView(fetch);
            fetch.setOnClickListener(v->importLink(article.url));
            status.setText("บันทึกลิงก์แล้ว");
            return;
        }
        display=new Spinner(this);display.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"ต้นฉบับ","ไทย","ต้นฉบับคู่ไทย"}));display.setSelection(viewMode);root.addView(display);
        display.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){public void onNothingSelected(AdapterView<?> p){}public void onItemSelected(AdapterView<?> p,View v,int pos,long id){viewMode=pos;if(blocks!=null)blocks.notifyDataSetChanged();}});
        LinearLayout languages=new LinearLayout(this);root.addView(languages);
        if(article.fromScreen())languages.setVisibility(View.GONE);
        source=new Spinner(this);source.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"อังกฤษ → ไทย","จีน → ไทย","ญี่ปุ่น → ไทย","ต้นฉบับไทย"}));
        int selected=Arrays.asList(CODES).indexOf(article.language);source.setSelection(Math.max(0,selected));languages.addView(source,new LinearLayout.LayoutParams(0,-2,1));
        translate=Ui.button(this,"แปล / แปลต่อ");languages.addView(translate);translate.setOnClickListener(v->askTranslate());
        stop=Ui.button(this,"พักการแปล · เก็บส่วนที่แปลแล้ว");root.addView(stop);stop.setVisibility(View.GONE);stop.setOnClickListener(v->pauseTranslation());
        list=new ListView(this);list.setDividerHeight(Ui.dp(this,8));root.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        blocks=new BlockAdapter();list.setAdapter(blocks);list.setSelection(Math.min(position,article.blocks.size()));
        progress("บันทึกแล้ว · อ่านออฟไลน์ได้");
    }
    private void chooseWebSection(Button button){
        if(busy)return;
        Article current=article;
        EditText name=new EditText(this);
        name.setSingleLine(true);name.setHint("เช่น อาวุธ หรือแผนที่");
        name.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(80)});
        name.setText(current.webSection);
        new AlertDialog.Builder(this).setTitle("หมวดใน "+current.website()).setView(name)
            .setNegativeButton("ยกเลิก",null).setPositiveButton("บันทึก",(d,w)->{
                String value=name.getText().toString().trim();
                run(()->{
                    store.webSection(current.id,value);
                    ui(()->{
                        current.webSection=value;
                        if(article==current)button.setText("หมวดในเว็บไซต์"+(value.isEmpty()?"":" · "+value));
                    });
                });
            }).show();
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
        for(int i=0;i<article.blocks.size();i++){Article.Block b=article.blocks.get(i);if(b.kind.equals("heading")){String name=viewMode==0||b.thai.isEmpty()?b.original:b.thai;labels.add(String.join("",Collections.nCopies(Math.max(0,b.level-1),"  "))+name);positions.add(i+1);}else if(article.fromScreen() && (i==0 || b.kind.equals("section"))){labels.add("ส่วนที่ "+(labels.size()+1)+" · "+b.original.substring(0,Math.min(70,b.original.length())).replace('\n',' '));positions.add(i+1);}}
        if(labels.isEmpty()){new AlertDialog.Builder(this).setMessage("หน้านี้ไม่มีหัวข้อที่เว็บระบุไว้ จัดข้อความตามลำดับเดิมแล้ว").setPositiveButton("ตกลง",null).show();return;}
        new AlertDialog.Builder(this).setTitle("สารบัญ").setItems(labels.toArray(new String[0]),(d,w)->list.setSelection(positions.get(w))).setNegativeButton("ปิด",null).show();
    }
    private void more(){
        new AlertDialog.Builder(this).setTitle("บทความนี้").setItems(new String[]{"ส่งออกเป็น Markdown (แบบที่กำลังอ่าน)",article.fromScreen()?"แหล่งที่มา: แปลจากหน้าจอ":"เปิดเว็บต้นฉบับ","ลบบทความจากเครื่อง"},(d,w)->{
            if(w==0)exportArticle(article,viewMode);
            if(w==1){if(article.fromScreen()){status.setText("เรื่องนี้บันทึกจากหน้าจอ");return;}try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(article.url)));}catch(ActivityNotFoundException e){status.setText("ไม่พบเบราว์เซอร์");}}
            if(w==2){if(busy){status.setText("กรุณาพักการแปลให้เสร็จก่อนลบบทความ");return;}long id=article.id;new AlertDialog.Builder(this).setTitle("ลบบทความนี้?").setMessage("จะลบต้นฉบับและคำแปลที่บันทึกไว้ในเครื่อง").setNegativeButton("ยกเลิก",null).setPositiveButton("ลบ",(x,y)->run(()->{store.delete(id);ui(()->home(""));})).show();}
        }).show();
    }
    private void exportArticle(Article document,int mode){
        exportId=document.id;exportView=mode;Intent i=new Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("text/markdown");i.putExtra(Intent.EXTRA_TITLE,document.title.replaceAll("[\\\\/:*?\"<>|]","_").substring(0,Math.min(70,document.title.length()))+".md");try{startActivityForResult(i,EXPORT);}catch(ActivityNotFoundException e){status.setText("ไม่พบแอปเลือกไฟล์สำหรับส่งออก");}
    }
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request!=EXPORT)return;long id=exportId;int mode=exportView;exportId=0;
        if(result!=RESULT_OK||data==null||data.getData()==null||id==0)return;Uri uri=data.getData();
        worker.execute(()->{try{Article saved=store.load(id);if(saved==null)throw new IOException();try(OutputStream out=getContentResolver().openOutputStream(uri,"wt")){if(out==null)throw new IOException();out.write(saved.markdown(mode).getBytes(StandardCharsets.UTF_8));}message("ส่งออกเอกสารแล้ว");}catch(Exception e){message("ส่งออกไม่ได้ ต้นฉบับในแอปยังอยู่ กรุณาเลือกตำแหน่งใหม่");}});
    }
    private void remember(){if(article!=null&&!article.linkOnly()&&list!=null){long id=article.id;int pos=list.getFirstVisiblePosition();worker.execute(()->store.scroll(id,pos));}}
    private void pauseTranslation(){cancel.set(true);Thread t=activeWorker;if(t!=null)t.interrupt();status.setText("กำลังพัก เก็บคำแปลที่เสร็จแล้วไว้ในเครื่อง…");}
    private void leaveReader(){
        if(busy){returnToList=true;pauseTranslation();return;}
        remember();home("");
    }
    @Override public void onBackPressed(){
        if(editingNote){
            if(busy)return;
            String title=noteTitle.getText().toString().trim();
            if(title.isEmpty())title="บันทึกข้อความ";
            boolean changed=article==null?!noteTitle.getText().toString().trim().isEmpty()||noteOriginal.length()>0||noteThai.length()>0
                :!title.equals(article.title)||!article.blocks.get(0).original.contentEquals(noteOriginal.getText())
                    ||!article.blocks.get(0).thai.contentEquals(noteThai.getText());
            if(changed)new AlertDialog.Builder(this).setMessage("ออกจากหน้าโดยไม่บันทึกการแก้ไข?")
                .setNegativeButton("แก้ไขต่อ",null).setPositiveButton("ออก",(d,w)->home("")).show();
            else home("");
            return;
        }
        if(article!=null){leaveReader();return;}if(!website.isEmpty()){leaveIndex();return;}super.onBackPressed();}
    @Override protected void onPause(){remember();super.onPause();}
    @Override protected void onStop(){if(busy&&article!=null&&!editingNote)pauseTranslation();super.onStop();}
    @Override protected void onSaveInstanceState(Bundle out){super.onSaveInstanceState(out);out.putBoolean("newNote",editingNote&&article==null);out.putInt("view",viewMode);out.putString("website",website);out.putString("section",section);out.putBoolean("sectionOpen",sectionOpen);out.putString("query",query);out.putString("filter",filter);if(article!=null)out.putLong("article",article.id);if(link!=null)out.putString("link",link.getText().toString());out.putLong("exportId",exportId);out.putInt("exportView",exportView);}
    @Override public Object onRetainNonConfigurationInstance(){
        return editingNote?new String[]{noteTitle.getText().toString(),noteOriginal.getText().toString(),
            noteThai.getText().toString(),Integer.toString(source.getSelectedItemPosition())}:null;
    }
    @Override protected void onDestroy(){closed=true;cancel.set(true);Thread t=activeWorker;if(t!=null)t.interrupt();worker.execute(()->store.close());worker.shutdown();super.onDestroy();}
    private final class BlockAdapter extends BaseAdapter {
        public int getCount(){return article.blocks.size()+1;}
        public Object getItem(int p){return p==0?article:article.blocks.get(p-1);}
        public long getItemId(int p){return p;}
        public View getView(int pos,View recycled,ViewGroup parent){
            LinearLayout card=Ui.column(ArticleActivity.this,12);card.setBackground(Ui.surface(ArticleActivity.this,Ui.PANEL,15,Ui.EDGE));
            if(pos==0){TextView title=Ui.text(ArticleActivity.this,article.title,23);Ui.bold(title);card.addView(title);card.addView(Ui.text(ArticleActivity.this,article.sourceLabel()+"\nบันทึก "+android.text.format.DateFormat.format("dd/MM/yyyy HH:mm",article.savedAt),12));card.addView(Ui.text(ArticleActivity.this,article.notice+"\nคำแปลอัตโนมัติ · บล็อกโค้ดคงต้นฉบับ · ตารางจัดเป็นข้อความแยกแถว",12));if(article.language.equals("unknown"))card.addView(Ui.text(ArticleActivity.this,"ตรวจภาษา: เลือกอังกฤษ จีน หรือญี่ปุ่นก่อนแปล",15));return card;}
            Article.Block b=article.blocks.get(pos-1);boolean code=b.kind.equals("code");int size=b.kind.equals("heading")?Math.max(18,27-b.level*2):17;
            if(article.fromScreen() && (pos==1 || b.kind.equals("section")))card.addView(Ui.text(ArticleActivity.this,"ส่วนที่บันทึก",13));
            String prefix=b.kind.equals("list")?"• ":"";
            if(viewMode!=1||code){TextView text=Ui.text(ArticleActivity.this,prefix+b.original,size);text.setTextIsSelectable(true);if(code)text.setTypeface(Typeface.MONOSPACE);if(b.kind.equals("heading"))Ui.bold(text);card.addView(text);}
            if(viewMode!=0&&!code){TextView thai=Ui.text(ArticleActivity.this,prefix+(b.thai.isEmpty()?"[ยังไม่แปล] "+(viewMode==1?b.original:""):b.thai),size);thai.setTextColor(Ui.GREEN);thai.setTextIsSelectable(true);if(b.kind.equals("heading"))Ui.bold(thai);card.addView(thai);}
            return card;
        }
    }
}
