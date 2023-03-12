from flask_app import app 
from flask import render_template, redirect, request, flash, session 
from flask_app.models.companies import Company
from flask_app.models.agencies import Agency
from flask_app.models.reviews import Review
from flask_app.models.services import Service

@app.route('/')
def index():

    return redirect('/home')


@app.route('/home')
def home():

    return render_template('home.html')


@app.route('/company/signup')
def company_signup():

    return render_template('company_signup.html')


@app.route('/register/company', methods=["POST"])
def register():

    if not Company.validate_registrartion(request.form):
        return redirect('/company/signup')
    
    Company.sign_company(request.form)
    return redirect('/company/signup')


@app.route('/edit_company')
def edit_company():

    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/')

    company = Company.find_company_by_id(session['user_id'])

    return render_template('edit_company.html', company=company)
    
@app.route('/update/company', methods=["POST"])
def update_company():

    if not 'user_id' in session:
        flash("Please log in first!")
        return redirect('/')


    Company.update_company(request.form)
    return redirect("/company/dashboard")


@app.route('/dashboard')
def dashboard():

    if not 'user_id' in session:
        flash("Please log in first!")
        return redirect('/')
    
    agencies = Agency.get_all()
    company = Company.find_company_by_id(session['user_id'])
    return render_template('dashboard.html', company=company, agencies=agencies)

@app.route('/view/agency/<int:agency_id>')
def view_agency(agency_id):
        
    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/')
        
    reviews = Review.get_agency_reviews(agency_id)
    services = Service.get_agency_services(agency_id)
    company = Company.find_company_by_id(session['user_id'])
    agency = Agency.get_agency_by_id(agency_id)
    return render_template('view_agency.html', reviews=reviews, services=services, company=company, agency=agency)

