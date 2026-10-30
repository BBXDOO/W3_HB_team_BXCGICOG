package org.w3.translate;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.widget.*;
final class Ui {
    static final int INK=Color.rgb(26,47,43), GREEN=Color.rgb(22,108,98), BG=Color.rgb(243,245,239);
    static int dp(Context c,float x){ return (int)(x*c.getResources().getDisplayMetrics().density+.5f); }
    static GradientDrawable round(int color,int radius){ GradientDrawable d=new GradientDrawable();d.setColor(color);d.setCornerRadius(radius);return d; }
    static TextView text(Context c,String s,int size){TextView t=new TextView(c);t.setText(s);t.setTextSize(size);t.setTextColor(INK);t.setPadding(0,dp(c,6),0,dp(c,6));return t;}
    static Button button(Context c,String s){Button b=new Button(c);b.setText(s);b.setTextSize(15);b.setTextColor(Color.WHITE);b.setAllCaps(false);b.setBackgroundTintList(android.content.res.ColorStateList.valueOf(GREEN));b.setMinHeight(dp(c,50));return b;}
    static LinearLayout column(Context c,int pad){LinearLayout l=new LinearLayout(c);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(c,pad),dp(c,pad),dp(c,pad),dp(c,pad));return l;}
    static void bold(TextView t){t.setTypeface(null,Typeface.BOLD);}
}
