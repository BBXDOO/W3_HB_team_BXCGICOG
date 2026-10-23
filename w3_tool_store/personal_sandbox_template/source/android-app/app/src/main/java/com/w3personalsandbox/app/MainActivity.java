package com.w3personalsandbox.app;

import android.app.Activity;
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
    private static final int PICK_FILE = 1201;
    private static final int SAVE_FILE = 1202;
    private WebView webView;
    private ValueCallback<Uri[]> fileCallback;
    private byte[] pendingExport;

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
        @JavascriptInterface public void saveJson(String name, String contents) {
            runOnUiThread(() -> {
                pendingExport = contents.getBytes(StandardCharsets.UTF_8);
                Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("application/json");
                intent.putExtra(Intent.EXTRA_TITLE, name);
                try { startActivityForResult(intent, SAVE_FILE); }
                catch (Exception e) {
                    pendingExport = null;
                    Toast.makeText(MainActivity.this, "เปิดหน้าบันทึกไฟล์ไม่ได้", Toast.LENGTH_SHORT).show();
                }
            });
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
                    Toast.makeText(this, "บันทึกไฟล์สำรองแล้ว", Toast.LENGTH_SHORT).show();
                } catch (Exception e) {
                    Toast.makeText(this, "บันทึกไฟล์ไม่สำเร็จ", Toast.LENGTH_LONG).show();
                }
            }
            pendingExport = null;
        }
    }

    @Override public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
    @Override protected void onDestroy() {
        if (fileCallback != null) fileCallback.onReceiveValue(null);
        webView.destroy();
        super.onDestroy();
    }
}
