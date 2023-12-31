from flask import Flask, render_template, request, redirect, url_for
import json
from os import environ
from config import PORT, JSON_FILE
from database import collection, populate_db
from logger import logger
from tickets import tickets_cache, reload_cache, create_ticket

app = Flask(__name__)


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
        new_ticket = create_ticket(
            subject, severity, description, tickets_cache)
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


if __name__ == "__main__":
    if environ.get('MONGODB_CONNECTION_STRING') is None:
        logger.error(
            "Conection String for MongoDB in environment variable MONGODB_CONNECTION_STRING not set!")
        exit(1)
    # Read data from the JSON file
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
            tickets_cache = data.get('Tickets', [])
    except FileNotFoundError:
        logger.error(f"File '{JSON_FILE}' not found.")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")

    populate_db(tickets_cache)
    reload_cache(tickets_cache, collection)
    # Run on 0.0.0.0 instead of 127.0.0.1 to allow access from the docker host
    app.run(host="0.0.0.0", port=PORT, debug=True)
