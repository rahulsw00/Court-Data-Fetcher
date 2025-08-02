# Court Data Fetcher & Dashboard
A web application for fetching and displaying case metadata and orders/judgments from Indian court website.

## Target Court
Delhi High Court (https://delhihighcourt.nic.in/)

## Technologies Used
- Backend: Django (Python)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Scraping: Selenium

## Setup Instructions
### Prerequisites
- Python 3.13.3+

### Installation
1. Clone the repository:
```
git clone https://github.com/yourusername/court-data-fetcher.git
cd court-data-fetcher
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Apply database migrations:
```
python manage.py migrate
```

5. Create a superuser (optional):
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

## CAPTCHA Handling Strategy
Scans HTML for elements with `id` containing "captcha"

## API Endpoints
- `api/cases/` - REST API endpoint (GET)
- `/` - Main search interface (GET/POST)
- `/admin/` - Django admin interface

## Screenshots
<img width="1918" height="944" alt="image" src="https://github.com/user-attachments/assets/db69748e-6bcb-4e19-903c-6ea15bba333b" />
<img width="1920" height="946" alt="image" src="https://github.com/user-attachments/assets/3d03ce65-a56b-476a-8b36-42a834023e04" />
<img width="1920" height="1383" alt="image" src="https://github.com/user-attachments/assets/fa8b5d8b-2d35-47e0-bb8a-18f1c2f54614" />



