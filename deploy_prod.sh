docker stop covidmex
docker rm covidmex

docker stop covidmex-mysql
docker rm covidmex-mysql

docker build -t covidmex:latest .

docker run -d --name covidmex-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw mysql:latest
docker run -d --name covidmex --cpus="1.5" --memory="3g" --link covidmex-mysql:covidmex-mysql -e MYSQL_USER=root -e MYSQL_PASSWORD=my-secret-pw -e MYSQL_HOST=covidmex-mysql -p 80:80 -e MYSQL_DB=covidmex_db -e COVIDMEX_ENVIRONMENT=development covidmex:latest

docker ps