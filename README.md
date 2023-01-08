# Social Media app using FastAPI
This is a social networking application that allows users to sign up, log in, create, edit, delete and view posts, like or dislike other users' posts, and use an in-memory DB (Redis) for storing post likes and dislikes. It uses FastAPI for a RESTful API, JWT for authentication and registration, Postgres as the database, and SQLAlchemy as the ORM.

## Running the app
### Prerequisites
* Docker
* Docker Compose
* `EMAILHUNTER_API_KEY` you first get the email huntur api key inorder to correctly run the app `https://hunter.io/email-verifier`

### Development 
1. Make sure you have Docker and Docker Compose installed on your machine. 
2. Clone this repository. 
```shell
git clone https://github.com/abdulra7ma/social-media-app.git
cd social-media-app
```
3. Navigate to the `development` dir in the `docker` repository and create a `.env` file and `.env.db` and then update `EMAILHUNTER_API_KEY` in the `.env` file. This file should contain all the environment variables needed for the app to run properly. An example of this file can be found in `.env.example` and `.env.db.example`.
```shell
cd docker/development
touch .env
cat .env.db > .env.db
```
4. Return to the root dir and Run the command `docker-compose -f docker-compose.development.yml build` to build the development environment. 
```shell
cd ../..
docker-compose -f docker-compose.dev.yml build
```
5. Run the command `docker-compose -f docker-compose.development.yml up` to start the development environment.
```shell
docker-compose -f docker-compose.development.yml up
# to run it in the background add `-d` to the end 
docker-compose -f docker-compose.development.yml up -d
```
6. access the app api from ``http://127.0.0.0:8000/docs``

### Production 
1. Make sure you have Docker and Docker Compose installed on your machine. 
2. Clone this repository. 
```shell
git clone https://github.com/abdulra7ma/social-media-app.git
cd social-media-app
```
3. Navigate to the `production` dir in the `docker` repository and create a `.env` file and `.env.db` and then update `EMAILHUNTER_API_KEY` in the `.env` file.. This file should contain all the environment variables needed for the app to run properly. An example of this file can be found in `.env.example` and `.env.db.example`.
```shell
cd docker/development
touch .env
cat .env.db.example > .env.db
```
4. Return to the root dir and Run the command `docker-compose -f docker-compose.production.yml build` to build the development environment. 
```shell
cd ../..
docker-compose -f docker-compose.production.yml build
```
5. Run the command `docker-compose -f docker-compose.production.yml up` to start the development environment.
```shell
docker-compose -f docker-compose.production.yml up
# to run it in the background add `-d` to the end 
docker-compose -f docker-compose.production.yml up -d
```
6. access the app api from ``http://127.0.0.0/``


### Tests 
1. Make sure you have Docker and Docker Compose installed on your machine. 
2. Clone this repository. 
```shell
git clone https://github.com/abdulra7ma/social-media-app.git
cd social-media-app
```
3. Navigate to the `test` dir in the `docker` repository and create a `.env` file and `.env.db` and then update `EMAILHUNTER_API_KEY` in the `.env` file.. This file should contain all the environment variables needed for the app to run properly. An example of this file can be found in `.env.example` and `.env.db.example`.
```shell
cd docker/development
touch .env
cat .env.db.example > .env.db
```
4. Return to the root dir and Run the command `docker-compose -f docker-compose.test.yml build` to build the development environment. 
```shell
cd ../..
docker-compose -f docker-compose.test.yml build
```
5. Run the command `docker-compose -f docker-compose.test.yml up` to start the development environment.
```shell
docker-compose -f docker-compose.production.yml up
```

## API Endpoints
* `/signup`: sign up a new user 
* `/signin`: log in an existing user 
* `/posts`: create, edit, delete, and view posts 
* `/like`: like a post 
* `/unlike`: unlike a post 
* `/dislike`: dislike a post (removes any previous likes)
* `/undislike`: dislike a post (removes any previous likes)


## License
This project is licensed under the [GNU] License 

## Acknowledgments
* This app have not been fully tested just basic unit test for auth endpoint
* Inspiration
