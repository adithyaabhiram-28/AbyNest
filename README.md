# AbyNest

A Flask-based blogging web app with user authentication, profile image uploads via Cloudinary, and CRUD operations for posts.

## Features

- User registration, login, logout, and account updates
- Password hashing using Flask-Bcrypt
- Profile image upload and replacement using Cloudinary
- Create, read, update, and delete blog posts
- User-specific post listing with pagination
- Password reset token flow (email sending currently disabled in code)
- PostgreSQL-compatible database support via SQLAlchemy

## Tech Stack

- Python + Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Bcrypt
- Flask-Mail
- Cloudinary
- Pillow
- Gunicorn (for deployment)

## Project Structure

- `run.py` - app entrypoint and database table creation
- `flaskblog/__init__.py` - app factory, extension initialization, blueprint registration
- `flaskblog/config.py` - environment-driven configuration
- `flaskblog/models.py` - `User` and `Post` models
- `flaskblog/main/routes.py` - home/about routes
- `flaskblog/users/routes.py` - auth/account/password reset routes
- `flaskblog/posts/routes.py` - post CRUD routes
- `flaskblog/users/utils.py` - Cloudinary image helpers and reset-email placeholder

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt