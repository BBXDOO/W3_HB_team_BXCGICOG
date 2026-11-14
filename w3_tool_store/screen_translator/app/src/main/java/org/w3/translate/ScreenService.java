package org.w3.translate;

import android.app.*;
import android.content.*;
import android.content.pm.ServiceInfo;
import android.content.res.Configuration;
import android.graphics.*;
import android.hardware.display.*;
import android.media.*;
import android.media.projection.*;
import android.os.*;
import android.provider.Settings;
import android.view.*;
import android.widget.*;
import com.google.mlkit.vision.common.InputImage;
import com.google.mlkit.vision.text.*;
import com.google.mlkit.vision.text.latin.TextRecognizerOptions;
import com.google.mlkit.vision.text.chinese.ChineseTextRecognizerOptions;
import com.google.mlkit.vision.text.japanese.JapaneseTextRecognizerOptions;
import com.google.mlkit.nl.translate.*;
import com.google.android.gms.tasks.*;
import java.nio.ByteBuffer;
import java.util.*;

/** One consent token, one VirtualDisplay, one OCR/translation job at a time. */
public class ScreenService extends Service {
    public static volatile boolean running;
    private final Handler main=new Handler(Looper.getMainLooper());
    private MediaProjection projection;
    private VirtualDisplay display;
    private ImageReader images;
    private WindowManager wm;
    private LinearLayout controls,actionHost,actionRow;
    private int actionCount;
    private String statusText="";
    private WindowManager.LayoutParams controlParams;
    private FrameLayout subtitles;
    private View reading,selection;
    private TextView state;
    private TextRecognizer recognizer;
    private final Map<String,Translator> translators=new HashMap<>();
    private final LinkedHashMap<String,String> cache=new LinkedHashMap<>();
    private final List<Piece> latest=new ArrayList<>();
    private String source="auto";
    private int screenW,screenH,captureW,captureH;
    private boolean busy,paused,hidden,expanded,readerMode,dead,selecting;
    private RectF region=new RectF(0,0,1,1);
    private int generation;
    private int captureAttempts;
    private long lastCapture;
    private final Runnable tick=()->capture(false);
    private final Runnable watch=this::watchFrame;
    private final int[] reference=new int[48*64];
    private boolean watching, moved;
    private AlertDialog saveDialog;
    private final java.util.concurrent.ExecutorService storage=java.util.concurrent.Executors.newSingleThreadExecutor();
    private static final int LIMIT=40;
    private static final int READER_LIMIT=200;
    private static class Piece {
        final String original,language;final Rect box;String translated;
        Piece(String t,String l,Rect r){original=t;language=l;box=r;}
    }
    @Override public IBinder onBind(Intent i){return null;}
    @Override public int onStartCommand(Intent i,int flags,int id){
        if(i==null || "stop".equals(i.getAction())){stopSelf();return START_NOT_STICKY;}
        if(running)return START_NOT_STICKY;
        try {
            NotificationManager nm=getSystemService(NotificationManager.class);
            nm.createNotificationChannel(new NotificationChannel("translate","แปลหน้าจอ",NotificationManager.IMPORTANCE_LOW));
            PendingIntent stop=PendingIntent.getService(this,0,new Intent(this,ScreenService.class).setAction("stop"),PendingIntent.FLAG_IMMUTABLE);
            PendingIntent home=PendingIntent.getActivity(this,1,new Intent(this,MainActivity.class),PendingIntent.FLAG_IMMUTABLE);
            Notification n=new Notification.Builder(this,"translate").setSmallIcon(R.drawable.ic_translate).setContentTitle("W3 แปลหน้าจอกำลังทำงาน").setContentText("แตะหยุดเพื่อปิดการอ่านหน้าจอ").setContentIntent(home).setOngoing(true).addAction(new Notification.Action.Builder(null,"หยุดแปล",stop).build()).build();
            if(Build.VERSION.SDK_INT>=29)startForeground(8,n,ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION);else startForeground(8,n);
            if(!Settings.canDrawOverlays(this))throw new IllegalStateException("ยังไม่ได้อนุญาตปุ่มลอย");
            source=i.getStringExtra("source");if(source==null)source="auto";
            readerMode=i.getBooleanExtra("reader",false);paused=readerMode;
            wm=(WindowManager)getSystemService(WINDOW_SERVICE);
            android.util.DisplayMetrics metrics=new android.util.DisplayMetrics();wm.getDefaultDisplay().getRealMetrics(metrics);
            screenW=metrics.widthPixels;screenH=metrics.heightPixels;
            float scale=Math.min(1f,1080f/screenW);captureW=Math.round(screenW*scale);captureH=Math.round(screenH*scale);
            images=ImageReader.newInstance(captureW,captureH,PixelFormat.RGBA_8888,3);
            MediaProjectionManager pm=(MediaProjectionManager)getSystemService(MEDIA_PROJECTION_SERVICE);
            Intent consent=Build.VERSION.SDK_INT>=33?i.getParcelableExtra("data",Intent.class):i.getParcelableExtra("data");
            projection=pm.getMediaProjection(i.getIntExtra("code",Activity.RESULT_CANCELED),consent);
            if(projection==null)throw new IllegalStateException("ไม่ได้รับสิทธิ์จับภาพ กรุณาเริ่มใหม่");
            projection.registerCallback(new MediaProjection.Callback(){
                @Override public void onStop(){stopSelf();}
                @Override public void onCapturedContentResize(int w,int h){
                    // A fresh user session is required for a changed capture geometry.
                    if(w>0 && h>0 && Math.abs((double)w/h-(double)screenW/screenH)>.05){toast("ขนาดหน้าจอเปลี่ยน กรุณาเปิด W3 แล้วเริ่มแปลใหม่");stopSelf();}
                }
                @Override public void onCapturedContentVisibilityChanged(boolean visible){
                    if(!visible){paused=true;if(subtitles!=null)invalidateFrame();status("หน้าจอที่เลือกไม่แสดงอยู่ • พักแล้ว");}
                }
            },main);
            display=projection.createVirtualDisplay("W3Translate",captureW,captureH,metrics.densityDpi,DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,images.getSurface(),null,main);
            recognizer="en".equals(source)?TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS):"zh".equals(source)?TextRecognition.getClient(new ChineseTextRecognizerOptions.Builder().build()):TextRecognition.getClient(new JapaneseTextRecognizerOptions.Builder().build());
            for(String lang:new String[]{"en","zh","ja"})translators.put(lang,Translation.getClient(new TranslatorOptions.Builder().setSourceLanguage(lang).setTargetLanguage("th").build()));
            setupOverlays();running=true;
            status(readerMode?"พร้อม • กดอ่านส่วนที่เห็น":"พร้อม • กำลังอ่านหน้าจอ");
            if(!paused)main.postDelayed(tick,1500);
        }catch(Exception e){toast("เริ่มแปลไม่ได้ กรุณาตรวจสิทธิ์แล้วกดเริ่มใหม่");stopSelf();}
        return START_NOT_STICKY;
    }
    private WindowManager.LayoutParams params(int w,int h,boolean touch){
        WindowManager.LayoutParams p=new WindowManager.LayoutParams(w,h,WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE | WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN | (touch?0:WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE),PixelFormat.TRANSLUCENT);
        p.gravity=Gravity.TOP|Gravity.LEFT;
        if(Build.VERSION.SDK_INT>=30)p.setFitInsetsTypes(0);
        return p;
    }
    private void setupOverlays(){
        subtitles=new FrameLayout(this);
        WindowManager.LayoutParams subs=params(-1,-1,false);
        // Android 12+ passes touches through untrusted overlays only below the
        // system obscuring-opacity threshold. Use a lower window-wide alpha.
        subs.alpha=Build.VERSION.SDK_INT>=31
            ?Math.min(.75f,getSystemService(android.hardware.input.InputManager.class).getMaximumObscuringOpacityForTouch())
            :.75f;
        subtitles.setVisibility(View.INVISIBLE);
        wm.addView(subtitles,subs);
        controls=Ui.column(this,0);controls.setClipChildren(false);controls.setClipToPadding(false);
        controlParams=params(Ui.dp(this,68),-2,true);controlParams.gravity=Gravity.TOP|Gravity.LEFT;controlParams.x=screenW-Ui.dp(this,76);controlParams.y=Ui.dp(this,140);
        wm.addView(controls,controlParams);rebuildControls();
    }
    private void rebuildControls(){
        controls.removeAllViews();actionCount=0;
        int padding=Ui.dp(this,expanded?14:0);controls.setPadding(padding,padding,padding,padding);
        if(expanded)SoftControls.surface(controls,25,Ui.BG,Ui.EDGE);else{controls.setBackground(null);controls.setLayerType(View.LAYER_TYPE_NONE,null);}
        TextView handle=Ui.text(this,expanded?"ไทย   ·   ลากย้าย    ⌃":"ไทย",14);
        handle.setGravity(Gravity.CENTER);handle.setTextColor(Ui.INK);handle.setIncludeFontPadding(false);handle.setPadding(0,0,0,0);Ui.bold(handle);
        SoftControls.surface(handle,26,expanded?Ui.PANEL:0xff27222c,expanded?Ui.EDGE:Ui.ROSE);
        controls.addView(handle,new LinearLayout.LayoutParams(-1,Ui.dp(this,expanded?38:48)));
        handle.setContentDescription("เมนูแปลภาษา แตะเพื่อเปิดหรือย่อ ลากเพื่อย้าย");
        handle.setOnClickListener(v->{expanded=!expanded;rebuildControls();});
        handle.setOnTouchListener(new View.OnTouchListener(){float x,y;int sx,sy;boolean moved;
            public boolean onTouch(View v,android.view.MotionEvent e){
                switch(e.getAction()){
                    case MotionEvent.ACTION_DOWN:x=e.getRawX();y=e.getRawY();sx=controlParams.x;sy=controlParams.y;moved=false;return true;
                    case MotionEvent.ACTION_MOVE:float dx=e.getRawX()-x,dy=e.getRawY()-y;if(Math.abs(dx)+Math.abs(dy)>Ui.dp(ScreenService.this,8))moved=true;if(moved){controlParams.x=Math.max(0,Math.min(screenW-controls.getWidth(),sx+(int)dx));controlParams.y=Math.max(Ui.dp(ScreenService.this,30),Math.min(screenH-Ui.dp(ScreenService.this,70),sy+(int)dy));wm.updateViewLayout(controls,controlParams);}return true;
                    case MotionEvent.ACTION_UP:if(!moved)v.performClick();return true;
                    default:return true;
                }
            }
        });
        int menuHeight=0;
        if(expanded){
            state=Ui.text(this,statusText.isEmpty()?(paused?"พักการแปล":"แปลอัตโนมัติ"):statusText,12);
            state.setTextColor(paused?Ui.AMBER:SoftControls.GREEN);state.setGravity(Gravity.CENTER);state.setMaxLines(2);
            controls.addView(state,new LinearLayout.LayoutParams(-1,Ui.dp(this,40)));
            ScrollView menu=new ScrollView(this);menu.setFillViewport(false);menu.setClipToPadding(false);
            actionHost=Ui.column(this,0);actionHost.setClipChildren(false);menu.addView(actionHost);
            int cardHeight=Ui.dp(this,Math.max(80,58*getResources().getConfiguration().fontScale));
            menuHeight=Math.min((cardHeight+Ui.dp(this,6))*3,Math.max(Ui.dp(this,100),screenH-Ui.dp(this,170)));
            controls.addView(menu,new LinearLayout.LayoutParams(-1,menuHeight));
            control(paused?"อัตโนมัติ":"พักการแปล",paused?"play":"pause",!paused,false,()->{paused=!paused;generation++;main.removeCallbacks(tick);status(paused?"พักการแปล":"แปลอัตโนมัติ");if(!paused){readerMode=false;removeReading();main.postDelayed(tick,300);}rebuildControls();});
            control("แปลครั้งเดียว","once",false,false,()->{paused=true;readerMode=false;removeReading();rebuildControls();capture(true);});
            control("อ่านส่วนที่เห็น","book",false,false,()->{
                if(busy)return;
                paused=true;readerMode=true;hidden=false;expanded=false;
                rebuildControls();capture(true);
            });
            control("เลือกพื้นที่","crop",false,false,this::chooseRegion);
            control(hidden?"แสดงคำแปล":"ซ่อนคำแปล",hidden?"show":"hide",false,false,()->{hidden=!hidden;generation++;if(subtitles!=null)subtitles.setVisibility(hidden || reading!=null || subtitles.getChildCount()==0?View.INVISIBLE:View.VISIBLE);if(reading!=null)reading.setVisibility(hidden?View.INVISIBLE:View.VISIBLE);rebuildControls();if(!hidden){if(!readerMode && watching){main.removeCallbacks(watch);main.post(watch);}schedule();}});
            control("ปิดตัวแปล","stop",false,true,this::stopSelf);
        }else state=null;
        int width=Ui.dp(this,expanded?244:68);
        controlParams.x+=controlParams.width-width;controlParams.width=width;
        controlParams.x=Math.max(0,Math.min(controlParams.x,screenW-width));
        int panelHeight=expanded?menuHeight+Ui.dp(this,106):Ui.dp(this,48);
        controlParams.y=Math.max(Ui.dp(this,30),Math.min(controlParams.y,screenH-panelHeight-Ui.dp(this,16)));
        wm.updateViewLayout(controls,controlParams);
    }
    private void control(String text,String icon,boolean active,boolean destructive,Runnable action){
        if(actionCount++%2==0){actionRow=new LinearLayout(this);actionRow.setClipChildren(false);actionHost.addView(actionRow,new LinearLayout.LayoutParams(-1,-2));}
        Button b=SoftControls.button(this,text,icon,active,destructive);
        int height=Ui.dp(this,Math.max(80,58*getResources().getConfiguration().fontScale));
        LinearLayout.LayoutParams cell=new LinearLayout.LayoutParams(0,height,1);cell.setMargins(Ui.dp(this,3),Ui.dp(this,3),Ui.dp(this,3),Ui.dp(this,3));
        actionRow.addView(b,cell);b.setOnClickListener(v->action.run());
    }
    private void status(String s){statusText=s;if(state!=null)state.setText(s);}
    private void toast(String s){Toast.makeText(this,s,Toast.LENGTH_LONG).show();}
    private void schedule(){if(!dead && !paused && !hidden && !selecting){main.removeCallbacks(tick);main.postDelayed(tick,moved?200:2200);}}
    private void capture(boolean once){
        if(dead || busy || selecting)return;
        if(hidden){status("ซ่อนอยู่ • กดแสดงก่อนแปล");return;}
        if(!once && paused)return;
        busy=true;moved=false;stopWatching();captureAttempts=0;int job=++generation;
        latest.clear();subtitles.removeAllViews();removeReading();
        controls.setVisibility(View.INVISIBLE);subtitles.setVisibility(View.INVISIBLE);if(reading!=null)reading.setVisibility(View.INVISIBLE);
        // Drain old frames, then wait for composition with our windows hidden.
        try(Image old=images.acquireLatestImage()){}catch(Exception ignored){}
        lastCapture=System.nanoTime();
        main.postDelayed(()->readFrame(job),250);
    }
    private void readFrame(int job){
        if(dead || job!=generation){finishJob();return;}
        Image frame=null;Bitmap bitmap=null;
        try {
            frame=images.acquireLatestImage();
            if(frame==null || frame.getTimestamp()<lastCapture){
                if(++captureAttempts<8){main.postDelayed(()->readFrame(job),100);return;}
                status("ยังอ่านภาพไม่ได้ • ลองแปลใหม่");finishJob();return;
            }
            Image.Plane p=frame.getPlanes()[0];int stride=p.getPixelStride(),row=p.getRowStride();
            int padded=captureW+(row-stride*captureW)/stride;
            Bitmap full=Bitmap.createBitmap(padded,captureH,Bitmap.Config.ARGB_8888);ByteBuffer buffer=p.getBuffer();full.copyPixelsFromBuffer(buffer);
            bitmap=Bitmap.createBitmap(full,0,0,captureW,captureH);if(bitmap!=full)full.recycle();
            for(int y=0;y<64;y++)for(int x=0;x<48;x++){
                reference[y*48+x]=bitmap.getPixel(sample(x,48,captureW),sample(y,64,captureH));
            }
        }catch(Exception e){status("จับภาพไม่สำเร็จ • ลองเริ่มใหม่");finishJob();return;}
        finally{if(frame!=null)frame.close();}
        restoreWindows();
        if(!readerMode){watching=true;main.postDelayed(watch,120);}
        final Bitmap owned=bitmap;
        status("กำลังอ่านข้อความ…");
        recognizer.process(InputImage.fromBitmap(owned,0)).addOnSuccessListener(text->{
            if(dead || job!=generation){finishJob();return;}
            List<Piece> pieces=new ArrayList<>();
            for(Text.TextBlock block:text.getTextBlocks()){
                StringBuilder raw=new StringBuilder();Rect box=null;
                for(Text.Line line:block.getLines()){
                    Rect lineBox=line.getBoundingBox();String value=line.getText().trim();
                    if(lineBox==null || !LanguagePolicy.screenContent(value) || !region.contains(lineBox.exactCenterX()/captureW,lineBox.exactCenterY()/captureH)){
                        addPiece(pieces,raw,box);box=null;continue;
                    }
                    if(raw.length()>0)raw.append('\n');raw.append(value);
                    if(box==null)box=new Rect(lineBox);else box.union(lineBox);
                }
                addPiece(pieces,raw,box);
                if(pieces.size()>=pieceLimit())break;
            }
            if(pieces.isEmpty()){latest.clear();subtitles.removeAllViews();removeReading();status("ไม่พบข้อความ • อาจเล็กหรือป้องกันจับภาพ");toastIfReader("ไม่พบข้อความที่อ่านได้");finishJob();return;}
            pieces.sort(Comparator.comparingInt((Piece p)->p.box.top).thenComparingInt(p->p.box.left));
            status("กำลังแปล "+pieces.size()+" ส่วน…");translate(pieces,job);
        }).addOnFailureListener(e->{status("อ่านข้อความไม่สำเร็จ • ลองใหม่");toastIfReader("อ่านข้อความไม่สำเร็จ");finishJob();}).addOnCompleteListener(t->owned.recycle());
    }
    private int pieceLimit(){return readerMode?READER_LIMIT:LIMIT;}
    private void addPiece(List<Piece> pieces,StringBuilder raw,Rect box){
        if(box!=null && raw.length()>0 && pieces.size()<pieceLimit()){String value=raw.toString();pieces.add(new Piece(value,LanguagePolicy.source(value,source),new Rect(box)));}
        raw.setLength(0);
    }
    private void translate(List<Piece> pieces,int job){
        List<Task<String>> tasks=new ArrayList<>();
        List<LanguagePolicy.ProtectedText> inputs=new ArrayList<>();
        for(Piece p:pieces){
            String hit=cache.get(p.language+":"+p.original);
            LanguagePolicy.ProtectedText input=hit==null?new LanguagePolicy.ProtectedText(p.original):null;
            inputs.add(input);
            tasks.add(input==null?Tasks.forResult(hit):translators.get(p.language).translate(input.input));
        }
        Tasks.whenAllComplete(tasks).addOnCompleteListener(done->{
            if(dead || job!=generation){finishJob();return;}
            int failures=0,protectedValues=0;
            for(int i=0;i<pieces.size();i++){
                Piece p=pieces.get(i);Task<String> t=tasks.get(i);
                if(t.isSuccessful()){
                    String value=t.getResult();
                    if(value!=null && inputs.get(i)!=null)value=inputs.get(i).restore(value);
                    if(value!=null && LanguagePolicy.preservesNumbers(p.original,value)){p.translated=value;cache.put(p.language+":"+p.original,p.translated);}
                    else{p.translated=p.original;protectedValues++;}
                }else{p.translated="[แปลไม่สำเร็จ — กลับไปเตรียมชุดภาษา]\n"+p.original;failures++;}
            }
            while(cache.size()>256)cache.remove(cache.keySet().iterator().next());
            if(!readerMode && changedFrame()){invalidateFrame();finishJob();return;}
            latest.clear();latest.addAll(pieces);
            if(readerMode)showReading();else drawSubtitles();
            status(failures>0?"บางส่วนแปลไม่ได้ • เตรียมชุดภาษาใหม่":"แปลแล้ว "+pieces.size()+" ส่วน"+(pieces.size()==pieceLimit()?" • ถึงขีดจำกัด ลองเลือกพื้นที่":""));
            if(failures==0 && protectedValues>0)status("คงต้นฉบับ "+protectedValues+" ส่วน เพื่อรักษาตัวเลขและชื่อเฉพาะ");
            if(failures>0){paused=true;toast("บางส่วนแปลไม่ได้ กลับไปกดดาวน์โหลด / ตรวจชุดภาษาใน W3");}
            finishJob();
        });
    }
    private static int sample(int index,int count,int size){
        return (index*size+size/2)/count;
    }
    private void stopWatching(){
        watching=false;
        main.removeCallbacks(watch);
    }
    private void invalidateFrame(){
        moved=true;
        generation++;
        stopWatching();
        latest.clear();
        subtitles.removeAllViews();
        status(paused?"ภาพเปลี่ยน • กดแปลใหม่":"ภาพเปลี่ยน • กำลังจัดตำแหน่งใหม่");
        if(!busy)schedule();
    }
    private void watchFrame(){
        if(!watching || dead || hidden || selecting || readerMode)return;
        if(changedFrame())invalidateFrame();
        else main.postDelayed(watch,120);
    }
    private boolean changedFrame(){
        try(Image image=images.acquireLatestImage()){
            if(image==null)return false;
            Image.Plane plane=image.getPlanes()[0];
            ByteBuffer pixels=plane.getBuffer();
            List<Rect> masked=new ArrayList<>();
            addMask(masked,controls);
            for(int i=0;i<subtitles.getChildCount();i++)addMask(masked,subtitles.getChildAt(i));
            int tested=0,changed=0;
            for(int row=4;row<62;row++)for(int col=0;col<48;col++){
                int x=sample(col,48,captureW),y=sample(row,64,captureH);
                int sx=sample(col,48,screenW),sy=sample(row,64,screenH);
                boolean covered=false;
                for(Rect r:masked)if(r.contains(sx,sy)){covered=true;break;}
                if(covered)continue;
                int offset=y*plane.getRowStride()+x*plane.getPixelStride();
                int previous=reference[row*48+col];
                int delta=Math.abs((pixels.get(offset)&255)-Color.red(previous))
                    +Math.abs((pixels.get(offset+1)&255)-Color.green(previous))
                    +Math.abs((pixels.get(offset+2)&255)-Color.blue(previous));
                tested++;
                if(delta>105)changed++;
            }
            return tested>0 && changed>=Math.max(16,tested/30);
        }catch(RuntimeException e){return false;}
    }
    private static void addMask(List<Rect> masks,View view){
        if(!view.isShown() || view.getWidth()==0 || view.getHeight()==0)return;
        int[] location=new int[2];
        view.getLocationOnScreen(location);
        Rect rect=new Rect(location[0],location[1],location[0]+view.getWidth(),location[1]+view.getHeight());
        rect.inset(-4,-4);
        masks.add(rect);
    }
    private void toastIfReader(String s){if(readerMode)toast(s);}
    private void drawSubtitles(){
        subtitles.removeAllViews();
        for(Piece p:latest){
            if(p.original.equals(p.translated) || p.translated.startsWith("[แปลไม่สำเร็จ"))continue;
            TextView label=Ui.text(this,p.translated,14);label.setTextColor(Color.WHITE);label.setBackground(Ui.round(0xff102d28,Ui.dp(this,5)));label.setPadding(Ui.dp(this,5),Ui.dp(this,3),Ui.dp(this,5),Ui.dp(this,3));
            int x=Math.round((float)p.box.left/captureW*screenW),y=Math.round((float)p.box.top/captureH*screenH);
            int width=Math.min(screenW-x,Math.round((float)p.box.width()/captureW*screenW));
            if(width<=0 || y>=screenH)continue;
            int maxHeight=Math.min(screenH-y,Math.round((float)p.box.height()/captureH*screenH));
            if(maxHeight<=0)continue;
            label.setTextSize(12);
            label.measure(View.MeasureSpec.makeMeasureSpec(width,View.MeasureSpec.EXACTLY),
                View.MeasureSpec.makeMeasureSpec(0,View.MeasureSpec.UNSPECIFIED));
            if(label.getMeasuredHeight()>maxHeight)continue;
            FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(width,maxHeight);lp.leftMargin=x;lp.topMargin=y;subtitles.addView(label,lp);
        }
        subtitles.setVisibility(hidden || subtitles.getChildCount()==0?View.INVISIBLE:View.VISIBLE);
    }
    private void showReading(){
        removeReading();subtitles.setVisibility(View.INVISIBLE);
        LinearLayout page=Ui.column(this,18);page.setBackground(Ui.round(Ui.BG,Ui.dp(this,20)));
        LinearLayout buttons=new LinearLayout(this);
        Button close=Ui.button(this,"กลับไปเลื่อนต้นทาง");
        buttons.addView(close,new LinearLayout.LayoutParams(0,-2,1));
        close.setOnClickListener(v->{removeReading();status("เลื่อนต้นทาง แล้วกดอ่านส่วนที่เห็นอีกครั้ง");});
        Button copy=Ui.button(this,"คัดลอกไทย");buttons.addView(copy,new LinearLayout.LayoutParams(0,-2,1));copy.setOnClickListener(v->{StringBuilder s=new StringBuilder();for(Piece p:latest)s.append(p.translated).append("\n\n");((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE)).setPrimaryClip(ClipData.newPlainText("คำแปลไทย",s.toString()));toast("คัดลอกแล้ว");});page.addView(buttons);
        Button save=Ui.button(this,"บันทึกเข้าเรื่อง · เปิดอ่านย้อนหลัง");page.addView(save);
        save.setOnClickListener(v->saveReading());
        ScrollView scroll=new ScrollView(this);LinearLayout body=Ui.column(this,4);scroll.addView(body);page.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
        body.addView(Ui.text(this,"คำแปลของส่วนที่มองเห็น · เลื่อนในกรอบเพื่ออ่านผล",14));
        for(Piece p:latest){body.addView(Ui.text(this,p.translated,21));TextView original=Ui.text(this,p.original,14);original.setTextColor(Ui.MUTED);body.addView(original);}
        WindowManager.LayoutParams rp=params(-1,(int)(screenH*.7),true);rp.gravity=Gravity.BOTTOM|Gravity.LEFT;
        reading=page;wm.addView(page,rp);
    }
    private void saveReading(){
        if(saveDialog!=null || latest.isEmpty())return;
        List<Piece> snapshot=new ArrayList<>(latest);
        String[] categories={"คู่มือ","หนังสือ","เกม","อื่น ๆ"};
        LinearLayout form=Ui.column(this,18);
        EditText name=new EditText(new ContextThemeWrapper(this,android.R.style.Theme_Material));
        name.setSingleLine(true);
        name.setHint("ชื่อเรื่องเดิม หรือชื่อเรื่องใหม่");
        name.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(120)});
        android.content.SharedPreferences recent=getSharedPreferences("screen-reading",MODE_PRIVATE);
        name.setText(recent.getString("title",""));
        form.addView(name);
        Spinner category=new Spinner(this);
        category.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,categories));
        category.setSelection(Math.min(categories.length-1,recent.getInt("category",0)));
        form.addView(category);
        saveDialog=new AlertDialog.Builder(this,android.R.style.Theme_Material_Dialog_Alert)
            .setTitle("บันทึกคำแปลจากหน้าจอ")
            .setMessage("ใช้ชื่อและหมวดเดิมเพื่อเติมส่วนใหม่ในเรื่องเดิม")
            .setView(form).setNegativeButton("ยกเลิก",null).setPositiveButton("บันทึก",null).create();
        saveDialog.setOnDismissListener(d->saveDialog=null);
        saveDialog.getWindow().setType(WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY);
        saveDialog.show();
        saveDialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v->{
            String title=name.getText().toString().trim().replaceAll("\\s+"," ");
            if(title.isEmpty()){name.setError("กรอกชื่อเรื่อง");return;}
            Article a=new Article();
            a.title=title;a.language=snapshot.get(0).language;a.savedAt=System.currentTimeMillis();
            int selected=category.getSelectedItemPosition();
            a.url="screen:"+android.net.Uri.encode(categories[selected])+"/"+android.net.Uri.encode(title.toLowerCase(Locale.ROOT));
            a.notice="เก็บข้อความที่อ่านได้จากหน้าจอ · เรียงตามส่วนที่บันทึก";
            for(Piece piece:snapshot){
                Article.Block block=new Article.Block(a.blocks.isEmpty()?"section":"paragraph",0,piece.original);
                if(!piece.original.equals(piece.translated) && !piece.translated.startsWith("[แปลไม่สำเร็จ"))block.thai=piece.translated;
                a.blocks.add(block);
            }
            AlertDialog submitting=saveDialog;
            submitting.getButton(AlertDialog.BUTTON_POSITIVE).setEnabled(false);
            storage.execute(()->{
                ArticleStore store=new ArticleStore(this);
                try{
                    store.mergeScreen(a);
                    recent.edit().putString("title",title).putInt("category",selected).apply();
                    main.post(()->{if(!dead){if(saveDialog==submitting)submitting.dismiss();toast("บันทึกแล้ว · เปิดได้จากสารบัญในแอป");}});
                }catch(RuntimeException e){
                    main.post(()->{if(!dead){if(saveDialog==submitting)submitting.getButton(AlertDialog.BUTTON_POSITIVE).setEnabled(true);toast("บันทึกไม่สำเร็จ");}});
                }finally{store.close();}
            });
        });
    }
    private void removeReading(){if(reading!=null){try{wm.removeView(reading);}catch(Exception ignored){}reading=null;}}
    private void restoreWindows(){if(dead)return;controls.setVisibility(View.VISIBLE);subtitles.setVisibility(hidden || reading!=null || subtitles.getChildCount()==0?View.INVISIBLE:View.VISIBLE);if(reading!=null)reading.setVisibility(hidden?View.INVISIBLE:View.VISIBLE);}
    private void finishJob(){busy=false;restoreWindows();schedule();}
    private void chooseRegion(){
        if(busy){status("รอแปลรอบนี้เสร็จก่อน");return;}
        paused=true;selecting=true;generation++;stopWatching();latest.clear();subtitles.removeAllViews();main.removeCallbacks(tick);controls.setVisibility(View.INVISIBLE);subtitles.setVisibility(View.INVISIBLE);removeReading();
        selection=new View(this){final Paint paint=new Paint(3);float x0,y0,x1,y1;boolean down;
            @Override protected void onDraw(Canvas c){
                c.drawColor(0x55203028);paint.setColor(Color.WHITE);paint.setTextSize(Ui.dp(ScreenService.this,19));c.drawText("ลากกรอบพื้นที่แปล • แตะครั้งเดียว = ทั้งจอ",Ui.dp(ScreenService.this,16),Ui.dp(ScreenService.this,90),paint);
                if(down){paint.setStyle(Paint.Style.STROKE);paint.setStrokeWidth(Ui.dp(ScreenService.this,3));c.drawRect(Math.min(x0,x1),Math.min(y0,y1),Math.max(x0,x1),Math.max(y0,y1),paint);paint.setStyle(Paint.Style.FILL);}
            }
            @Override public boolean onTouchEvent(android.view.MotionEvent e){
                if(e.getAction()==MotionEvent.ACTION_DOWN){x0=x1=e.getX();y0=y1=e.getY();down=true;invalidate();return true;}
                if(e.getAction()==MotionEvent.ACTION_MOVE){x1=e.getX();y1=e.getY();invalidate();return true;}
                if(e.getAction()==MotionEvent.ACTION_UP || e.getAction()==MotionEvent.ACTION_CANCEL){
                    x1=e.getX();y1=e.getY();if(Math.abs(x1-x0)<Ui.dp(ScreenService.this,25)||Math.abs(y1-y0)<Ui.dp(ScreenService.this,25))region=new RectF(0,0,1,1);else region=new RectF(Math.min(x0,x1)/screenW,Math.min(y0,y1)/screenH,Math.max(x0,x1)/screenW,Math.max(y0,y1)/screenH);
                    wm.removeView(selection);selection=null;selecting=false;restoreWindows();status("เลือกแล้ว • กดแปลครั้งเดียวหรืออัตโนมัติ");return true;
                }return true;
            }
        };wm.addView(selection,params(-1,-1,true));
    }
    @Override public void onConfigurationChanged(Configuration c){super.onConfigurationChanged(c);toast("หน้าจอหมุนแล้ว เปิด W3 และเริ่มแปลใหม่");stopSelf();}
    @Override public void onDestroy(){
        dead=true;running=false;generation++;main.removeCallbacksAndMessages(null);
        if(saveDialog!=null)saveDialog.dismiss();storage.shutdown();
        for(View v:new View[]{controls,subtitles,reading,selection})if(v!=null && wm!=null)try{wm.removeView(v);}catch(Exception ignored){}
        if(display!=null)display.release();if(images!=null)images.close();if(projection!=null)projection.stop();
        if(recognizer!=null)recognizer.close();for(Translator t:translators.values())t.close();cache.clear();latest.clear();
        stopForeground(STOP_FOREGROUND_REMOVE);super.onDestroy();
    }
}
