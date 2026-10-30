package org.w3.translate;

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
        return text.codePoints().anyMatch(Character::isLetter);
    }
}
