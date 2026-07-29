# Flask Account Security

A secure user authentication system built with Flask that demonstrates secure authentication practices, session management, and common web application security controls. This project was developed as part of a learning roadmap toward becoming a Web & API Security Consultant.

The application focuses on building authentication securely first before progressing to REST APIs and advanced web security testing.

---

# Features

## Authentication

* User registration
* User login
* User logout
* Protected dashboard
* Session-based authentication using Flask-Login

---

## Password Security

* Password hashing using Flask-Bcrypt
* Strong password policy

  * Minimum 8 characters
  * At least one uppercase letter
  * At least one lowercase letter
  * At least one number
  * At least one special character

---

## Session Security

* Automatic session expiration after 10 minutes
* Session refresh on every request
* Session fixation mitigation using `session.clear()` after successful login
* Protected routes requiring authentication

---

## Account Validation

* Unique usernames
* Unique email addresses
* Password confirmation during registration

---

## Security Controls

* CSRF protection using Flask-WTF
* Login rate limiting (5 login attempts per minute)
* Open redirect protection after login
* Custom HTTP 429 error page for rate limiting

The application also includes commented production-ready session cookie settings:

* Secure cookies (`SESSION_COOKIE_SECURE`)
* HTTPOnly cookies (`SESSION_COOKIE_HTTPONLY`)
* SameSite cookies (`SESSION_COOKIE_SAMESITE`)

These should be enabled when deploying over HTTPS.

---

# Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-WTF
* Flask-Bcrypt
* Flask-Login
* Flask-Limiter
* PostgreSQL
* Docker
* Gunicorn
* HTML
* CSS

---

# Project Structure

```text
.
├── app.py
├── templates/
├── static/
├── migrations/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/<your-username>/flask-account-security.git

cd flask-account-security
```

---

## Create a virtual environment

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure environment variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost/flask_security
CSRF_SECRET_KEY=your-secret-key
```

---

## Run database migrations

```bash
flask db upgrade
```

or, if creating the database for the first time:

```bash
flask db init

flask db migrate -m "Initial migration"

flask db upgrade
```

---

## Start the application

```bash
python app.py
```

or

```bash
flask run
```

---

# Running with Docker

Build and start the application using Docker Compose.

```bash
docker compose up --build
```

Stop the containers.

```bash
docker compose down
```

---

# Security Features Implemented

| Feature                     | Status |
| --------------------------- | ------ |
| Password Hashing            | ✅      |
| Strong Password Validation  | ✅      |
| CSRF Protection             | ✅      |
| Session Authentication      | ✅      |
| Protected Routes            | ✅      |
| Session Expiration          | ✅      |
| Session Refresh             | ✅      |
| Session Fixation Mitigation | ✅      |
| Login Rate Limiting         | ✅      |
| Open Redirect Protection    | ✅      |
| Password Confirmation       | ✅      |
| Unique Username Validation  | ✅      |
| Unique Email Validation     | ✅      |

---

# Security Testing

This application is intended to be tested in a local lab environment using tools such as:

* Burp Suite
* Browser Developer Tools
* Postman

The goal is to understand how authentication works, identify potential weaknesses, and implement secure mitigations.

---

# Future Improvements

Planned enhancements include:

* JWT authentication
* Refresh tokens
* Password reset via email
* Email verification
* Account lockout after repeated failed logins
* Remember Me functionality
* Role-Based Access Control (RBAC)
* Multi-Factor Authentication (MFA)
* Blueprint-based project structure
* Audit logging
* Security headers
* Automated security testing

---

# Learning Objectives

This project demonstrates practical implementation of:

* Secure user authentication
* Password storage best practices
* Session management
* Cookie security
* Authentication hardening
* Defensive programming
* Basic web application security

It forms the foundation for later projects involving REST APIs, JWT authentication, OWASP Top 10 vulnerabilities, API security, penetration testing, and secure software development.

---

# Disclaimer

This project is intended for educational purposes and secure software development practice. Any security testing should only be performed against systems you own or are explicitly authorised to test.

---

# Licence

This project is released under the MIT Licence.
