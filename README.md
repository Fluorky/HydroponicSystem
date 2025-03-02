# HydroponicSystem

## Project Description
HydroponicSystem is a web-based application built with Django and Django REST Framework (DRF) that allows users to monitor and manage hydroponic systems. The application integrates sensor data collection, device control, and real-time analytics to optimize plant growth.

## Features
- **Hydroponic System Management** – Users can create and manage their hydroponic systems.
- **Sensor Data Collection** – The system records pH, temperature, and TDS (total dissolved solids) measurements.
- **User Authentication** – Secure user authentication using JWT (JSON Web Token).
- **REST API** – Provides a structured API for integration with external systems.

## Technologies Used
- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL (or SQLite for development)
- **Containerization**: Docker, Docker Compose
- **Authentication**: JWT authentication (SimpleJWT)

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- Poetry
- Docker and Docker Compose
- PostgreSQL (for production use)

### Environment Variables
Before running the application, create a `.env` file in the root directory and define the following:
```env
SECRET_KEY = your_secret_key
DEBUG= True/False (for production please use False)
DB_NAME = dbname
DB_USER = username
DB_PASSWORD = password
DB_HOST = address
DB_PORT = port
```

### Manual Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/user/HydroponicSystem.git
   cd HydroponicSystem
   ```
2. Install dependencies using Poetry:
   ```sh
   poetry install
   ```
3. Activate Poetry virtual environment:
   ```sh
   poetry shell
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Start the development server:
   ```sh
   python manage.py runserver
   ```

### Running with Docker
1. Build and start containers:
   ```sh
   docker-compose up --build
   ```
2. The application will be available at `http://host:8000` for example `http://localhost:8000` .

#### Docker Configuration Details
- **`Dockerfile`**: Configures the Django application environment.
- **`docker-compose.yml`**:
  - **`web` service**: Runs Django.
  - **`db` service**: PostgreSQL database container.
  - **`.env` file**: Stores environment variables.

To run in detached mode:
```sh
docker-compose up -d
```

To stop and remove containers:
```sh
docker-compose down
```

## Project Structure
```
HydroponicSystem/
│── HydroponicsSystem/       # Django project configuration
│   ├── __init__.py          # Package initializer
│   ├── settings.py          # Application settings
│   ├── urls.py              # Main URL routing
│   ├── asgi.py              # ASGI entry point
│   ├── wsgi.py              # WSGI entry point
│   ├── .env                 # Example environment variables file
│
│── api/                     # API module
│   ├── __init__.py          # Package initializer
│   ├── models.py            # Database models
│   ├── serializers.py       # API serializers
│   ├── views.py             # API views
│   ├── urls.py              # API routing
│   ├── admin.py             # Admin panel configurations
│   ├── apps.py              # Django app configuration
│   ├── migrations/          # Database migrations
│   ├── tests/               # Test cases
│
│── requirements.txt         # Dependencies list
│── manage.py                # Django management tool
│── Dockerfile               # Docker configuration
│── docker-compose.yml       # Docker Compose configuration
│── README.md                # Readme
│── CHANGELOG.md             # Changelog
│── .gitignore               # Gitignore

```

## API Endpoints
The API is powered by Django REST Framework. Below are the actual endpoints:

### Hydroponic System Management
- `GET /api/systems/` – Retrieve the list of hydroponic systems.
- `POST /api/systems/` – Create a new hydroponic system.
- `GET /api/systems/{id}/` – Retrieve details of a specific system.
- `PUT /api/systems/{id}/` – Update an existing hydroponic system.
- `DELETE /api/systems/{id}/` – Delete a hydroponic system.

### Sensor Data
- `GET /api/measurements/` – Retrieve all sensor measurements.
- `POST /api/measurements/` – Submit a new sensor measurement.
- `GET /api/measurements/{id}/` – Retrieve a specific sensor measurement.

### Authentication
- `POST /api/auth/register/` – Register a new user.
- `POST /api/auth/login/` – Obtain authentication token.
- `POST /api/auth/logout/` – Log out the user.
- `GET /api/auth/me/` – Retrieve authenticated user details.

API documentation can be accessed at `/swagger/` or `/redoc/` if configured.

## Testing
1. Run unit tests:
   ```sh
   python manage.py test
   ```
2. API testing can be done using Postman or `curl`.

## Authors
- **Fluorky(Maciej Bujalski)** – Lead Developer

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contact
For questions, reach out to [maciej.bujalski.dev@gmail.com](mailto:maciej.bujalski.dev@gmail.com).

