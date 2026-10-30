package org.w3.translate;

import java.io.*;
import java.net.*;
import java.util.Locale;
import java.util.regex.*;

final class ArticleFetcher {
    static final class ReadException extends IOException { ReadException(String message){super(message);} }
    static final int MAX_BYTES=8*1024*1024;
    static String url(String text) throws IOException {
        String raw=text.trim();if(raw.length()>8192)throw new ReadException("ลิงก์ยาวเกินขนาดที่รองรับ");if(!raw.contains(":"))raw="https://"+raw;
        try{
            URI u=new URI(raw);
            if(!"https".equalsIgnoreCase(u.getScheme()) || u.getHost()==null || u.getUserInfo()!=null || (u.getPort()!=-1&&u.getPort()!=443))throw new Exception();
            String host=u.getHost().toLowerCase(Locale.ROOT);
            if(host.equals("localhost") || host.endsWith(".localhost") || host.endsWith(".local"))throw new Exception();
            String full=u.toASCIIString();int hash=full.indexOf('#');return hash<0?full:full.substring(0,hash);
        }catch(Exception e){throw new ReadException("กรุณาใช้ลิงก์เว็บ HTTPS สาธารณะ เช่น https://docs.github.com/…");}
    }
    private static void publicHost(URL u) throws IOException {
        for(InetAddress addr:InetAddress.getAllByName(u.getHost())){
            byte[] b=addr.getAddress();boolean shared=b.length==4&&(b[0]&255)==100&&((b[1]&255)>=64&&(b[1]&255)<=127);
            if(addr.isAnyLocalAddress()||addr.isLoopbackAddress()||addr.isLinkLocalAddress()||addr.isSiteLocalAddress()||addr.isMulticastAddress()||shared||(b.length==16&&(b[0]&254)==252))throw new ReadException("รองรับลิงก์เว็บสาธารณะเท่านั้น");
        }
    }
    static Article fetch(String input) throws IOException {
        String target=url(input);
        for(int hop=0;hop<6;hop++){
            if(Thread.currentThread().isInterrupted())throw new InterruptedIOException();
            URL u=new URL(target);publicHost(u);
            HttpURLConnection c=(HttpURLConnection)u.openConnection();
            c.setInstanceFollowRedirects(false);c.setConnectTimeout(15000);c.setReadTimeout(20000);
            c.setRequestProperty("User-Agent","W3Reader/0.4 (Android; text-only personal reading)");
            c.setRequestProperty("Accept","text/html,application/xhtml+xml");c.setRequestProperty("Accept-Encoding","identity");
            try{
                int code=c.getResponseCode();
                if(code==301||code==302||code==303||code==307||code==308){String location=c.getHeaderField("Location");if(location==null)throw new ReadException("เว็บส่งลิงก์ต่อไม่สมบูรณ์");target=url(new URL(u,location).toString());continue;}
                if(code!=200)throw new ReadException("เว็บตอบกลับ "+code+" อาจต้องเข้าสู่ระบบ หรือไม่อนุญาตให้ดึงข้อความ");
                String type=c.getContentType();if(type==null||!(type.toLowerCase(Locale.ROOT).startsWith("text/html")||type.toLowerCase(Locale.ROOT).startsWith("application/xhtml+xml")))throw new ReadException("ลิงก์นี้ไม่ใช่บทความ HTML (ยังไม่รองรับ PDF หรือไฟล์ดาวน์โหลด)");
                if(c.getContentLengthLong()>MAX_BYTES)throw new ReadException("หน้าเว็บใหญ่เกิน 8 MB จึงยังไม่บันทึก");
                ByteArrayOutputStream data=new ByteArrayOutputStream();
                String encoding=c.getContentEncoding();
                if(encoding!=null&&!encoding.equalsIgnoreCase("identity")&&!encoding.equalsIgnoreCase("gzip"))throw new ReadException("รูปแบบบีบอัดของเว็บนี้ยังไม่รองรับ");
                try(InputStream in="gzip".equalsIgnoreCase(encoding)?new java.util.zip.GZIPInputStream(c.getInputStream()):c.getInputStream()){
                    byte[] buf=new byte[8192];int n;
                    while((n=in.read(buf))!=-1){if(Thread.currentThread().isInterrupted())throw new InterruptedIOException();if(data.size()+n>MAX_BYTES)throw new ReadException("หน้าเว็บใหญ่เกิน 8 MB จึงยังไม่บันทึก");data.write(buf,0,n);}
                }
                Matcher charset=Pattern.compile("charset\\s*=\\s*[\"']?([^;\\s\"']+)",Pattern.CASE_INSENSITIVE).matcher(type);
                Article article=ArticleExtractor.parse(data.toByteArray(),charset.find()?charset.group(1):null,target);
                if(article.title.toLowerCase(Locale.ROOT).matches(".*(just a moment|access denied|checking your browser|security verification|verify you are human).*"))throw new ReadException("เว็บขอให้ยืนยันตัวตน จึงยังดึงบทความไม่ได้ กรุณาเปิดผ่านเบราว์เซอร์");
                int chars=0;for(Article.Block b:article.blocks)chars+=b.original.length();
                if(chars<60)throw new ReadException("ไม่พบเนื้อหาบทความเพียงพอ เว็บนี้อาจต้องโหลดด้วย JavaScript หรือเข้าสู่ระบบ");
                return article;
            }finally{c.disconnect();}
        }
        throw new ReadException("เว็บเปลี่ยนเส้นทางหลายครั้งเกินไป จึงยังไม่บันทึก");
    }
}
