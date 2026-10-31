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
    private static final int LIMIT=40;
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
                    if(!visible){paused=true;status("หน้าจอที่เลือกไม่แสดงอยู่ • พักแล้ว");}
                }
            },main);
            display=projection.createVirtualDisplay("W3Translate",captureW,captureH,metrics.densityDpi,DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,images.getSurface(),null,main);
            recognizer="en".equals(source)?TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS):"zh".equals(source)?TextRecognition.getClient(new ChineseTextRecognizerOptions.Builder().build()):TextRecognition.getClient(new JapaneseTextRecognizerOptions.Builder().build());
            for(String lang:new String[]{"en","zh","ja"})translators.put(lang,Translation.getClient(new TranslatorOptions.Builder().setSourceLanguage(lang).setTargetLanguage("th").build()));
            setupOverlays();running=true;
            status(readerMode?"พร้อม • กดแปลครั้งเดียว":"พร้อม • กำลังอ่านหน้าจอ");
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
        subs.alpha=.75f;
        wm.addView(subtitles,subs);
        controls=Ui.column(this,0);controls.setClipChildren(false);controls.setClipToPadding(false);
        controlParams=params(Ui.dp(this,48),-2,true);controlParams.gravity=Gravity.TOP|Gravity.LEFT;controlParams.x=screenW-Ui.dp(this,56);controlParams.y=Ui.dp(this,140);
        wm.addView(controls,controlParams);rebuildControls();
    }
    private void rebuildControls(){
        controls.removeAllViews();actionCount=0;
        int padding=Ui.dp(this,expanded?14:0);controls.setPadding(padding,padding,padding,padding);
        if(expanded)SoftControls.surface(controls);else{controls.setBackground(null);controls.setLayerType(View.LAYER_TYPE_NONE,null);}
        TextView handle=Ui.text(this,expanded?"ไทย   ·   ลากย้าย    ⌃":"ไทย",14);
        handle.setGravity(Gravity.CENTER);handle.setTextColor(Color.BLACK);handle.setIncludeFontPadding(false);handle.setPadding(0,0,0,0);Ui.bold(handle);
        if(!expanded)SoftControls.surface(handle);
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
            state.setTextColor(paused?0xff776134:SoftControls.GREEN);state.setGravity(Gravity.CENTER);state.setMaxLines(2);
            controls.addView(state,new LinearLayout.LayoutParams(-1,Ui.dp(this,40)));
            ScrollView menu=new ScrollView(this);menu.setFillViewport(false);menu.setClipToPadding(false);
            actionHost=Ui.column(this,0);actionHost.setClipChildren(false);menu.addView(actionHost);
            int cardHeight=Ui.dp(this,Math.max(80,58*getResources().getConfiguration().fontScale));
            menuHeight=Math.min((cardHeight+Ui.dp(this,6))*3,Math.max(Ui.dp(this,100),screenH-Ui.dp(this,170)));
            controls.addView(menu,new LinearLayout.LayoutParams(-1,menuHeight));
            control(paused?"อัตโนมัติ":"พักการแปล",paused?"play":"pause",!paused,false,()->{paused=!paused;generation++;main.removeCallbacks(tick);status(paused?"พักการแปล":"แปลอัตโนมัติ");if(!paused){readerMode=false;removeReading();main.postDelayed(tick,300);}rebuildControls();});
            control("แปลครั้งเดียว","once",false,false,()->{paused=true;readerMode=false;removeReading();rebuildControls();capture(true);});
            control("อ่านเต็มหน้า","book",false,false,()->{paused=true;readerMode=true;rebuildControls();capture(true);});
            control("เลือกพื้นที่","crop",false,false,this::chooseRegion);
            control(hidden?"แสดงคำแปล":"ซ่อนคำแปล",hidden?"show":"hide",false,false,()->{hidden=!hidden;generation++;if(subtitles!=null)subtitles.setVisibility(hidden || reading!=null?View.INVISIBLE:View.VISIBLE);if(reading!=null)reading.setVisibility(hidden?View.INVISIBLE:View.VISIBLE);rebuildControls();if(!hidden)schedule();});
            control("ปิดตัวแปล","stop",false,true,this::stopSelf);
        }else state=null;
        int width=Ui.dp(this,expanded?220:48);
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
    private void schedule(){if(!dead && !paused && !hidden && !selecting){main.removeCallbacks(tick);main.postDelayed(tick,2200);}}
    private void capture(boolean once){
        if(dead || busy || selecting)return;
        if(hidden){status("ซ่อนอยู่ • กดแสดงก่อนแปล");return;}
        if(!once && paused)return;
        busy=true;captureAttempts=0;int job=++generation;
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
        }catch(Exception e){status("จับภาพไม่สำเร็จ • ลองเริ่มใหม่");finishJob();return;}
        finally{if(frame!=null)frame.close();}
        restoreWindows();
        final Bitmap owned=bitmap;
        status("กำลังอ่านข้อความ…");
        recognizer.process(InputImage.fromBitmap(owned,0)).addOnSuccessListener(text->{
            if(dead || job!=generation){finishJob();return;}
            List<Piece> pieces=new ArrayList<>();
            for(Text.TextBlock block:text.getTextBlocks()){
                StringBuilder raw=new StringBuilder();Rect box=null;
                for(Text.Line line:block.getLines()){
                    Rect lineBox=line.getBoundingBox();String value=line.getText().trim();
                    if(lineBox==null || !LanguagePolicy.readable(value) || !region.contains(lineBox.exactCenterX()/captureW,lineBox.exactCenterY()/captureH)){
                        addPiece(pieces,raw,box);box=null;continue;
                    }
                    if(raw.length()>0)raw.append('\n');raw.append(value);
                    if(box==null)box=new Rect(lineBox);else box.union(lineBox);
                }
                addPiece(pieces,raw,box);
                if(pieces.size()>=LIMIT)break;
            }
            if(pieces.isEmpty()){latest.clear();subtitles.removeAllViews();removeReading();status("ไม่พบข้อความ • อาจเล็กหรือป้องกันจับภาพ");toastIfReader("ไม่พบข้อความที่อ่านได้");finishJob();return;}
            status("กำลังแปล "+pieces.size()+" ส่วน…");translate(pieces,job);
        }).addOnFailureListener(e->{status("อ่านข้อความไม่สำเร็จ • ลองใหม่");toastIfReader("อ่านข้อความไม่สำเร็จ");finishJob();}).addOnCompleteListener(t->owned.recycle());
    }
    private void addPiece(List<Piece> pieces,StringBuilder raw,Rect box){
        if(box!=null && raw.length()>0 && pieces.size()<LIMIT){String value=raw.toString();pieces.add(new Piece(value,LanguagePolicy.source(value,source),new Rect(box)));}
        raw.setLength(0);
    }
    private void translate(List<Piece> pieces,int job){
        List<Task<String>> tasks=new ArrayList<>();
        for(Piece p:pieces){String key=p.language+":"+p.original;String hit=cache.get(key);tasks.add(hit!=null?Tasks.forResult(hit):translators.get(p.language).translate(p.original));}
        Tasks.whenAllComplete(tasks).addOnCompleteListener(done->{
            if(dead || job!=generation){finishJob();return;}
            int failures=0,protectedValues=0;
            for(int i=0;i<pieces.size();i++){
                Piece p=pieces.get(i);Task<String> t=tasks.get(i);
                if(t.isSuccessful()){
                    String value=t.getResult();
                    if(value!=null && LanguagePolicy.preservesNumbers(p.original,value)){p.translated=value;cache.put(p.language+":"+p.original,p.translated);}
                    else{p.translated=p.original;protectedValues++;}
                }else{p.translated="[แปลไม่สำเร็จ — กลับไปเตรียมชุดภาษา]\n"+p.original;failures++;}
            }
            while(cache.size()>256)cache.remove(cache.keySet().iterator().next());
            latest.clear();latest.addAll(pieces);drawSubtitles();if(readerMode)showReading();
            status(failures>0?"บางส่วนแปลไม่ได้ • เตรียมชุดภาษาใหม่":"แปลแล้ว "+pieces.size()+" ส่วน"+(pieces.size()==LIMIT?" • ถึงขีดจำกัด ลองเลือกพื้นที่":""));
            if(failures==0 && protectedValues>0)status("คงต้นฉบับ "+protectedValues+" ส่วน เพื่อรักษาตัวเลข");
            if(failures>0){paused=true;toast("บางส่วนแปลไม่ได้ กลับไปกดดาวน์โหลด / ตรวจชุดภาษาใน W3");}
            finishJob();
        });
    }
    private void toastIfReader(String s){if(readerMode)toast(s);}
    private void drawSubtitles(){
        subtitles.removeAllViews();
        for(Piece p:latest){
            TextView label=Ui.text(this,p.translated,14);label.setTextColor(Color.WHITE);label.setBackground(Ui.round(0xff102d28,Ui.dp(this,5)));label.setPadding(Ui.dp(this,5),Ui.dp(this,3),Ui.dp(this,5),Ui.dp(this,3));
            int x=Math.round((float)p.box.left/captureW*screenW),y=Math.round((float)p.box.top/captureH*screenH);
            int width=Math.max(Ui.dp(this,86),Math.round((float)p.box.width()/captureW*screenW));width=Math.min(width,screenW-x);
            int maxHeight=Math.max(Ui.dp(this,32),Math.min(Ui.dp(this,150),screenH-y));label.setMaxHeight(maxHeight);
            FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(width,-2);lp.leftMargin=x;lp.topMargin=y;subtitles.addView(label,lp);
        }
        subtitles.setVisibility(hidden?View.INVISIBLE:View.VISIBLE);
    }
    private void showReading(){
        removeReading();subtitles.setVisibility(View.INVISIBLE);
        LinearLayout page=Ui.column(this,18);page.setBackground(Ui.round(Ui.BG,Ui.dp(this,20)));
        LinearLayout buttons=new LinearLayout(this);
        Button close=Ui.button(this,"ปิดหน้าอ่าน");buttons.addView(close,new LinearLayout.LayoutParams(0,-2,1));close.setOnClickListener(v->{removeReading();if(!hidden)subtitles.setVisibility(View.VISIBLE);});
        Button copy=Ui.button(this,"คัดลอกไทย");buttons.addView(copy,new LinearLayout.LayoutParams(0,-2,1));copy.setOnClickListener(v->{StringBuilder s=new StringBuilder();for(Piece p:latest)s.append(p.translated).append("\n\n");((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE)).setPrimaryClip(ClipData.newPlainText("คำแปลไทย",s.toString()));toast("คัดลอกแล้ว");});page.addView(buttons);
        ScrollView scroll=new ScrollView(this);LinearLayout body=Ui.column(this,4);scroll.addView(body);page.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
        body.addView(Ui.text(this,"คำแปลไทย · เทียบต้นฉบับด้านล่าง",14));
        for(Piece p:latest){body.addView(Ui.text(this,p.translated,21));TextView original=Ui.text(this,p.original,14);original.setTextColor(0xff586b62);body.addView(original);}
        WindowManager.LayoutParams rp=params(-1,(int)(screenH*.7),true);rp.gravity=Gravity.BOTTOM|Gravity.LEFT;
        reading=page;wm.addView(page,rp);
    }
    private void removeReading(){if(reading!=null){try{wm.removeView(reading);}catch(Exception ignored){}reading=null;}}
    private void restoreWindows(){if(dead)return;controls.setVisibility(View.VISIBLE);subtitles.setVisibility(hidden || reading!=null?View.INVISIBLE:View.VISIBLE);if(reading!=null)reading.setVisibility(hidden?View.INVISIBLE:View.VISIBLE);}
    private void finishJob(){busy=false;restoreWindows();schedule();}
    private void chooseRegion(){
        if(busy){status("รอแปลรอบนี้เสร็จก่อน");return;}
        paused=true;selecting=true;generation++;main.removeCallbacks(tick);controls.setVisibility(View.INVISIBLE);subtitles.setVisibility(View.INVISIBLE);removeReading();
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
        for(View v:new View[]{controls,subtitles,reading,selection})if(v!=null && wm!=null)try{wm.removeView(v);}catch(Exception ignored){}
        if(display!=null)display.release();if(images!=null)images.close();if(projection!=null)projection.stop();
        if(recognizer!=null)recognizer.close();for(Translator t:translators.values())t.close();cache.clear();latest.clear();
        stopForeground(STOP_FOREGROUND_REMOVE);super.onDestroy();
    }
}
