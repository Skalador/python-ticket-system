# Python-Ticket-System

In this repostiory a `python` web application is built which has the basic functionality of a ticketing system. `Flask` will be used as a web development framework.
Most of the frontend will be reused from the `GO` ticket system.

## Architecture
The ticket system utilizes the `Flask` framework and templating engine. The system uses a write-through cache model for the tickets with the `tickets_cache` variable. 

The backend database is `MongoDB`. MongoDB is hosted for free on Atlas. The Data can be visualized with `MongoDBCompass`.
On first startup the `MongoDB` will be checked for a database called `pythondb`. If this database does not exist, then the database will be created and populated with the data from `data.json`.


## Prerequisites
Installing dependencies:
```
pip install flask pymongo pytest
```
Note: It might be required to upgrade the `watchdog` package for `flask`. `pip install --upgrade watchdog`

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