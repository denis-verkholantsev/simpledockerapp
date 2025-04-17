# simpledockerapp
## components
* **flask-app** - REST API based on Flask framework
* **database** - MySQL database

## Step 1: create .env file
```cp .env.template .env```  for Unix-like systems

```copy .env.template .env``` for Windows

## Step 2: install [Docker Engine and Docker Compose](https://docs.docker.com/compose/install/)
Start containers with

```docker-compose up``` for Docker Compose

```docker compose up``` for Docker Compose v2

## Step 3: for testing use [curl](https://curl.se/)
Create item:
```curl -X POST http://localhost:5000/items  -H "Content-Type: application/json" -d '{"name": "string"}'```

Get items:
```curl -X GET http://localhost:5000```

Delete item:
```curl -X DELETE http://localhost:5000/items?id=1```
