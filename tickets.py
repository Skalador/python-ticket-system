tickets_cache = []  # list of tickets


def reload_cache(tickets_cache, collection):
    tickets_cache = collection.find({})  # sync cache with database
