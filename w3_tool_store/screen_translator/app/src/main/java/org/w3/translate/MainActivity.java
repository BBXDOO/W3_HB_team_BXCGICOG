package org.w3.translate;

import android.Manifest;
import android.app.*;
import android.content.*;
import android.content.pm.PackageManager;
import android.media.projection.MediaProjectionManager;
import android.media.projection.MediaProjectionConfig;
import android.net.Uri;
import android.os.*;
import android.provider.Settings;
import android.view.*;
import android.widget.*;
import com.google.mlkit.common.model.DownloadConditions;
import com.google.mlkit.nl.translate.*;
import java.util.*;

public class MainActivity extends Activity {
    private static final int CAPTURE=31;
    private Spinner language,mode;
    private TextView status;
    private Button prepare,start;
    private boolean loading,notificationAsked,capturePending;
    private final List<Translator> downloads=new ArrayList<>();
    private final String[] codes={"auto","zh","ja","en"};
    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);
        LinearLayout root=Ui.column(this,22);root.setBackgroundColor(Ui.BG);scroll.addView(root);setContentView(scroll);
        root.setOnApplyWindowInsetsListener((v,in)->{root.setPadding(Ui.dp(this,22),in.getSystemWindowInsetTop()+Ui.dp(this,18),Ui.dp(this,22),in.getSystemWindowInsetBottom()+Ui.dp(this,22));return in;});
        TextView brand=Ui.text(this,"W3  /  เครื่องมือช่วยอ่าน",13);root.addView(brand);
        TextView title=Ui.text(this,"อ่านเข้าใจ\nไปต่อได้",36);Ui.bold(title);root.addView(title);
        root.addView(Ui.text(this,"แปลจีน · ญี่ปุ่น · อังกฤษ → ไทย\nบนหน้าจอเกม คู่มือ และหนังสือ",17));
        LinearLayout card=Ui.column(this,18);card.setBackground(Ui.round(0xffffffff,Ui.dp(this,20)));root.addView(card,new LinearLayout.LayoutParams(-1,-2));
        card.addView(Ui.text(this,"1   เลือกภาษาต้นฉบับ",17));
        language=new Spinner(this);language.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"อัตโนมัติ (ทดลอง)","จีน","ญี่ปุ่น","อังกฤษ"}));card.addView(language);
        language.setSelection(getPreferences(0).getInt("lang",0));
        card.addView(Ui.text(this,"2   เลือกรูปแบบการอ่าน",17));
        mode=new Spinner(this);mode.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,new String[]{"แปลบนจออัตโนมัติ","หยุดอ่านเป็นหน้า"}));card.addView(mode);mode.setSelection(getPreferences(0).getInt("mode",0));
        card.addView(Ui.text(this,"3   เตรียมชุดภาษา (ใช้เน็ตครั้งแรก)",17));
        prepare=Ui.button(this,"ดาวน์โหลด / ตรวจชุดภาษา");card.addView(prepare);prepare.setOnClickListener(v->prepareModels());
        status=Ui.text(this,"ดาวน์โหลดสำเร็จแล้วจะแปลในเครื่องได้\nไม่ต้องตั้งค่าบริการแปลเอง",14);card.addView(status);
        start=Ui.button(this,"เริ่มแปลหน้าจอ");root.addView(start);start.setOnClickListener(v->startCapture());
        Button stop=Ui.button(this,"หยุดแปลและปิดปุ่มลอย");root.addView(stop);stop.setOnClickListener(v->{stopService(new Intent(this,ScreenService.class));status.setText("หยุดแปลแล้ว");});
        root.addView(Ui.text(this,"วิธีใช้",20));
        root.addView(Ui.text(this,"เริ่มแปล → อนุญาตหน้าจอ → สลับไปแอปที่ต้องการ\n\nปุ่มลอย «ไทย» เปิดเมนู: พัก / แปลครั้งเดียว / อ่านเต็มหน้า / เลือกพื้นที่ / ซ่อน / ปิด\n\nคำแปลเป็นชั้นทับหน้าจอ กดซ่อนก่อนแตะเมนูที่อ่านแล้วได้ ปุ่มลอยลากย้ายได้\n\nโหมดอัตโนมัติจะเว้นช่วงอ่านจอ มีหน่วงและอาจเห็นคำแปลหายชั่วครู่ระหว่างจับภาพ",15));
        root.addView(Ui.text(this,"ก่อนเริ่ม",20));
        root.addView(Ui.text(this,"• Android ขอสิทธิ์แสดงทับแอปและจับภาพหน้าจอ\n• แอปที่ป้องกันการจับภาพจะอ่านไม่ได้\n• ตัวหนังสือเล็ก ฟอนต์เกม และภาษาญี่ปุ่นที่มีแต่คันจิอาจอ่านผิด เลือกภาษาตรง ๆ ช่วยได้\n• คำศัพท์วิชาการ สูตร และตารางควรเทียบต้นฉบับ\n• ไม่บันทึกภาพหรือประวัติคำแปล แปลในเครื่องหลังเตรียมภาษา; SDK อาจติดต่อ Google เพื่อดาวน์โหลดและส่งข้อมูลวินิจฉัย\n• รุ่นทดลอง 0.2 — ยังต้องทดสอบบน OPPO จริง",14));
        root.addView(Ui.text(this,"ใช้ ML Kit ของ Google · คำแปลอัตโนมัติ",12));
    }
    private String selected(){return codes[language.getSelectedItemPosition()];}
    private void prepareModels(){
        if(loading)return;
        loading=true;prepare.setEnabled(false);start.setEnabled(false);
        String chosen=selected();List<String> sources="auto".equals(chosen)?Arrays.asList("zh","ja","en"):Collections.singletonList(chosen);
        downloadNext(sources,0);
    }
    private void downloadNext(List<String> sources,int index){
        if(isDestroyed())return;
        if(index==sources.size()){loading=false;prepare.setEnabled(true);start.setEnabled(true);status.setText("พร้อมแปล ✓ ชุดภาษาที่เลือกอยู่ในเครื่องแล้ว");return;}
        String src=sources.get(index);String name="zh".equals(src)?"จีน":"ja".equals(src)?"ญี่ปุ่น":"อังกฤษ";status.setText("กำลังเตรียม "+name+" → ไทย\nครั้งแรกอาจใช้เวลาหลายนาที กรุณาเปิดเน็ตไว้");
        Translator t=Translation.getClient(new TranslatorOptions.Builder().setSourceLanguage(src).setTargetLanguage("th").build());downloads.add(t);
        t.downloadModelIfNeeded(new DownloadConditions.Builder().build()).addOnSuccessListener(v->{t.close();downloads.remove(t);getSharedPreferences("models",0).edit().putBoolean(src,true).apply();downloadNext(sources,index+1);}).addOnFailureListener(e->{t.close();downloads.remove(t);loading=false;if(!isDestroyed()){prepare.setEnabled(true);start.setEnabled(true);status.setText("ยังดาวน์โหลดไม่สำเร็จ ตรวจอินเทอร์เน็ตแล้วลองใหม่");}});
    }
    private void startCapture(){
        if(capturePending)return;
        String chosen=selected();
        for(String code:("auto".equals(chosen)?new String[]{"en","zh","ja"}:new String[]{chosen})){if(!getSharedPreferences("models",0).getBoolean(code,false)){status.setText("กรุณากดดาวน์โหลด / ตรวจชุดภาษาก่อนเริ่มแปล");return;}}
        if(ScreenService.running){status.setText("กำลังแปลอยู่แล้ว ใช้ปุ่มลอย «ไทย» หรือกดหยุดก่อนเริ่มใหม่");return;}
        if(!Settings.canDrawOverlays(this)){
            new AlertDialog.Builder(this).setTitle("อนุญาตปุ่มลอย").setMessage("เปิด «อนุญาตให้แสดงทับแอปอื่น» แล้วกลับมากดเริ่มแปลอีกครั้ง").setPositiveButton("เปิดการตั้งค่า",(d,w)->startActivity(new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,Uri.parse("package:"+getPackageName())))).setNegativeButton("ไว้ก่อน",null).show();return;
        }
        if(Build.VERSION.SDK_INT>=33 && !notificationAsked && checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED){notificationAsked=true;requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS},10);return;}
        getPreferences(0).edit().putInt("lang",language.getSelectedItemPosition()).putInt("mode",mode.getSelectedItemPosition()).apply();
        MediaProjectionManager pm=(MediaProjectionManager)getSystemService(MEDIA_PROJECTION_SERVICE);
        Intent capture=Build.VERSION.SDK_INT>=34?pm.createScreenCaptureIntent(MediaProjectionConfig.createConfigForDefaultDisplay()):pm.createScreenCaptureIntent();
        capturePending=true;startActivityForResult(capture,CAPTURE);
    }
    @Override public void onRequestPermissionsResult(int request,String[] permissions,int[] results){super.onRequestPermissionsResult(request,permissions,results);if(request==10)startCapture();}
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request!=CAPTURE)return;
        capturePending=false;
        if(result!=RESULT_OK || data==null){status.setText("ยังไม่อนุญาตจับภาพ กดเริ่มใหม่ได้เมื่อพร้อม");return;}
        Intent i=new Intent(this,ScreenService.class).putExtra("code",result).putExtra("data",data).putExtra("source",selected()).putExtra("reader",mode.getSelectedItemPosition()==1);
        startForegroundService(i);status.setText("เปิดปุ่มลอยแล้ว สลับไปแอปที่ต้องการอ่านได้เลย");
    }
    @Override protected void onDestroy(){super.onDestroy();for(Translator t:downloads)t.close();downloads.clear();}
}
