CREATE TABLE IF NOT EXISTS si_no(
   CLAVE       INTEGER  NOT NULL PRIMARY KEY 
  ,DESCRIPCION VARCHAR(25) NOT NULL
);
INSERT INTO si_no(CLAVE,DESCRIPCION) VALUES (1,'SI');
INSERT INTO si_no(CLAVE,DESCRIPCION) VALUES (2,'NO');
INSERT INTO si_no(CLAVE,DESCRIPCION) VALUES (97,'NO APLICA');
INSERT INTO si_no(CLAVE,DESCRIPCION) VALUES (98,'SE IGNORA');
INSERT INTO si_no(CLAVE,DESCRIPCION) VALUES (99,'NO ESPECIFICADO');