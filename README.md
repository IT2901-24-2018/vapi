# VAPI - Vegnett API

[![Build Status](https://travis-ci.org/IT2901-24-2018/vapi.svg?branch=dev)](https://travis-ci.org/IT2901-24-2018/vapi) [![codecov](https://codecov.io/gh/IT2901-24-2018/vapi/branch/dev/graph/badge.svg)](https://codecov.io/gh/IT2901-24-2018/vapi)

Vapi is an API that gathers Norways digital roadnet, then segments it into reasonably sized road segments. We also accept input for production data related to road condition influences like weather and maintenance (snow plowing, gravelling, salting). This data is mapped to the road segments, and outputted as a RESTful API.

Vapi was built by a team of seven students in their sixth semester of the Bachelor’s in Informatics programme at [NTNU](https://www.ntnu.edu/), as a part of the course [IT2901](https://www.ntnu.edu/studies/courses/IT2901) - Informatics Project II, colloquially known as the bachelor's thesis. Vapi was developed for the [Norwegian Public Roads Administration](https://www.vegvesen.no/en/home).

Additional documentation and information can be found in our [wiki](https://github.com/it2901-24-2018/vapi/wiki). As this is a student project, the wiki also contains a lot of administrative information related to the project. 

Vapi was built with [Django](https://www.djangoproject.com/) as a multi-container [Docker](https://www.docker.com/) application. Huge thanks to [Christian Duvholt](https://github.com/duvholt) for Docker guidance.

# Setup

## Github

We recommend cloning the repository with SSH (see [here](https://help.github.com/articles/connecting-to-github-with-ssh/) for adding SSH key if you haven't already):

```
git@github.com:IT2901-24-2018/vapi.git
cd vapi
```

If you wish to contribute to Vapi, we would also appreciate you setting the following configuration options:

```
git config --global core.autocrlf false
git config --global user.name "<your github username>"
git config --global user.email your.github@email.com
```

## Dependencies

Docker (Compose) will handle most of our dependencies, but first you need to install it! Install the Developer Desktop for Mac or Windows, or the Linux Server for your distribution of choice [here](https://www.docker.com/community-edition).

The Developer Desktop for Mac and Windows already include Docker Compose, but Linux users will have to install Compose [here](https://docs.docker.com/compose/install/).

Our Django container depends on environment variables. Make a file called `.env` at the root directory, with the following contents:

```
DJANGO_DEBUG=True
```

## Initial build
We have a Makefile that simplifies interaction with our Docker containers. You will likely need to use `sudo` for most Docker commands, but you can omit it depending on your installation.

Start up the application for the first time, building your containers and starting them up by running:

`sudo make`

Your Postgres container might be slower than the Django container when starting Vapi for the first time, but the server isn't ready yet anyways, so that's hardly an issue. Stop the server with `CTRL+C`.

## Migrations

Get your database up to speed by applying existing migrations:

`sudo make migrate`

## Log in

Create a superuser in Django:

`sudo make superuser`

You are now ready to start the server again:

`sudo make`

Navigate to [http://localhost:8000/](http://localhost:8000/), and see that Vapi is up and running!

To gain access to all the endpoints of the API, you must log in as a superuser. Navigate to the [API page](http://localhost:8000/api/) and log in with your superuser in the top-right corner.

## Vapi example scripts

To run our example scripts, you will need to fill in your superuser credentials to the `.env` file you made earlier. This file will not be checked in to Git. Modify the `.env` file so that it looks like this, replacing yourusername with your username, and yourpassword with your password:

```
DJANGO_DEBUG=True
API_USERNAME=yourusername
API_PASSWORD=yourpassword
```

To run our example road segmenter `example_roadnet_to_db.py`, make sure that the server is running. Open a new terminal, then make a bash-shell in your container with:

`sudo docker exec -t -i vapi_django_1 /bin/bash`

When you're inside, run:

`python /vapi/apps/data/road_segmenting/example_roadnet_to_db.py`

You can also run `example_create_test_prod_data.py` to simulate production data input here, which requires you to have a `apps/data/production_input_data.geojson` file:

`python /vapi/apps/data/example_create_test_prod_data.py`

## Other make commands

`sudo make start`

Generally speaking, you will only need to build your containers when updating the Docker configurations, or new dependencies have been added. For general use, `sudo make start` will be faster and sufficient.

`sudo make test`

This will run our tests and lint the backend locally. We advice you to run this before pushing your code to Github, to ensure your code will pass our [Travis CI](https://travis-ci.org) build.

`sudo make migrations`

This will run `python manage.py makemigrations`, creating new migrations based on changes made to models.

`sudo make shell`

This will start up a Django shell within the container.

## Other other make commands

`sudo make build`

This will build the containers.

`sudo make stop`

This will stop your containers if they're running in detached mode.

`sudo make restart`

This will stop and start (restart) your containers if they're running in detached mode.

`sudo make status`

This will display the status of your containers.

## Example files

We have two files to help with populating the database with road segments and production data. These can be used in further development.
Both example_create_test_prod_data.py and example_roadnet_to_db.py are well described and easy to use.
NOTE: These are not necessary for the API and can be removed as you see fit. 

## Credits 

Thanks to Jan Kristian Jensen https://github.com/LtGlahn for letting us use his https://github.com/LtGlahn/nvdbapi-V2 repo for interacting with the NVDB API.
We used it for getting the official road network from the NVDB API and processing it. 
