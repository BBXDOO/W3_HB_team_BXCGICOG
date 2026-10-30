package org.w3.translate;
import org.junit.Test;
import static org.junit.Assert.*;
public class LanguagePolicyTest {
    @Test public void manualLanguageOverridesHanAmbiguity(){assertEquals("ja",LanguagePolicy.source("設定","ja"));}
    @Test public void detectsKanaEvenWithLatinAndHan(){assertEquals("ja",LanguagePolicy.source("System 設定を変更","auto"));}
    @Test public void handlesHalfWidthKana(){assertEquals("ja",LanguagePolicy.source("ｶﾀｶﾅ","auto"));}
    @Test public void hanOnlyDefaultsToChinese(){assertEquals("zh",LanguagePolicy.source("语言设置","auto"));}
    @Test public void englishMenus(){assertEquals("en",LanguagePolicy.source("Open settings","auto"));}
    @Test public void avoidsTranslatingCountersAndSymbols(){assertFalse(LanguagePolicy.readable("123 / 456 →"));assertTrue(LanguagePolicy.readable("設定"));}
}
