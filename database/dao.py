from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_nodes( n_alb):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select t1.id_a,  t1.name_a
                from(SELECT ar.id as id_a, ar.name as name_a, COUNT(al.id) as n_album
                        FROM artist ar, album al
                        where al.artist_id = ar.id
                        group by id_a,  name_a) as t1
                where t1.n_album >= %s
                """
        cursor.execute(query,(n_alb,))
        for row in cursor:
            artist = Artist(id=row['id_a'], name=row['name_a'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artits_album(n_alb):

        conn = DBConnect.get_connection()
        dict = {}
        dict_final = {}
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.id as id_a, ar.name as name_a, al.id as id_al
                FROM artist ar, album al
                where al.artist_id = ar.id
                """
        cursor.execute(query)
        for row in cursor:
            if row['id_a'] not in dict:
                dict[row['id_a']] = {"name":row['name_a'], "album":{row["id_al"]}}
            dict[row['id_a']]["album"].add(row["id_al"])
        for id_a in dict:
            if len(dict[id_a]["album"]) >= n_alb:
                result.append(Artist(id_a, dict[id_a]["name"]))
                dict_final[id_a] = dict[id_a]
        cursor.close()
        conn.close()
        return result, dict_final

    @staticmethod
    def get_generi():

        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                select album_id, genre_id
                FROM track
                order by album_id ASC
                """
        cursor.execute(query)
        for row in cursor:
            if row['album_id'] not in result:
                result[row['album_id']] = {"generi":{row["genre_id"]}}
            result[row['album_id']]["generi"].add(row["genre_id"])
        
        cursor.close()
        conn.close()
        return result
