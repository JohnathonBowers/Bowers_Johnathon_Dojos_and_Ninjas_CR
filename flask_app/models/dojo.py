from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo:
    def __init__ (self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.ninjas = []
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        results = connectToMySQL('dojos_ninjas_schema').query_db(query, data)
        return results
    
    @classmethod #In the comments below, I'm writing notes from Jonathan's lecture so I can refer back and understand the process better.
    def get_all_dojos(cls):
        query = "SELECT * FROM dojos ORDER BY name ASC;"
        results = connectToMySQL('dojos_ninjas_schema').query_db(query)  #This will return a list of dictionaries from our database. "results" will be that list of dictionaries
        dojo_objects = []
        for dojo in results: # "dojo" is going to be a dictionary
            dojo_objects.append(cls(dojo)) #We're appending an instance of the class "Dojo" using each dictionary from our query. Using "cls" with parentheses means we are trying to access the __init__ method and create an instance of our class.
        return dojo_objects
    
    @classmethod
    def get_dojo_with_ninjas(cls, data):
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s ORDER BY last_name ASC;"
        results = connectToMySQL('dojos_ninjas_schema').query_db(query, data)
        dojo = cls( results[0] )
        for dbrow in results:
            ninja_data = {
                'id': dbrow['ninjas.id'],
                'first_name': dbrow['first_name'],
                'last_name': dbrow['last_name'],
                'age': dbrow['age'],
                'created_at': dbrow['ninjas.created_at'],
                'updated_at': dbrow['ninjas.updated_at']
            }
            dojo.ninjas.append(ninja.Ninja(ninja_data))
        return dojo