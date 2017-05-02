# coding: utf8

import uuid
import hashlib
import unicodedata
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


def valider_article(articles):
    erreur_data = {}
    if valider_champs(articles.auteur):
        erreur_data.update({"auteur": "Nom d'auteur invalide"})
    if valider_champs(articles.titre):
        erreur_data.update({"titre": "Titre invalide"})
    if valider_texte(articles.texte):
        erreur_data.update({"texte": "Paragraphe est invalide"})
    if valider_mydate(articles.mydate):
        erreur_data.update({"mydate": "Date est invalide"})
    if valider_url(articles.url):
        erreur_data.update({"url": "l'url est invalide ou il exite deja"})
    return erreur_data


def valider_mise_a_jour(article):
    erreur_data = {}
    if article.titre == "" or valider_champs(article.titre):
        erreur_data.update({"titre": "Titre invalide"})
    if article.texte == "" or valider_texte(article.texte):
        erreur_data.update({"texte": "le texte est invalide"})
    return erreur_data


def valider_mydate(mydate):
    if not mydate:
        return True
    return False


def valider_texte(texte):
    if not texte:
        return True
    count = 0
    for lettre in texte:
        if lettre == '\n':
            count = count + 1
    if count > 1:
        return True
    else:
        return False


def valider_url(url):
    if not url:
        return True
    for lettre in url:
        if not(lettre == "-" or lettre.isalnum()):
            return True
    return get_db().select_url(url)


def enlever_accent(texte):
    return unicodedata.normalized('NFKD', texte).encode('ASCII', 'ignore')


def valider_champs(champs):
    if not champs:
        return True
    for lettre in champs:
        if not (lettre.isalnum() or lettre == " "):
            return True
    return False


def validerJSONarticle(data):
    if 'auteur' not in data:
        return "auteur missing", 327
    if 'titre' not in data:
        return "titre missing", 328
    if 'texte' not in data:
        return "texte missing", 329
    if 'date' not in data:
        return "date missing", 330
    if 'url' not in data:
        return "url missing", 331
    return True


def valider_mot_passe(motpasse, motpasse2):
    erreur_data = []
    upper = 0
    nonalphanum = 0
    isnumeric = 0
    alpha = 0
    lower = 0
    if motpasse == motpasse2:
        if len(motpasse) < 8:
            erreur_data.append("moins de 8 caracteres")
        for l in motpasse:
            if l.isupper():
                upper = 1
            if not l.isalnum():
                nonalphanum = 1
            if l.isnumeric():
                nombre = 1
            if l.isalpha():
                alpha = 1
            if l.islower():
                lower = 1
        if upper == 0:
            erreur_data.append("doit un caractere en majuscule")
        if nonalphanum == 0:
            erreur_data.append("manque un caractere special ex [@,#,%,*]")
        if alpha == 0:
            erreur_data.append("manque un chiffre entre [0-9]")
        if upper == 0:
            erreur_data.append("manque un caractere en minuscule")
        if alpha == 0:
            erreur_data.append("manque un caractere [a-z]")
    else:
        erreur_data.append("les deux mots passe sont differant")
    return erreur_data


def valider_donnees_usager(nom, courriel, motpasse, motpasse2):
    erreur = {}
    if nom == "":
        erreur.update({"nom": "nom vide"})
    if courriel == "":
        erreur.update({"courriel": "courriel vide"})
    else:
        if not get_db().valider_courriel(courriel):
            erreur.update({"courriel": "le courriel existe deja"})
    if motpasse == "":
        erreur.update({"motpasse": "mot passe vide"})
    if motpasse2 == "":
        erreur.update({"motpasse2": "mot passe de verification vide"})
    return erreur
