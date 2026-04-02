
from flask import Flask, render_template, request, redirect, url_for, jsonify
from booking import Booking
from booking_db import Booking_DB



db1 = Booking_DB()
db1.create_table()

app = Flask(__name__)

# root directory
@app.route('/')
def root():
    return render_template('index.html')



# show all bookings
@app.route('/bookings', methods = ['GET'])
def show_bookings():     
    results = [booking.to_dict() for booking in db1.get_all_bookings()]
    
    if 'error' in results:
        return jsonify(results), 400
        
    return jsonify(results), 200




# find a booking
@app.route('/bookings/<string:search_term>', methods = ['GET'])
def find_booking(search_term):
    search_term = search_term.strip()
    if not search_term:
        return jsonify({"error":"please enter something other than spaces..."}), 404      
      
    bookings = db1.search_bookings(search_term)
    
    if not bookings:
        return jsonify({"error":"sorry, booking not found..."}), 404
    
    if 'error' in bookings:
        return jsonify(bookings), 500
    
    results = [booking.to_dict() for booking in bookings]   
    return jsonify(results), 200





# make a new booking
@app.route('/bookings', methods = ['POST'])
def new_booking():

    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ('name', 'email', 'headcount')):
        return jsonify({"error": "name, email and headcount are required fields in order to secure your spot..."}), 400
    
    valid_name = Booking.validate_name(data['name'])
    valid_email = Booking.validate_email(data['email'])
    valid_headcount = Booking.validate_headcount(data['headcount'])

    if not valid_name:
        return {"error":"Name must contain letters and/or spaces..."}, 400
    if not valid_email:
        return {"error":"Not a valid email..."}, 400
    if not valid_headcount:
        return {"error":"headcount must be a number between 1 and 4..."}, 400
    
    new_booking = Booking(name = valid_name, email = valid_email, headcount = valid_headcount)
    result = db1.add_booking(new_booking)
   
    if 'error' in result:
        return jsonify(result), 409
    
    return jsonify(result), 200





# edit a current booking
# silent=True in request.json() tells Flask: "Try to parse JSON, but don’t crash if it fails — just return None.”
@app.route('/bookings/<int:booking_id>', methods = ['PUT'])
def update_booking(booking_id):

    data = request.get_json(silent=True)
    if not data or not any(k in data for k in ('name', 'email', 'headcount')):
        return jsonify({"error": "At least one of name or email or headcount is required to make an update"}), 400
    
    valid_name = None
    valid_email = None
    valid_headcount = None

    if 'name' in data:
        valid_name = Booking.validate_name(data['name'])
        if not valid_name:
            return {"error": "Name must contain letters and/or spaces..."}, 400

    if 'email' in data:
        valid_email = Booking.validate_email(data['email'])
        if not valid_email:
            return {"error": "Not a valid email..."}, 400
        
    if 'headcount' in data:
        valid_headcount = Booking.validate_headcount(data['headcount'])
        if not valid_headcount:
            return {"error":"headcount must be a number between 1 and 4..."}, 400      
    
    updated_booking = db1.update_booking(booking_id, valid_name, valid_email, valid_headcount)
    if 'error' in updated_booking:
        return jsonify(updated_booking), 500 
    
    return jsonify(updated_booking), 200





# delete a booking
@app.route('/bookings/<int:booking_id>', methods = ['DELETE'])
def delete_booking(booking_id):
    status = db1.delete_booking(booking_id)
    
    if status is True:
        return jsonify({"result": "booking deleted successfully..."}), 200
    elif status is False:
        return jsonify({"result": "booking does not exist..."}), 404  
    else:
        return status, 500




if __name__=='__main__':
    app.run(debug=True)