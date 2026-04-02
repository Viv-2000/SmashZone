
import psycopg, os
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row
from booking import Booking


class Booking_DB:
    def __init__(self, db_name="bookings.db"):
        self.database_url = os.environ.get("DATABASE_URL")

        if not self.database_url:
            raise ValueError(
                "DATABASE_URL is not set. Example: "
                "postgresql://postgres:password@localhost:5432/bookings_db"
            )






    def get_connection(self):
        try:
            return psycopg.connect(
                self.database_url,
                row_factory=dict_row
            )
        
        except Exception as e:
            print('database connection error:', e)
            raise




    def create_table(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        headcount INTEGER NOT NULL
                    )
                """)
        except Exception as e:
            print('Error creating table:', e)
            raise







    # CREATE
    def add_booking(self, booking):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO bookings (name, email, headcount) VALUES (%s, %s, %s) RETURNING id",
                    (booking.name, booking.email, booking.headcount)
                )
                new_id = cursor.fetchone()['id']
                booking.id = new_id
                return booking.to_dict()

        except UniqueViolation:
            return {"error": "This email is already in use..."}

        except psycopg.IntegrityError as e:
            return {"error": f"Database integrity error: {e}"}
        
        except Exception as e:
            return {"error": f"Some unknown error occured creating the booking: {e}"}







    # READ (ALL)
    def get_all_bookings(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM bookings")

                rows = cursor.fetchall()
                return [Booking.db_row_to_booking(row) for row in rows]
       
        except Exception as e:
            return {"error": f"Some unknown error occured while fetching all bookings: {e}"}







    # search for bookings
    def search_bookings(self, search_term=None):
        try: 
            with self.get_connection() as conn:
                cursor = conn.cursor()

                query = """ SELECT * FROM bookings WHERE name LIKE %s OR email LIKE %s """
                params = (f"%{search_term}%", f"%{search_term}%")

                cursor.execute(query, params)
                rows = cursor.fetchall()

                return [Booking.db_row_to_booking(row) for row in rows]
            
        except Exception as e:
            return {"error": f"Some unknown error occured while searching for booking: {e}"}






    # UPDATE
    def update_booking(self, booking_id, name, email, headcount):
        try:
            booking = self.get_booking_by_id(booking_id)
            
            if booking is None:
                return {"error":"no booking found for given id"}
            
            if isinstance(booking, dict):
                return booking

            name = booking.name if name is None else name
            email = booking.email if email is None else email
            headcount = booking.headcount if headcount is None else headcount

            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE bookings SET name = %s, email = %s, headcount = %s WHERE id = %s",
                    (name, email, headcount, booking_id)
                )
                
                return Booking(booking_id, name, email, headcount).to_dict()
            
        except UniqueViolation:
            return {"error": "This email is already in use..."}

        except psycopg.IntegrityError as e:
            return {"error": f"Database integrity error: {e}"}

        except Exception as e:
            return {"error": "Some unknown error occured while updating the booking"}







    # find booking by id
    def get_booking_by_id(self, booking_id):     
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM bookings WHERE id = %s",(booking_id,))
                row = cursor.fetchone()

                return Booking.db_row_to_booking(row)
            
        except Exception as e:
            return {"error": f"Some unknown error occured while fetching id: {e}"}






    # DELETE
    def delete_booking(self, booking_id):
        try:
            booking = self.get_booking_by_id(booking_id)

            if booking is None:
                return False
            
            if isinstance(booking, dict):
                return booking

            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
                return True
            
        except Exception as e:
            return {"error": f"Some unknown error occured while deleting the booking: {e}"}
    

