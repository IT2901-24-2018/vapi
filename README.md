# bit24
Map-based overview of road conditions in relation to maintenance and weather

## Setup

### Setup for django and react

clone project

set up vitual environment and activate (probably a good idea to do it in the same folder you cloned the project?)

cd into repository and `pip install requirements.txt`

or

`pip install django`

`pip install django-webpack-loader`

cd into folder with manage.py

`./manage.py migrate` (`python manage.py migrate` for windows)

can at this point run `./manage.py runserver` (see above for windows) but since the react part is missing it will show a blank page for now.

open new cmd, activate environment cd into frontend folder

`npm install`

wait...

`npm run start`

open localhost:8000 in web (there will also be a react site on port 3000 can probably be removed)

### PostreSQL db setup (work in progress)
Install PostreSQL linux: (https://www.postgresql.org/download/linux/ubuntu/)

Create the file /etc/apt/sources.list.d/pgdg.list, and add a line for the repository

Open cmd in/cd to above dir.

Type `sudo touch pgdg.list`

then `sudo vi pgdg.list` to open file in vim

i to edit. When done press escape then `:wq` to save and quit.

then `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`

and `sudo apt-get update`

last `apt-get install postgresql-9.6` or `apt-get install postgresql-9.6`

`pip install psycopg2` (unnecessary if pip install requirements.txt)

make a user with password

edit bit24/settings.py (the django settings file)

under databases remove the current bit and uncomment the postgres stuff

set the username and password to the username and password you made earlier (for some reason this did not work with the postgres user, think?)

then migrate and run server.

### TODO
Need to improve a lot of this. It still makes the sqlite3 db file.

The bit24 folder should be named backend?, but to do that you need to set up the django part again. See django and react tutorial below.

Everything in the "project" folder can be freely moved up one level (and delete "project"). Migrate again just in case.

### Tutorials
django and react: http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/

postresql, django and react with authorization https://hackernoon.com/creating-websites-using-react-and-django-rest-framework-b14c066087c7
