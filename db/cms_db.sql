BEGIN TRANSACTION;
CREATE TABLE "users" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`nom`	varchar(50),
	`courriel`	varchar(50),
	`salt`	varchar(100),
	`hash`	varchar(250)
);
CREATE TABLE "sessions" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`courriel`	varchar(50),
	`id_session`	varchar(100)
);
CREATE TABLE "recuperations" ( 
	`id` INTEGER PRIMARY KEY AUTOINCREMENT, 
	`courriel` varchar(50), 
	`token` varchar(100),
	`date_demande` NUMERIC 
);
CREATE TABLE "invitation" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`courriel`	varchar(50),
	`token`	varchar(100),
	`date_invitation`	varchar(50)
);
CREATE TABLE "article" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`titre`	varchar(100),
	`identifiant`	varchar(50),
	`auteur`	varchar(100),
	`date_publication`	varchar(50),
	`paragraphe`	varchar(500)
);
COMMIT;
