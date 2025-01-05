# Car Rental Platform Backend

This is the backend for a car rental platform, developed using Django and Django REST Framework (DRF). It provides APIs
for managing users, cars, and reservations. Authentication is handled using JSON Web Tokens (JWT) with the Simple JWT
library.

---

## Features

- **User Management**:  
  Create, update, and manage user accounts.

- **Car Management**:  
  Add, update, and retrieve details of cars available for rent.

- **Reservation Management**:  
  Book cars for specific time slots, check availability, and manage reservations.

- **JWT Authentication**:  
  Secure authentication with token-based access using Simple JWT.

---

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/car-rental-backend.git
   cd car-rental-backend
    ```
2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
    ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
    ```
4. **Set up environment variables**:

   Create a `.env` file in the project root and configure your settings. Example:
   ```makefile
    SECRET_KEY=your_secret_key
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=ayour_db_password
    DB_HOST=your_host
    DB_PORT=your_port
    ```
5. **Run migrations**:
   ```bash
    python manage.py migrate
    ```
6. **Start the development server**:
   ```bash
    python manage.py runserver
    ```

## API Endpoints

### Authentication
- `POST /api/login/`: Obtain JWT tokens and user information.
- `POST /api/token/refresh/`: Refresh the access token.

### Users
- `GET /api/users/`: List all users (admin only).
- `POST /api/users/register_user`: Create a new user.
- `GET /api/users/<id>/`: Retrieve, update, or delete a user.

### Cars
- `GET /api/cars/`: List all cars.
- `POST /api/cars/`: Add a new car.
- `GET /api/cars/<id>/`: Retrieve, update, or delete a car.

### Reservations
- `GET /api/reservations/`:  List all reservations.
- `POST /api/reservations/`: Create a new reservation.
- `GET /api/reservations/<id>/`: Retrieve, update, or delete a reservation.

## Project Structure
```bash
    ├── drivolution/           # Project settings and configuration
    ├── users/                 # User-related features
    ├── cars/                  # Car-related features
    ├── reservations/          # Reservation-related features
    ├── car_images/            # Uploaded car images
    ├── manage.py              # Django's command-line utility
    └── .env                   # Environment variables
```
## Dependencies

- Python 3.x
- PostgreSQL (or your database of choice)
