## Running the App in Development Environment
1. Make sure you have Docker and Docker Compose installed on your machine. 
2. Clone this repository. 
3. Navigate to the root of the repository and create a `.env` file. This file should contain all the environment variables needed for the app to run properly. An example of this file can be found in `.env.example`.
4. Run the command `docker-compose -f docker-compose.dev.yml build` to build the development environment. 
5. Run the command `docker-compose -f docker-compose.dev.yml up` to start the development environment.