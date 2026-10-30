package org.w3.translate;

import android.app.*;
import android.content.*;
import android.content.pm.*;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;
import android.widget.*;
import org.json.*;
import java.io.*;
import java.net.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

/** Only a user click starts network access. Android always confirms installation. */
final class UpdateController {
    static final int INSTALL_PERMISSION=61;
    private final Activity activity;
    private final Button button;
    private final TextView status;
    private final ExecutorService worker=Executors.newSingleThreadExecutor();
    private final AtomicBoolean working=new AtomicBoolean();
    private volatile boolean closed;
    private Offer pending;
    private static final long MAX_APK=100L*1024*1024;
    private static final class Offer {
        final int version;final String url,digest,notes;
        Offer(int v,String u,String d,String n){version=v;url=u;digest=d;notes=n;}
    }
    UpdateController(Activity a,Button b,TextView s){activity=a;button=b;status=s;b.setOnClickListener(v->check());}
    private boolean alive(){return !closed && !activity.isFinishing() && !activity.isDestroyed();}
    private void ui(Runnable task){activity.runOnUiThread(()->{if(alive())task.run();});}
    private void message(String text){ui(()->status.setText(text));}
    private long installedVersion() throws PackageManager.NameNotFoundException {
        return code(activity.getPackageManager().getPackageInfo(activity.getPackageName(),0));
    }
    private static long code(PackageInfo info){return Build.VERSION.SDK_INT>=28?info.getLongVersionCode():info.versionCode;}
    private void begin(String text){button.setEnabled(false);status.setText(text);}
    private void finish(){working.set(false);ui(()->button.setEnabled(true));}
    void check(){
        if(!working.compareAndSet(false,true))return;
        begin("กำลังตรวจรุ่นใหม่…");
        worker.execute(()->{
            try {
                JSONArray releases=new JSONArray(readMetadata());
                Offer newest=null;long current=installedVersion();
                for(int i=0;i<releases.length();i++){
                    JSONObject release=releases.getJSONObject(i);
                    int version=UpdatePolicy.version(release.optString("tag_name"));
                    if(release.optBoolean("draft") || version<=current || (newest!=null && version<=newest.version))continue;
                    JSONArray assets=release.optJSONArray("assets");if(assets==null)continue;
                    for(int j=0;j<assets.length();j++){
                        JSONObject asset=assets.getJSONObject(j);String name=asset.optString("name"),url=asset.optString("browser_download_url"),digest=asset.optString("digest");
                        if(UpdatePolicy.validAsset(version,name,url,digest)){
                            String notes=release.optString("body").trim();if(notes.length()>500)notes=notes.substring(0,500)+"…";
                            newest=new Offer(version,url,digest,notes);break;
                        }
                    }
                }
                if(newest==null){message("ยังไม่พบรุ่นใหม่ที่เผยแพร่สำหรับแอปนี้");return;}
                final Offer offer=newest;
                ui(()->new AlertDialog.Builder(activity).setTitle("พบอัปเดตแอปแปลหน้าจอ")
                    .setMessage("รุ่นใหม่ v"+offer.version+"\n\n"+offer.notes+"\n\nการติดตั้งจะหยุดตัวแปลชั่วคราว และ Android จะให้คุณยืนยันอีกครั้ง")
                    .setNegativeButton("ไว้ก่อน",null).setPositiveButton("ดาวน์โหลดและติดตั้ง",(d,w)->installOffer(offer)).show());
                message("พบรุ่นใหม่ พร้อมดาวน์โหลดเมื่อคุณเลือก");
            }catch(Exception error){if(!closed)message("ตรวจอัปเดตไม่สำเร็จ ตรวจอินเทอร์เน็ตแล้วลองใหม่ภายหลัง");}
            finally{finish();}
        });
    }
    private void installOffer(Offer offer){
        activity.stopService(new Intent(activity,ScreenService.class));
        if(!activity.getPackageManager().canRequestPackageInstalls()){
            pending=offer;status.setText("เปิดสิทธิ์ติดตั้งจาก W3 แปลหน้าจอ แล้วกลับมาที่แอป");
            try{activity.startActivityForResult(new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,Uri.parse("package:"+activity.getPackageName())),INSTALL_PERMISSION);}
            catch(Exception e){pending=null;status.setText("เปิดหน้าสิทธิ์ติดตั้งไม่ได้ กรุณาตรวจในการตั้งค่าแอป");}
            return;
        }
        download(offer);
    }
    void permissionReturned(){
        Offer offer=pending;pending=null;
        if(offer!=null && activity.getPackageManager().canRequestPackageInstalls())download(offer);
        else status.setText("ยังไม่ได้อนุญาตติดตั้ง กดอัปเดตใหม่ได้เมื่อพร้อม");
    }
    private String readMetadata() throws Exception {
        HttpURLConnection connection=connect(UpdatePolicy.API);
        try(InputStream in=connection.getInputStream();ByteArrayOutputStream out=new ByteArrayOutputStream()){
            byte[] buffer=new byte[8192];int count;
            while((count=in.read(buffer))!=-1){if(closed || out.size()+count>4*1024*1024)throw new IOException("Metadata limit");out.write(buffer,0,count);}
            return out.toString("UTF-8");
        }finally{connection.disconnect();}
    }
    private HttpURLConnection connect(String address) throws Exception {
        URL url=new URL(address);
        for(int redirects=0;redirects<6;redirects++){
            String host=url.getHost();
            if(!"https".equals(url.getProtocol()) || !(host.equals("api.github.com") || host.equals("github.com") || host.equals("release-assets.githubusercontent.com") || host.equals("objects.githubusercontent.com")))throw new IOException("Unexpected download host");
            HttpURLConnection c=(HttpURLConnection)url.openConnection();c.setInstanceFollowRedirects(false);c.setConnectTimeout(15000);c.setReadTimeout(30000);c.setRequestProperty("User-Agent","W3-Screen-Translator-Android");
            try {
                int code=c.getResponseCode();if(code==200)return c;
                if(code==301 || code==302 || code==303 || code==307 || code==308){String next=c.getHeaderField("Location");if(next==null)throw new IOException("Missing redirect");url=new URL(url,next);c.disconnect();continue;}
                throw new IOException("HTTP "+code);
            }catch(Exception error){c.disconnect();throw error;}
        }
        throw new IOException("Too many redirects");
    }
    private void download(Offer offer){
        if(!working.compareAndSet(false,true))return;
        begin("กำลังดาวน์โหลดไฟล์อัปเดต…");
        worker.execute(()->{
            File partial=new File(activity.getCacheDir(),"update.partial.apk");
            File ready=new File(activity.getCacheDir(),"update.apk");
            try {
                HttpURLConnection c=connect(offer.url);MessageDigest hash=MessageDigest.getInstance("SHA-256");long total=0,lastReport=0;
                try(InputStream in=c.getInputStream();FileOutputStream out=new FileOutputStream(partial)){
                    byte[] chunk=new byte[32768];int count;long length=c.getContentLengthLong();
                    if(length>MAX_APK)throw new IOException("APK size limit");
                    while((count=in.read(chunk))!=-1){
                        total+=count;if(closed || Thread.currentThread().isInterrupted() || total>MAX_APK)throw new IOException("Download cancelled or too large");
                        hash.update(chunk,0,count);out.write(chunk,0,count);
                        if(total-lastReport>1024*1024){lastReport=total;message(length>0?"กำลังดาวน์โหลด "+Math.min(100,total*100/length)+"%":"กำลังดาวน์โหลด "+(total/1024/1024)+" MB");}
                    }
                    out.getFD().sync();
                }finally{c.disconnect();}
                if(!("sha256:"+hex(hash.digest())).equalsIgnoreCase(offer.digest))throw new IOException("File checksum mismatch");
                PackageManager pm=activity.getPackageManager();int flags=Build.VERSION.SDK_INT>=28?PackageManager.GET_SIGNING_CERTIFICATES:PackageManager.GET_SIGNATURES;
                PackageInfo archive=pm.getPackageArchiveInfo(partial.getAbsolutePath(),flags);
                PackageInfo installed=pm.getPackageInfo(activity.getPackageName(),flags);
                if(archive==null || !activity.getPackageName().equals(archive.packageName) || code(archive)!=offer.version || code(archive)<=code(installed))throw new IOException("Package or version mismatch");
                if(!UpdatePolicy.sameSigners(signers(installed),signers(archive)))throw new IOException("Signing certificate mismatch");
                if(closed)throw new IOException("Closed");
                if(ready.exists() && !ready.delete())throw new IOException("Cannot replace cache");
                if(!partial.renameTo(ready))throw new IOException("Cannot prepare installer");
                ui(()->{
                    try {
                        Intent install=new Intent(Intent.ACTION_VIEW).setDataAndType(Uri.parse("content://"+activity.getPackageName()+".updates/apk"),"application/vnd.android.package-archive");
                        install.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);activity.startActivity(install);status.setText("ตรวจไฟล์และลายเซ็นผ่านแล้ว ยืนยันติดตั้งในหน้าของ Android");
                    }catch(Exception e){status.setText("เปิดหน้าติดตั้งไม่ได้ กรุณาตรวจสิทธิ์ติดตั้งแล้วลองอีกครั้ง");}
                });
            }catch(Exception error){if(!closed)message("ยังติดตั้งไม่ได้: ดาวน์โหลดไม่ครบ หรือไฟล์/รุ่น/ลายเซ็นไม่ตรง กรุณาลองใหม่หรือติดต่อผู้พัฒนา");}
            finally{if(partial.exists())partial.delete();finish();}
        });
    }
    private static List<String> signers(PackageInfo p) throws Exception {
        android.content.pm.Signature[] signatures=Build.VERSION.SDK_INT>=28?(p.signingInfo==null?null:p.signingInfo.getApkContentsSigners()):p.signatures;
        List<String> result=new ArrayList<>();if(signatures!=null)for(android.content.pm.Signature s:signatures)result.add(hex(MessageDigest.getInstance("SHA-256").digest(s.toByteArray())));return result;
    }
    private static String hex(byte[] bytes){StringBuilder s=new StringBuilder();for(byte b:bytes)s.append(String.format(Locale.ROOT,"%02x",b&255));return s.toString();}
    void close(){closed=true;pending=null;worker.shutdownNow();}
}
