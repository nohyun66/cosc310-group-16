# COSC 310 Group 16

> Team name: (TODO)

## Required Python version

Python `3.13.0`

## Setup instructions

Clone repo to location of your choice.

Run this once from the project root:

```powershell
python -m venv .venv
```

### Virtual-environment instructions

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
    (TODO)
## /docs path:
    http://127.0.0.1:8000/docs
## Location of representative data:
    (TODO)
## How to run tests:
    (TODO)
## Repository Structure

```text
app/          Source code
data/         Database
scrum/        SCRUM documentation
tests/        Tests
```
