package org.w3.translate;

import android.content.Context;
import android.graphics.*;
import android.graphics.drawable.Drawable;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;

/** Small native surfaces with a light upper-left and dark lower-right shadow. */
final class SoftControls {
    static final int INK=0xff30383b, MUTED=0xff586269, GREEN=0xff17685c, RED=0xff923d3d;
    private SoftControls() {}

    static void surface(View view,float radius,boolean active){
        view.setLayerType(View.LAYER_TYPE_SOFTWARE,null);
        view.setBackground(new Surface(view.getContext(),radius,active));
        view.setElevation(0);
    }
    static Button button(Context c,String label,String icon,boolean active,boolean destructive){
        Button b=new Button(c);
        b.setText(label);b.setAllCaps(false);b.setTextSize(13);b.setMaxLines(2);
        b.setMinWidth(0);b.setMinimumWidth(0);b.setMinHeight(0);b.setMinimumHeight(0);
        b.setGravity(Gravity.CENTER);b.setIncludeFontPadding(false);
        b.setBackgroundTintList(null);surface(b,20,active);
        b.setPadding(Ui.dp(c,9),Ui.dp(c,10),Ui.dp(c,9),Ui.dp(c,10));
        int ink=destructive?RED:active?GREEN:INK;b.setTextColor(ink);
        Icon glyph=new Icon(icon,ink);glyph.setBounds(0,0,Ui.dp(c,23),Ui.dp(c,23));
        b.setCompoundDrawables(null,glyph,null,null);b.setCompoundDrawablePadding(Ui.dp(c,3));
        return b;
    }
    private static final class Surface extends Drawable {
        private final Paint paint=new Paint(Paint.ANTI_ALIAS_FLAG);
        private final float inset,radius,blur,offset;
        private final boolean active;
        private boolean pressed;
        private int alpha=255;
        Surface(Context c,float r,boolean a){inset=Ui.dp(c,7);radius=Ui.dp(c,r);blur=Ui.dp(c,5);offset=Ui.dp(c,3);active=a;}
        @Override public void draw(Canvas canvas){
            Rect b=getBounds();RectF face=new RectF(b.left+inset,b.top+inset,b.right-inset,b.bottom-inset);
            if(face.width()<=0 || face.height()<=0)return;
            paint.setAlpha(alpha);paint.setStyle(Paint.Style.FILL);
            int color=pressed?0xffd2d8d9:active?0xffdce7e3:0xffe3e5e7;
            paint.setColor(color);
            if(!pressed){
                paint.setShadowLayer(blur,-offset,-offset,0xfaffffff);canvas.drawRoundRect(face,radius,radius,paint);
                paint.setShadowLayer(blur,offset,offset,0x707a838b);canvas.drawRoundRect(face,radius,radius,paint);
            }
            paint.clearShadowLayer();
            paint.setShader(new LinearGradient(face.left,face.top,face.right,face.bottom,
                pressed?color:active?0xffe5eeea:0xffeceef0,color,Shader.TileMode.CLAMP));
            canvas.drawRoundRect(face,radius,radius,paint);paint.setShader(null);
            paint.setStyle(Paint.Style.STROKE);paint.setStrokeWidth(1f);
            paint.setColor(pressed?0xffa7b2b4:0x90ffffff);canvas.drawRoundRect(face,radius,radius,paint);
            paint.setStyle(Paint.Style.FILL);
        }
        @Override public boolean isStateful(){return true;}
        @Override protected boolean onStateChange(int[] states){
            boolean next=false;for(int state:states)if(state==android.R.attr.state_pressed)next=true;
            if(pressed==next)return false;pressed=next;invalidateSelf();return true;
        }
        @Override public void setAlpha(int a){alpha=a;invalidateSelf();}
        @Override public void setColorFilter(ColorFilter f){paint.setColorFilter(f);invalidateSelf();}
        @Override public int getOpacity(){return PixelFormat.TRANSLUCENT;}
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
