class Booking:
    def __init__(self, booking_id = None, name = None, email = None):
        self.id = booking_id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def validate_name(name):
        if not name.strip().isalpha():
            raise ValueError("Name is invalid")

    @staticmethod
    def validate_email(email):
        if not email.strip().isalnum() or "@" not in email or "." not in email:
            raise NameError("Email cannot containt bla bla")

    @staticmethod
    def db_row_to_booking(row):
        if row is None:
            return None

        return Booking(
            booking_id=row["id"],
            name=row["name"],
            email=row["email"]
        )
    
    @staticmethod
    def db_row_to_dict(row):
        if row is None:
            return None

        return {
            'booking_id':row["id"],
            'name':row["name"],
            'email':row["email"]
        }
    

    @staticmethod
    def booking_to_dict(booking):
        return {"booking_id":booking.id,'name':booking.name,'email':booking.email}
    

