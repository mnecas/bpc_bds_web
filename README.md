# BPC BDS WEB
## Info
This is BUT project for database security.
The project contains website wrote in python framework Django.
The website idea is for the ordering foods like wolt.

The Django database structe was inspired by first part of the project.
There were few changes so it would work with the Django models.
https://github.com/mnecas/bds-db-design

For the Database I'm using the contianer with postgres.

## Start the web
To run the project in your enviroment you can either run
`docker-compose up`
or 
`podman-compose up` (tested with podman).

This will create two containers one with the postgres db and another with Django website.

## Admin page
The container automatically creates one default admin account with which you can log in to the admin part of the website.
Default login: 

User: `mnecas`
Password: `mnecas`

## Development
To run the web server you need to install all necessary python dependencies for it you can run:

`pip3 install -r ./requirements.txt`

For database initialization:

`python3 manage.py makemigrations`

`python3 manage.py migrate`

To run the server use: 

`python3 maange.py runserver`

(Recommend chaning the `DEBUG` in settings to `True`)
