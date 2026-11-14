package org.w3.translate;
import android.content.Context;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.widget.*;
final class Ui {
    static final int BG=0xff131416, PANEL=0xff202226, EDGE=0xff363940;
    static final int INK=0xfff4f5f7, MUTED=0xffbec3cc, GREEN=0xffa8ef83;
    static final int CYAN=0xff79e3f3, VIOLET=0xffd6afff, AMBER=0xffffcb74, ROSE=0xffff9eac;
    static int dp(Context c,float x){ return (int)(x*c.getResources().getDisplayMetrics().density+.5f); }
    static GradientDrawable round(int color,int radius){ GradientDrawable d=new GradientDrawable();d.setColor(color);d.setCornerRadius(radius);return d; }
    static GradientDrawable surface(Context c,int color,int radius,int stroke){
        GradientDrawable shape=round(color,dp(c,radius));shape.setStroke(dp(c,1),stroke);return shape;
    }
    static android.graphics.drawable.Drawable pressable(Context c,int color,int radius,int stroke){
        return new android.graphics.drawable.RippleDrawable(
            android.content.res.ColorStateList.valueOf(0x26ffffff),surface(c,color,radius,stroke),null);
    }
    static TextView text(Context c,String s,int size){TextView t=new TextView(c);t.setText(s);t.setTextSize(size);t.setTextColor(INK);t.setPadding(0,dp(c,6),0,dp(c,6));return t;}
    static Button button(Context c,String label){
        Button button=new Button(c);
        button.setText(label);button.setTextSize(15);button.setAllCaps(false);
        button.setMinWidth(0);button.setMinimumWidth(0);button.setMinHeight(dp(c,48));
        button.setPadding(dp(c,10),dp(c,7),dp(c,10),dp(c,7));
        button.setBackgroundTintList(null);button.setStateListAnimator(null);
        button.setBackground(pressable(c,PANEL,14,EDGE));
        button.setTextColor(new android.content.res.ColorStateList(
            new int[][]{new int[]{-android.R.attr.state_enabled},new int[]{}},new int[]{0xff858992,INK}));
        return button;
    }
    static LinearLayout column(Context c,int pad){LinearLayout l=new LinearLayout(c);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(c,pad),dp(c,pad),dp(c,pad),dp(c,pad));return l;}
    static void bold(TextView t){t.setTypeface(null,Typeface.BOLD);}
}
