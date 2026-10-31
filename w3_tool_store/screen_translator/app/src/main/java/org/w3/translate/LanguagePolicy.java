package org.w3.translate;

import java.util.*;
import java.util.regex.*;

/** Heuristic only: Han-only Japanese cannot be distinguished from Chinese. */
public final class LanguagePolicy {
    private LanguagePolicy() {}
    public static String source(String text, String selected) {
        if (!"auto".equals(selected)) return selected;
        boolean han = false;
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if ((c >= '\u3040' && c <= '\u30ff') || (c >= '\uff66' && c <= '\uff9f')) return "ja";
            if (Character.UnicodeScript.of(c) == Character.UnicodeScript.HAN) han = true;
        }
        return han ? "zh" : "en";
    }
    public static boolean readable(String text) {
        if(text==null || text.trim().isEmpty())return false;
        String clean=text.trim();
        // Numeric HUDs may contain OCR-confused I/l/O, units, or short stat labels.
        boolean digits=clean.codePoints().anyMatch(Character::isDigit);
        String remainder=clean.replaceAll("[\\p{N}\\p{P}\\p{S}\\sIiLlOoXx]","");
        if(digits && (remainder.isEmpty() || clean.matches("(?i)\\s*(?:hp|mp|xp|sp|ap|lv|lvl|fps|ms|kg|km|mb|gb)\\s*[:=]?\\s*[+−\\-0-9０-９.,:/%\\s]+")))return false;
        boolean latinRun=false;int previous=0;
        for(int cp:clean.codePoints().toArray()){
            Character.UnicodeScript script=Character.UnicodeScript.of(cp);
            if(script==Character.UnicodeScript.HAN || script==Character.UnicodeScript.HIRAGANA || script==Character.UnicodeScript.KATAKANA)return true;
            if(script==Character.UnicodeScript.LATIN && Character.isLetter(cp)){if(++previous>=2)latinRun=true;}else previous=0;
        }
        return latinRun;
    }
    private static final Pattern NUMBER=Pattern.compile("(?:[+−-]\\s*)?(?:\\p{Nd}+(?:[.,:/]\\p{Nd}+)*|\\.\\p{Nd}+)%?");
    /** Do not display/cache a translation that dropped, changed, or invented values. */
    public static boolean preservesNumbers(String original,String translated){
        return numbers(original).equals(numbers(translated));
    }
    private static List<String> numbers(String text){
        List<String> result=new ArrayList<>();Matcher m=NUMBER.matcher(text);
        while(m.find()){
            String value=m.group().replaceAll("\\s","").replace('−','-');
            // Only normalize a missing leading zero; keep versions/fractions exact.
            if(value.startsWith("."))value="0"+value;
            else if(value.startsWith("-.")||value.startsWith("+."))value=value.substring(0,1)+"0"+value.substring(1);
            result.add(value);
        }
        return result;
    }
}
