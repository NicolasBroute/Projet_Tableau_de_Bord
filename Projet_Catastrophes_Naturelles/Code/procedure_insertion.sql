/*------------------------------------------------------------
*        Script PROC SQLSERVER 
------------------------------------------------------------*/


/*------------------------------------------------------------
-- Procedure : INSERTION_ARTICLE 
------------------------------------------------------------*/
CREATE PROC INSERTION_ARTICLE 
	@pid_article INT,
	@pjournal VARCHAR (30),
	@pauteur VARCHAR (50),
	@pdate_article DATETIME,
	@ptheme VARCHAR (25)
AS   
INSERT INTO Articles (id_article,journal,auteur, date_article, theme) VALUES(@pid_article, @pjournal, @pauteur, @pdate_article, @ptheme);



/*------------------------------------------------------------
-- Procedure : INSERTION_TITRE 
------------------------------------------------------------*/
CREATE PROC INSERTION_TITRE 
	@pid_titre INT ,
	@pposition_mot INT ,
	@pscore_tf_idf FLOAT   ,
	@pid_article   INT  ,
	@pid_mot       INT ,
	@pid_nombre       INT
AS   
INSERT INTO Titres (id_titre, position_mot, score_tf_idf, id_article, id_mot, id_nombre) VALUES (@pid_titre, @pposition_mot, @pscore_tf_idf,@pid_article,@pid_mot,@pid_nombre);



/*------------------------------------------------------------
-- Procedure : INSERTION_CONTENU_MOTS_CLES 
------------------------------------------------------------*/
CREATE PROC INSERTION_CONTENU_MOTS_CLES 
	@pid_contenu INT ,
	@pposition_mot INT ,
	@pscore_tf_idf FLOAT  ,
	@pid_article   INT  ,
	@pid_mot       INT  ,
	@pid_nombre INT
AS
INSERT INTO Contenus_mots_cles (id_contenu, position_mot, score_tf_idf, id_article, id_mot, id_nombre) VALUES (@pid_contenu, @pposition_mot, @pscore_tf_idf, @pid_article, @pid_mot, @pid_nombre);



/*------------------------------------------------------------
-- Procedure : INSERTION_MOTS 
------------------------------------------------------------*/
CREATE PROC INSERTION_MOTS
	@pid_mot INT ,
	@pmot        VARCHAR (30) ,
	@ptype_mot   VARCHAR (25)  ,
	@pentite  VARCHAR (40)
AS
INSERT INTO Mots (id_mot, mot,type_mot,entite) VALUES (@pid_mot,@pmot,@ptype_mot,@pentite);



/*------------------------------------------------------------
-- Procedure : INSERTION_NOMBRES 
------------------------------------------------------------*/
CREATE PROC INSERTION_NOMBRES
	@pid_nombre INT ,
	@pnombre FLOAT ,
	@pid_mot INT
AS
INSERT INTO Nombres (id_nombre, nombre, id_mot) VALUES (@pid_nombre, @pnombre, @pid_mot);

