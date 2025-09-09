# TressRelief Server

A Django REST API server for a hair styling service platform that connects clients with professional stylists. This server provides endpoints for user management, service categories, hair services, and stylist-service relationships.

## Related Repositories

- **Client Application**: [tressrelief-client](https://github.com/alyssacleland/tressrelief-client) - React with Next.js frontend for the TressRelief platform

## Features

- **User Management**: Firebase authentication integration with role-based access (Client, Stylist, Admin)
- **Service Categories**: Organize hair services into categories (Braids, Feedins, etc.)
- **Hair Services**: Detailed service listings with descriptions, pricing, and duration
- **Stylist-Service Links**: Connect stylists with their offered services
- **RESTful API**: Clean, consistent API endpoints for all resources
- **Database Fixtures**: Pre-seeded data for categories, services, and user information

## Technology Stack

- **Framework**: Django with Django REST Framework
- **Database**: SQLite (development)
- **Authentication**: Firebase Authentication
- **Language**: Python 3.9
- **Package Management**: Pipenv

## Quick Start

### Prerequisites

- Python 3.9+
- Pipenv

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/alyssacleland/tressrelief-server.git
   cd tressrelief-server
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Activate virtual environment**
   ```bash
   pipenv shell
   ```

4. **Set up the database**
   ```bash
   chmod +x seed_database.sh
   ./seed_database.sh
   ```

5. **Load fixture data**
   ```bash
   python manage.py loaddata tressreliefapi/fixtures/categories.json
   python manage.py loaddata tressreliefapi/fixtures/services.json
   python manage.py loaddata tressreliefapi/fixtures/user_infos.json
   python manage.py loaddata tressreliefapi/fixtures/stylists_services.json
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The server will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /get-or-create-user` - Create or retrieve user based on Firebase auth

### User Management
- `GET /userinfo/` - List all users
- `POST /userinfo/` - Create new user
- `GET /userinfo/{id}/` - Get specific user
- `PUT /userinfo/{id}/` - Update user
- `DELETE /userinfo/{id}/` - Delete user

### Categories
- `GET /categories/` - List all service categories
- `POST /categories/` - Create new category
- `GET /categories/{id}/` - Get specific category
- `PUT /categories/{id}/` - Update category
- `DELETE /categories/{id}/` - Remove category

### Services
- `GET /services/` - List all hair services
- `POST /services/` - Create new service
- `GET /services/{id}/` - Get specific service
- `PUT /services/{id}/` - Update service
- `DELETE /services/{id}/` - Remove service

### Stylist Services
- `GET /stylist-services` - Get stylist-service relationships
- `POST /stylist-services` - Create stylist-service link
- `GET /service-stylist-options` - Get available stylists for services

## Project Structure

```
tressrelief-server/
├── manage.py                   # Django management script
├── Pipfile                     # Python dependencies
├── seed_database.sh           # Database setup script
├── db.sqlite3                 # SQLite database
├── tressreliefapi/            # Main API application
│   ├── models/                # Data models
│   │   ├── user_info.py       # User model with Firebase auth
│   │   ├── category.py        # Service category model
│   │   ├── service.py         # Hair service model
│   │   └── stylist_service.py # Stylist-service relationship
│   ├── serializers/           # API serializers
│   ├── views/                 # API views and endpoints
│   ├── fixtures/              # Sample data files
│   └── migrations/            # Database migrations
└── tressreliefproject/        # Django project settings
    ├── settings.py            # Project configuration
    └── urls.py               # URL routing
```

## Models

### UserInfo
- Firebase UID integration
- Role-based access (Client, Stylist, Admin)
- Google profile information
- Timestamps for creation and updates

### Category
- Service categorization (Braids, Feedins, etc.)
- Descriptions and image URLs
- Hierarchical organization

### Service
- Detailed service information
- Pricing and duration
- Category relationships
- Active/inactive status

### StylistService
- Links stylists to their offered services
- Many-to-many relationship management

## Authentication

The API uses Firebase Authentication for user management. Users are created or retrieved via the `/get-or-create-user` endpoint, which integrates with Firebase tokens.

Currently configured for development with `AllowAny` permissions. For production, uncomment the token authentication settings in `settings.py`.

## Dependencies

- **Django**: Web framework
- **Django REST Framework**: API development
- **django-cors-headers**: CORS handling
- **autopep8**: Code formatting
- **pylint & pylint-django**: Code linting



## Contact

**Author**: Alyssa Cleland  
**GitHub**: [@alyssacleland](https://github.com/alyssacleland)
