tickets_cache = []  # list of tickets


def reload_cache(tickets_cache, collection):
    tickets_cache = collection.find({})  # sync cache with database


def create_ticket(subject, severity, description, tickets_cache):
    new_ticket = {
        "Subject": subject,
        "Severity": severity,
        "Description": description,
        # Assign a unique ID based on the number of existing tickets
        "ID": len(tickets_cache)
    }
    return new_ticket
