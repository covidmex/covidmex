#!/bin/sh

# vars

GSBUCKET=covidmex-open-data
FILENAME=covidmex_json_files
MYSQL_CONTAINER_NAME=covidmex_covidmex-mysql_1


# compression (tar.gz)
echo -e "1. Starting compression..."
tar czf ${FILENAME}.tar.gz ../json
echo -e "DONE: Compressing the json files."
echo -e "\n"

# upload 
echo -e "2. Uploading the new backup..."
gsutil cp ${FILENAME}.tar.gz gs://${GSBUCKET}/
echo -e "DONE: New backup uploaded."
echo -e "\n"

# remove databases dump
echo -e "3. Removing the cache files..."
rm ${FILENAME}.tar.gz
echo -e "DONE: Files removed."

echo -e "\n Job completed"
