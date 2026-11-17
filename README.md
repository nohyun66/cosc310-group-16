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

In the root directory:

```powershell
uvicorn app.main:app --reload 
```
Open `http://127.0.0.1:8000/` in your browser to access the application.

Press `Ctrl+C` to exit the application.

## API endpoint paths:
| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Check whether the API is running |
| `GET` | `/restaurants` | Get all restaurants |
| `GET` | `/restaurants/{restaurant_id}` | Get one restaurant by ID |

## /docs path:
    http://127.0.0.1:8000/docs
## Location of representative data:

The representative data is stored in:

```text
restaurants.json
items.json
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
│   │       ├── item_router.py
│   │       └── restaurant_router.py
│   ├── core/                    # Application configuration
│   │   └── config.py
│   ├── repositories/            # Data access layer
│   │   ├── item_repository.py
│   │   └── restaurant_repository.py
│   ├── schemas/                 # Pydantic models and enums
│   │   ├── cuisine.py
│   │   ├── item.py
│   │   ├── item_category.py
│   │   └── restaurant.py
│   ├── services/                # Application business logic
│   │   ├── item_service.py
│   │   └── restaurant_service.py
│   └── main.py                  # FastAPI application entry point
├── .github/
│   └── workflows/
│       └── tests.yml             # Automated test workflow
├── data/                        # Representative JSON data
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
