JobFinder Project
========================================

About
-----

This is a job portal where job seekers can apply for job posted by companies. 
It has job management, company management, applicant management, resumee management and much more

Prerequisites
-------------

- Python >= 3.**
- pip
- virtualenv (optional)

Installation
------------

To setup a local development environment::

    virtualenv env --prompt="({{ project_name }})"  # or mkvirtualenv {{ project_name }}
    source env/bin/activate

    cd src
    make

    cp {{ project_name }}/settings/local.py.example {{ project_name }}/settings/local.py  # To enable debugging
    edit {{ project_name }}/settings/local.py    # Enter your DB credentials

    sudo su - postgres
    createuser {{ project_name }}  -P  
    createdb --template=template0 --encoding='UTF-8' --lc-collate='en_US.UTF-8' --lc-ctype='en_US.UTF-8' --owner={{ project_name }} {{ project_name }}
    exit

    ./manage.py migrate
    ./manage.py runserver

