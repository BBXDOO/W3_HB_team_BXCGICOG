package org.w3.translate;

import android.content.Context;
import android.graphics.*;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.StateListDrawable;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;

/** Crisp white rectangular controls, without blur, gradients, or software shadows. */
final class SoftControls {
    static final int INK=0xff30383b, MUTED=0xff586269, GREEN=0xff17685c, RED=0xff923d3d;
    private SoftControls() {}

    static void surface(View view){
        StateListDrawable background=new StateListDrawable();
        for(int color:new int[]{0xffeeeeee,Color.WHITE}){
            GradientDrawable shape=new GradientDrawable();shape.setShape(GradientDrawable.RECTANGLE);
            shape.setColor(color);shape.setCornerRadius(0);shape.setStroke(Math.max(1,Ui.dp(view.getContext(),1)),Color.BLACK);
            background.addState(color==Color.WHITE?new int[]{}:new int[]{android.R.attr.state_pressed},shape);
        }
        view.setLayerType(View.LAYER_TYPE_NONE,null);view.setBackground(background);
        view.setElevation(0);view.setTranslationZ(0);view.setStateListAnimator(null);
    }
    static Button button(Context c,String label,String icon,boolean active,boolean destructive){
        Button b=new Button(c);
        b.setText(label);b.setAllCaps(false);b.setTextSize(13);b.setMaxLines(2);
        b.setMinWidth(0);b.setMinimumWidth(0);b.setMinHeight(0);b.setMinimumHeight(0);
        b.setGravity(Gravity.CENTER);b.setIncludeFontPadding(false);
        b.setBackgroundTintList(null);surface(b);
        b.setPadding(Ui.dp(c,9),Ui.dp(c,10),Ui.dp(c,9),Ui.dp(c,10));
        int ink=destructive?RED:active?GREEN:INK;b.setTextColor(ink);
        Icon glyph=new Icon(icon,ink);glyph.setBounds(0,0,Ui.dp(c,23),Ui.dp(c,23));
        b.setCompoundDrawables(null,glyph,null,null);b.setCompoundDrawablePadding(Ui.dp(c,3));
        return b;
    }
    private static final class Icon extends Drawable {
        private final Paint p=new Paint(Paint.ANTI_ALIAS_FLAG);
        private final String kind;
        Icon(String k,int color){kind=k;p.setColor(color);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(1.8f);p.setStrokeCap(Paint.Cap.ROUND);p.setStrokeJoin(Paint.Join.ROUND);}
        @Override public void draw(Canvas original){
            Canvas c=original;int save=c.save();Rect b=getBounds();c.translate(b.left,b.top);c.scale(b.width()/24f,b.height()/24f);
            switch(kind){
                case "play":{Path path=new Path();path.moveTo(8,4);path.lineTo(20,12);path.lineTo(8,20);path.close();c.drawPath(path,p);break;}
                case "pause":c.drawLine(8,5,8,19,p);c.drawLine(16,5,16,19,p);break;
                case "once":c.drawRoundRect(4,3,20,21,3,3,p);c.drawLine(8,8,16,8,p);c.drawLine(8,12,16,12,p);c.drawLine(8,16,13,16,p);break;
                case "book":{Path path=new Path();path.moveTo(12,6);path.cubicTo(9,3,5,3,2,5);path.lineTo(2,20);path.cubicTo(5,18,9,18,12,21);path.cubicTo(15,18,19,18,22,20);path.lineTo(22,5);path.cubicTo(19,3,15,3,12,6);path.lineTo(12,21);c.drawPath(path,p);break;}
                case "crop":c.drawLine(7,2,7,17,p);c.drawLine(7,17,22,17,p);c.drawLine(2,7,17,7,p);c.drawLine(17,7,17,22,p);break;
                case "show":case "hide":{Path path=new Path();path.moveTo(2,12);path.cubicTo(7,3,17,3,22,12);path.cubicTo(17,21,7,21,2,12);c.drawPath(path,p);c.drawCircle(12,12,3,p);if(kind.equals("hide"))c.drawLine(3,3,21,21,p);break;}
                case "stop":c.drawArc(4,4,20,21,-50,280,false,p);c.drawLine(12,2,12,12,p);break;
            }
            c.restoreToCount(save);
        }
        @Override public void setAlpha(int a){p.setAlpha(a);invalidateSelf();}
        @Override public void setColorFilter(ColorFilter f){p.setColorFilter(f);invalidateSelf();}
        @Override public int getOpacity(){return PixelFormat.TRANSLUCENT;}
    }
}
