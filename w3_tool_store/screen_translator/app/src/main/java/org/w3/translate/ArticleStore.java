package org.w3.translate;

import android.content.*;
import android.database.Cursor;
import android.database.sqlite.*;
import java.util.*;

/** Persistent app-private database under files/databases, never cacheDir. */
final class ArticleStore extends SQLiteOpenHelper {
    ArticleStore(Context c){super(c.getApplicationContext(),"reading.db",null,2);setWriteAheadLoggingEnabled(true);}
    @Override public void onConfigure(SQLiteDatabase db){db.setForeignKeyConstraintsEnabled(true);}
    @Override public void onCreate(SQLiteDatabase db){
        db.execSQL("CREATE TABLE articles (id INTEGER PRIMARY KEY,title TEXT NOT NULL,url TEXT NOT NULL UNIQUE,language TEXT NOT NULL,notice TEXT NOT NULL,saved INTEGER NOT NULL,scroll INTEGER NOT NULL DEFAULT 0,web_section TEXT NOT NULL DEFAULT '')");
        db.execSQL("CREATE TABLE blocks (article INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,pos INTEGER NOT NULL,kind TEXT NOT NULL,level INTEGER NOT NULL,original TEXT NOT NULL,thai TEXT NOT NULL DEFAULT '',PRIMARY KEY(article,pos))");
    }
    @Override public void onUpgrade(SQLiteDatabase db,int old,int next){
        if(old==1 && next==2){
            db.execSQL("ALTER TABLE articles ADD COLUMN web_section TEXT NOT NULL DEFAULT ''");
            return;
        }
        throw new IllegalStateException("Unsupported reading database version");
    }
    long find(String url){try(Cursor c=getReadableDatabase().rawQuery("SELECT id FROM articles WHERE url=?",new String[]{url})){return c.moveToFirst()?c.getLong(0):0;}}
    long save(Article a){
        SQLiteDatabase db=getWritableDatabase();db.beginTransaction();
        try{
            ContentValues v=new ContentValues();v.put("title",a.title);v.put("url",a.url);v.put("language",a.language);v.put("notice",a.notice);v.put("saved",a.savedAt);v.put("web_section",a.webSection);
            long id=db.insertOrThrow("articles",null,v);
            writeBlocks(db,id,a.blocks);
            db.setTransactionSuccessful();a.id=id;return id;
        }finally{db.endTransaction();}
    }
    long saveFetched(String requestedUrl,Article fetched){
        SQLiteDatabase db=getWritableDatabase();db.beginTransaction();
        try{
            Article requested=load(find(requestedUrl));
            Article canonical=requestedUrl.equals(fetched.url)?requested:load(find(fetched.url));
            long id;
            if(canonical!=null && !canonical.linkOnly()){
                id=canonical.id;
                if(requested!=null && requested.linkOnly() && canonical.webSection.isEmpty()){
                    webSection(id,requested.webSection);
                }
            }else if(canonical!=null || requested!=null){
                Article pending=canonical!=null?canonical:requested;
                id=pending.id;
                ContentValues values=new ContentValues();
                values.put("title",fetched.title);values.put("url",fetched.url);
                values.put("language",fetched.language);values.put("notice",fetched.notice);
                if(pending.webSection.isEmpty() && requested!=null)values.put("web_section",requested.webSection);
                db.update("articles",values,"id=?",new String[]{Long.toString(id)});
                writeBlocks(db,id,fetched.blocks);
            }else{
                id=save(fetched);
            }
            if(requested!=null && requested.linkOnly() && requested.id!=id)delete(requested.id);
            db.setTransactionSuccessful();
            return id;
        }finally{db.endTransaction();}
    }
    void webSection(long id,String section){
        ContentValues values=new ContentValues();values.put("web_section",section);
        getWritableDatabase().update("articles",values,"id=?",new String[]{Long.toString(id)});
    }
    long saveNote(Article note){
        if(note.id==0)return save(note);
        SQLiteDatabase db=getWritableDatabase();
        db.beginTransaction();
        try{
            ContentValues title=new ContentValues();title.put("title",note.title);title.put("language",note.language);
            db.update("articles",title,"id=?",new String[]{Long.toString(note.id)});
            Article.Block block=note.blocks.get(0);
            ContentValues body=new ContentValues();body.put("original",block.original);body.put("thai",block.thai);
            db.update("blocks",body,"article=? AND pos=0",new String[]{Long.toString(note.id)});
            db.setTransactionSuccessful();
            return note.id;
        }finally{db.endTransaction();}
    }
    long mergeScreen(Article incoming){
        SQLiteDatabase db=getWritableDatabase();db.beginTransaction();
        try{
            long id=find(incoming.url);
            if(id==0){
                List<Article.Block> captured=new ArrayList<>(incoming.blocks);
                incoming.blocks.clear();
                incoming.mergeScreen(captured);
                id=save(incoming);
                db.setTransactionSuccessful();
                return id;
            }
            Article saved=load(id);
            int position=scroll(id);
            Article.Block current=position>0 && position<=saved.blocks.size()?saved.blocks.get(position-1):null;
            saved.mergeScreen(incoming.blocks);
            if(current!=null)scroll(id,saved.blocks.indexOf(current)+1);
            db.delete("blocks","article=?",new String[]{""+id});
            writeBlocks(db,id,saved.blocks);
            db.setTransactionSuccessful();return id;
        }finally{db.endTransaction();}
    }
    private void writeBlocks(SQLiteDatabase db,long id,List<Article.Block> blocks){
        for(int i=0;i<blocks.size();i++){
            Article.Block b=blocks.get(i);ContentValues row=new ContentValues();
            row.put("article",id);row.put("pos",i);row.put("kind",b.kind);row.put("level",b.level);
            row.put("original",b.original);row.put("thai",b.thai);db.insertOrThrow("blocks",null,row);
        }
    }
    Article load(long id){
        Article a=new Article();a.id=id;
        try(Cursor c=getReadableDatabase().rawQuery("SELECT title,url,language,notice,saved,web_section FROM articles WHERE id=?",new String[]{""+id})){
            if(!c.moveToFirst())return null;a.title=c.getString(0);a.url=c.getString(1);a.language=c.getString(2);a.notice=c.getString(3);a.savedAt=c.getLong(4);a.webSection=c.getString(5);
        }
        try(Cursor c=getReadableDatabase().rawQuery("SELECT kind,level,original,thai FROM blocks WHERE article=? ORDER BY pos",new String[]{""+id})){
            while(c.moveToNext()){Article.Block b=new Article.Block(c.getString(0),c.getInt(1),c.getString(2));b.thai=c.getString(3);a.blocks.add(b);}
        }
        return a;
    }
    List<Article> list(String search){
        String like="%"+search.replace("\\","\\\\").replace("%","\\%").replace("_","\\_")+"%";
        List<Article> rows=new ArrayList<>();
        String sql="SELECT id,title,url,language,saved,web_section FROM articles a WHERE title LIKE ? ESCAPE '\\' OR url LIKE ? ESCAPE '\\' OR web_section LIKE ? ESCAPE '\\' OR EXISTS(SELECT 1 FROM blocks b WHERE b.article=a.id AND (original LIKE ? ESCAPE '\\' OR thai LIKE ? ESCAPE '\\')) ORDER BY saved DESC";
        try(Cursor c=getReadableDatabase().rawQuery(sql,new String[]{like,like,like,like,like})){
            while(c.moveToNext()){Article a=new Article();a.id=c.getLong(0);a.title=c.getString(1);a.url=c.getString(2);a.language=c.getString(3);a.savedAt=c.getLong(4);a.webSection=c.getString(5);rows.add(a);}
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
