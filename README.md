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
| `GET` | `/restaurants/{restaurant_id}/menu` | Get a restaurant menu |
| `GET` | `/restaurants/{restaurant_id}/menu/{item_id}` | Get one menu item |
| `POST` | `/customers/register` | Register a customer |
| `POST` | `/customers/login` | Log in and receive a bearer token |
| `GET` | `/customers/me` | Get the authenticated customer |
| `PATCH` | `/customers/me` | Update the customer profile |
| `DELETE` | `/customers/me` | Deactivate the customer account |
| `GET` | `/cart` | Get the current cart |
| `POST` | `/cart/items` | Add an item to the cart |
| `PUT` | `/cart/items/{item_id}` | Update an item quantity |
| `DELETE` | `/cart/items/{item_id}` | Remove an item from the cart |
| `DELETE` | `/cart` | Clear the cart |
| `POST` | `/checkout` | Create an order from the cart |
| `GET` | `/orders` | List the customer's orders |
| `GET` | `/orders/{order_id}` | Get one of the customer's orders |

Protected endpoints require a bearer token. To receive one, login with valid credentials 
and a token will be included in the response body.

## /docs path:
    http://127.0.0.1:8000/docs
## Location of representative data:

The representative data is stored in:

```text
data/restaurants.json
data/items.json
data/commerce.json
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
│   │       ├── cart_router.py
│   │       ├── customer_router.py
│   │       ├── item_router.py
│   │       ├── order_router.py
│   │       └── restaurant_router.py
│   ├── core/                    # Application configuration
│   │   ├── auth.py
│   │   └── config.py
│   ├── repositories/            # Data access layer
│   │   ├── commerce_repository.py
│   │   ├── item_repository.py
│   │   ├── json_storage.py
│   │   └── restaurant_repository.py
│   ├── schemas/                 # Pydantic models and enums
│   │   ├── authorization.py
│   │   ├── cart.py
│   │   ├── cuisine.py
│   │   ├── customer.py
│   │   ├── item.py
│   │   ├── item_category.py
│   │   ├── order.py
│   │   └── restaurant.py
│   ├── services/                # Application business logic
│   │   ├── auth_service.py
│   │   ├── cart_service.py
│   │   ├── commerce_services.py
│   │   ├── customer_service.py
│   │   ├── item_service.py
│   │   ├── order_service.py
│   │   ├── restaurant_service.py
│   │   └── util.py
│   └── main.py                  # FastAPI application entry point
├── .github/
│   └── workflows/
│       └── tests.yml             # Automated test workflow
├── data/                        # Representative JSON data
│   ├── commerce.json
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


## Milestone 2

For M2, we worked on connecting the different parts of our food ordering system so customers can actually go through the ordering process.

Users can create an account, log in, browse restaurants, add food to their cart, and place an order. They can also change item quantities, remove items, and check their previous orders.

We kept the cart limited to one restaurant at a time to make checkout easier to handle. The backend also checks things like item availability and whether a restaurant is open before creating an order.

### How to run it

Install the dependencies and start the server from the project folder:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Once the server is running, you can open:

- `http://127.0.0.1:8000/` for the restaurant page
- `http://127.0.0.1:8000/m2.html` for the ordering page
- `http://127.0.0.1:8000/docs` for the API endpoints

### Testing

To run the tests:

```powershell
python -m pytest -q
```
