CREATE TABLE IF NOT EXISTS origen(
   CLAVE       INTEGER  NOT NULL PRIMARY KEY 
  ,DESCRIPCION VARCHAR(15) NOT NULL
);
INSERT INTO origen(CLAVE,DESCRIPCION) VALUES (1,'USMER');
INSERT INTO origen(CLAVE,DESCRIPCION) VALUES (2,'FUERA DE USMER');
INSERT INTO origen(CLAVE,DESCRIPCION) VALUES (99,'NO ESPECIFICADO');