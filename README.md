# SmashZone

SmashZone is a Flask-based booking application built to showcase backend development, API-style routing, database integration, object-oriented programming and frontend-backend communication.

The project allows users to:

- create a booking
- search for bookings by name
- view all bookings
- update a booking
- delete a booking

This project was built as part of my Python development portfolio to demonstrate practical API programming skills with Flask and SQL.

---

## Live App

Hosted app: **https://smashzone-version-1-1.onrender.com**


---

## Repository

This repo will have all future updates of SmashZone

---

## Project Overview

SmashZone is a simple end-to-end booking system where the frontend interacts with a Flask backend through HTTP requests.

The application supports CRUD operations:

- **Create** → add a booking
- **Read** → view all bookings
- **Search** → find bookings by name
- **Update** → edit an existing booking
- **Delete** → remove a booking

The goal of the project is to demonstrate:

- Python backend programming
- Flask route handling
- database operations
- object-oriented code structure
- frontend and backend integration
- deployment preparation

---

## Tech Stack

- **Python**
- **Flask**
- **SQLite** for local development
- **PostgreSQL** planned for deployment
- **HTML**
- **CSS**
- **JavaScript**

---

## Current Features

- Create a new booking
- View all bookings
- Search bookings by name
- Update a booking by ID
- Delete a booking by ID
- JSON-based backend responses
- Frontend integration using JavaScript `fetch()`

---

## Planned Improvements

Future updates planned for this project include:

- login page
- authentication
- session handling
- password hashing
- datetime support for bookings
- better validation
- improved error handling
- PostgreSQL deployment integration
- cleaner UI and UX improvements

---

## Project Structure

```bash
smashzone/
│
├── app.py
├── booking.py
├── booking_db.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── data/
    └── bookings.db
```
The data folder is created locally only during local testing as sqlite3 is used.
It will not be created in production as the database server created on deployment is managed by Render
