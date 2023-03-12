from flask_app import app 
from flask import render_template, redirect, request, flash, session 
from flask_app.models.companies import Company
from flask_app.models.agencies import Agency
from flask_app.models.services import Service

@app.route('/signin')
def sign_in():

    return render_template('login.html')

@app.route('/company/dashboard')
def company_dashboard():

    if not 'user_id' in session:
        flash("Please log in first!")
        return redirect('/')
    

    company= Company.find_company_by_id(session['user_id'])
    return render_template('company_dashboard.html', company=company)

@app.route('/agency/dashboard')
def agency_dashboard():

    if not 'user_id' in session:
        flash("Please log in first!")
        return redirect('/')

    agency = Agency.get_agency_by_id(session['user_id'])
    services = Service.get_agency_services(session['user_id'])
    return render_template('agency_dashboard.html', agency=agency, services=services)



@app.route('/login', methods=["POST"])
def login():

    # Check if the email and password combination exists in the Company table
    found_user = Company.validate_login(request.form)
    if found_user:
        session['user_id'] = found_user.id
        return redirect('/company/dashboard')
    

    # Check if the email and password combination exists in the Agency table
    found_user = Agency.validate_login(request.form)
    if found_user:
        session['user_id'] = found_user.id
        return redirect('/agency/dashboard')

    # If the email and password combination doesn't exist in either table, flash an error message and redirect back to the login page
    flash("Email and password combination does not meet our records.", "login")
    return redirect('/signin')



@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'logout')
    return redirect('/')
