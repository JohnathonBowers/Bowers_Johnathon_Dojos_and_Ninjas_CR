from flask_app.config.mysqlconnection import connectToMySQL

class Ninja:
    def __init__ (self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.age = db_data['age']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def get_all_ninjas(cls):
        query = "SELECT * FROM ninjas ORDER BY last_name ASC;"
        results = connectToMySQL('dojos_ninjas_schema').query_db(query)
        ninja_objects = []
        for ninja in results:
            ninja_objects.append(cls(ninja)) #We're appending an instance of the class "Dojo" using each dictionary from our query. Using "cls" with parentheses means we are trying to access the __init__ method and create an instance of our class.
        return ninja_objects
    
    @classmethod
    def save (cls, data):
        query = "INSERT INTO ninjas (first_name, last_name, age, dojo_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);"
        return connectToMySQL('dojos_ninjas_schema').query_db(query, data)