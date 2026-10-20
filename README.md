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
Open `http://127.0.0.1:8000/` in your browser to access the application.

Press `Ctrl+C` to exit the application.

## API endpoint paths:
| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Check whether the API is running |
| `GET` | `/restaurants` | Get all restaurants |
| `GET` | `/restaurants/{restaurant_id}` | Get one restaurant by ID |

### Search restaurants

Search by part of a restaurant name. Capitalization does not matter.

Example:
http://127.0.0.1:8000/restaurants?search=pizza

Without search text, all restaurants are returned.
If no names match, an empty list is returned.

### Filter restaurants by cuisine

Example:
http://127.0.0.1:8000/restaurants?cuisine=ASIAN

Supported values: NORAM, ASIAN, MED, LATAM, EURO.

Without a cuisine filter, all restaurants are returned.
If no restaurants match, an empty list is returned.
Unsupported cuisine values return a 422 validation error.



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

Restaurant tests use temporary copies or temporary test records so that
the representative data is not changed.

### Continuous integration

GitHub Actions installs the project dependencies and runs pytest
automatically on pushes and pull requests.

View the results in the repository's Actions tab.

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── tests.yml             # GitHub Actions test workflow
├── app/                         # FastAPI application
│   ├── api/
│   │   └── routes/
│   │       └── restaurant_router.py
│   ├── core/                    # Application configuration
│   ├── repositories/            # Data access layer
│   │   └── restaurant_repository.py
│   ├── schemas/                 # Pydantic models and enums
│   │   ├── cuisine.py
│   │   ├── item_category.py
│   │   ├── item.py
│   │   └── restaurant.py
│   ├── services/                # Application business logic
│   │   └── restaurant_service.py
│   └── main.py                  # FastAPI application entry point
├── data/                        # Representative JSON data
│   ├── items.json
│   └── restaurants.json
├── docs/                        # Project documentation
├── scrum/                       # Team documentation
│   └── team-agreement.md
├── tests/                       # Automated tests
│   ├── test_main.py
│   ├── test_restaurant_search.py
│   └── test_restaurant_filter.py
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Git ignore rules
```
