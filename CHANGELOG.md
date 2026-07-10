Changelog
All notable changes to this project are documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

1.0.0 - 2026-07-10
Added
Flask application scaffold with templates/ and static/ structure, running via a configured workflow on port 5000.
SQLite database (Flask-SQLAlchemy) with Service, Incident, and AdminUser models, seeded on startup with three sample services.
Public homepage displaying service cards with live status colors (Operational / Degraded / Down).
Reverse-chronological incident timeline on the homepage, with title, description, status, and timestamp.
Admin login and a protected admin dashboard, gated by a login_required decorator and Flask sessions.
Incident creation form on the admin dashboard that records a new incident and updates the related service's status.
Server-side form validation on incident creation, with retained input and inline error messages on invalid submissions.
Empty states for services and incidents, plus try/except error handling around all database queries, with a shared friendly error page.
Deployment configuration for autoscale publishing using Gunicorn as the production server.
README.md, LICENSE (MIT), .env.example, and .gitignore.
Changed
Admin authentication upgraded from hardcoded plaintext credentials to hashed passwords (Werkzeug generate_password_hash / check_password_hash).
Status badge styling refactored from a binary operational/down scheme to a proper three-state scheme (Operational / Degraded / Down), fixing a bug where "Degraded" incorrectly rendered with "Down" (red) styling.
Full typography and spacing redesign: 8px spacing scale, 14–32px type scale, Inter font.
Full color scheme redesign: neutral gray scale, single teal accent, semantic status colors, and a consistent 8px border-radius applied across cards, buttons, and panels.
The "StatusForge" heading restyled as the page's visual anchor via size and weight alone, with no boxes or borders.
Improved
Mobile responsiveness: viewport meta tags, stacking service cards, and a card-style layout for the incident table on narrow screens.
Accessibility and usability of interactive elements: visible keyboard focus outlines, hover and active states on all buttons and links, and a minimum 44x44px tap target for clickable elements.
Security
Replaced plaintext admin password storage with hashed passwords.
Wrapped all database-backed routes in error handling to avoid leaking stack traces and to fail gracefully.
