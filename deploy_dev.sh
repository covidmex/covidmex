docker stop covidmex
docker rm covidmex
docker build -t covidmex:latest .
docker run -d --name covidmex  -p 5000:5000 covidmex:latest
docker ps
