# COSC 310 Group 16

> Team name: Todos

## Required Python version

Python `3.13.0`

## Setup instructions

Clone repo to location of your choice.

Create your Virtual Environement.
From project root:

```powershell
python -m venv .venv
```

### Virtual-environment instructions

Always keep your VE active unless you need it to be deactivated for whatever reason.

Activate your virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Deactivate your virtual environment:

```powershell
deactivate
```

### Dependency installation

With your VE active:

```powershell
pip install -r requirements.txt
```

When adding a dependency, make sure to update the `requirements.txt` before pushing:

```powershell
pip freeze > requirements.txt
```

## Running the Application

In the root directory, set a JWT signing key and start the app from the same terminal:

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/ in your browser to access the application.

Press `Ctrl+C` to exit the application.

## Authentication

The key stays available for that terminal session. Changing it invalidates
previously issued tokens. Do not commit the actual key to Git.

### Sign in through /docs

1. Register using `POST /customers`.
2. Submit your email and password to `POST /auth/login`.
3. Copy the returned `access_token`.
4. Click **Authorize** in `/docs`, paste the token, and click **Authorize**.
5. Use `GET /auth/me` to check the signed-in account.

Tokens expire after 30 minutes. Restaurant and menu browsing are public.
Creating or updating restaurants and menu items requires an active admin account.

### Local demo administrator

Public registration always creates a customer account.
To provision an administrator locally:

1. Register the intended account.
2. Stop the application.
3. Find that account by email in `data/customers.json`.
4. Change only its `"role"` from `"customer"` to `"admin"`.
5. Restart the application and sign in.

This is a manual setup step requiring access to the server's data file.
Do not commit personal demo account data.

## API endpoint paths:

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Check whether the API is running |
| `GET` | `/restaurants` | Get all restaurants |
| `GET` | `/restaurants/{restaurant_id}` | Get one restaurant by ID |
| `POST` | `/customers` | Register a customer |
| `POST` | `/auth/login` | Sign in and receive a token |
| `GET` | `/auth/me` | Get the signed-in customer |

## /docs path:

http://127.0.0.1:8000/docs

## Location of representative data:

The representative data is stored in:

```text
data/restaurants.json
data/items.json
data/customers.json
```

## How to run tests:

```powershell
python -m pytest -v
```

## Repository Structure

```text
.
├── app/                         # FastAPI application
│   ├── api/                     # API routes
│   │   └── routes/
│   │       ├── auth_router.py
│   │       ├── customer_router.py
│   │       ├── item_router.py
│   │       └── restaurant_router.py
│   ├── core/                    # Application configuration
│   │   ├── config.py
│   │   └── security.py
│   ├── repositories/            # Data access layer
│   │   ├── customer_repository.py
│   │   ├── item_repository.py
│   │   └── restaurant_repository.py
│   ├── schemas/                 # Pydantic models and enums
│   │   ├── auth.py
│   │   ├── cuisine.py
│   │   ├── customer.py
│   │   ├── item.py
│   │   ├── item_category.py
│   │   └── restaurant.py
│   ├── services/                # Application business logic
│   │   ├── auth_service.py
│   │   ├── customer_service.py
│   │   ├── item_service.py
│   │   └── restaurant_service.py
│   └── main.py                  # FastAPI application entry point
├── .github/
│   └── workflows/
│       └── tests.yml             # Automated test workflow
├── data/                        # Representative JSON data
│   ├── customers.json
│   ├── items.json
│   └── restaurants.json
├── docs/                        # Project documentation
│   └── PROVENANCE.md
├── scrum/                       # Team documentation
│   └── team-agreement.md
├── tests/                       # Automated tests
│   └── test_main.py
├── web/                         # Basic frontend
│   ├── index.html                # Restaurant search and listing
│   └── restaurant.html           # Restaurant details and menu
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Git ignore rules
```