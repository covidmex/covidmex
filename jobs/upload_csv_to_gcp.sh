#!/bin/sh

# vars
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=my-secret-pw
GSBUCKET=covidmex-open-data
FILENAME=covidmex_csv_files
MYSQL_CONTAINER_NAME=covidmex_covidmex-mysql_1
TMP_PATH=~/
DATESTAMP=$(date +".%d.%m.%Y")

# Iterate over all tables
echo -e "\n\n\n1. Iterate over tables"
for table in $(docker exec ${MYSQL_CONTAINER_NAME} /usr/bin/mysql -u ${MYSQL_USER} --password=${MYSQL_ROOT_PASSWORD}  --batch  covidmex_db -e "SHOW TABLES"); do
     echo "Creatind CSV for $table";
     docker exec ${MYSQL_CONTAINER_NAME} /usr/bin/mysql -u ${MYSQL_USER} --password=${MYSQL_ROOT_PASSWORD} --batch  covidmex_db -e "SELECT *FROM $table;" | sed "s/\"/\"\"/g;s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > ../csv/$table${DATESTAMP}.csv
     echo "File  $table${DATESTAMP}.csv saved"
done

echo -e "\n"
echo -e "DONE: CSV files exported"
echo -e "\n"

# compression (tar.gz)
echo -e "1. Starting compression..."
tar czf ${FILENAME}.tar.gz ../csv
echo -e "DONE: Compressing the CSV files."
echo -e "\n"

# upload 
echo -e "2. Uploading the new backup..."
gsutil cp ${FILENAME}.tar.gz gs://${GSBUCKET}/
echo -e "DONE: New backup uploaded."
echo -e "\n"

# remove databases dump
echo -e "3. Removing the cache files..."
rm ${FILENAME}.tar.gz
rm ../csv/*.csv
echo -e "DONE: Files removed."

echo -e "\n Job completed"
