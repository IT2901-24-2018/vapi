## Setting up React and Django

### Frontend
Make sure you have [npm](https://nodejs.org/en/) installed through Node. You can easily test this by running `npm -v` in your terminal. We also recommend you use [Yarn](https://yarnpkg.com/lang/en/) to install packages, and our instructions will assume that you do.
Now you should be ready to install our frontend dependencies.
```
cd frontend
yarn
```

When the dependencies are finished installing, you can start up the frontend server. It will automatically open your browser at localhost:3000, but you can close that.

### Backend
While the frontend server is running in your terminal, open up another terminal to set up the backend.

We recommend setting up a virtualenv to contain the backend dependencies. [Here's](https://gist.github.com/IamAdiSri/a379c36b70044725a85a1216e7ee9a46) a solid guide on installing virtualenvwrapper for Python3. 
Make yourself a virtualenv for the project with `mkvirtualenv bit24` and remember to run `workon bit24` to have access to the backend dependencies.

When your virtual environment is set up, get the required dependencies for the backend:

`pip install -r requirements.txt`

Apply the latest and greatest in database migrations:

`python manage.py migrate`

Now you can start up the backend server.

`python manage.py runserver`

The website should now be available at [localhost:8000](http://localhost:8000)

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

## Misc
Thanks to [Vikas Yadav](http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/) for the React+Django setup tutorial we used.
