from flask_app import app 
from flask import render_template, redirect, request, flash, session 
from flask_app.models.agencies import Agency
from flask_app.models.services import Service

@app.route('/agency/signup')
def agency_signup():

    return render_template('agency_signup.html')


@app.route('/register/agency', methods=["POST"])
def register_agency():

    if not Agency.validate_registrartion(request.form):
        return redirect('/agency/signup')
    
    Agency.sign_agency(request.form)
    return redirect('/agency/dashboard')


@app.route('/add_services', methods=['POST'])
def add_services():

    selected_services = request.form.getlist('services')
    agency_id = session['user_id']

    print("Selected services:", selected_services)
    print("Agency ID:", agency_id)
    # Use create_service method for each selected service
    for name in selected_services:
        Service.create_service(name, agency_id)

    return redirect('/edit/services')


@app.route('/edit_agency')
def edit_agency():

    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/')

    agency = Agency.get_agency_by_id(session['user_id'])

    return render_template('edit_agency.html', agency=agency)
    
@app.route('/update/agency', methods=["POST"])
def update_agency():

    if not 'user_id' in session:
        flash("Please log in first!")
        return redirect('/')


    Agency.update_agency(request.form)
    return redirect("/agency/dashboard")


@app.route('/edit/services')
def edit_services():

    if 'user_id' not in session:
        flash("Please log in first!")
        return redirect('/')

    agency = Agency.get_agency_by_id(session['user_id'])
    services = Service.get_agency_services(session['user_id'])

    return render_template('edit_services.html', agency=agency, services=services)
    
@app.route('/update/services/<int:service_id>', methods=["POST"])
def update_services(service_id):

    if not 'user_id' in session:
        flash("Please log in first!")
        return redirect('/')

    try:
        for key in request.form:
            print(key + ": " + request.form[key])
            
        Service.update_services(request.form, service_id)
        return redirect("/edit/services")

    except Exception as e:
        print(str(e))
        flash("An error occurred while updating the services.")
        return redirect("/agency/dashboard")
    
    # Service.update_services(request.form)
    # return redirect("/agency/dashboard")


@app.route('/delete_service/<int:service_id>', methods=["POST"])
def delete_service(service_id):

    Service.delete_service(service_id)

    return redirect('/edit/services')