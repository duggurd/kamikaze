docker build -f ./pg.dockerfile -t postgres_kamikaze .

docker run -d -p 5432:5432 --name postgres_kamikaze postgres_kamikaze