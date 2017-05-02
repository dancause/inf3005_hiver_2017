Il y a 3 API disponibles

pPour se connecter aux différant API l'utilisateur doit être connecter sur le site web 
avec un nom d'usager et mot de passe

 GET /api/articles/

retourne dans un fichier json la liste des articles présent dans la base de données


[
  {
    "auteur": "sadfdsfsdf", 
    "titre": "allo", 
    "url": "sdfsdf"
  }, 
  {
    "auteur": "sadfdsfsdf", 
    "titre": "allo", 
    "url": "testjson"
  }, 
  {
    "auteur": "sadfdsfsdf", 
    "titre": "allo", 
    "url": "testjson2"
  }, 
  {
    "auteur": "auteur", 
    "titre": "allo", 
    "url": "testjson3"
  }, 
  {
    "auteur": "test", 
    "titre": "allo comment ca va ", 
    "url": "allourl"
  }
]

GET api/articles/<index>

pour obtenir toutes les information d'un article il faut ajouter l'index de l'article
sinon vous obtiendrez une erreur de code 401 
si l'article existe on retourne le json et le code 200

   {
      "auteur": "sadfdsfsdf",
      "date": "2017-04-25",
      "id": 5,
      "texte": "sadfdsfsdafsdf",
      "titre": "allo",
      "url": "testjson"
   }


Ajouter

POST /api/ajout_article/

Pour ajouter un article il faut utiliser les 5 entrées

auteur ne doit pas être vide
date de format ISO
texte d'un paragraphe
titre ne doit être vide
url l'url est validé pour s'assurer qu'il n'existe pas déjà
	l'url ne doit pas avoir d'espace et de caractère accentué

si le fichier échoue a un des tests l'article ne sera pas créer

 {
      "auteur": "auteur",
      "date": "2017-04-25",
      "texte": "essaie d'un texte",
      "titre": "allo",
      "url": "testjson3"
   }

Les erreurs dans les cas ou il manque des clés dans le fichier json
auteur absent erreur 327
Titre absent erreur 328
Texte absent erreur 329
date absent erreur 330
url absent erreur 331

Pour les erreurs de valeur pour les différentes clés 400

