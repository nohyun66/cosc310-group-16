# COSC 310 Group 16

> Team name: (TODO)

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
│   │       └── restaurant_router.py
│   ├── core/                    # Application configuration
│   ├── repositories/            # Data access layer
│   │   └── restaurant_repository.py
│   ├── schemas/                 # Pydantic models and enums
│   │   ├── cuisine.py
│   │   ├── item.py
│   │   └── restaurant.py
│   ├── services/                # Application business logic
│   │   └── restaurant_service.py
│   └── main.py                  # FastAPI application entry point
├── data/                        # Representative JSON data
│   ├── items.json
│   └── restaurants.json
├── scrum/                       # Team documentation
│   └── team-agreement.md
├── tests/                       # Automated tests
│   └── test_main.py
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Git ignore rules
```
