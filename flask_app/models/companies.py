from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, BCRYPT
from flask import flash
import re
import datetime, time 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Company:

    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.name = data['name']
        self.location = data['location']
        self.contact = data['contact']
        self.industry = data['industry']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def sign_company(cls, form):

        bct_password = BCRYPT.generate_password_hash(form['password'])

        data = {
            **form, 
            'password': bct_password
            }

        query = """
        INSERT INTO companies (email, password, name, location, contact, industry)
        VALUES (%(email)s, %(password)s, %(name)s, %(location)s, %(contact)s, %(industry)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)


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



    ############################################## Login Validation #############################################

    @classmethod
    def get_one_by_email(cls, email):

        data = {
            'email' : email
        }

        query = "SELECT * FROM companies WHERE email = %(email)s;"

        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])

        else: 
            return False 

    @classmethod
    def find_company_by_id(cls, company_id):

        data = {
            'id': company_id
            
            }

        query = "SELECT * FROM companies WHERE id = %(id)s;"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])

        
    # @classmethod
    # def get_all_users(cls):

    #     query = "SELECT * FROM users;"

    #     results = connectToMySQL(DATABASE).query_db(query)

    #     users = []

    #     for result in results: 
    #         users.append(cls(result))

    #     return users


    @classmethod
    def validate_login(cls, form):
        data = {
            'email': form['email']
        }

        query = "SELECT * FROM companies WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            found_user = cls(results[0])
            hashed_pw = results[0]['password']
            valid_password = BCRYPT.check_password_hash(hashed_pw, form['password'])

            if valid_password:
                return found_user

        return False

    @classmethod
    def update_company(cls, data):

        query = """
        UPDATE companies SET 
        email = %(email)s,
        name = %(name)s, 
        location = %(location)s,
        contact = %(contact)s,
        industry = %(industry)s, 
        updated_at = NOW()
        WHERE id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query, data)