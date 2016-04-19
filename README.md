# CSE 110 - 41 Inc.
We're all about that simple maths.

## How To Install (Mac)

### Grab this Repo
1. Open Terminal
2. `cd` to whatever folder you want to put this repo in ex. `cd ~/Projects`
3. `git clone https://github.com/MikeShi42/41Inc.git`
4. Log into your GitHub account if neccessary

### Install Python and Pip

1. `brew install python` this will install both Python and Pip on your system
  * `Python` is the language we'll be using for the back end, it's kinda like
  needing to install Java.
  * `Pip` is a package manager, it'll help you install more Python things on
  your system.
2. `python -V` to test out Python was installed successfully. It should
print out something like `Python 2.7.11`
3. `pip --version` to test out Pip was installed successfully. It should
print out a bunch of crap including `pip 8.1.1`

### Install/Use Virtualenv

1. `pip install virtualenv`
  * This will install virtualenv on your system, virtualenv is used to manage
  different Python environments. So if you install FooBar package 
  for our project, it won't conflict with your FooBar installations 
  with your other projects.
2. `virtualenv --version` to check out if virtual env was installed
successfully. Should print out `12.0.7`
2. Make sure you're currently in the `41Inc` directory. Your current path
should look like `~/Projects/41Inc`.
3. `virtualenv venv`
  * This will set up a virtual environment in your 41Inc project folder.
  * Check out that a folder called `venv` was made under `$ ~/../41Inc/`
4. `source venv/bin/activate`
  * This will activate your new virtual environment. Your terminal should
  say something like `(venv) macbook-pro$` on the left side now. 
  * Now all Python commands being run will be using this virtual environment. 
  You can leave the environment by using `deactivate` 
  (don't do this yet though)
5. `pip install -r requirements.txt`
  * This will tell `pip` to install all the packages specified in 
  `requirements.txt`

### Trying Out Django

1. `cd` to the `fourtyone` folder under `41Inc`. So your current directory
should be `$ ~/../41Inc/fourtyone`
2. `python manage.py runserver`
3. Visit `http://127.0.0.1:8000/` in your browser.
  * A success page should pop up


## General Resources
* General Python Setup Guide: http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/
* Virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
* Getting started with Django: https://docs.djangoproject.com/en/1.9/topics/install/#installing-official-release
