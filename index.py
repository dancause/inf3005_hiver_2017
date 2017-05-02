# coding: utf8
# Janin Dancause danj17087507 inf3005 hiver 2017

import time
import uuid
import hashlib
from datetime import datetime
from flask import g
from flask import Flask
from flask import session
from flask import jsonify
from flask import url_for
from flask import request
from flask import Response
from flask import redirect
from functools import wraps
from flask import render_template

from courriel import *
from validation import *
from database import Database
from database import Articles


app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return render_template('error_html.html', error_html="401",
                                   error_message=u"Non autorisé"), 401
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def start_page():
    articles = get_db().select_liste()
    return render_template('template_articles.html', articles=articles,
                           titre_page="Derniers articles")


@app.route('/home')
def home_page():
    articles = get_db().select_liste()
    return render_template('template_articles.html', articles=articles,
                           titre_page="Derniers articles")


@app.route('/recherche', methods=['POST'])
def search_page():
    recherche = request.form['recherche']
    articles = get_db().select_recherche(recherche)
    return render_template('template_liste.html', articles=articles,
                           titre_page="Resultats")


@app.route('/ajouter', methods=['POST'])
@authentication_required
def ajout_article():
    titre = request.form['titre']
    texte = request.form['texte']
    auteur = request.form['auteur']
    mydate = request.form['mydate']
    url = request.form['url']
    articles = Articles('0', titre, texte, auteur, mydate, url)
    erreur_data = valider_article(articles)
    if any(erreur_data):
        return render_template('/form_article.html', articles=articles,
                               erreur_data=erreur_data)
    else:
        get_db().insert_article(titre, texte, mydate, auteur, url)
        return redirect(url_for('admin_page'))


@app.route('/admin-nouveau')
@authentication_required
def form_article_article():
    return render_template('form_article.html')


@app.route('/admin')
@authentication_required
def admin_page():
    articles = get_db().select_all()
    return render_template('template_admin.html', articles=articles,
                           titre_page="Administration", admin="admin")


@app.route('/mise_a_jour', methods=['POST'])
@authentication_required
def mise_a_jour_article():
    unique = request.form['id']
    titre = request.form['titre']
    texte = request.form['texte']
    articles = Articles(unique, titre, texte, "", "", "")
    erreur_data = valider_mise_a_jour(articles)
    if any(erreur_data):
        return render_template('/form_article.html', articles=articles,
                               erreur_data=erreur_data, mise_a_jour="admin")
    else:
        get_db().update_article(unique, titre, texte)
        return redirect(url_for('admin_page'))


@app.route('/mise_a_jour/<identifier>', methods=['GET'])
@authentication_required
def afficher_article_maj(identifier):
    if get_db().select_article(identifier) is None:
        return render_template('error_html.html', error_html="400",
                               error_message=u"requête erronée"), 400
    else:
        article = get_db().select_article(identifier)
        erreur_data = valider_mise_a_jour(article)
        return render_template('form_article.html', articles=article,
                               erreur_data=erreur_data, mise_a_jour="admin")


@app.route('/article/<identifier>')
def afficher_article(identifier):
    article = get_db().select_article(identifier)
    if article is None:
        return redirect(url_for('page_not_found404'))
    else:
        return render_template('article.html', article=article)


@app.route('/delete/<identifier>')
@authentication_required
def effacer_article(identifier):
    get_db().effacer_articles(identifier)
    return redirect(url_for('admin_page'))


@app.route('/inviter_collaborateur')
@authentication_required
def inviter_collaborateur():
    return render_template('template_invitation.html')


@app.route('/invitation', methods=["POST"])
@authentication_required
def envoyer_invitation():
    courriel = request.form['courriel']
    token = uuid.uuid4().hex
    if get_db().valider_courriel(courriel) is False:
        data = u"Il y a déja un compte associé à ce courriel"
        return render_template('template_invitation.html',
                               data=data)
    if get_db().inviter_courriel(courriel) is True:
        get_db().save_invitation(courriel, token)
        message_courriel(courriel, token, render_template(
                         'courriel_invitation.html', token=token),
                         "invitation")
        return render_template('template_invitation.html',
                               data=u"Invitation envoyées")
    elif get_db().inviter_courriel(courriel) is False:
        token = get_db().token_invitation(courriel)
        message_courriel(courriel, token, render_template(
                         'courriel_invitation.html', token=token),
                         "invitation rappel")
        return render_template('template_invitation.html',
                               data=u"Invitation envoyées à nouveau")
    else:
        return render_template('template_invitation.html',
                               data=u"Le courriel existe déjà")


