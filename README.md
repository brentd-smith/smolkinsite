[![Build Status](https://travis-ci.org/brentd-smith/smolkinsite.svg?branch=master)](https://travis-ci.org/brentd-smith/smolkinsite)


# Jewish Prayers & Songs Website

Website for learning how to chant the traditional Torah and Haftarah Shabbat Readings. Also includes songs traditionally sung in Conservative Synagogues on Friday Night and Shabbat Morning.

## Features

Each song/prayer/reading includes recordings of the melody/chant alongside lyrics that are in Hebrew and sometimes transliterated for easier learning.

## How to Use


## Project Information

Created with the heroku-django-template ::

    $ django-admin.py startproject --template=https://github.com/heroku/heroku-django-template/archive/master.zip --name=Procfile smolkinsite

- Uses Python3
- Uses Django 1.11

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate


