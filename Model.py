from cx_Oracle import *
class Model:
    def __init__(self):
        self.song_dict={}
        self.db_status=True
        self.conn=None
        self.cur=None
        try:
            self.conn=connect("mouzikka/music@DESKTOP-D1U1HFD/xe")
            print("connect open successfull")
            self.cur=self.conn.cursor()
        except DatabaseError as ex:
            self.db_status=False
            print(ex)
    def get_db_status(self):
        return self.db_status
    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor closed successfully")
        if self.conn is not None:
            self.conn.close()
            print("Disconnect successfully from db")
    def add_song(self,song_name,song_path):
        self.song_dict[song_name]=song_path
        print("song added",self.song_dict[song_name])

    def get_song_path(self,song_name):
        return self.song_dict[song_name]
    def remove_song(self,song_name):
        self.song_dict.pop(song_name)
        print(self.song_dict)
    def search_song_in_favourites(self,song_name):
        self.cur.execute("select song_name from myfauvorites where song_name=:1",(song_name,))
        song_tuple=self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True
    def add_song_to_favourites(self,song_name,song_path):
        song_present=self.search_song_in_favourites(song_name)
        if song_present:
            return "Song already present in your favorites"
        self.cur.execute("select max(song_id) from myfauvorites")
        last_id=self.cur.fetchone()[0]
        next_id=1
        if last_id is not None:
            next_id=last_id+1
        self.cur.execute("insert into myfauvorites values(:1,:2,:3)",(next_id,song_name,song_path))
        self.conn.commit()
        return "song added to your fauvorites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfauvorites")
        song_pre=False
        for song_name,song_path in self.cur:
            self.song_dict[song_name]=song_path
            song_pre=True
        if song_pre is True:
            return "List Populated from my favorites"
        else:
            return "No song present in my favorites"


    def remove_song_from_favorites(self,song_name):
        self.cur.execute("delete from myfauvorites where song_name =:1",(song_name,))
        self.conn.commit()
        if self.cur.rowcount==1:
         return "Song delete from your favorites"
        else:
            return "Song not present in your favorites"


if __name__=="__main__":
    m=Model()
    print(m.db_status)






