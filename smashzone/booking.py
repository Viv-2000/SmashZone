import re

class Booking:
    def __init__(self, booking_id = None, name = None, email = None, headcount = None):
        self.id = booking_id
        self.name = name
        self.email = email
        self.headcount = headcount



    def to_dict(self):
        return {
            "booking_id" : self.id,
            "name" : self.name,
            "email" : self.email,
            "headcount" : self.headcount 
        }



    @staticmethod
    def validate_name(name):
        name = name.strip()
        if not name or not all(c.isalpha() or c.isspace() for c in name):
            return None
        return name
    



    @staticmethod
    def validate_email(email):
        email = email.strip()
        pattern = r"(?!.*\.\.)[A-Za-z0-9._%+-]{1,20}@[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*(?:\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)+"
        if re.fullmatch(pattern, email):
            return email
        return None




    @staticmethod
    def validate_headcount(count):
        if not isinstance(count, int):     
            return None
        if count < 1 or count > 4:
            return None
        return count




    @staticmethod
    def db_row_to_booking(row):
        if row is None:
            return None

        return Booking(
            booking_id = row["id"],
            name = row["name"],
            email = row["email"],
            headcount = row["headcount"] 
        )
    



    @staticmethod
    def db_row_to_dict(row):
        if row is None:
            return None

        return {
            'booking_id' : row["id"],
            'name' : row["name"],
            'email' : row["email"],
            "headcount" : row["headcount"] 
        }
    

