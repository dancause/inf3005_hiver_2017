Le site utilise une base de donnée SQLITE
le script de base se trouve dans le dossier db

le script peut être rouler dans l'utilitaire DB Browser for SQLITE

http://sqlitebrowser.org/

windows 32bits
https://github.com/sqlitebrowser/sqlitebrowser/releases/download/v3.9.1/DB.Browser.for.SQLite-3.9.1-win32.exe

windows 64bits
https://github.com/sqlitebrowser/sqlitebrowser/releases/download/v3.9.1/DB.Browser.for.SQLite-3.9.1-win64.exe

mac
https://github.com/sqlitebrowser/sqlitebrowser/releases/download/v3.9.1/DB.Browser.for.SQLite-3.9.1v2.dmg


commande shell

s'assurer de télécharger l'application SQLite pour le terminal

il faut entrer les commandes suivantes dans le terminal shell
vous devez aller dans le repertoire de la base de donnée avant d'exécuter les commandes

$sqlite3 cms_db.db
SQLite version 3.7.15.2 2013-01-09 11:53:05
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite>

$sqlite>.quit

$sqlite3 cms_db.db < cms_db.sql
