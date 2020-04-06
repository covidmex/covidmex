#!/bin/sh

# vars
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=my-secret-pw
GSBUCKET=covidmex-open-data
FILENAME=covidmex_database
MYSQL_CONTAINER_NAME=covidmex_covidmex-mysql_1
TMP_PATH=~/
DATESTAMP=$(date +".%d.%m.%Y")

# dump database
echo -e "\n\n\n1. Starting backing up the database to a file..."
docker exec ${MYSQL_CONTAINER_NAME} /usr/bin/mysqldump -u ${MYSQL_USER} --single-transaction --quick --lock-tables=false  --password=${MYSQL_ROOT_PASSWORD} covidmex_db > ${TMP_PATH}${FILENAME}${DATESTAMP}.sql

echo -e "DONE: Backing up the database to a sql file."
echo -e "\n"

# compression (tar.gz)
echo -e "2. Starting compression..."
tar czf ${TMP_PATH}${FILENAME}.tar.gz ${TMP_PATH}${FILENAME}${DATESTAMP}.sql
echo -e "DONE: Compressing the sql file."
echo -e "\n"

# upload 
echo -e "3. Uploading the new backup..."
gsutil cp ${TMP_PATH}${FILENAME}.tar.gz gs://${GSBUCKET}/
echo -e "DONE: New backup uploaded."
echo -e "\n"

# remove databases dump
echo -e "4. Removing the cache files..."
rm ${TMP_PATH}${FILENAME}${DATESTAMP}.sql
rm ${TMP_PATH}${FILENAME}.tar.gz
echo -e "DONE: Files removed."

echo -e "\n Job completed"
