# CSE 110 - 41 Inc.
We're all about that simple maths.

Project boilerplate generated using [Pinax](http://pinaxproject.com).

## How To Install (Mac)

### Grab this Repo
1. Open Terminal
2. `cd` to whatever folder you want to put this repo in ex. `cd ~/Projects`
3. `git clone https://github.com/MikeShi42/41Inc.git`
4. Log into your GitHub account if neccessary

### Install Node.js and npm
We need npm to install our frontend build tools. Likewise, we need node to run the tools.
1. `brew install node`
  * `Node` is JavaScript for backend
  * `npm` is the package manager, it'll help you install more Node things on your system.
2. `node -v` to test that Node was installed successfully. It should print out something like `v5.0.0`
3. `npm -v` to test that npm was installed successfully. It should print out something like `3.3.6`.

### Install Gulp - IMPORTANT EVEN IF YOU'VE USED THIS BEFORE
Pinax uses Gulp 4.0!

1. ```npm install gulpjs/gulp#4.0 -g```
  * This installs Gulp 4.0 globally for you. Don't forget the `-g` flag!
2. `gulp -v` to test that Gulp 4.0 was installed successfully. Should show something like:
```
[22:35:08] CLI version 1.2.1
[22:35:08] Local version 4.0.0-alpha.2
```

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
successfully. Should print out something like `15.0.1`
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

### Installing the Project
1. `pip install -r requirements.txt`
  * This will tell `pip` to install all the packages specified in 
  `requirements.txt`
2. Set up the database
```
./manage.py migrate
./manage.py loaddata sites
```
3. `npm install`
  * This will install the frontend dependencies.

### Trying Out Django

1. `cd` to the `41Inc` if you aren't there already. So your current directory
should be `$ ~/../41Inc`
2. `python manage.py runserver`
3. Visit `http://127.0.0.1:8000/` in your browser.
  * A success page should pop up

### Generating the frontend assets
1. To watch: `npm run watch`
  * This is basically a magical command that will build everything. In other words, it'll convert all the SCSS into CSS,
   minimize everything, concatenate everything, and make sure it's in the right place.
  * If you just run `gulp`, then it'll "watch" the frontend assets in `/static`. This means that it'll automatically build everything when it notices a change.
2. To build only: `npm run build`
  * This only builds the assets and places them in the correct folders.




## General Resources
* General Python Setup Guide: http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/
* Virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
* Getting started with Django: https://docs.djangoproject.com/en/1.9/topics/install/#installing-official-release
