# covidmex
Sitio con estadisticas del Coronavirus (COVID-19) en México. Información extraida desde el comunicado Técnico Diario de la Dirección General de Epidemiología de la  Secretaría de Salud.

# Inicializar la aplicación (Propositos de desarrollo)

## Requisitos

Instalar Docker - https://docs.docker.com/install/

## Despliegue

### 1. Clonar el repositorio

### 2. Ejecutar el script de despliegue de entorno de de desarrollo
  $ chmod a+x deploy_dev.sh
  $ ./deploy_dev.sh
  
###  3. Inicializar la base de datos
$  docker exec -it covidmex python manage.py initdb
