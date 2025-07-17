# 🧠 Cubot — Debate Chat API (LLM-powered)

Welcome to **Cubot**, a Django-based API for LLM-driven debate-style conversations. Built with Docker, using Ollama and a structured microservices approach.

---

## 🚀 Features

- Django REST API with structured conversation logic
- Integration with local Ollama LLM models (e.g., `phi3`)
- Fully containerized with Docker + Docker Compose
- Easily extensible `ChatEngine` and `DebateService` classes
- Includes Makefile commands for quick setup, test, and maintenance

---

## 📦 Requirements

- Docker
- Docker Compose plugin

---

## 🛠️ Installation

Run the following to install Docker and Docker Compose if not already present:

```bash
make install
```

⚠️ If the current user is not in the `docker` group, log out and back in, or run:

```bash
newgrp docker
```

---

## 🧪 Running the Project

### Start the API and dependencies

```bash
make run
```

Visit the API at:  
```
http://localhost:3031
```

---

## 🔌 API Usage

### Endpoint: `POST api/chat/`

```json
{
  "conversation_id": "optional-uuid",
  "message": "Your message to the bot"
}
```

- If `conversation_id` is omitted, a new conversation is created.
- The response includes the updated conversation and latest messages.

---

## 🧪 Running Tests

### Build and run the test suite:

```bash
make test
```

### Build only (useful for caching Docker layers):

```bash
make test-build
```

### Clean up test containers and volumes:

```bash
make test-clean
```

---

## ⚙️ Environment Variables

Configure your `.env` file at the root of the project:

```ini
SECRET_KEY=...
DEBUG=True

# Database
DB_HOST=localhost
DB_USER=postgres
DB_NAME=cubot_db
DB_PORT=5434
DB_PASSWORD=postgres

# Django
DJANGO_SETTINGS_MODULE=cubot.settings
ALLOWED_HOST=localhost

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3
```

---

## 📁 Project Structure

```
.
├── apps/
│   ├── chat/
│   │   ├── models.py
│   │   ├── services/
│   │   │   └── debate.py
│   │   └── engines/
│   │       ├── base.py
│   │       └── ollama_engine.py
├── cubot/
│   └── settings.py
├── Dockerfile
├── docker-compose.yml
├── docker-compose.test.yml
├── entrypoint.sh
├── Makefile
└── README.md
```

---

## 🤖 Powered By

- [Django](https://www.djangoproject.com/)
- [Ollama](https://ollama.com/)
- [Docker](https://www.docker.com/)
- [pytest + pytest-django](https://pytest-django.readthedocs.io/)

---

## 🧠 Tips

- Use the `DebateService` and `ChatEngine` abstractions to plug in new LLMs or fine-tune logic.
- Run `make` to list all available commands.

---

