# Python-Ticket-System

In this repostiory a `python` web application is built which has the basic functionality of a ticketing system. `Flask` will be used as a web development framework.
Most of the frontend will be reused from the `GO` ticket system.

## Architecture
The ticket system utilizes the `Flask` framework and templating engine. The system uses a write-through cache model for the tickets with the `tickets_cache` variable. 

The backend database is `MongoDB`. MongoDB is hosted for free on Atlas. The Data can be visualized with `MongoDBCompass`.
On first startup the `MongoDB` will be checked for a database called `pythondb`. If this database does not exist, then the database will be created and populated with the data from `data.json`.

## Demo
https://github.com/Skalador/python-ticket-system/assets/117681263/6e8b62f5-dbab-4597-afc7-123226285602


## Prerequisites

### Install from requirements.txt

Installing dependencies:
```
pip install --no-cache-dir -r requirements.txt
```
Note: It might be required to upgrade the `watchdog` package for `flask`. `pip install --upgrade watchdog`

### Generate requirements.txt

```
# install
pip install pipreqs

# Run in current directory
python -m  pipreqs.pipreqs .
```

## Execute the code
An environment variable `MONGODB_CONNECTION_STRING` is used for the database connectivity, thus the connection string is not exposed in the code itself.

Expose the variable:
```
Windows: $env:MONGODB_CONNECTION_STRING = 'mongodb+srv://username:password@database/'
Linux: export MONGODB_CONNECTION_STRING="mongodb+srv://username:password@database/"
```

Run the code:
```
python main.py
```

## Testing

Tests are written with `pytest`.
Running tests with output:
```
python -m pytest
```

## Build the container image

Build the image with the `latest` tag
```
docker build -t python-ticket-system .
```

## Run the container image

Run the image with `docker` and use the environment variable `MONGODB_CONNECTION_STRING` 
```
docker run  -e "MONGODB_CONNECTION_STRING=$MONGODB_CONNECTION_STRING" -p 5000:5000 python-ticket-system
```

