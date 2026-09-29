# CRM System

A web-based Customer Relationship Management (CRM) system built with Django for managing leads, tracking sales activities, automating lead scoring, monitoring the sales pipeline, and analyzing CRM performance.

## Features

* User authentication and login
* Role-based access control
* Lead creation and management
* Lead status tracking
* Automatic lead scoring
* Configurable lead scoring rules
* Lead search and filtering
* Follow-up and activity management
* Upcoming and overdue follow-ups
* Sales pipeline dashboard
* Conversion rate calculation
* Average lead score analytics
* CSV lead import
* Duplicate lead detection
* Closed Won conversion tracking
* Responsive Bootstrap interface

## Lead Management

The system allows users to:

* Create new leads
* View detailed lead information
* Edit existing leads
* Track lead status
* View lead scores
* Filter leads by status
* Search leads by name, email, or company
* Filter leads based on minimum score

## Automated Lead Scoring

The CRM calculates a lead score automatically based on configurable rules.

Example scoring rules:

| Rule               | Points |
| ------------------ | -----: |
| Qualified Lead     |     20 |
| Proposal Lead      |     20 |
| Company Provided   |     10 |
| Phone Provided     |     10 |
| Job Title Provided |     10 |
| Email Provided     |     10 |

The score is automatically recalculated when a lead is created or updated.

## Sales Pipeline

The system supports the following stages:

* New
* Contacted
* Qualified
* Proposal
* Negotiation
* Closed Won
* Closed Lost

The dashboard displays pipeline statistics and conversion information.

## Follow-up Management

Users can create activities and follow-ups for individual leads.

The system separates activities into:

* Upcoming follow-ups
* Overdue follow-ups
* Completed activities

## CSV Import

Leads can be imported using a CSV file.

The import system:

* Validates the CSV file
* Requires an email address
* Prevents duplicate email addresses
* Creates leads automatically
* Calculates lead scores
* Reports successfully imported and skipped leads

## Dashboard

The dashboard provides an overview of CRM performance, including:

* Total leads
* Qualified leads
* Closed Won leads
* Closed Lost leads
* Average lead score
* Conversion rate
* Sales pipeline distribution

## Technologies

* Python
* Django 5.2
* SQLite
* HTML5
* CSS3
* Bootstrap
* Django Templates
* Git & GitHub

## Project Structure

```text
crm_system/
│
├── crm/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── leads/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── services.py
│   ├── decorators.py
│   └── ...
│
├── templates/
│   └── registration/
│
├── manage.py
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/crm-system.git
cd crm-system
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install django
```

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Future Enhancements

* Email notifications for follow-ups
* Advanced sales reports
* Lead assignment to sales representatives
* Pagination
* REST API
* PostgreSQL deployment
* Cloud deployment
* Advanced analytics
* Automated email integration

## Author

ARPITHA M 