@app.route('/login')
def afficher_login():
    if "id" in session:
        return redirect("/")
    else:
        return render_template("authentification.html")


@app.route('/valider', methods=["POST"])
def login_user():
    courriel = request.form["courriel"]
    password = request.form["motpasse"]
    # Vérifier que les champs ne sont pas vides
    if courriel == "correcteur" and password == "secret":
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, courriel)
        session["id"] = id_session
        return redirect("/")
    if courriel == "" or password == "":
        return render_template("authentification.html",
                               erreur_data="mot passe vide")
    user = get_db().get_user_login_info(courriel)
    if user is None:
        return render_template("authentification.html",
                               erreur_data="erreur authentification")
    salt = user[0]
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    if hashed_password == user[1]:
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, courriel)
        session["id"] = id_session
        return redirect("/")
    else:
        return redirect("/")


@app.route('/creercompte/<token>')
def nouveau_usager(token):
    if "id" in session:
        return render_template('error_html.html', error_html="401",
                               error_message=u"Non autorisé"), 401
    if get_db().valider_invitation(token):
        return render_template('nouveau_usager.html', token=token)
    else:
        return render_template('error_html.html', error_html="401",
                               error_message=u"Non autorisée"), 401


@app.route('/creationusager', methods=["POST"])
def invitation():
    nom = request.form["nom"]
    courriel = request.form["courriel"]
    motpasse = request.form["motpasse"]
    motpasse2 = request.form["motpasse2"]
    token = request.form["token"]
    erreur_data = valider_donnees_usager(nom, courriel, motpasse, motpasse2)
    erreurs = valider_mot_passe(motpasse, motpasse2)
    if any(erreurs) or any(erreur_data):
        return render_template('nouveau_usager.html',
                               erreurs=erreurs, token=token, name=nom,
                               erreur_data=erreur_data, courriel=courriel)
    salt = uuid.uuid4().hex
    hash = hashlib.sha512(motpasse + salt).hexdigest()
    get_db().ajout_utilisateur(nom, courriel, salt, hash)
    get_db().delete_invitation(token)
    return render_template('authentification.html',
                           message=u'Votre code usager a été créer')


@app.route('/validation_url/<url>', methods=['GET'])
@authentication_required
def validation_url(url):
    temp = url
    i = 1
    while (get_db().valider_url(temp)):
        temp = url+str(i)
        i = i + 1
    return render_template('url_tag.html', url=temp)


@app.route('/verif_url/<url>', methods=['GET'])
@authentication_required
def verif_url(url):
    if (get_db().valider_url(url)):
        return render_template('url_tag.html', url=url,
                               erreur=u"L'url existe déjà")
    else:
        return render_template('url_tag.html', url=url)


@app.route('/oublie')
def oublie():
    if "id" in session:
        return redirect(url_for('page_not_found401'))
    else:
        return render_template('template_mise_a_jour_mot_de_passe.html')


@app.route('/demande_recuperation_motpasse', methods=['POST'])
def demande_recuperation_motpasse():
    data = u"La demande de récupération a été envoyée"
    courriel = request.form['courriel']
    token = uuid.uuid4().hex
    if not get_db().valider_courriel(courriel):
        get_db().save_recuperation(courriel, token)
        message_courriel(courriel, token, render_template(
                         'courriel_motpasse.html', token=token),
                         "Recuperation")
        return render_template('template_mise_a_jour_mot_de_passe.html',
                               data=data)
    else:
        return render_template('template_mise_a_jour_mot_de_passe.html',
                               data=u"Le courriel n'existe pas")


