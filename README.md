<p align="center">
  <strong>Flask-App-Generator</strong> is a simple Flask Application Generator/Build-Tool runs via CLI
</p>

## What is Flask-App-Generator
Since Flask is commonly used in kickstarting a project, developers shouldn't waste their time with creating folders like static/css, static/js, configuration, controllers, models etc. Aim of Flask-App-Generator is __*auto generating necessity folders and files according to your architectural pattern*__.

### Architecture
Flask-App-Generator supports two different patterns:

#### simple
- It is a very simple flask application structure for very small applications
```
/your_project_folder
    .python_version
    app.py
    requirements.txt
    /apps
         __init__.py
         config.py
         /api
            __init__.py
            routes.py
         /authentication
            __init__.py
            forms.py
            models.py
            routes.py
         /static
            /assets
            /css
            /js
         /templates
            /home
                index.html
                signup.html
                login.html
            /layout
                base.html
                field.html
    
```

## How to use

#### Requirements
- Python 3.x
- pyenv
- pip3

Let me explain this project with an example. Assume that we want to create an Flask Application called ```todo-app```

### GNU/Linux - OSX

### Install

Clone this repo.
The installation via pip will be done in the future.


#### Usage
- Go to the flask-app-generator folder
- Create the app! Let's assume that we want to create an app named 'todo-app'

```
python3 flask-app-generator.py --name todo-app --directory ~/ --db sqlite

```
- That's it. Now activate the virtualenv, install the requirements and run the project:
```
cd ~/todo-app && pyenv activate todo-app && flask run
```

## RoadMap

- Add a run.py script to run the application
- Adding more options for configuration file.
- Better smart code generation for Postgresql/Mysql/Sqlite/MongoDB database
- Smart configuration for database
- Install via pip


## Contribution

Please feel free to contribute to this project, open issues, fork it, send pull requests.

You can also send email to my mail adress.__davidbarthelemy28@gmail.com__

Happy coding :metal:
