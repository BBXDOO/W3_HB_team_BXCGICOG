package org.w3.translate;
import org.junit.Test;
import java.util.*;
import static org.junit.Assert.*;
public class UpdatePolicyTest {
    private final String digest="sha256:"+String.join("",Collections.nCopies(64,"a"));
    private final String url="https://github.com/BBXDOO/W3_HB_team_BXCGICOG/releases/download/screen-translator-v4/W3-Screen-Translator-v4.apk";
    @Test public void ignoresUnrelatedAndAmbiguousTags(){assertEquals(-1,UpdatePolicy.version("v999"));assertEquals(-1,UpdatePolicy.version("screen-translator-v04"));assertEquals(-1,UpdatePolicy.version("screen-translator-v2147483648"));assertEquals(4,UpdatePolicy.version("screen-translator-v4"));}
    @Test public void acceptsExactReleaseAsset(){assertTrue(UpdatePolicy.validAsset(4,"W3-Screen-Translator-v4.apk",url,digest));}
    @Test public void rejectsOtherRepositoryOrLookalikeHost(){assertFalse(UpdatePolicy.validAsset(4,"W3-Screen-Translator-v4.apk",url.replace("github.com/","github.com.evil/"),digest));assertFalse(UpdatePolicy.validAsset(4,"W3-Screen-Translator-v4.apk",url.replace("BBXDOO","other"),digest));}
    @Test public void rejectsInsecureAndModifiedUrls(){for(String changed:new String[]{url.replace("https:","http:"),url+"?raw=1",url+"#fragment",url.replace("github.com","user@github.com"),url.replace("github.com","github.com:443")})assertFalse(UpdatePolicy.validAsset(4,"W3-Screen-Translator-v4.apk",changed,digest));}
    @Test public void rejectsMissingHashAndWrongVersion(){assertFalse(UpdatePolicy.validAsset(4,"W3-Screen-Translator-v4.apk",url,""));assertFalse(UpdatePolicy.validAsset(5,"W3-Screen-Translator-v4.apk",url,digest));assertFalse(UpdatePolicy.validAsset(4,"W3-Screen-Translator-v4.apk",url,digest.substring(1)));}
    @Test public void requiresSameNonemptySignerSet(){assertTrue(UpdatePolicy.sameSigners(Arrays.asList("a","b"),Arrays.asList("b","a")));assertFalse(UpdatePolicy.sameSigners(Collections.singletonList("a"),Collections.singletonList("b")));assertFalse(UpdatePolicy.sameSigners(Collections.singletonList("a"),Arrays.asList("a","b")));assertFalse(UpdatePolicy.sameSigners(Collections.emptyList(),Collections.emptyList()));}
}
