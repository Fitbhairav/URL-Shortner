# 🚀 High-Performance URL Shortener

A modern, high-throughput URL shortening service built with **FastAPI**, **Redis**, and **SQLite**. It features a premium glassmorphic UI, real-time click analytics, and efficient caching for lightning-fast redirections.

![URL Shortener Preview](https://img.shields.io/badge/Project-URL--Shortener-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-05998b?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

## ✨ Features

- **Blazing Fast**: Redirections are cached in Redis for sub-millisecond response times.
- **Modern UI**: Sleek, responsive, and interactive glassmorphic design.
- **Analytics**: Track total clicks and performance for every shortened URL.
- **Dockerized**: Easy setup and deployment using Docker and Docker Compose.
- **Robust API**: Well-documented endpoints for programmatic integration.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: SQLite (SQLAlchemy / aiosqlite)
- **Cache**: Redis
- **Frontend**: Vanilla HTML/CSS/JS (Glassmorphic Design)
- **Deployment**: Docker & Docker Compose

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/url-shortener.git
    cd url-shortener
    ```

2.  **Environment Setup:**
    Create a `.env` file from the example:
    ```bash
    cp .env.example .env
    ```

3.  **Run with Docker Compose:**
    ```bash
    docker compose up --build
    ```

The application will be available at:
- **Frontend/API**: [http://localhost:8000](http://localhost:8000)
- **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/shorten` | Create a shortened URL |
| `GET` | `/{short_code}` | Redirect to the original URL |
| `GET` | `/api/analytics/{short_code}` | Get usage statistics |

---

## 📂 Project Structure

```text
├── app/
│   ├── api/          # API Route definitions
│   ├── core/         # Configuration and security
│   ├── db/           # Database models and session management
│   ├── static/       # Frontend assets (HTML, CSS, JS)
│   └── main.py       # FastAPI application entry point
├── data/             # Persistent SQLite database storage
├── Dockerfile        # Container configuration
├── docker-compose.yml # Service orchestration
└── requirements.txt  # Python dependencies
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
