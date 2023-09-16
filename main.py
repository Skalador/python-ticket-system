from flask import Flask, render_template, request, redirect, url_for
import json
import os
import pymongo
import logging

# Constant
PORT = 5000
CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

# Global Variables
json_file = 'data.json'
tickets_cache = []  # list of tickets
client = pymongo.MongoClient(CONNECTION_STRING)
db = client['pythondb']
collection = db['tickets']
app = Flask(__name__)

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the log level (e.g., INFO, DEBUG, WARNING)
    # Define log message format
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Define date and time format
)
# Create a logger instance
logger = logging.getLogger(__name__)


def reload_cache(tickets_cache):
    tickets_cache = collection.find({})  # sync cache with database


@app.route("/")
def index():
    return render_template('index.html', tickets=tickets_cache)


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        # Get data from the submitted form
        subject = request.form.get("subject")
        severity = request.form.get("severity")
        description = request.form.get("description")

        # Create a new ticket dictionary
        new_ticket = {
            "Subject": subject,
            "Severity": severity,
            "Description": description,
            # Assign a unique ID based on the number of existing tickets
            "ID": len(tickets_cache)
        }
        logger.info("Adding ticket: " + str(new_ticket))

        # Add the new ticket to the list of tickets
        tickets_cache.append(new_ticket)

        # Add the ticket to the database
        result = collection.insert_one(new_ticket)
        logger.debug(result)

        # Redirect back to the main page
        return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        # Get the ID of the ticket to delete from the form data
        ticket_id = int(request.form.get("id"))

        # Find and remove the ticket with the specified ID from the list
        for ticket in tickets_cache:
            if ticket["ID"] == ticket_id:
                logger.info("Removing ticket: " + str(ticket))

                # Remove ticket from database
                delete_query = {"ID": ticket_id}
                result = collection.delete_one(delete_query)
                logger.debug(result)

                # Remove ticket from cache
                tickets_cache.remove(ticket)

        # Redirect back to the main page
        return redirect(url_for("index"))


def populate_db():
    db_names = client.list_database_names()
    python_db_exists = False
    for db in db_names:
        logger.debug("Following db exists: " + db)
        if db == 'pythondb':
            python_db_exists = True

    if python_db_exists:
        logger.debug("pythondb exists, no population needed!")
    else:
        result = collection.insert_many(tickets_cache)
        logger.debug(result)


if __name__ == "__main__":
    # Read data from the JSON file
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            tickets_cache = data.get('Tickets', [])
    except FileNotFoundError:
        logger.error(f"File '{json_file}' not found.")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")

    populate_db()
    reload_cache(tickets_cache)
    app.run(host="127.0.0.1", port=PORT, debug=True)
