import sqlite3
from datetime import datetime
import time


class Articles:
    def __init__(self, unique, titre, texte, auteur, mydate, url):
        self.unique = unique
        self.titre = titre
        self.texte = texte
        self.mydate = mydate
        self.auteur = auteur
        self.url = url


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/cms_db.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def insert_article(self, titre, texte, mydate, auteur, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("""insert into article(titre, paragraphe, date_publication,
                        auteur, identifiant)values(?, ?, ?, ?, ?)"""),
                       (titre, texte, mydate, auteur, url))
        connection.commit()

    def select_liste(self):
        connection = self.get_connection()

        cursor = connection.cursor()
        cursor.execute("""select * from article where date_publication <=
                       (select date('now'))
                       order by date_publication desc limit 5""")
        listes = []
        for row in cursor:
            p = Articles(row[0], row[1], row[5], row[3], row[4], row[2])
            listes.append(p)
        return listes

    def select_all(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from article order by date_publication desc")
        listes = []
        for row in cursor:
            p = Articles(row[0], row[1], row[5], row[3], row[4], row[2])
            listes.append(p)
        return listes

    def get_json_all(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article order by date_publication desc")
        articles = cursor.fetchall()
        return [(un_article[0], un_article[1], un_article[2], un_article[3],
                 un_article[4], un_article[5]) for un_article in articles]

    def get_json_article(self, id_article):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from article where id = ?"), (id_article, ))
        article = cursor.fetchone()
        if article is None:
            return None
        else:
            return (article[0], article[1], article[2], article[3], article[4],
                    article[5])

    def select_recherche(self, recherche):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""select * from article where date_publication <=
                        (select date('now')) and
                        (titre like ? or paragraphe like ?)
                        order by date_publication desc""",
                       ("%"+recherche+"%", "%"+recherche+"%", ))
        listes = []
        for row in cursor:
            p = Articles(row[0], row[1], row[5], row[3], row[4], row[2])
            listes.append(p)
        return listes

    def select_url(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from article where identifiant like ?",
                       (url, ))
        row = cursor.fetchone()
        if row:
            return True
        else:
            return False

    def select_article(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from article where identifiant like ?",
                       (url, ))
        for row in cursor:
                article = Articles(row[0], row[1], row[5],
                                   row[3], row[4], row[2])
        if article is None:
            return None
        else:
            return article

    def update_article(self, unique, titre, texte):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("update article set titre=?,paragraphe=? where id=?",
                       (titre, texte, unique, ))
        connection.commit()

    def effacer_articles(self, unique):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("delete from article where id=?", (unique, ))
        connection.commit()

    def ajout_utilisateur(self, nom, courriel, salt, hash):
        connection = self.get_connection()
        connection.execute(("""insert into users(nom,courriel,salt,hash)values
                           (?,?,?,?)"""), (nom, courriel, salt, hash))
        connection.commit()

    def get_user_login_info(self, courriel):
        cursor = self.get_connection().cursor()
        cursor.execute(("select salt, hash from users where courriel=?"),
                       (courriel, ))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    def save_session(self, id_session, username):
        connection = self.get_connection()
        connection.execute(("insert into sessions(id_session, courriel) "
                            "values(?, ?)"), (id_session, username))
        connection.commit()

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("delete from sessions where id_session=?"),
                           (id_session, ))
        connection.commit()

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("select courriel from sessions where id_session=?"),
                       (id_session, ))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def save_invitation(self, courriel, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into invitation(courriel, token) "
                        "values(?, ?)"), (courriel, token))
        connection.commit()

    def save_recuperation(self, courriel, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into recuperations(courriel, token, "
                        "date_demande) values(?, ?, ?)"), (courriel, token,
                        time.mktime(datetime.now().timetuple()), ))
        connection.commit()

    def inviter_courriel(self, courriel):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from invitation where courriel like ?"),
                       (courriel, ))
        data = cursor.fetchone()
        if data is None:
            return True
        else:
            return False

    def valider_courriel(self, courriel):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from users where courriel like ?"),
                       (courriel, ))
        data = cursor.fetchone()
        if data is None:
            return True
        else:
            return False

    def valider_invitation(self, id_token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from invitation where token like ?"),
                       (id_token, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def delete_invitation(self, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("delete from invitation where token=?"),
                       (token, ))
        connection.commit()

    def update_mot_passe(self, courriel, salt, hash):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("update users set salt=?, hash =? where courriel=?"),
                       (salt, hash, courriel, ))
        connection.commit()

    def courriel_session(self, id_session):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select courriel from sessions where id_session "
                       "like ?"), (id_session, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return data

    def courriel_recuperation(self, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select courriel from recuperations where token "
                       "like ?"), (token, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return data[0]

    def recuperer_motpasse(self, id_token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select date_demande from recuperations where "
                       "token like ?"), (id_token,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def delete_recuperation(self, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("delete from recuperations where token=?"),
                       (token, ))
        connection.commit()

    def valider_url(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from article where identifiant like ?"),
                       (url, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def token_invitation(self, courriel):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from invitation where courriel like ?"),
                       (courriel, ))
        data = cursor.fetchone()
        return data[2]
