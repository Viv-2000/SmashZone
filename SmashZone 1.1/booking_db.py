
from booking import Booking

import psycopg, os
from psycopg.rows import dict_row


class Booking_DB:
    def __init__(self, db_name="bookings.db"):
        self.database_url = os.environ.get("DATABASE_URL")

        if not self.database_url:
            raise ValueError(
                "DATABASE_URL is not set. Example: "
                "postgresql://postgres:password@localhost:5432/bookings_db"
            )

    def get_connection(self):
        return psycopg.connect(
            self.database_url,
            row_factory=dict_row
        )

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

        conn.commit()
        conn.close()

    # CREATE
    def add_booking(self, booking):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO bookings (name, email) VALUES (%s, %s) RETURNING id",
            (booking.name, booking.email)
        )
        new_id = cursor.fetchone()['id']
        booking.id = new_id
        


        conn.commit()
        conn.close()
        return Booking.booking_to_dict(booking)

    # READ (ALL)
    def get_all_bookings(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()

        conn.close()
        return [Booking.db_row_to_booking(row) for row in rows]


    # search for bookings
    def search_bookings(self, name=None, email=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM bookings WHERE 1=1"
        params = []

        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")

        if email:
            query += " AND email LIKE %s"
            params.append(f"%{email}%")

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        conn.close()

        return [Booking.db_row_to_booking(row) for row in rows]


    # find booking by id
    def get_booking_by_id(self, booking_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bookings WHERE id = %s",(booking_id,))
        row = cursor.fetchone()
        conn.close()

        return Booking.db_row_to_booking(row)


    # UPDATE
    def update_booking(self, booking_id, name, email):
        existing = self.get_booking_by_id(booking_id)

        if existing is None:
            return None

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE bookings SET name = %s, email = %s WHERE id = %s",
            (name, email, booking_id)
        )

        conn.commit()
        conn.close()

        return Booking(booking_id, name, email)


    # DELETE
    def delete_booking(self, booking_id):
        existing = self.get_booking_by_id(booking_id)

        if existing is None:
            return False

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        conn.commit()
        conn.close()

        return True