/*------------------------------------------------------------
*        Script SQLSERVER 
------------------------------------------------------------*/


/*------------------------------------------------------------
-- Table: Articles
------------------------------------------------------------*/
CREATE TABLE Articles(
	id_article   INT IDENTITY (1,1) NOT NULL ,
	journal      VARCHAR (30)  ,
	auteur       VARCHAR (50)  ,
	date_article DATETIME  ,
	theme        VARCHAR (25)  ,
	CONSTRAINT prk_constraint_Articles PRIMARY KEY NONCLUSTERED (id_article)
);


/*------------------------------------------------------------
-- Table: Titres
------------------------------------------------------------*/
CREATE TABLE Titres(
	id_titre     INT IDENTITY (1,1) NOT NULL ,
	position_mot INT IDENTITY (1,1) NOT NULL ,
	score_tf_idf FLOAT   ,
	id_article   INT  NOT NULL ,
	id_mot       INT  NOT NULL ,
	CONSTRAINT prk_constraint_Titres PRIMARY KEY NONCLUSTERED (id_titre,position_mot)
);


/*------------------------------------------------------------
-- Table: Contenus_mots_cles
------------------------------------------------------------*/
CREATE TABLE Contenus_mots_cles(
	id_contenu   INT IDENTITY (1,1) NOT NULL ,
	position_mot INT IDENTITY (1,1) NOT NULL ,
	score_tf_idf FLOAT  NOT NULL ,
	id_article   INT  NOT NULL ,
	id_mot       INT  NOT NULL ,
	id_nombre    INT  NOT NULL ,
	CONSTRAINT prk_constraint_Contenus_mots_cles PRIMARY KEY NONCLUSTERED (id_contenu,position_mot)
);


/*------------------------------------------------------------
-- Table: Entites
------------------------------------------------------------*/
CREATE TABLE Entites(
	id_entite   INT IDENTITY (1,1) NOT NULL ,
	type_entite VARCHAR (40) NOT NULL ,
	CONSTRAINT prk_constraint_Entites PRIMARY KEY NONCLUSTERED (id_entite)
);


/*------------------------------------------------------------
-- Table: Mots
------------------------------------------------------------*/
CREATE TABLE Mots(
	id_mot    INT IDENTITY (1,1) NOT NULL ,
	mot       VARCHAR (30) NOT NULL ,
	type_mot  VARCHAR (25)  ,
	id_entite INT  NOT NULL ,
	CONSTRAINT prk_constraint_Mots PRIMARY KEY NONCLUSTERED (id_mot)
);


/*------------------------------------------------------------
-- Table: Nombres
------------------------------------------------------------*/
CREATE TABLE Nombres(
	id_nombre INT IDENTITY (1,1) NOT NULL ,
	nombre    FLOAT   ,
	id_mot    INT  NOT NULL ,
	CONSTRAINT prk_constraint_Nombres PRIMARY KEY NONCLUSTERED (id_nombre)
);



ALTER TABLE Titres ADD CONSTRAINT FK_Titres_id_article FOREIGN KEY (id_article) REFERENCES Articles(id_article);
ALTER TABLE Titres ADD CONSTRAINT FK_Titres_id_mot FOREIGN KEY (id_mot) REFERENCES Mots(id_mot);
ALTER TABLE Contenus_mots_cles ADD CONSTRAINT FK_Contenus_mots_cles_id_article FOREIGN KEY (id_article) REFERENCES Articles(id_article);
ALTER TABLE Contenus_mots_cles ADD CONSTRAINT FK_Contenus_mots_cles_id_mot FOREIGN KEY (id_mot) REFERENCES Mots(id_mot);
ALTER TABLE Contenus_mots_cles ADD CONSTRAINT FK_Contenus_mots_cles_id_nombre FOREIGN KEY (id_nombre) REFERENCES Nombres(id_nombre);
ALTER TABLE Mots ADD CONSTRAINT FK_Mots_id_entite FOREIGN KEY (id_entite) REFERENCES Entites(id_entite);
ALTER TABLE Nombres ADD CONSTRAINT FK_Nombres_id_mot FOREIGN KEY (id_mot) REFERENCES Mots(id_mot);
