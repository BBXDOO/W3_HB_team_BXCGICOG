package org.w3.translate;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import java.util.Locale;
import org.junit.Test;

public class NoteMarkdownTest {
    @Test public void preservesCodeAndMarkdownWhileTranslatingProse(){
        String original="# Title\r\n- [x] Use `foo()` and [docs](https://example.org)\n\n~~~python\n    keep_me()\n~~~\n| Name | Value |\n| --- | --- |\n";
        String expected="# TITLE\r\n- [x] USE `foo()` AND [docs](https://example.org)\n\n~~~python\n    keep_me()\n~~~\n| NAME | VALUE |\n| --- | --- |\n";
        assertEquals(expected,NoteMarkdown.translate(original,value->value.toUpperCase(Locale.ROOT)));
    }

    @Test public void wrapsCodeWithFenceLongerThanExistingBackticks(){
        String wrapped=NoteMarkdown.codeBlock("```\nexample\n```");
        assertTrue(wrapped.startsWith("\n````\n"));
        assertEquals(wrapped,NoteMarkdown.translate(wrapped,value->{throw new AssertionError(value);}));
    }
}
