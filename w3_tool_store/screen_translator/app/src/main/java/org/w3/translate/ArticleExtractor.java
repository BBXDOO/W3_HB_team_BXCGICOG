package org.w3.translate;

import org.jsoup.Jsoup;
import org.jsoup.nodes.*;
import java.io.*;
import java.util.*;

/** Deterministic HTML extraction; never executes or renders remote code. */
final class ArticleExtractor {
    static final int MAX_CHARS=400_000, MAX_BLOCKS=2000;
    static Article parse(byte[] html,String charset,String url) throws IOException {
        return extract(Jsoup.parse(new ByteArrayInputStream(html),charset,url),url);
    }
    static Article extract(Document doc,String url){
        Article a=new Article();a.url=url;a.savedAt=System.currentTimeMillis();
        Element meta=doc.selectFirst("meta[property=og:title]");
        a.title=meta==null?doc.title():meta.attr("content");
        String lang=doc.select("html").attr("lang").toLowerCase(Locale.ROOT);
        // Remove page chrome, not headers inside an article (often its title/byline).
        doc.select("script,style,noscript,template,nav,footer,aside,form,button,svg,canvas,iframe,[hidden],[aria-hidden=true],[role=navigation],[role=banner],.sidebar,.cookie-banner,.advertisement,#comments,.comments").remove();
        Element root=best(doc.select("article,[itemprop=articleBody],.markdown-body,.post-content,.entry-content,.article-body,#main"));
        if(root==null)root=best(doc.select("main,[role=main]"));
        if(root==null)root=best(doc.select("#content,.content"));
        if(root==null)root=doc.body();
        if(a.title.trim().isEmpty()){Element h=root.selectFirst("h1");a.title=h==null?"บทความ":h.text();}
        if(a.title.length()>500)a.title=a.title.substring(0,500);
        walk(root,a,0);
        String sample="";for(Article.Block b:a.blocks){sample+=b.original;if(sample.length()>3000)break;}
        if(lang.startsWith("ja"))a.language="ja";
        else if(lang.startsWith("zh"))a.language="zh";
        else if(lang.startsWith("th"))a.language="th";
        else if(lang.startsWith("en"))a.language="en";
        else if(sample.matches("(?s).*[\u3040-\u30ff].*"))a.language="ja";
        else if(sample.matches("(?s).*[\u4e00-\u9fff].*"))a.language="zh";
        else if(!lang.isEmpty())a.language="unknown";
        a.notice="เก็บเฉพาะข้อความที่ดึงได้จากหน้านี้ ไม่รวมรูป ไฟล์แนบ หรือหน้าลิงก์ถัดไป; โปรดตรวจต้นฉบับว่าครบตามต้องการ"+(a.notice.isEmpty()?"":"\n"+a.notice);
        return a;
    }
    private static Element best(List<Element> candidates){
        Element best=null;double score=-1;
        for(Element e:candidates){int len=e.text().length(),links=0;for(Element link:e.select("a"))links+=link.text().length();double n=len-links*.8;if(n>score){score=n;best=e;}}
        return best;
    }
    private static int count(Article a){int n=0;for(Article.Block b:a.blocks)n+=b.original.length();return n;}
    private static void add(Article a,String kind,int level,String value){
        String s=value.trim();if(s.isEmpty())return;
        int remaining=MAX_CHARS-count(a);
        if(a.blocks.size()>=MAX_BLOCKS || remaining<=0){a.notice="หน้านี้เกินขนาดที่รองรับ จึงบันทึกเนื้อหาได้บางส่วน";return;}
        if(s.length()>remaining){int end=remaining;if(Character.isHighSurrogate(s.charAt(end-1)))end--;s=s.substring(0,end);a.notice="หน้านี้เกินขนาดที่รองรับ จึงบันทึกเนื้อหาได้บางส่วน";}
        // Keep every SQLite row well below Android CursorWindow limits, including Thai.
        for(String part:Article.chunks(s,8000)){
            if(a.blocks.size()>=MAX_BLOCKS){a.notice="หน้านี้เกินขนาดที่รองรับ จึงบันทึกเนื้อหาได้บางส่วน";break;}
            a.blocks.add(new Article.Block(kind,level,part));
        }
    }
    private static void walk(Element e,Article a,int depth){
        if(depth>120){a.notice="โครงสร้างหน้านี้ลึกเกินขีดจำกัด อาจมีข้อความบางส่วนตกหล่น";return;}
        String tag=e.normalName();
        if(tag.matches("h[1-6]")){add(a,"heading",tag.charAt(1)-'0',e.text());return;}
        if(tag.equals("pre")){add(a,"code",0,e.wholeText());return;}
        if(tag.equals("table")){
            for(Element row:e.select("tr")){List<String> cells=new ArrayList<>();for(Element cell:row.children())if(cell.normalName().matches("t[dh]"))cells.add(cell.text());add(a,"table",0,String.join(" | ",cells));}return;
        }
        // Emit text in DOM order, flushing around structural child elements.
        String kind=tag.equals("li")?"list":"paragraph";
        StringBuilder pending=new StringBuilder();
        for(Node node:e.childNodes()){
            if(node instanceof TextNode){pending.append(((TextNode)node).text());continue;}
            if(!(node instanceof Element))continue;
            Element child=(Element)node;
            if(child.normalName().equals("br")){pending.append('\n');continue;}
            if(child.isBlock() || child.normalName().equals("li")){
                add(a,kind,0,pending.toString());pending.setLength(0);walk(child,a,depth+1);
            }else pending.append(child.text());
        }
        add(a,kind,0,pending.toString());
    }
}