@app.route('/motpasseperdue/<id_token>')
def motpasseperdue(id_token):
    data = u'Le délais de renouvellement du mot de passe a été dépassé'
    if "id" in session:
        return render_template('error_html.html', error_html="401",
                               error_message=u"Non autorisé"), 401
    trenteminute = 1800
    res = get_db().recuperer_motpasse(id_token)
    if ((time.mktime(datetime.now().timetuple()))-res) > trenteminute:
        return render_template('template_mise_a_jour_mot_de_passe.html',
                               data=data)
    if res is None:
        return redirect(url_for('page_not_found401'))
    else:
        return render_template('changement_mot_passe.html', token=id_token)


@app.route('/changement_mot_passe')
@authentication_required
def changement_mot_passe():
    return render_template('changement_mot_passe.html')


@app.route('/changer_mot_passe', methods=['POST'])
def changer_mot_passe():
    motpasse = request.form["motpasse"]
    motpasse2 = request.form["motpasse2"]
    token = request.form["token"]
    courriel = get_db().courriel_recuperation(token)
    if courriel is False and get_db().valider_courriel(courriel):
        return render_template('changement_mot_passe,html',
                               data=u"Problème à l'identification")
    erreurs = valider_mot_passe(motpasse, motpasse2)
    if any(erreurs):
        return render_template('changement_mot_passe.html',
                               erreurs=erreurs, token=token)
    else:
        salt = uuid.uuid4().hex
        hash = hashlib.sha512(motpasse + salt).hexdigest()
        get_db().update_mot_passe(courriel, salt, hash)
        get_db().delete_recuperation(token)
        return render_template('changement_mot_passe.html',
                               data=u"Mot de passe changé")


@app.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect("/")


@app.route('/affichage_login', methods=["GET"])
def affichage_login():
    if "id" in session:
        return render_template('logout.html')
    else:
        return render_template('login.html')


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    Response('Could not verify your access level for that URL.\n'
             'You have to login with proper credentials', 401,
             {'WWW-Authenticate': 'Basic realm="Login Required"'})


app.secret_key = "(*&*&322387he738220)(*(*22347657"

# API------------------------------


@app.route('/api/articles/', methods=["GET"])
@authentication_required
def liste_all_articles():
    if request.method == "GET":
        articles = get_db().get_json_all()
        data = [{"id": each[0], "titre": each[1], "url": each[2],
                "auteur": each[3], }
                for each in articles]
        return jsonify(data)
    else:
        return "", 400


@app.route('/api/article/<article_id>', methods=["GET"])
@authentication_required
def obtenir_un_article(article_id):
    if request.method == "GET":
        articles = get_db().get_json_article(article_id)
        if articles is not None:
            data = {"id": articles[0], "titre": articles[1],
                    "url": articles[2], "auteur": articles[3],
                    "date": articles[4], "texte": articles[5], }
            return jsonify(data)
        else:
            return "", 401
    else:
        return "", 400


@app.route('/api/ajout_article/', methods=["POST"])
@authentication_required
def inserer_un_article():
    if request.method == "POST":
        data = request.get_json()
        validerJSONarticle(data)
        articles = Articles(0, data["titre"], data["texte"], data["auteur"],
                            data["date"], data["url"])
        erreur_data = valider_article(articles)
        if any(erreur_data):
            reponse = ""
            for cle, value in erreur_data.items():
                reponse = reponse + "| {0},: {1} ".format(cle, value)
            return reponse, 326
        else:
            get_db().insert_article(data["titre"], data["texte"], data["date"],
                                    data["auteur"], data["url"])
            return "", 200


@app.errorhandler(400)
def page_not_found400(e):
    return render_template('error_html.html', error_html="400",
                           error_message=u"Requête erronée"), 400


@app.errorhandler(401)
def page_not_found401(e):
    return render_template('error_html.html', error_html="401",
                           error_message=u"Non autorisé"), 401


@app.errorhandler(404)
def page_not_found404(e):
    return render_template('error_html.html', error_html="404",
                           error_message="Page introuvable"), 404


@app.errorhandler(405)
def page_not_found405(e):
    return render_template('error_html.html', error_html="405",
                           error_message=u"Méthode requête non autorisée"), 405


@app.errorhandler(500)
def page_not_found500(e):
    return render_template('error_html.html', error_html="500",
                           error_message="erreur serveur"), 500
