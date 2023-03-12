from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.agencies import Agency

class Review:

    def __init__(self, data):
        self.id = data['id']
        self.rating = data['rating']
        self.text= data['text']
        self.agency_id = data['agency_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_agency_reviews(cls, agency_id):

        data = {
            'agency_id': agency_id
        }

        query = """SELECT * FROM reviews JOIN agencies  ON agencies.id = agency_id WHERE agency_id = %(agency_id)s;  """

        results = connectToMySQL(DATABASE).query_db(query, data)

        reviews = []
        if results:
            for result in results:
                review  = cls(result)

                agency_data = {
                    **result,
                    'id': result['agencies.id'],
                    'created_at': result['agencies.created_at'],
                    'updated_at': result['agencies.updated_at'],
                }

                review.agency = Agency(agency_data)
                reviews.append(review)

        return reviews
    

    @classmethod
    def create_review(cls, data):

        data = {
            'rating' : data['rating'],
            'text' : data['text'],
            'agency_id' : data['agency_id']
        }

        query = "INSERT INTO reviews (rating, text, agency_id) VALUES (%(rating)s, %(text)s,%(agency_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data)