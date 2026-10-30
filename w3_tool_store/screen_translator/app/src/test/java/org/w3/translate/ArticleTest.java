package org.w3.translate;

import org.junit.Test;
import org.jsoup.Jsoup;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import static org.junit.Assert.*;

public class ArticleTest {
    private Article parse(String html){return ArticleExtractor.extract(Jsoup.parse(html),"https://example.org/manual");}
    @Test public void manualKeepsStructureAndCodeWithoutChrome(){
        Article a=parse("<html lang=en><title>Git guide</title><nav>Menu</nav><main><h1>Getting started</h1><p>Install <strong>Git</strong> first.</p><h2>Create repository</h2><ol><li>Open terminal</li><li>Run command<ul><li>Choose folder</li></ul></li></ol><pre>git init\n  git status</pre><table><tr><th>Flag</th><th>Meaning</th></tr><tr><td>-a</td><td>All</td></tr></table></main><footer>Cookies</footer></html>");
        assertEquals("en",a.language);assertEquals("Getting started",a.blocks.get(0).original);
        assertEquals("Install Git first.",a.blocks.get(1).original);
        assertEquals("heading",a.blocks.get(2).kind);assertEquals(2,a.blocks.get(2).level);
        assertEquals("Open terminal",a.blocks.get(3).original);assertEquals("Run command",a.blocks.get(4).original);
        assertEquals("Choose folder",a.blocks.get(5).original);assertEquals("git init\n  git status",a.blocks.get(6).original);
        assertFalse(a.blocks.get(6).translatable());assertEquals("Flag | Meaning",a.blocks.get(7).original);
        assertFalse(a.markdown(0).contains("Cookies"));assertFalse(a.markdown(0).contains("Menu"));
    }
    @Test public void nestedArticleDoesNotDuplicateParagraphsAndHandlesMalformedHtml(){
        Article a=parse("<main><article><header><h1>News</h1></header><div><p>First &amp; second<p>Third</div></article></main>");
        assertEquals(3,a.blocks.size());assertEquals("First & second",a.blocks.get(1).original);
    }
    @Test public void fallbackKeepsTextAroundNestedBlocksInOrder(){
        Article a=parse("<body>Intro<div>Section<p>Paragraph</p>End</div>Tail</body>");
        assertEquals(Arrays.asList("Intro","Section","Paragraph","End","Tail"),originals(a));
    }
    @Test public void legacyManualDoesNotIncludeWholeBookNavigation(){
        Article a=parse("<div id=content><ol class=book-toc><li><h2>Other chapter</h2>"+"Navigation ".repeat(100)+"</li></ol><div id=main><h1>Current chapter</h1><p>Content to keep</p></div></div>");
        assertEquals(Arrays.asList("Current chapter","Content to keep"),originals(a));
    }
    @Test public void languageUsesMetadataThenScriptAndMarksUnsupported(){
        assertEquals("ja",parse("<html lang=ja><p>漢字</p></html>").language);
        assertEquals("zh",parse("<p>中文文字</p>").language);
        assertEquals("ja",parse("<p>こんにちは</p>").language);
        assertEquals("unknown",parse("<html lang=fr><p>Bonjour</p></html>").language);
    }
    @Test public void charsetAutoDetectionKeepsJapaneseText() throws Exception {
        Article a=ArticleExtractor.parse("<meta charset=Shift_JIS><p>日本語テスト</p>".getBytes("Shift_JIS"),null,"https://example.org");
        assertEquals("日本語テスト",a.blocks.get(0).original);
    }
    @Test public void limitsAreVisibleRatherThanSilent(){
        Article a=parse("<main><p>"+"a".repeat(ArticleExtractor.MAX_CHARS+1)+"</p><p>Last</p></main>");
        assertTrue(a.notice.contains("บางส่วน"));assertEquals(ArticleExtractor.MAX_CHARS,String.join("",originals(a)).length());assertFalse(a.markdown(0).contains("Last"));
    }
    @Test public void largeParagraphsAreSplitForPersistentCursorRowsWithoutLosingText(){
        String original="中文".repeat(12000);Article a=parse("<p>"+original+"</p>");
        assertEquals(original,String.join("",originals(a)));for(Article.Block b:a.blocks)assertTrue(b.original.length()<=8000);
    }
    @Test public void urlRetainsEscapesAndQueryButDropsOnlyFragment() throws Exception {
        assertEquals("https://example.org/a%20b?q=%2F",ArticleFetcher.url("https://example.org/a%20b?q=%2F#heading"));
        assertEquals("https://example.org/path",ArticleFetcher.url("example.org/path"));
    }
    @Test public void rejectsNonWebAndCredentialsAndInsecureRedirectTargets(){
        for(String url:new String[]{"file:///etc/hosts","javascript:alert(1)","http://example.org","https://user:pass@example.org/","https://localhost/","https://example.local/","https://example.org:8443/"}){
            try{ArticleFetcher.url(url);fail(url);}catch(IOException expected){}
        }
    }
    @Test public void chunksAreLosslessAndDoNotSplitSurrogates(){
        String text="Long text ".repeat(500)+"\ud83d\ude00".repeat(1000)+"中文".repeat(1000);
        List<String> chunks=Article.chunks(text,1500);assertEquals(text,String.join("",chunks));
        for(String s:chunks){assertTrue(s.length()<=1500);assertFalse(Character.isHighSurrogate(s.charAt(s.length()-1)));assertFalse(Character.isLowSurrogate(s.charAt(0)));}
    }
    @Test public void exportsKeepUntranslatedOriginalsAndNeverTranslateCode(){
        Article a=parse("<title>Manual</title><h2>Heading</h2><p>Original</p><pre>git status</pre>");a.blocks.get(0).thai="หัวข้อ";
        assertTrue(a.markdown(1).contains("## หัวข้อ"));assertTrue(a.markdown(1).contains("[ยังไม่แปล] Original"));
        assertTrue(a.markdown(1).contains("    git status"));assertTrue(a.markdown(2).contains("Original"));
        assertFalse(a.markdown(0).contains("หัวข้อ"));assertEquals(1,a.translated());assertEquals(2,a.translatable());
    }
    private List<String> originals(Article a){List<String> s=new ArrayList<>();for(Article.Block b:a.blocks)s.add(b.original);return s;}
}
