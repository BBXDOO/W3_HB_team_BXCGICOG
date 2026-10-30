package org.w3.translate;

import java.util.*;

/** Text only. Original blocks are immutable; translations are separate values. */
final class Article {
    long id, savedAt;
    String title="", url="", language="en", notice="";
    final List<Block> blocks=new ArrayList<>();
    static final class Block {
        final String kind, original;
        final int level;
        String thai="";
        Block(String kind,int level,String original){this.kind=kind;this.level=level;this.original=original;}
        boolean translatable(){return !"code".equals(kind);}
    }
    int translated(){int n=0;for(Block b:blocks)if(b.translatable()&&!b.thai.isEmpty())n++;return n;}
    int translatable(){int n=0;for(Block b:blocks)if(b.translatable())n++;return n;}
    static List<String> chunks(String text,int max){
        List<String> parts=new ArrayList<>();int start=0;
        while(start<text.length()){
            int end=Math.min(start+max,text.length());
            if(end<text.length()){
                if(Character.isHighSurrogate(text.charAt(end-1)))end--;
                int space=text.lastIndexOf(' ',end-1),line=text.lastIndexOf('\n',end-1);
                int boundary=Math.max(space,line);if(boundary>start+max/2)end=boundary+1;
            }
            parts.add(text.substring(start,end));start=end;
        }
        return parts;
    }
    String markdown(int view){
        StringBuilder s=new StringBuilder("# ").append(title).append("\n\n").append(url).append("\n\n");
        s.append("บันทึก: ").append(new java.util.Date(savedAt)).append("\n\n");
        if(!notice.isEmpty())s.append("> ").append(notice.replace("\n"," ")).append("\n\n");
        s.append("> คำแปลอัตโนมัติ ควรเทียบต้นฉบับ; บล็อกโค้ดคงต้นฉบับ\n\n");
        for(Block b:blocks){
            if("code".equals(b.kind)){s.append("    ").append(b.original.replace("\n","\n    ")).append("\n\n");continue;}
            String prefix="heading".equals(b.kind)?String.join("",Collections.nCopies(b.level,"#"))+" ":"list".equals(b.kind)?"- ":"";
            if(view!=1)s.append(prefix).append(b.original).append("\n\n");
            if(view!=0)s.append(prefix).append(b.thai.isEmpty()?"[ยังไม่แปล] "+b.original:b.thai).append("\n\n");
        }
        return s.toString();
    }
}
