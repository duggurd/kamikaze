FROM postgres:alpine
ENV POSTGRES_PASSWORD=123
ENV POSTGRES_USER=ingestion
ENV POSTGRES_DB=ingestion_db
COPY ./init.sql /docker-entrypoint-initdb.d 
EXPOSE 5432