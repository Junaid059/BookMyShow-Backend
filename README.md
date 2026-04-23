# BookMyShow - Movie Booking Platform Backend

A production-ready movie ticket booking API built with **FastAPI**, **PostgreSQL**, and **JWT authentication**. Features role-based access control, theatre & show management, seat booking, reviews, and payment processing.

---

## Architecture Overview

![BookMyShow Architecture](bookMyShow.drawio.png)

---

## Key Features

| Feature | Description |
|---|---|
| **JWT Authentication** | Access + Refresh tokens with token blacklisting on logout |
| **Role-Based Access Control** | Three roles: `admin`, `organizer`, `user` with granular permissions |
| **Movie Management** | Full CRUD with genre, rating, duration, and release date |
| **Theatre & City Management** | Multi-location support with screen management |
| **Show Scheduling** | Link movies to theatres with show times, pricing, and screen numbers |
| **Seat Management** | Per-screen seat tracking with availability status |
| **Booking System** | Seat-level booking with status tracking (pending/confirmed) |
| **Reviews & Ratings** | 1–5 star ratings with comments per movie |
| **Payment Processing** | Schema-ready payment system (credit card, bank transfer, EasyPaisa, JazzCash) |
| **Notifications** | User notification model with read/unread tracking |

---

## Tech Stack

| Component | Technology |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn |
| Database | PostgreSQL |
| ORM | SQLAlchemy + asyncpg |
| Authentication | JWT (python-jose) + HTTPBearer |
| Password Hashing | bcrypt (passlib) |
| Validation | Pydantic |
| Caching | Redis / aioredis |
| Logging | Loguru |
| Email | aiosmtplib |

---

## Project Structure

```
BookMyShow-Backend/
├── requirements.txt
└── app/
    ├── main.py              # FastAPI app entry point & router registration
    ├── auth.py              # JWT token creation, verification & blacklisting
    ├── db.py                # PostgreSQL connection & session factory
    ├── Registration.py      # Auth routes (register, login, logout)
    ├── utils.py             # Password hashing utilities
    ├── models/
    │   └── models.py        # SQLAlchemy ORM models (10 tables)
    ├── routers/
    │   ├── users.py         # User CRUD
    │   ├── movies.py        # Movie CRUD
    │   ├── shows.py         # Show scheduling
    │   ├── bookings.py      # Booking management
    │   ├── reviews.py       # Ratings & reviews
    │   ├── cities.py        # City management
    │   ├── seats.py         # Seat management
    │   ├── threaters.py     # Theatre CRUD
    │   └── payments.py      # Payment endpoints (WIP)
    └── schemas/
        ├── userSchema.py
        ├── movieSchema.py
        ├── showSchema.py
        ├── BookingSchema.py
        ├── ReviewSchema.py
        ├── citySchema.py
        ├── seatSchema.py
        ├── TheatreSchema.py
        ├── paymentSchema.py
        └── notificationSchema.py
```

---

## Database Schema

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    USERS     │       │   MOVIES     │       │   CITIES     │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)      │       │ id (PK)      │
│ name         │       │ title        │       │ name         │
│ email (UQ)   │       │ description  │       │ state        │
│ password     │       │ duration     │       └──────┬───────┘
│ role         │       │ release_date │              │
│ created_at   │       │ genre        │              │
└──┬───┬───┬───┘       │ rating       │       ┌──────▼───────┐
   │   │   │           └──────┬───────┘       │  THEATRES    │
   │   │   │                  │               ├──────────────┤
   │   │   │           ┌──────▼───────┐       │ id (PK)      │
   │   │   │           │   REVIEWS    │       │ name         │
   │   │   │           ├──────────────┤       │ location     │
   │   │   └──────────►│ user_id (FK) │       │ city_id (FK) │
   │   │               │ movie_id(FK) │       │ total_screens│
   │   │               │ rating       │       └──┬───────┬───┘
   │   │               │ comment      │          │       │
   │   │               └──────────────┘          │       │
   │   │                                         │       │
   │   │               ┌──────────────┐          │  ┌────▼───────┐
   │   │               │    SHOWS     │◄─────────┘  │   SEATS    │
   │   │               ├──────────────┤             ├────────────┤
   │   │               │ id (PK)      │             │ id (PK)    │
   │   │               │ show_time    │             │ seat_number│
   │   │               │ price        │             │ screen_no  │
   │   │               │ screen_no    │             │ is_available│
   │   │               │ movie_id(FK) │             │ theatre_id │
   │   │               │ theatre_id   │             └────────────┘
   │   │               └──────┬───────┘
   │   │                      │
   │   │               ┌──────▼───────┐       ┌──────────────┐
   │   └──────────────►│  BOOKINGS   │──────►│  PAYMENTS    │
   │                   ├──────────────┤       ├──────────────┤
   │                   │ id (PK)      │       │ id (PK)      │
   │                   │ booking_date │       │ amount       │
   │                   │ total_amount │       │ payment_date │
   │                   │ status       │       │ method       │
   │                   │ seat_numbers │       │ status       │
   │                   │ user_id (FK) │       │ booking_id   │
   │                   │ show_id (FK) │       └──────────────┘
   │                   └──────────────┘
   │
   │                   ┌──────────────┐
   └──────────────────►│NOTIFICATIONS │
                       ├──────────────┤
                       │ id (PK)      │
                       │ message      │
                       │ is_read      │
                       │ created_at   │
                       │ user_id (FK) │
                       └──────────────┘
