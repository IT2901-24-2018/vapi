# VAPI - Vegnett API

Vapi is an API that gathers Norways digital roadnet, then segments it into reasonably sized road segments. We also accept input for production data related to road condition influences like weather and maintenance (snow plowing, gravelling, salting). This data is mapped to the road segments, and outputted as a RESTful API.

Vapi was built by a team of seven students in their sixth semester of the Bachelor’s in Informatics programme at [NTNU](https://www.ntnu.edu/), as a part of the course [IT2901](https://www.ntnu.edu/studies/courses/IT2901) - Informatics Project II, colloquially known as the bachelor's thesis. Vapi was developed for the [Norwegian Public Roads Administration](https://www.vegvesen.no/en/home).

Additional documentation and information can be found in our [wiki](https://github.com/it2901-24-2018/vapi/wiki). As this is a student project, the wiki also contains a lot of administrative information related to the project. 

Vapi was built with React (setup with [create-react-app](https://github.com/facebook/create-react-app)), and [Django](https://www.djangoproject.com/). The two were combined with [this guide](http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/) by Vikas Yadav. Vapi is built as a multi-container [Docker](https://www.docker.com/) application, with huge thanks to [Christian Duvholt](https://github.com/duvholt) for setup guidance.

# Setup

For a more detailed walkthrough, [move past this introduction](#github).

In short, clone the repository, install [Docker Compose](https://docs.docker.com/compose/install/), run `sudo make`, which will likely fail because you need to add your superuser with `sudo make superuser` and fill in an `.env` file in the project root with the following:

```
DJANGO_DEBUG=True
API_USERNAME=yourusername
API_PASSWORD=yourpassword
```

Run `sudo make migrate` to apply database migrations, and you're good to go. `sudo make start` will be sufficient for starting the containers, as you should only need to build when changing dependencies or Docker configuration.

## Github

We recommend cloning the repository with SSH (see [here](https://help.github.com/articles/connecting-to-github-with-ssh/) for adding SSH key if you haven't already):

```
git clone git@github.com:dotkom/onlineweb4.git
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

Our Django container depends on environment variables. Make an `.env` file at the root directory, with the following contents:

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

## Superuser

Create a superuser in Django:

`sudo make superuser`

While we plan to remove the need for this in the future, we need to fill in the superuser credentials to the `.env` file you made earlier. This file will not be checked in to Git. Modify the `.env` file so that it looks like this, replacing yourusername with your username, and yourpassword with your password:

```
DJANGO_DEBUG=True
API_USERNAME=yourusername
API_PASSWORD=yourpassword
```

## Vapi example scripts

Start the server again:

`sudo make start`

To run our example road segmenter `example_roadnet_to_db.py`, open a new terminal, then make a bash-shell in your container with:

`sudo docker exec -t -i vapi_django_1 /bin/bash`

When you're inside, run:

`python /app/backend/data/road_segmenting/example_roadnet_to_db.py`

You can also run `example_create_test_prod_data.py` to simulate production data input here, which requires you to have a `backend/Driftsdata_SubSet_Small.geojson` file:

`python /app/backend/data/example_create_test_prod_data.py`

## Other make commands

`sudo make start`

Generally speaking, you will only need to build your containers when updating the Docker configurations, or new dependencies have been added. For general use, `sudo make start` will be faster and sufficient.

`sudo make test`

This will run our tests and lint the frontend and backend locally. We advice you to run this before pushing your code to Github, to ensure your code will pass our [Travis CI](https://travis-ci.org) build.

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
