StatusForge
A lightweight incident status page for tracking service health and posting live incident updates.

Features
Public status page showing real-time health for all services (Operational / Degraded / Down)
Reverse-chronological incident timeline with title, description, status, and timestamp
Password-protected admin dashboard for managing services and posting incidents
Incident creation form with server-side validation and retained input on error
Automatic service status updates driven by the latest incident
Hashed admin credentials (Werkzeug password hashing, not plaintext)
Empty states and graceful error handling around all database queries
Fully responsive layout, from 320px mobile up to desktop
Accessible interactive states: visible keyboard focus outlines, hover/active feedback, and 44x44px minimum tap targets
Cohesive design system: 8px spacing scale, typographic scale, neutral/accent/status color tokens, and consistent 8px border radius
Tech Stack
Backend: Python, Flask
Database: SQLite via Flask-SQLAlchemy
Auth: Flask sessions + Werkzeug password hashing
Frontend: Jinja2 templates, vanilla CSS (no framework), Inter font
Production server: Gunicorn
Quick Start
Install dependencies (handled automatically in Replit; for local setup):
pip install flask flask-sqlalchemy gunicorn

Run the app:
python app.py

Open the app in your browser at http://localhost:5000.
The SQLite database is created automatically on first run (instance/app.db) and seeded with three sample services and a demo admin account.

Environment Variables
Variable	Required	Description
SESSION_SECRET	No	Secret key used to sign Flask session cookies. Falls back to a development key if unset — set a strong value in production.
Demo Login
Use these credentials to sign in to the admin dashboard at /admin/login:

Username	Password
admin	admin123
This is a seeded demo account for evaluation purposes only.

Built for the Digital Heroes Full Stack Developer trial.

