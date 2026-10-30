package com.w3personalsandbox.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.pm.PackageInfo;
import android.os.Build;
import android.provider.Settings;
import android.content.pm.PackageManager;
import java.io.File;
import java.io.FileOutputStream;
import java.io.ByteArrayOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.MessageDigest;
import org.json.JSONArray;
import org.json.JSONObject;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.MimeTypeMap;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {
    private static final String ORIGIN = "https://appassets.androidplatform.net";
    private static final String ROOT = "/assets/www/";
    private static final String RELEASE_API = "https://api.github.com/repos/BBXDOO/W3-personal-sandbox-app/releases/latest";
    private static final String RELEASE_PREFIX = "https://github.com/BBXDOO/W3-personal-sandbox-app/releases/download/";
    private static final int PICK_FILE = 1201;
    private static final int SAVE_FILE = 1202;
    private WebView webView;
    private ValueCallback<Uri[]> fileCallback;
    private byte[] pendingExport;
    private boolean storyWriterOpen;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        webView = new WebView(this);
        setContentView(webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setBuiltInZoomControls(true);
        webView.getSettings().setDisplayZoomControls(false);
        webView.getSettings().setAllowFileAccess(false);
        // Android's system picker supplies content:// URIs for JSON and images.
        webView.getSettings().setAllowContentAccess(true);
        webView.getSettings().setJavaScriptCanOpenWindowsAutomatically(false);
        webView.addJavascriptInterface(new ExportBridge(), "AndroidBridge");
        webView.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (!"https".equals(uri.getScheme()) || !"appassets.androidplatform.net".equals(uri.getHost())) return null;
                String path = uri.getPath();
                if (path == null || !path.startsWith(ROOT)) return null;
                String name = path.substring(ROOT.length());
                if (name.isEmpty()) name = "index.html";
                if (name.contains("..") || name.startsWith("/") || name.contains("\\")) return null;
                try {
                    InputStream input = getAssets().open("www/" + name);
                    String ext = MimeTypeMap.getFileExtensionFromUrl(name);
                    String mime = MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext);
                    if (mime == null) mime = "application/octet-stream";
                    if ("js".equals(ext)) mime = "text/javascript";
                    if ("json".equals(ext)) mime = "application/json";
                    if ("svg".equals(ext)) mime = "image/svg+xml";
                    return new WebResourceResponse(mime, "UTF-8", input);
                } catch (Exception ignored) {
                    return new WebResourceResponse("text/plain", "UTF-8", 404, "Not Found", null, null);
                }
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                return !("https".equals(uri.getScheme()) && "appassets.androidplatform.net".equals(uri.getHost()) && uri.getPath() != null && uri.getPath().startsWith(ROOT));
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (fileCallback != null) fileCallback.onReceiveValue(null);
                fileCallback = callback;
                try {
                    Intent intent = params.createIntent();
                    startActivityForResult(intent, PICK_FILE);
                    return true;
                } catch (Exception e) {
                    fileCallback = null;
                    callback.onReceiveValue(null);
                    Toast.makeText(MainActivity.this, "เปิดตัวเลือกไฟล์ไม่ได้", Toast.LENGTH_SHORT).show();
                    return true;
                }
            }
        });
        webView.loadUrl(ORIGIN + ROOT + "index.html");
    }

    private class ExportBridge {
        @JavascriptInterface public void checkUpdate() { new Thread(MainActivity.this::checkForUpdate).start(); }
        @JavascriptInterface public void saveJson(String name, String contents) {
            saveDocument(name, contents, "application/json");
        }
        @JavascriptInterface public void saveText(String name, String contents, String mime) {
            if (!"text/markdown".equals(mime) && !"text/plain".equals(mime)) return;
            saveDocument(name, contents, mime);
        }
        @JavascriptInterface public void setWriterOpen(boolean open) {
            runOnUiThread(() -> storyWriterOpen = open);
        }
        @JavascriptInterface public void openExternal(String address) {
            runOnUiThread(() -> {
                try {
                    Uri uri = Uri.parse(address);
                    String scheme = uri.getScheme();
                    if (!"https".equalsIgnoreCase(scheme) && !"http".equalsIgnoreCase(scheme) && !"mailto".equalsIgnoreCase(scheme)) return;
                    startActivity(new Intent(Intent.ACTION_VIEW, uri));
                } catch (Exception e) { Toast.makeText(MainActivity.this, "เปิดลิงก์ไม่สำเร็จ", Toast.LENGTH_SHORT).show(); }
            });
        }
    }

    private void saveDocument(String name, String contents, String mime) {
        runOnUiThread(() -> {
            if (pendingExport != null) {
                Toast.makeText(this, "มีหน้าบันทึกไฟล์เปิดอยู่แล้ว", Toast.LENGTH_SHORT).show();
                return;
            }
            pendingExport = contents.getBytes(StandardCharsets.UTF_8);
            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType(mime);
            intent.putExtra(Intent.EXTRA_TITLE, name);
            try { startActivityForResult(intent, SAVE_FILE); }
            catch (Exception e) {
                pendingExport = null;
                Toast.makeText(this, "เปิดหน้าบันทึกไฟล์ไม่ได้", Toast.LENGTH_SHORT).show();
            }
        });
    }


    private long currentVersion() {
        try {
            PackageInfo info = getPackageManager().getPackageInfo(getPackageName(), 0);
            return Build.VERSION.SDK_INT >= 28 ? info.getLongVersionCode() : info.versionCode;
        } catch (Exception ignored) { return -1; }
    }

    private void showUpdateMessage(String text) {
        runOnUiThread(() -> {
            if (!isFinishing()) new AlertDialog.Builder(this)
                .setTitle("อัปเดต Personal Sandbox").setMessage(text).setPositiveButton("ตกลง", null).show();
        });
    }

    private HttpURLConnection connect(String address) throws Exception {
        if (!address.startsWith("https://")) throw new IllegalArgumentException("HTTPS required");
        HttpURLConnection connection = (HttpURLConnection) new URL(address).openConnection();
        connection.setConnectTimeout(15000);
        connection.setReadTimeout(30000);
        connection.setRequestProperty("User-Agent", "W3-Personal-Sandbox-Android");
        if (connection.getResponseCode() != 200) {
            int code = connection.getResponseCode();
            connection.disconnect();
            throw new IllegalStateException("HTTP " + code);
        }
        return connection;
    }

    private void checkForUpdate() {
        try {
            JSONObject release;
            HttpURLConnection connection = connect(RELEASE_API);
            try (InputStream in = connection.getInputStream(); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
                byte[] chunk = new byte[4096];
                int count;
                while ((count = in.read(chunk)) != -1) {
                    if (out.size() + count > 1000000) throw new IllegalStateException("Release metadata too large");
                    out.write(chunk, 0, count);
                }
                release = new JSONObject(out.toString("UTF-8"));
            } finally { connection.disconnect(); }

            String tag = release.getString("tag_name");
            if (!tag.matches("v[0-9]+")) throw new IllegalStateException("Invalid release tag");
            int version = Integer.parseInt(tag.substring(1));
            if (version <= currentVersion()) {
                showUpdateMessage("รุ่นนี้เป็นรุ่นล่าสุดแล้ว (v" + currentVersion() + ")");
                return;
            }
            JSONArray assets = release.getJSONArray("assets");
            JSONObject apk = null;
            for (int i = 0; i < assets.length(); i++) {
                JSONObject candidate = assets.getJSONObject(i);
                if (candidate.optString("name").endsWith(".apk")) { apk = candidate; break; }
            }
            if (apk == null) throw new IllegalStateException("No APK in release");
            String address = apk.getString("browser_download_url");
            String digest = apk.optString("digest");
            if (!address.startsWith(RELEASE_PREFIX + tag + "/") || !digest.matches("sha256:[0-9a-fA-F]{64}"))
                throw new IllegalStateException("Invalid update asset");
            String notes = release.optString("body", "").trim();
            if (notes.length() > 500) notes = notes.substring(0, 500) + "…";
            final String message = "มีรุ่น " + tag + " (ปัจจุบัน v" + currentVersion() + ")\n\n"
                + notes + "\n\nควรส่งออก JSON สำรองก่อนติดตั้ง";
            runOnUiThread(() -> {
                if (!isFinishing()) new AlertDialog.Builder(this).setTitle("พบอัปเดต")
                    .setMessage(message).setNegativeButton("ไว้ก่อน", null)
                    .setPositiveButton("ดาวน์โหลดและติดตั้ง", (dialog, which) -> {
                        if (Build.VERSION.SDK_INT >= 26 && !getPackageManager().canRequestPackageInstalls()) {
                            Toast.makeText(this, "อนุญาตติดตั้งแอปจาก Personal Sandbox แล้วกดตรวจอัปเดตอีกครั้ง", Toast.LENGTH_LONG).show();
                            Intent intent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                                Uri.parse("package:" + getPackageName()));
                            startActivity(intent);
                            return;
                        }
                        Toast.makeText(this, "กำลังดาวน์โหลด APK", Toast.LENGTH_SHORT).show();
                        new Thread(() -> downloadAndInstall(address, digest, version)).start();
                    }).show();
            });
        } catch (Exception error) {
            showUpdateMessage("ตรวจอัปเดตไม่สำเร็จ: " + error.getMessage());
        }
    }

    private void downloadAndInstall(String address, String expectedDigest, int version) {
        File partial = new File(getCacheDir(), "update.partial.apk");
        File apk = new File(getCacheDir(), "update.apk");
        HttpURLConnection connection = null;
        try {
            connection = connect(address);
            MessageDigest hash = MessageDigest.getInstance("SHA-256");
            long bytes = 0;
            try (InputStream input = connection.getInputStream(); FileOutputStream output = new FileOutputStream(partial)) {
                byte[] chunk = new byte[8192];
                int count;
                while ((count = input.read(chunk)) != -1) {
                    bytes += count;
                    if (bytes > 50000000L) throw new IllegalStateException("APK too large");
                    hash.update(chunk, 0, count);
                    output.write(chunk, 0, count);
                }
            }
            StringBuilder actual = new StringBuilder("sha256:");
            for (byte value : hash.digest()) actual.append(String.format(java.util.Locale.ROOT, "%02x", value & 0xff));
            if (!actual.toString().equalsIgnoreCase(expectedDigest)) throw new IllegalStateException("SHA-256 mismatch");
            PackageInfo info = getPackageManager().getPackageArchiveInfo(partial.getAbsolutePath(), 0);
            if (info == null || !getPackageName().equals(info.packageName)
                || (Build.VERSION.SDK_INT >= 28 ? info.getLongVersionCode() : info.versionCode) != version)
                throw new IllegalStateException("APK package or version mismatch");
            if (apk.exists() && !apk.delete()) throw new IllegalStateException("Cannot replace cached APK");
            if (!partial.renameTo(apk)) throw new IllegalStateException("Cannot prepare APK");
            runOnUiThread(() -> {
                try {
                    Intent install = new Intent(Intent.ACTION_VIEW);
                    install.setDataAndType(Uri.parse("content://" + getPackageName() + ".updates/apk"),
                        "application/vnd.android.package-archive");
                    install.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    startActivity(install);
                } catch (Exception error) {
                    showUpdateMessage("เปิดหน้าติดตั้งไม่สำเร็จ: " + error.getMessage());
                }
            });
        } catch (Exception error) {
            partial.delete();
            showUpdateMessage("ดาวน์โหลดอัปเดตไม่สำเร็จ: " + error.getMessage());
        } finally {
            if (connection != null) connection.disconnect();
        }
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request == PICK_FILE && fileCallback != null) {
            fileCallback.onReceiveValue(WebChromeClient.FileChooserParams.parseResult(result, data));
            fileCallback = null;
        }
        if (request == SAVE_FILE) {
            if (result == RESULT_OK && data != null && data.getData() != null && pendingExport != null) {
                try (OutputStream output = getContentResolver().openOutputStream(data.getData())) {
                    if (output == null) throw new IllegalStateException("No output stream");
                    output.write(pendingExport);
                    Toast.makeText(this, "บันทึกไฟล์แล้ว", Toast.LENGTH_SHORT).show();
                } catch (Exception e) {
                    Toast.makeText(this, "บันทึกไฟล์ไม่สำเร็จ", Toast.LENGTH_LONG).show();
                }
            }
            pendingExport = null;
        }
    }

    @Override public void onBackPressed() {
        if (storyWriterOpen) { webView.evaluateJavascript("window.dispatchEvent(new Event('w3-story-back'));", null); return; }
        if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
    @Override protected void onDestroy() {
        if (fileCallback != null) fileCallback.onReceiveValue(null);
        webView.destroy();
        super.onDestroy();
    }
}
