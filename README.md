# Job Board - Django REST API

A comprehensive job board platform built with Django REST Framework, featuring job posting, application management, company profiles, and AI-powered resume analysis.

## 🚀 Features

### Core Functionality
- **Job Management**: Create, update, and manage job postings with detailed requirements and responsibilities
- **Application System**: Complete job application workflow with cover letters and resume uploads
- **Company Profiles**: Company registration and office management with location support
- **User Management**: Custom user model with email-based authentication
- **Bookmarking**: Save and manage favorite job postings

### Advanced Features
- **AI-Powered Analysis**: Automatic cover letter AI detection and resume analysis
- **Social Authentication**: Google OAuth2 integration for seamless login
- **Location Support**: Integration with cities-light for global location data
- **File Management**: Resume upload and storage with content extraction
- **Background Tasks**: Celery integration for asynchronous processing

### Technical Features
- **RESTful API**: Complete REST API with JWT authentication
- **Database**: PostgreSQL with Redis caching
- **Task Queue**: Celery with Redis broker for background tasks
- **Monitoring**: Flower for Celery monitoring and Silk for profiling
- **Documentation**: Auto-generated API documentation with drf-spectacular
- **Testing**: Comprehensive test suite with pytest and factory-boy

## 🏗️ Architecture

```
Job Board/
├── job_board/          # Main Django project
│   ├── settings/       # Environment-specific settings
│   ├── urls.py         # Main URL configuration
│   └── celery.py       # Celery configuration
├── users/              # User management app
├── job/                # Job posting and application app
├── company/            # Company and office management app
├── chat/               # Chat functionality (placeholder)
├── media/              # File uploads
└── requirements.txt    # Python dependencies
```

## 🛠️ Technology Stack

- **Backend**: Django 5.1.6, Django REST Framework
- **Database**: PostgreSQL 17
- **Cache & Broker**: Redis
- **Task Queue**: Celery
- **Authentication**: JWT, Google OAuth2
- **File Storage**: Local file system with media handling
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Testing**: pytest, factory-boy
- **Development Tools**: Silk profiler, Flower monitoring

## 📋 Prerequisites

- Python 3.10+
- Docker and Docker Compose
- PostgreSQL (if running locally)
- Redis (if running locally)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone http://github.com/YousefSedik/job-Board/
   cd job-board
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec django python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

6. **Access the application**
   - Main application: http://localhost:8000
   - Admin interface: http://localhost:8000/admin
   - API documentation: http://localhost:8000/api/schema/swagger-ui/
   - Celery monitoring: http://localhost:5555
   - Database admin: http://localhost:5050

### Local Development

1. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up database**
   ```bash
   # Start PostgreSQL and Redis
   # Update .env with database credentials
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=job_board
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Google OAuth2
YOUR_GOOGLE_CLIENT_ID=your-google-client-id
YOUR_GOOGLE_CLIENT_SECRET=your-google-client-secret

# Redis
REDIS_URL=redis://localhost:6379/0
```

### Google OAuth2 Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs: `http://localhost:8000/complete/google-oauth2/`
6. Update your `.env` file with the credentials

## 📚 API Documentation

### Authentication

The API supports multiple authentication methods:

- **JWT Tokens**: Primary authentication method
- **Token Authentication**: For legacy support
- **Session Authentication**: For web interface

#### JWT Authentication

```bash
# Get access token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use token in requests
curl -H "Authorization: Bearer <your-token>" \
  http://localhost:8000/api/job/
```

### Core Endpoints

#### Users
- `POST /api/register` - User registration
- `POST /api/token/` - Get JWT token
- `GET /api/user/profile/` - Get user profile
- `POST /api/auth/google/` - Google OAuth2 login

#### Jobs
- `GET /api/job/` - List jobs
- `POST /api/job` - Create job
- `GET /api/job/{id}/` - Get job details
- `PUT /api/job/{id}/` - Update job
- `POST /api/job/apply` - Apply for job
- `GET /api/bookmarks` - List bookmarks
- `POST /api/bookmark` - Create bookmark

#### Companies
- `GET /api/company/{id}/` - Get company details
- `PUT /api/company/{id}/` - Update company
- `GET /api/company/{id}/managers` - List company managers

#### Resumes
- `GET /api/resume` - List user resumes
- `POST /api/resume` - Upload resume
- `GET /api/resume/{id}/` - Get resume details

### API Documentation

Access the interactive API documentation:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## 🧪 Testing

### Run Tests

```bash
# Using Docker
docker exec -it jobboard-django-1 python3 manage.py test

# Local development
python3 manage.py test
```

### Generate Test Data

```bash
# Using management command
python manage.py generate_data

# Using factories
python manage.py shell
>>> from job.factories.factories import JobFactory
>>> JobFactory.create_batch(10)
```

## 🔄 Background Tasks

The application uses Celery for background task processing:

### Available Tasks

- **Resume Analysis**: Automatic resume content extraction and analysis
- **Cover Letter AI Detection**: Analyze cover letters for AI-generated content
- **Email Notifications**: Send application status updates

### Monitor Tasks

Access Flower dashboard at http://localhost:5555 to monitor:
- Task execution status
- Worker performance
- Queue statistics

## 📁 File Structure

```
Job Board/
├── job_board/              # Main Django project
│   ├── settings/           # Environment-specific settings
│   │   ├── base.py         # Base settings
│   │   ├── development.py  # Development settings
│   │   └── production.py   # Production settings
│   ├── urls.py             # Main URL configuration
│   ├── celery.py           # Celery configuration
│   └── wsgi.py             # WSGI configuration
├── users/                  # User management
│   ├── models.py           # Custom user and resume models
│   ├── api.py              # API views
│   ├── serializers.py      # Data serialization
│   ├── tasks.py            # Background tasks
│   └── factories/          # Test data factories
├── job/                    # Job management
│   ├── models.py           # Job and application models
│   ├── api.py              # API views
│   ├── serializers.py      # Data serialization
│   ├── tasks.py            # Background tasks
│   ├── services.py         # Business logic
│   └── factories/          # Test data factories
├── company/                # Company management
│   ├── models.py           # Company and office models
│   ├── api.py              # API views
│   ├── serializers.py      # Data serialization
│   └── factories/          # Test data factories
├── templates/              # Jinja2 templates (to be implemented)
├── media/                  # File uploads
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker services configuration
├── Dockerfile              # Docker image configuration
└── manage.py               # Django management script
```

