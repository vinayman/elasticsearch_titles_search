# ElasticSearch Titles Search #

* This is a repo to to show examples of how to use ElasticSearch as a search engine backend with a Python Flask app
* We tokenise titles to enable more reactive searching when indexing the data
* Version 0.1

### Python Environment Setup ###

If you would like to use virtualenv as your Python package manager, you can setup the environment by doing the following:
### Install ###
Create and activate python3 virtual environment like:

    virtualenv -p python3 _environment_name_
    source _environtment_name_/bin/activate

### Install dependencies with pip: ###

    pip install -r requirements.txt



If you would like to use pipenv, you can setup the environment using the followig:
### pipenv ###

Install pipenv in your machine:

    `$ pip install pipenv`
    
Create a virtual environment and install the dependencies:

    `$ pipenv sync --dev`        

Activate the virtualenv:

    `$ pipenv shell`

To exit the venv shell:

    `$exit`


### PythonPath ###

From the root directory of the repo, set the PYTHONPATH:

`export PYTHONPATH="."`

### Docker ElasticSearch ###

To bring up the ElasticSearch instance, simply do the following:

`docker-compose up -d elasticsearch`


### Sample data ###

There is a script to import some sample data into the ElasticSearch instance, run the following script to insert the data:

`python scripts/titles2es.py --es-index titles`

### Environment variables ###

Remember to set the environment variables for the flask service:

```
export FLASK_DEBUG=1
export FLASK_APP=./dashboard/app.py
```

Now you should be able to access the application at:

`http://127.0.0.1:5000/`


Repo Owner:
`vinaymanektalla@gmail.com`