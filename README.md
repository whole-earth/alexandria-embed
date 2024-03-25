# Installation Guide

This installation guide is tailored for windows. Some commands may be different on Mac or Linux.

# Step 1 - Docker

Download Docker to universalize our dev environments:

https://www.docker.com/get-started/

# Step 2 - Python

## Create a venv environment 

``` py -m venv env ```

``` venv\Scripts\activate ```

## Install Django and Python Requirements

``` pip install -r requirements.txt ```

# Step 3 - Codebase

``` git clone ```

# Step 4 - Update the Djano App DB

``` python manage.py migrate ```

# Step 5 - Start the Server

## Start and Build the Container with docker compose 

We use docker compose to tell Docker to run the docker-compose.yml file. This will in turn use the Dockerfile to build the image into the container.

The build and d tags are for building the image and silently running it, respectively.

``` docker compose up --build -d ```

You should now see the container 'ondra_campus' in your Docker Desktop GUI

After building, if you make no changes to the Dockerfile requirements, you can just start the container in the docker desktop.

# File Structure

The Django App runs via the outward poking manage.py. It then calls the 'core/' app to run the server. 

```
manage.py
core/
  data/
  scripts/
  migrations/
  templates/
    core/
  static/
    core/
        js/
        css/
   *.py's
```

You'll find the three.js file in the static/core/js dir (home.js) 

You'll find the html file in the templates/core/ dir (index.html)

You'll find the embedding pipeline in scripts/ (factory.py)

The django app primarily functions off of urls, manage and views. views.py will contain most of the instructions in relaying the JSON to the frontend. models.py is our DB structure. And urls.py is our server URL routing. A standard MVC flow. 