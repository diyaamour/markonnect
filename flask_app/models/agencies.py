from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, BCRYPT
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Agency:

    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.name = data['name']
        self.location = data['location']
        self.contact = data['contact']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def sign_agency(cls, form):

        bct_password = BCRYPT.generate_password_hash(form['password'])

        data = {
            **form, 
            'password': bct_password
            }

        query = """
        INSERT INTO agencies (email, password, name, location, contact)
        VALUES (%(email)s, %(password)s, %(name)s, %(location)s, %(contact)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
        # # Insert the agency into the database
        # cursor = connectToMySQL(DATABASE).query_db(query, data)

        # # Get the ID of the newly created agency
        # agency_id = cursor.lastrowid

        # # Return the agency ID
        # return agency_id


        
        # agency_id = connectToMySQL(DATABASE).query_db(query, data)
        # return agency_id

    ############################################### REGISTRATION VALIDATION ######################################## 

    @staticmethod 
    def validate_registrartion(data):


        # Email Requirements 
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email format.', 'error')
            return False

        # Password Requirements
        MIN_LENGTH = 8
        has_uppercase = False
        has_lowercase = False
        has_digits = False

        for char in data['password']:
            if char.isupper():
                has_uppercase= True  
            elif char.islower():
                has_lowercase = True
            elif char.isdigit():
                has_digits = True

        if not( len(data['password']) >= MIN_LENGTH and has_uppercase and has_lowercase and has_digits ):
            flash('Password must be at least 8 characters long and contains at least one uppercase letter, one lowercase letter, and one digit.', 'error')
            return False
        

        # to confirm passwords match 

        if (data['password'] != data['confirm_password']):
            flash('Passwords do not match!', 'error')
            return False


        flash ('Registration Complete!', 'success')
        return True 


    @classmethod
    def get_one_by_email(cls, email):

        data = {
            'email' : email
        }

        query = "SELECT * FROM agencies WHERE email = %(email)s;"

        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])

        else: 
            return False 

    @classmethod
    def validate_login(cls, form):
        data = {
            'email': form['email']
        }

        query = "SELECT * FROM agencies WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            found_user = cls(results[0])
            hashed_pw = results[0]['password']
            valid_password = BCRYPT.check_password_hash(hashed_pw, form['password'])

            if valid_password:
                return found_user

        return False
    


    @classmethod
    def get_agency_by_id(cls, agency_id):

        data = {
            'id': agency_id
        }

        query = """
        SELECT * from agencies WHERE id = %(id)s; """

        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            agency = cls(results[0])
            print(agency)

            return agency 
        
    @classmethod
    def update_agency(cls, data):

        query = """
        UPDATE agencies SET 
        email = %(email)s,
        name = %(name)s, 
        location = %(location)s,
        contact = %(contact)s, 
        updated_at = NOW()
        WHERE id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all(cls):

        query = "SELECT * FROM agencies"

        return connectToMySQL(DATABASE).query_db(query)
    
    
    # @classmethod
    # def view_agency_details(cls, agency_id):

    #     data = {
    #         'id': agency_id
    #     }

    #     query = """"
    #             SELECT *
    #             FROM agencies
    #             LEFT JOIN services ON agencies.id = services.agency_id
    #             LEFT JOIN reviews ON agencies.id = reviews.agency_id
    #             WHERE agencies.id = %(id)s;"""
        
    #     results = connectToMySQL(DATABASE).query_db(query, data)

    #     if results: 
    #         agency = cls(results[0])
    #         agency.services = Service.get_agency_services(agency.id)
    #         agency.reviews = Review.get_agency_reviews(agency.id)

    #     return agency
    
