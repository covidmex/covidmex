if [ "$1" == "--resetdb" ]
then
	echo "Reseting Database..."
	docker stop covidmex-mysql
	docker rm covidmex-mysql

	docker stop covidmex
	docker rm covidmex

	docker build -t covidmex:latest -f Dockerfile.covidmex .

	docker run -d --name covidmex-mysql -p 3306:3306 --env-file=environment.env mysql:8.0 mysqld --default-authentication-plugin=mysql_native_password
	docker run -d --name covidmex --link covidmex-mysql:covidmex-mysql -p 80:80  --env-file=environment.env  covidmex:latest
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

docker run -d --name covidmex --link covidmex-mysql:covidmex-mysql -p 80:80 --env-file=environment.env covidmex:latest

docker ps
exit 0

