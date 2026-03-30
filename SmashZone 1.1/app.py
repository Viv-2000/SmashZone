
from flask import Flask, render_template, request, jsonify
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
    return jsonify([Booking.booking_to_dict(booking) for booking in db1.get_all_bookings()])


# find a booking
@app.route('/bookings/<string:name>', methods = ['GET'])
def find_booking(name):
    bookings = db1.search_bookings(name)
    if bookings is None:
        return jsonify({"error":"no booking found"})
    return jsonify([Booking.booking_to_dict(booking) for booking in bookings])


# make a new booking
@app.route('/bookings', methods = ['POST'])
def new_booking():
    if not 'name' in request.json or not 'email' in request.json:
        return jsonify({"error":"incomplete information"})
    new_booking=Booking(name=request.json['name'], email=request.json["email"])

    return jsonify(db1.add_booking(new_booking))


# edit a current booking
@app.route('/bookings/<int:booking_id>', methods = ['PUT'])
def update_booking(booking_id):

    booking = db1.get_booking_by_id(booking_id)
    if booking is None:
        return jsonify({"error": "booking not found"})
    
    updated_booking = db1.update_booking(booking_id,
                                 request.json.get('name', booking.name),
                                 request.json.get('email', booking.email))

    return jsonify(Booking.booking_to_dict(updated_booking))


# delete a booking
@app.route('/bookings/<int:booking_id>', methods = ['DELETE'])
def delete_booking(booking_id):
    status = db1.delete_booking(booking_id)
    if status:
        return jsonify({"result": "booking deleted"})
    else:
        return jsonify({"result": "booking does not exist"})



if __name__=='__main__':

    app.run(debug=True)