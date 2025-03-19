# Day- 2 Server Basics

The syllabus and the asserssment for the session is in this [docs](https://docs.google.com/document/d/1hAE8tr56tLtnMrA4ttCCNuSPG5nQQA_6Gr0vt2Fk_6w/edit?tab=t.0)

---

## Session Overview

- Django project and app setup
- Model, serializer, and viewset for a basic user API
- CRUD operations with Django REST Framework
- Common edge cases and troubleshooting

---

## Assessment Overview

The assessment focuses on deepening our understanding of Django ORM through various practical tasks in the Django ORM Shell. The tasks include:

1. **Creation:** Learn how to use bulk_create(), get_or_create(), and update_or_create() to manage user data.
2. **Basic Retrieval:** Retrieve users with different conditions using methods like get(), filter(), and exists().
3. **Filtering & Lookups:** Use Django's filtering capabilities with conditions like startswith, icontains, and exclude().
4. **Ordering & Aggregation:** Learn how to sort, slice, and aggregate data, as well as annotate each user with computed fields.
5. **Updates & Deletions:** Update records using update() and bulk_update(), and delete records efficiently.
6. **Transactions & Error Handling:** Practice handling errors within database transactions.
7. **Query Inspection:** Understand how to inspect and optimize queries for performance.

---

## Assessment Directory Structure

I have created the assessment folder `Day3-Django` inside the root `Internship-Assessment-2025` Folder. The django project is created inside the `Day3-Django` folder. The Django root project directory is `Project`.

The `Day3-Django` Directory looks like this:

```
Day2Servers
│   .env
|   poetry.lock
|   pyproject.toml
│   README.md (This file)
|   db.sqlite3
│   manage.py
|   .gitignore
│
└───env
|   │   ...
|
└───Screenshots
|   │   ...
|
|
└───Project
|   |
|   └───__pycache__
|   |   |   ....
|   |
|   |   __init__.py
|   │   asgi.py
|   │   seetings.py
|   │   urls.py
|   │   wsgi.py
|
└───User
    |
    └───__pycache__
    |   |   ....
    │
    └───migrations
    |   |
    |   └───migration files
    |
    │   __init__.py
    │   admin.py
    │   apps.py
    │   models.py
    │   tests.py
    |   views.py
    |   serializers.py
    |   urls.py
    |   user_service.py
```

---

## Project Setup

1. **Clone the repo:** Use ssh to clone the repo

   ```bash
   git clone git@github.com:RanjanRamailoTech/Internship-Assessment-2025.git
   ```

2. **Set Up Virtual Environment:** Notice the root directory contains the assessment folder.
   use `cd Day3-Django` to enter the assessment folder. Then activate the virtual environment as:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Poetry:**

   ```bash
   pip install poetry
   ```

4. **Install dependencies:**

   ```bash
   poetry install
   ```

5. **Configure Environment Variables:**
   Create a `.env` file in the project root. Use `touch .env` to create a `.env` file and then `nano .env` to enter write the content. Write following content as they are required to setup the postgres database.

   ```
   DB_NAME=Your_DB_Name
   DB_USER=Your_DB_User
   DB_PASSWORD=Your_DB_Password
   DB_HOST=Your_DB_Host
   DB_PORT=Your_DB_Port
   ...(any other env variables)
   ```

6. **Initialize the database:**

   ```bash
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate
   ```

7. **Start the Development Server:**

   ```bash
   poetry run python manage.py runserver
   ```

   The backend server will be running at `127.0.0.1:8000`.

---

## Assessments

### 1️⃣ Creation

1. **Create 10 Users via bulk_create.**
   For Bulk user creation I used gpt to create dummy data.

```bash
users = [
    User(first_name="Alice", last_name="Smith", email="alice.smith@example.com"),
    User(first_name="Bob", last_name="Johnson", email="bob.johnson@example.com"),
    User(first_name="Charlie", last_name="Brown", email="charlie.brown@example.com"),
    User(first_name="David", last_name="Williams", email="david.williams@example.com"),
    User(first_name="Eva", last_name="Taylor", email="eva.taylor@example.com"),
    User(first_name="Frank", last_name="Davis", email="frank.davis@example.com"),
    User(first_name="Grace", last_name="Miller", email="grace.miller@example.com"),
    User(first_name="Henry", last_name="Wilson", email="henry.wilson@example.com"),
    User(first_name="Ivy", last_name="Moore", email="ivy.moore@example.com"),
    User(first_name="Jack", last_name="Taylor", email="jack.taylor@example.com")
]

User.objects.bulk_create(users)

```

![alt text]("")

2. Create user with create

```bash
user = User.objects.create(first_name="Ranjan", last_name="Lamsal", email="Ranjan@ramailo.tech")
```

3. Use get_or_create() for a user with email "unique@test.com".

```bash
user = User.objects.get_or_create(email="unique@test.com", defaults={"first_name": "Unique", "last_name": "User"})

```

4. Use update_or_create() to change first_name for "unique@test.com".

```bash
user = User.objects.update_or_create(email="unique@test.com", defaults={"first_name": "UpdatedUnique", "last_name": "User"})

```
