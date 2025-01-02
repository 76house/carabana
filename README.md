# Carabana

Carabana is a simple Django-based blog application.

## Prerequisites
- Python 3.10 or later
- Django 5.1 or later
- PostgreSQL (for production) or SQLite (for development)
- pip (Python package manager)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/76house/carabana.git
cd carabana
```

### 2. Create and activate a virtual environment
```bash
python -m venv .env
source .env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database

 - For development (SQLite): The project is preconfigured to use SQLite for development. No additional setup is required.
 - For production (PostgreSQL): Update the DATABASES setting in carabana/settings.py with your PostgreSQL credentials.

### 5. Apply database migrations
```bash
python manage.py migrate
```

### 6. Collect static files
```bash
python manage.py collectstatic
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit the app at http://127.0.0.1:8000.

## Media Files

Media files (e.g., uploaded pictures) are stored in the media/ directory.
During development, ensure the MEDIA_URL and MEDIA_ROOT settings in carabana/settings.py are configured correctly.

## Admin Access

Create a superuser to access the Django Admin panel:

```bash
python manage.py createsuperuser
```

Log in at http://127.0.0.1:8000/admin.

