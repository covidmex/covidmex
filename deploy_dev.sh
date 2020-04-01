
if [ "$1" == "--resetdb" ]
then
	echo "Reseting Database..."
	docker stop covidmex-mysql
	docker rm covidmex-mysql

	docker stop covidmex
	docker rm covidmex

	docker build -t covidmex:latest -f Dockerfile.covidmex .

	docker run -d --name covidmex-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw mysql:8.0 mysqld --default-authentication-plugin=mysql_native_password
	docker run -d --name covidmex --link covidmex-mysql:covidmex-mysql -e MYSQL_USER=root -e MYSQL_PASSWORD=my-secret-pw -e MYSQL_HOST=covidmex-mysql -p 80:80 -e MYSQL_DB=covidmex_db -e COVIDMEX_ENVIRONMENT=development -e COVIDMEX_ADMIN_PASSWORD=d9f8ej3w -e COVIDMEX_ADMIN_USER=admin  covidmex:latest
	 while ! docker exec covidmex-mysql mysqladmin --user=root --password=y-secret-pw --host "127.0.0.1" ping --silent &> /dev/null ; do
	    echo "Waiting for database connection..."
	    sleep 2
	done
	docker exec -it covidmex python manage.py initdb
	docker ps
	exit 0
fi 



docker stop covidmex
docker rm covidmex

docker build -t covidmex:latest -f Dockerfile.covidmex .

docker run -d --name covidmex --link covidmex-mysql:covidmex-mysql -e MYSQL_USER=root -e MYSQL_PASSWORD=my-secret-pw -e MYSQL_HOST=covidmex-mysql -p 80:80 -e MYSQL_DB=covidmex_db -e COVIDMEX_ENVIRONMENT=development -e COVIDMEX_ADMIN_PASSWORD=d9f8ej3w -e COVIDMEX_ADMIN_USER=admin  covidmex:latest

docker ps
exit 0
