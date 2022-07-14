from flask_app.config.mysqlconnection import connectToMySQL
# Might need to import the other model files
from flask_app.models import animal
# from flask_app import app # Might need to import the app in certain cases

class Zoo:
    # Use a class variable later on - it'd be nice to not have to change the schema name a million times (hint)

    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.city = data["city"]
        self.size_acres = data["size_acres"] # Acreage
        self.visitor_capacity = data["visitor_capacity"]
        self.opening_date = data["opening_date"] # When the zoo opened for the first time
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.animals = [] # NEW: Hold a list of Animals

    # We will write our queries here and talk to MySQL

    # Add a zoo to zoos
    @classmethod
    def add_zoo(cls, data):
        query = "INSERT INTO zoos (name, city, size_acres, visitor_capacity, opening_date) VALUES ( %(name)s, %(city)s, %(size_acres)s, %(visitor_capacity)s, %(opening_date)s );"

        # Connect to zoos_animals DB and pass it the query and the data to insert
        return connectToMySQL("zoos_animals").query_db(query, data)
    
    @classmethod
    def get_all_zoos(cls):
        query = "SELECT * FROM zoos;"
        results = connectToMySQL("zoos_animals").query_db(query)
        if len(results) == 0:
            return []
        else:
            zoo_objects = []
            for zoo_dictionary in results:
                new_zoo_object = cls(zoo_dictionary)
                zoo_objects.append(new_zoo_object)
            
            return zoo_objects
    

    @classmethod
    def get_one_zoo(cls, data):
        query = "SELECT * FROM zoos WHERE id = %(id)s;"
        results = connectToMySQL("zoos_animals").query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])