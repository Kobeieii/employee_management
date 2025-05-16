# Django Employee Management

## ✨ Getting Started

### 1. Setup Environment Variables

Copy the example environment file and update the values as needed:

```bash
cp .env_example .env
```

### 2. Start the Database with Docker Compose

Make sure Docker is running, then start the database container:

```bash
docker compose up -d
```

### 3. Run Database Migrations

After the database is running, apply migrations:

```bash
python manage.py migrate
```

### 4. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to access the application.

---

## 🔮 API Testing with Postman

A Postman collection is provided to help you test the available APIs.

### Import the Collection

1. Open [Postman](https://www.postman.com/).
2. Click **Import** and select the file: `postman_collection.json`.

This collection includes all available endpoints for user registration, login, employee management, etc.

Make sure to update the environment variables in Postman (e.g., `{{base_url}}`) to match your local server (`http://localhost:8000`).
