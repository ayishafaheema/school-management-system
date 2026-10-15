# School Management System

A Django-based School Management System built with PostgreSQL and Docker. The application provides role-based dashboards and tools for managing students, teachers, attendance, homework, examinations, and results.

## Features

- Role-based authentication and authorization
- Separate dashboards for administrators, teachers, and students
- Student and teacher management
- Attendance tracking and overview
- Homework assignment and status tracking
- Examination and result management
- Email notifications
- Profile management
- FullCalendar integration
- REST APIs using Django REST Framework
- PostgreSQL database integration
- Dockerized application and database using Docker Compose
- Persistent database storage and media-file mounting

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Tools:** Git, GitHub

## Prerequisites

- Git
- Docker Desktop or Docker Engine with Docker Compose

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ayishafaheema/school-management-system.git
cd school-management-system
```

### 2. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

Configure the following variables:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`

For Docker Compose, set `POSTGRES_HOST=db`. Use your own database credentials and Django secret key. Never commit your actual `.env` file to GitHub.

### 3. Build and Start the Application

```bash
docker compose up -d --build
```

### 4. Access the Application

Open your browser and visit:

http://localhost:8000

### 5. Check Running Containers

```bash
docker compose ps
```

### 6. View Application Logs

```bash
docker compose logs --tail=100 web
```

### 7. Stop the Application

```bash
docker compose stop
```

## Database and Media Storage

- PostgreSQL data is stored in a Docker named volume.
- Uploaded media files are mounted from the project's `media` directory.
- Each developer initializes their own database unless a database backup or sample data is provided separately.

## Notes

This project is configured for local development and testing using Django's development server.

## Author

**Ayisha Faheema**

- **GitHub:** [ayishafaheema](https://github.com/ayishafaheema)
- **LinkedIn:** [Ayisha Faheema](https://linkedin.com/in/ayisha-faheema/)
