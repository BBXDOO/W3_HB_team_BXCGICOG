package org.w3.translate;

import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

final class NoteMarkdown {
    private static final Pattern FENCE=Pattern.compile("^ {0,3}(`{3,}|~{3,})(.*)$");
    private static final Pattern PREFIX=Pattern.compile("^(\\s*(?:>\\s*)*(?:(?:#{1,6}|[-+*]|\\d+[.)])\\s+)?(?:\\[[ xX]\\]\\s+)?)");
    private static final Pattern PROTECTED=Pattern.compile("(`+)(.*?)\\1(?!`)|!?\\[[^\\]]*\\]\\([^)]*\\)|<[^>]+>|https?://[^\\s]+|&[A-Za-z0-9#]+;|[*_~|]+|\\\\.");

    private NoteMarkdown(){}

    static String codeBlock(String text){
        int size=3,run=0;
        for(int i=0;i<text.length();i++){
            run=text.charAt(i)=='`'?run+1:0;
            size=Math.max(size,run+1);
        }
        String fence=String.join("",java.util.Collections.nCopies(size,"`"));
        return "\n"+fence+"\n"+text+(text.endsWith("\n")?"":"\n")+fence+"\n";
    }

    static String translate(String markdown,Function<String,String> translate){
        StringBuilder output=new StringBuilder();
        String fence="";
        for(String line:markdown.split("(?<=\\n)",-1)){
            String body=line.endsWith("\n")?line.substring(0,line.length()-1):line;
            boolean cr=body.endsWith("\r");
            if(cr)body=body.substring(0,body.length()-1);
            Matcher marker=FENCE.matcher(body);
            if(marker.matches()){
                String run=marker.group(1);
                if(fence.isEmpty())fence=run;
                else if(run.charAt(0)==fence.charAt(0)&&run.length()>=fence.length()&&marker.group(2).trim().isEmpty())fence="";
                output.append(body);
            }else if(!fence.isEmpty()||body.startsWith("    ")||body.startsWith("\t")
                ||body.trim().matches("[-=|: *]+")){
                output.append(body);
            }else{
                Matcher prefix=PREFIX.matcher(body);
                prefix.find();
                output.append(prefix.group());
                int start=prefix.end();
                Matcher token=PROTECTED.matcher(body);
                token.region(start,body.length());
                while(token.find()){
                    appendText(output,body.substring(start,token.start()),translate);
                    output.append(token.group());
                    start=token.end();
                }
                appendText(output,body.substring(start),translate);
            }
            if(cr)output.append('\r');
            if(line.endsWith("\n"))output.append('\n');
        }
        return output.toString();
    }

    private static void appendText(StringBuilder output,String text,Function<String,String> translate){
        String content=text.trim();
        if(content.isEmpty()||content.codePoints().noneMatch(Character::isLetter)){
            output.append(text);
            return;
        }
        int start=text.indexOf(content);
        output.append(text,0,start).append(translate.apply(content)).append(text,start+content.length(),text.length());
    }
}
