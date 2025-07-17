# Social Network Engagement Bot

A Django-based RESTful API for tracking social media engagement, follower growth, and milestone alerts. It supports periodic follower checks, Telegram notifications, and follower insights.

## Features

- Register and monitor social media profiles (e.g., Twitter, Instagram)
- Set alerts for follower milestones
- Periodically check follower counts using Celery + Celery Beat
- Notify users via Telegram when milestones are hit
- Track top follower gains/losses in the past 24 hours
- Basic authentication via Django's built-in user model
- Swagger/OpenAPI API documentation

## Requirements

- Python 3.11+
- PostgreSQL
- Redis (for Celery)
- Docker + Docker Compose (optional)

## Setup Instructions

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/HoomanRadmehr/social-bot.git
cd social-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=social_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### 3. Run migrations and start the project

```bash
make run
```

This will:
- Run migrations
- Start Celery worker
- Start Celery beat
- Launch the Django dev server

### 4. API Documentation

Visit [http://localhost:8000/swagger/](http://localhost:8000/swagger/) for interactive Swagger docs.

## Docker Usage

Use Docker Compose to spin up the project:

```bash
docker-compose up --build
```

## Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/engagement/profiles/` | GET/POST | List or create social profiles |
| `/engagement/alerts/` | GET/POST | Set milestone alerts |
| `/engagement/insights/top-follower-changes/` | GET | Top gains/losses in last 24 hours |
| `/swagger/` | GET | Swagger UI |

## License

MIT License
