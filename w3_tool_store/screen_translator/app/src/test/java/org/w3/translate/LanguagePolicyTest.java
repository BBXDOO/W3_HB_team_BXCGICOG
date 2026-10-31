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
    @Test public void rejectsOcrConfusionsAndGameHud(){
        for(String text:new String[]{"I 94","l 89","O 98","II 100","10O","HP 100/120","XP: 94","FPS 60","0 / 10","１２ / １００","X 12 Y 34"})assertFalse(text,LanguagePolicy.readable(text));
    }
    @Test public void keepsMeaningfulTextWithValues(){
        for(String text:new String[]{"Collect 5 items","Level 2","Go 2","Use 10 HP to heal","第1章","薬を3個集める","收集3个物品","API v2.0"})assertTrue(text,LanguagePolicy.readable(text));
    }
    @Test public void avoidsThaiOnlyAndSingleLatinFragments(){
        assertFalse(LanguagePolicy.readable("ภาษาไทย 94"));assertFalse(LanguagePolicy.readable("I"));assertFalse(LanguagePolicy.readable("A 100"));assertTrue(LanguagePolicy.readable("Open settings"));
    }
    @Test public void translationMustKeepAllNumericValues(){
        assertTrue(LanguagePolicy.preservesNumbers("Collect 5 items in 10 days","เก็บ 5 ชิ้นใน 10 วัน"));
        assertTrue(LanguagePolicy.preservesNumbers("HP 100/120, -3.5%","พลัง 100/120, -3.5%"));
        assertTrue(LanguagePolicy.preservesNumbers("Version v1.23.2","รุ่น v1.23.2"));
        assertFalse(LanguagePolicy.preservesNumbers("5 items","เก็บ 6 ชิ้น"));
        assertFalse(LanguagePolicy.preservesNumbers("I 94","ฉัน"));
        assertFalse(LanguagePolicy.preservesNumbers("Hello","สวัสดี 94"));
        assertFalse(LanguagePolicy.preservesNumbers("100/120","100/100"));
        assertFalse(LanguagePolicy.preservesNumbers("-5%","5%"));
    }
    @Test public void leadingDecimalsCannotLoseDecimalPointOrSign(){
        assertFalse(LanguagePolicy.preservesNumbers("Use .5 mg","Use 5 mg"));
        assertFalse(LanguagePolicy.preservesNumbers("Use -.5 mg","Use 5 mg"));
        assertFalse(LanguagePolicy.preservesNumbers("Use -.5 mg","Use .5 mg"));
        assertFalse(LanguagePolicy.preservesNumbers("Use - .5 mg","Use .5 mg"));
        assertFalse(LanguagePolicy.preservesNumbers("Use .05 mg","Use .5 mg"));
        assertFalse(LanguagePolicy.preservesNumbers("Rate .5%","Rate 5%"));
    }
    @Test public void equivalentLeadingZeroAndMinusNotationIsAccepted(){
        assertTrue(LanguagePolicy.preservesNumbers("Use .5 mg","ใช้ 0.5 mg"));
        assertTrue(LanguagePolicy.preservesNumbers("Use -.5 mg","ใช้ -0.5 mg"));
        assertTrue(LanguagePolicy.preservesNumbers("Use -0.5 mg","ใช้ -.5 mg"));
        assertTrue(LanguagePolicy.preservesNumbers("Use +.5 mg","ใช้ +0.5 mg"));
        assertTrue(LanguagePolicy.preservesNumbers("Use −.5 mg","ใช้ -0.5 mg"));
        assertTrue(LanguagePolicy.preservesNumbers("Rate .5%","อัตรา 0.5%"));
    }
}