```

---

## API Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | Public |
| POST | `/auth/login` | Login & get JWT tokens | Public |
| POST | `/auth/logout` | Blacklist token & logout | Authenticated |

### Users

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createUser` | Create a user | Admin |
| GET | `/getUsers` | List all users | Admin |
| GET | `/getUser/{user_id}` | Get user by ID | Admin / Self |
| PUT | `/updateUser/{user_id}` | Update user | Authenticated |
| DELETE | `/deleteUser/{user_id}` | Delete user | Authenticated |

### Movies

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createMovie` | Add a movie | Admin / Organizer |
| GET | `/getMovies` | List all movies | Public |
| GET | `/getMovie/{movie_id}` | Get movie details | Public |
| PUT | `/updateMovie/{movie_id}` | Update movie | Admin / Organizer |
| DELETE | `/deleteMovie/{movie_id}` | Delete movie | Admin / Organizer |

### Shows

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createShows` | Create a show | Admin / Organizer |
| GET | `/getShows` | List all shows | Public |
| GET | `/getShowbyId/{show_id}` | Get show details | Public |
| PUT | `/updateShow/{show_id}` | Update show | Admin / Organizer |
| DELETE | `/deleteShow/{show_id}` | Delete show | Admin / Organizer |

### Bookings

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createBooking` | Create a booking | Authenticated |
| GET | `/getBookings` | List bookings | Admin/Organizer: all, User: own |
| GET | `/getBookingbyId/{id}` | Get booking details | Authenticated |
| PUT | `/updateBooking/{id}` | Update booking | Permission-based |
| DELETE | `/deleteBooking/{id}` | Delete booking | Permission-based |

### Reviews

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createReview` | Add a movie review | Authenticated |
| GET | `/getReviews/{movie_id}` | Get reviews for a movie | Public |
| PUT | `/updateReview/{id}` | Update review | Owner / Admin |
| DELETE | `/deleteReview/{id}` | Delete review | Owner / Admin |

### Theatres

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createThreater` | Add a theatre | Admin / Organizer |
| GET | `/getallThreater` | List all theatres | Public |
| GET | `/getThreater/{id}` | Get theatre details | Public |
| PUT | `/updateThreater/{id}` | Update theatre | Admin / Organizer |
| DELETE | `/deleteThreater/{id}` | Delete theatre | Admin / Organizer |

### Cities

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createCity` | Add a city | Admin / Organizer |
| GET | `/getCities` | List all cities | Public |
| GET | `/getCitybyId/{id}` | Get city details | Public |
| PUT | `/updateCity/{id}` | Update city | Admin / Organizer |
| DELETE | `/deleteCity/{id}` | Delete city | Admin / Organizer |

### Seats

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/createSeat` | Add a seat | Admin / Organizer |
| GET | `/getallSeats` | List all seats | Public |
| GET | `/getSeat/{id}` | Get seat details | Public |
| PUT | `/updateSeat/{id}` | Update seat availability | Admin / Organizer |
| DELETE | `/deleteSeat/{id}` | Delete seat | Admin / Organizer |

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (optional, for caching)

### Installation

```bash
# Clone the repository
git clone https://github.com/Junaid059/BookMyShow-Backend.git
cd BookMyShow-Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
DB_URL=postgresql+asyncpg://user:password@localhost:5432/bookmyshow
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

---

## Security Features

- **JWT Tokens** — Stateless authentication with access (30 min) & refresh (7 day) tokens
- **Token Blacklisting** — Revoke tokens on logout
- **Password Policy** — Enforces uppercase, lowercase, digit, and special character
- **Email Validation** — Domain whitelist enforcement
- **Role-Based Access** — Granular route-level permission checks
- **SQLAlchemy ORM** — Parameterized queries prevent SQL injection

---

## License

This project is open source and available under the [MIT License](LICENSE).
