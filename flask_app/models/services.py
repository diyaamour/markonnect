from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.agencies import Agency


class Service: 

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.cost = data['cost']
        self.agency_id = data['agency_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_service(cls, name, agency_id):

        # print('Name:', name)
        # print('Agency ID:', agency_id)
        data = {
            'name': name,
            'agency_id': agency_id
        }

        query = "INSERT INTO services (name, agency_id) VALUES (%(name)s, %(agency_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data)
    


    @classmethod
    def get_agency_services(cls, agency_id):

        data = {
            'agency_id': agency_id
        }

        query = """SELECT * FROM services JOIN agencies  ON agencies.id = agency_id WHERE agency_id = %(agency_id)s;  """

        results = connectToMySQL(DATABASE).query_db(query, data)

        services = []
        if results:
            for result in results:
                service  = cls(result)

                agency_data = {
                    **result,
                    'id': result['agencies.id'],
                    'created_at': result['agencies.created_at'],
                    'updated_at': result['agencies.updated_at']
                }

                service.agency = Agency(agency_data)
                services.append(service)

        return services
    
    @classmethod
    def update_services(cls, data, service_id):

        data = {
            "name": data["name"],
        "description": data["description"],
        "cost": data["cost"],
        "id": service_id
        }

        query = """
        UPDATE services SET
        name = %(name)s,
        description = %(description)s,
        cost = %(cost)s,
        updated_at = NOW()
        WHERE id = %(id)s;"""

        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    
    @classmethod
    def delete_service(cls, service_id):
        data = {
            'id' : service_id
        }
        query = "DELETE FROM services WHERE services.id=%(id)s;"
        
        return connectToMySQL(DATABASE).query_db(query, data)