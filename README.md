
# bewise_test_task

# Project Setup

This project can be set up using the following steps:

1. Clone the repository to your local machine.
2. Install Docker on your system if it is not already installed.
3. Open a terminal window and navigate to the root directory of this project.

## Building The Project

To build this project, follow these steps:

1. Run `docker-compose build` command in your terminal window from within the root directory of this project.

```bash
$ docker-compose build
```

This will download all necessary dependencies and create a Docker image for running our application.

## Running The Project

Once you have built the application, you can run it using `docker-compose up` command in your terminal window from within the root directory of this project.


```bash
$ docker-compose up 
```

The above command will start all services defined in our `docker-compose.yml` file and make them available for use.

You should now be able to access our web app by navigating to http://localhost:9999/docs in any web browser.

## Project Structure
  You can easily test all the endpoints using the FastApi automatic documentation http://localhost:9999/docs
  
1. Questions : responsible for the first web service

2. User and Record : responsible for the second web service
