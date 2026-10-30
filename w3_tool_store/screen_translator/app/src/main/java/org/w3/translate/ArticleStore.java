package org.w3.translate;

import android.content.*;
import android.database.Cursor;
import android.database.sqlite.*;
import java.util.*;

/** Persistent app-private database under files/databases, never cacheDir. */
final class ArticleStore extends SQLiteOpenHelper {
    ArticleStore(Context c){super(c.getApplicationContext(),"reading.db",null,1);setWriteAheadLoggingEnabled(true);}
    @Override public void onConfigure(SQLiteDatabase db){db.setForeignKeyConstraintsEnabled(true);}
    @Override public void onCreate(SQLiteDatabase db){
        db.execSQL("CREATE TABLE articles (id INTEGER PRIMARY KEY,title TEXT NOT NULL,url TEXT NOT NULL UNIQUE,language TEXT NOT NULL,notice TEXT NOT NULL,saved INTEGER NOT NULL,scroll INTEGER NOT NULL DEFAULT 0)");
        db.execSQL("CREATE TABLE blocks (article INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,pos INTEGER NOT NULL,kind TEXT NOT NULL,level INTEGER NOT NULL,original TEXT NOT NULL,thai TEXT NOT NULL DEFAULT '',PRIMARY KEY(article,pos))");
    }
    @Override public void onUpgrade(SQLiteDatabase db,int old,int next){throw new IllegalStateException("Unsupported reading database version");}
    long find(String url){try(Cursor c=getReadableDatabase().rawQuery("SELECT id FROM articles WHERE url=?",new String[]{url})){return c.moveToFirst()?c.getLong(0):0;}}
    long save(Article a){
        SQLiteDatabase db=getWritableDatabase();db.beginTransaction();
        try{
            ContentValues v=new ContentValues();v.put("title",a.title);v.put("url",a.url);v.put("language",a.language);v.put("notice",a.notice);v.put("saved",a.savedAt);
            long id=db.insertOrThrow("articles",null,v);
            for(int i=0;i<a.blocks.size();i++){Article.Block b=a.blocks.get(i);ContentValues row=new ContentValues();row.put("article",id);row.put("pos",i);row.put("kind",b.kind);row.put("level",b.level);row.put("original",b.original);row.put("thai",b.thai);db.insertOrThrow("blocks",null,row);}
            db.setTransactionSuccessful();a.id=id;return id;
        }finally{db.endTransaction();}
    }
    Article load(long id){
        Article a=new Article();a.id=id;
        try(Cursor c=getReadableDatabase().rawQuery("SELECT title,url,language,notice,saved FROM articles WHERE id=?",new String[]{""+id})){
            if(!c.moveToFirst())return null;a.title=c.getString(0);a.url=c.getString(1);a.language=c.getString(2);a.notice=c.getString(3);a.savedAt=c.getLong(4);
        }
        try(Cursor c=getReadableDatabase().rawQuery("SELECT kind,level,original,thai FROM blocks WHERE article=? ORDER BY pos",new String[]{""+id})){
            while(c.moveToNext()){Article.Block b=new Article.Block(c.getString(0),c.getInt(1),c.getString(2));b.thai=c.getString(3);a.blocks.add(b);}
        }
        return a;
    }
    List<Article> list(String search){
        String like="%"+search.replace("\\","\\\\").replace("%","\\%").replace("_","\\_")+"%";
        List<Article> rows=new ArrayList<>();
        String sql="SELECT id,title,url,language,saved FROM articles a WHERE title LIKE ? ESCAPE '\\' OR url LIKE ? ESCAPE '\\' OR EXISTS(SELECT 1 FROM blocks b WHERE b.article=a.id AND (original LIKE ? ESCAPE '\\' OR thai LIKE ? ESCAPE '\\')) ORDER BY saved DESC";
        try(Cursor c=getReadableDatabase().rawQuery(sql,new String[]{like,like,like,like})){
            while(c.moveToNext()){Article a=new Article();a.id=c.getLong(0);a.title=c.getString(1);a.url=c.getString(2);a.language=c.getString(3);a.savedAt=c.getLong(4);rows.add(a);}
        }
        return rows;
    }
    void translate(long id,int pos,String thai){ContentValues v=new ContentValues();v.put("thai",thai);getWritableDatabase().update("blocks",v,"article=? AND pos=?",new String[]{""+id,""+pos});}
    void language(long id,String source,boolean reset){
        SQLiteDatabase db=getWritableDatabase();db.beginTransaction();
        try{
            ContentValues v=new ContentValues();v.put("language",source);db.update("articles",v,"id=?",new String[]{""+id});
            if(reset){ContentValues clear=new ContentValues();clear.put("thai","");db.update("blocks",clear,"article=?",new String[]{""+id});}
            db.setTransactionSuccessful();
        }finally{db.endTransaction();}
    }
    int scroll(long id){try(Cursor c=getReadableDatabase().rawQuery("SELECT scroll FROM articles WHERE id=?",new String[]{""+id})){return c.moveToFirst()?c.getInt(0):0;}}
    void scroll(long id,int y){ContentValues v=new ContentValues();v.put("scroll",y);getWritableDatabase().update("articles",v,"id=?",new String[]{""+id});}
    void delete(long id){getWritableDatabase().delete("articles","id=?",new String[]{""+id});}
}
