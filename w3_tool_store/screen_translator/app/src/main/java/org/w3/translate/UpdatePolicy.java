package org.w3.translate;

import java.net.URI;
import java.util.*;

/** Channel boundaries, independently testable without network or Android UI. */
final class UpdatePolicy {
    static final String REPOSITORY="BBXDOO/W3_HB_team_BXCGICOG";
    static final String API="https://api.github.com/repos/"+REPOSITORY+"/releases?per_page=100";
    static final String TAG_PREFIX="screen-translator-v";
    static int version(String tag){
        if(tag==null || !tag.matches(TAG_PREFIX+"[1-9][0-9]{0,8}"))return -1;
        return Integer.parseInt(tag.substring(TAG_PREFIX.length()));
    }
    static String assetName(int version){return "W3-Screen-Translator-v"+version+".apk";}
    static boolean validAsset(int version,String name,String url,String digest){
        if(version<1 || !assetName(version).equals(name) || digest==null || !digest.matches("sha256:[a-fA-F0-9]{64}"))return false;
        try {
            URI uri=new URI(url);
            return "https".equals(uri.getScheme()) && "github.com".equalsIgnoreCase(uri.getHost())
                && uri.getPort()==-1 && uri.getUserInfo()==null && uri.getQuery()==null && uri.getFragment()==null
                && ("/"+REPOSITORY+"/releases/download/"+TAG_PREFIX+version+"/"+assetName(version)).equals(uri.getRawPath());
        }catch(Exception ignored){return false;}
    }
    static boolean sameSigners(Collection<String> installed,Collection<String> incoming){
        return installed!=null && incoming!=null && !installed.isEmpty() && !incoming.isEmpty()
            && new HashSet<>(installed).equals(new HashSet<>(incoming));
    }
    private UpdatePolicy(){}
}
