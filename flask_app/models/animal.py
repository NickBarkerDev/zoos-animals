from flask_app.config.mysqlconnection import connectToMySQL
# Might need to import the other model files
from flask_app.models import zoo
# from flask_app import app # Might need to import the app in certain cases

class Animal:
    # Use a class variable later on - it'd be nice to not have to change the schema name a million times (hint)

    db_name = "zoos_animals"

    def __init__(self, data): # data is a dictionary - a row of data from your database
        self.id = data["id"]
        self.species = data["species"]
        self.name = data["name"]
        self.weight = data["weight"]
        self.color = data["color"]
        self.height = data["height"]
        self.birth_date = data["birth_date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.zoo = None # NEW: Linking one Zoo to this Animal

    # We will write our queries here and talk to MySQL

    @classmethod
    def add_animal(cls, data):
        query = "INSERT INTO animals (species, name, weight, color, height, birth_date, zoo_id) VALUES ( %(species)s, %(name)s, %(weight)s, %(color)s, %(height)s, %(birth_date)s, %(zoo_id)s );"

        return connectToMySQL("zoos_animals").query_db(query, data)

    @classmethod
    def get_all_animals(cls):
        query = "SELECT * FROM animals"
        results = connectToMySQL("zoos_animals").query_db(query)

        if len(results) == 0:
            return []
        else:
            animals = []
            for animal in results:
                new_animal = cls(animal)
                animals.append(animal)
                
            return animals
    
    @classmethod
    def get_all_animals_with_zoos(cls):
        query = "SELECT * FROM animals JOIN zoos ON animals.zoo_id = zoos.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        if len(results) == 0: # if no animals found
            return []         # return an empty list
        else:              
            all_animal_objects = []
            # Loop through list of Animal dictionaries
            for this_animal_dict in results:
            # Create Animal object
                new_animal_object = cls(this_animal_dict)

                # Create the Zoo object
                this_zoo_dict = {
                    "id": this_animal_dict['zoos.id'],
                    "city": this_animal_dict['city'],
                    "name": this_animal_dict['zoos.name'],
                    "size_acres": this_animal_dict['size_acres'],
                    "visitor_capacity": this_animal_dict['visitor_capacity'],
                    "opening_date": this_animal_dict['opening_date'],
                    "created_at": this_animal_dict['zoos.created_at'],
                    "updated_at": this_animal_dict['zoos.updated_at']
                }
                new_zoo_object = zoo.Zoo(this_zoo_dict)
                # Link this zoo object to this animal object
                new_animal_object.zoo = new_zoo_object

                # Add this Animal to the all_animal_objects list
                all_animal_objects.append(new_animal_object)
            return all_animal_objects
