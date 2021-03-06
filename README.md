# covidmex
Sitio con estadisticas del Coronavirus (COVID-19) en México. Información extraida desde el comunicado Técnico Diario de la Dirección General de Epidemiología de la  Secretaría de Salud.

# Live Data
Ingresa a https://covidmex.live/ para visualizar los datos


Dashboard principal:

+ Conteo de casos confirmados, sospechosos, defunciones.
+ Histograma de casos.
+ Tasa de letalidad y crecimiento.
+ Distribución de casos por rango de fechas.
+ Top 10 estados con más casos. 

![Dashboard principal](screenshots/index.png)

Exploración de datos:
+ Filtado de información por campos:  Estado	Sexo	Edad	Fecha Sintomas	Estatus	Tipo Contagio	Procedencia	Llegada.
+ Descarga de base de datos en formato SQL (MySQL).
+ Descarga de todos los casos en formato JSON.

![Exploración de datos](screenshots/explore.png)



# Inicializar la aplicación (Propositos de desarrollo)

## Requisitos

Instalar Docker - https://docs.docker.com/install/

## Despliegue

### 1. Clonar el repositorio

### 2. Crear archivo de variables de entorno

Crear un archivo con nombre environment.env y colocar las siguientes variables:

```

MYSQL_DB=covidmex_db
MYSQL_USER=root
MYSQL_PASSWORD=somesecretpassword # Colocar un password seguro
MYSQL_HOSTNAME=covidmex-mysql
COVIDMEX_ENVIRONMENT=development
COVIDMEX_ADMIN_USER=admin
COVIDMEX_ADMIN_PASSWORD=d9f8ej3s  # Colocar un password seguro

```

### 3. Ejecutar el script de despliegue de entorno de desarrollo

```
$ chmod a+x deploy_dev.sh 
$ ./deploy_dev.sh --resetdb
```

La opción --resetdb se debe ejecutar necesariamente la primera vez. Ejecutar el comando anterior sin la opción --resetdb no recreará la base de datos. 


###  4. (Opcional) Cargar un dump a la base de datos

Descargar el archivo sql y ejecutar:
```
$ cat covidmex.sql  | docker exec -i covidmex-mysql /usr/bin/mysql -u root --password=[MYSQL_ROOT_PASSWORD]  covidmex_db
```

### 5. Estamos desarrollando continuamente un API Rest para obtener los datos que vamos recopilando. Si quieres integrarlo y se puede usar libremente. 
```
https://documenter.getpostman.com/view/2749943/SzYgRvLZ?version=latest
```