# TressRelief Server

A comprehensive Django REST API server for a hair styling service platform that connects clients with professional stylists. This server provides complete service catalog management, sophisticated stylist-service relationship handling, role-based user management, and real-time appointment availability checking with Google Calendar integration. Full appointment booking functionality is planned for future development.

## Related Repositories

- **Client Application**: [tressrelief-client](https://github.com/alyssacleland/tressrelief-client) - React with Next.js frontend for the TressRelief platform

## Features

### Core Platform Features
- **User Management**: Firebase authentication integration with role-based access (Client, Stylist, Admin) and user filtering
- **Service Catalog**: Complete CRUD operations for hair services with descriptions, pricing, duration, and category organization
- **Service Categories**: Organized service categorization system (Braids, Feedins, etc.)
- **Relationship Management**: Sophisticated many-to-many stylist-service linking with diff algorithms
- **Multi-Stylist Assignment**: Add/remove multiple stylists to services with conflict prevention
- **Intelligent Filtering**: Query services by category or stylist using join table relationships

### Advanced Appointment System
- **Google Calendar Integration**: Stylists can connect their Google Calendar for seamless availability management
- **Real-time Availability**: Dynamic appointment slot generation based on stylist calendar availability
- **OAuth 2.0 Authentication**: Secure Google OAuth flow for stylist calendar access
- **Intelligent Slot Generation**: Converts Google Calendar busy times into bookable appointment slots
- **Timezone Management**: Handles UTC/Central Time conversion for accurate scheduling
- **Working Hours Enforcement**: Restricts available slots to business hours (9 AM - 5 PM CST)

### Technical Features
- **RESTful API**: Clean, consistent API endpoints for all resources
- **Database Fixtures**: Pre-seeded data for categories, services, and user information
- **Token Management**: Automatic OAuth token refresh for uninterrupted Google Calendar access
- **FreeBusy Integration**: Leverages Google Calendar FreeBusy API for conflict-free scheduling

## Technology Stack

- **Framework**: Django with Django REST Framework
- **Database**: SQLite (development)
- **Authentication**: Firebase Authentication + Google OAuth 2.0
- **External APIs**: Google Calendar API, Google FreeBusy API
- **Language**: Python 3.9
- **Package Management**: Pipenv
- **Key Libraries**: 
  - `google-auth` - Google authentication
  - `google-auth-oauthlib` - OAuth 2.0 flow handling
  - `google-api-python-client` - Google Calendar API integration
  - `pytz` - Timezone handling

## Quick Start

### Prerequisites

- Python 3.9+
- Pipenv
- **Google Cloud Project** (required for Google Calendar integration features)
  - Enable Google Calendar API
  - Create OAuth 2.0 credentials (Client ID and Client Secret)
  - Configure authorized redirect URIs

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

6. **Configure environment variables** (for Google Calendar features)
   Create a `.env` file in the project root:
   ```bash
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/google/callback/
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The server will be available at `http://localhost:8000`

## API Endpoints

### Authentication & User Management
- `POST /get-or-create-user` - Create or retrieve user based on Firebase auth
- `GET /userinfo/` - List all users
  - **Query Params**: `role` (filter by client/stylist/admin)
- `GET /userinfo/{id}/` - Get specific user

### Google OAuth Integration
- `GET /oauth/google/initiate` - Initiate Google OAuth flow for stylist calendar access
  - **Headers**: `Authorization: <stylist_uid>`
  - **Returns**: JSON with Google consent URL
  - **Scopes**: Calendar events and read-only access
  
- `GET /oauth/google/callback/` - Handle Google OAuth callback
  - **Query Params**: `code`, `state` (from Google)
  - **Function**: Exchanges authorization code for access/refresh tokens
  - **Storage**: Saves tokens to OAuthCredential model
  
- `GET /oauth/google/status` - Check stylist's Google Calendar connection status
  - **Headers**: `Authorization: <stylist_uid>`
  - **Returns**: Connection status, calendar ID, and last update timestamp

### OAuth Credential Management
- `GET /oauth-credentials/` - List all OAuth credentials (admin)
- `POST /oauth-credentials/` - Create OAuth credential
- `GET /oauth-credentials/{id}/` - Get specific credential
- `PUT /oauth-credentials/{id}/` - Update credential
- `DELETE /oauth-credentials/{id}/` - Remove credential

### Availability & Scheduling
- `GET /services/{id}/availability/` - Get available appointment slots for a service
  - **Query Params**: 
    - `date` (required): Date in YYYY-MM-DD format
    - `stylist_id` (optional): Filter to specific stylist
  - **Returns**: Array of stylists with their available time slots
  - **Features**:
    - Integrates with Google Calendar FreeBusy API
    - Respects stylist working hours (9 AM - 5 PM CST)
    - Generates slots based on service duration
    - 15-minute slot granularity
    - UTC time format for consistency

### Service Management
- `GET /categories/` - List all service categories
- `GET /categories/{id}/` - Get specific category

- `GET /services/` - List all hair services
  - **Query Params**: `categoryId`, `stylistId` (filters via join table)
- `POST /services/` - Create new service (accepts `stylist_ids` array to link stylists)
- `GET /services/{id}/` - Get specific service
- `PUT /services/{id}/` - Update service (manages stylist relationships via diff algorithm)
- `DELETE /services/{id}/` - Delete service
- `GET /services/{id}/stylists/` - Get stylists who offer this service
- `POST /services/{id}/add_stylist/` - Add stylist to service
- `DELETE /services/{id}/remove_stylist/?stylistId={id}` - Remove stylist from service

### Stylist-Service Relationships
- `GET /stylist-services?serviceId={id}` - Get stylist IDs linked to a service
- `GET /service-stylist-options?serviceId={id}` - Get all stylists with join status
  - **Returns**: All stylists with boolean `joined` field indicating if they offer the service

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
- Unique constraints to prevent duplicates

### OAuthCredential
- Stores Google OAuth tokens for stylist calendar integration
- Foreign key to UserInfo (stylist)
- OAuth provider identification ('google')
- Refresh and access token storage
- Automatic token refresh when expired

## Google Calendar Integration

### OAuth 2.0 Flow
1. **Initiation**: Stylist requests calendar connection via `/oauth/google/initiate`
2. **Consent**: User redirected to Google for permission approval
3. **Callback**: Google redirects back with authorization code
4. **Token Exchange**: Server exchanges code for access/refresh tokens
5. **Storage**: Tokens stored securely in OAuthCredential model

### Availability Algorithm
The system uses a sophisticated algorithm to convert Google Calendar data into bookable appointment slots:

1. **FreeBusy Query**: Retrieves busy intervals from stylist's Google Calendar
2. **Interval Normalization**: Merges overlapping busy times
3. **Working Hours**: Enforces 9 AM - 5 PM CST business hours
4. **Free Time Calculation**: Subtracts busy intervals from working hours
5. **Slot Generation**: Divides free time into service-duration chunks
6. **Granularity**: Aligns slots to 15-minute increments
7. **UTC Conversion**: Returns times in UTC for frontend timezone handling

### Token Management
- **Automatic Refresh**: Expired access tokens refreshed using stored refresh tokens
- **Error Handling**: Graceful fallback when OAuth credentials are missing
- **Security**: Tokens stored securely with appropriate field constraints

## Authentication

The API uses a dual authentication system:

### Firebase Authentication
- **Primary**: User management via Firebase tokens
- **Usage**: Client/admin authentication and user creation
- **Endpoint**: `/get-or-create-user` integrates with Firebase tokens

### Google OAuth 2.0
- **Purpose**: Stylist calendar integration for appointment scheduling
- **Scopes**: 
  - `calendar.events` - Create/update/delete calendar events
  - `calendar.readonly` - Read calendar availability
- **Flow**: Standard OAuth 2.0 authorization code flow
- **Security**: `access_type=offline` and `prompt=consent` for refresh token acquisition

## Dependencies

### Core Framework
- **Django**: Web framework
- **Django REST Framework**: API development
- **django-cors-headers**: CORS handling

### Google Integration
- **google-auth**: Google authentication library
- **google-auth-oauthlib**: OAuth 2.0 flow handling
- **google-api-python-client**: Google Calendar API client

### Utilities
- **pytz**: Timezone handling for appointment scheduling
- **python-dotenv**: Environment variable management
- **autopep8**: Code formatting
- **pylint & pylint-django**: Code linting



## Contact

**Author**: Alyssa Cleland  
**GitHub**: [@alyssacleland](https://github.com/alyssacleland)
