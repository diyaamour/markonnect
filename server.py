from flask_app import app
from flask_app.controllers import companies_controller, agencies_controller, login_controller

if __name__ == '__main__':
    app.run(debug=True, port=5001)