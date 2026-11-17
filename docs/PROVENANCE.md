You should record AI use when, for example:
- AI generates or substantially modifies code that you use or adapt.
- AI generates tests that you use or adapt.
- AI provides a design or architecture that your team adopts.
- AI helps you solve a bug and you use the resulting solution.
- AI substantially contributes to a diagram or documentation that you submit.
- AI provides a solution or partial solution that directly influences a project feature.

You normally do not need to record situations like:
- Asking for an explanation of a programming concept.
- Asking what an error message means.
- Asking for the meaning of a technical term.
- Using AI to learn a concept without using the resulting output in your project.
- Minor autocomplete suggestions that do not meaningfully affect your work.

| Label | Use when... |
|-------|-------------|
| AI-GENERATED | AI produced the content, or a substantial part of it, and you used or adapted that content in your final work. |
| AI-ASSISTED | AI helped you develop the work by providing ideas, explanations, alternatives, or guidance, but you created the final content yourself. |
| AI-REVISED | You created the original work yourself, and AI later substantially changed, refactored, or rewrote it. |
| NO-AI | You did not use generative AI to produce or influence the work described in the entry. |

### Template
- Student(s):
- Artifact:
- Label:
- AI tool:
- Purpose:
- Influence:
- Validation:
- PR:

### Entry 1
- Student(s): Tom
- Artifact: `app/schemas/item_category` and `/cuisine`
- Label: AI-ASSISTED
- AI tool: Copilot
- Purpose: Recommend a better way of storing static categories
- Influence: Adapted its suggestion of using StrEnum 
- PR: #2

### Entry 2
- Student(s): Tom
- Artifact: `app/repositories/restaurant_repository`
- Label: AI-GENERATED
- AI tool: Copilot
- Purpose: Resolve issues with creating a correct DATA_PATH
- Influence: Adapted the provided DATA_PATH
- PR: #2

### Entry 3
- Student(s): Tom
- Artifact: Every class that imported something from this project
- Label: AI-ASSISTED
- AI tool: Copilot
- Purpose: Resolve an error when trying to run the app after creating a new router
- Influence: Added "app.` in front of every import
- PR: #2

### Entry 4
- Student(s): Tom
- Artifact: data/restaurant.json and items.json
- Label: AI-GENERATED
- AI tool: Deepseek
- Purpose: Create a .json database given a list of food items (loosely based on a kaggle dataset) and required parameters, then another for the restaurants
- Influence: Adapted the generated files
- PR: #2

### Entry 5
- Student(s): Tom
- Artifact: README.md
- Label: AI-GENERATED
- AI tool: Copilot
- Purpose: Update the Repository Structure to match current state
- Influence: Adapted the generated markdown
- PR: #2

### Entry 6
- Student(s): Tom
- Artifact: web/index.html and restaurant.html
- Label: AI-GENERATED
- AI tool: Copilot
- Purpose: Create a basic frontend given a series of (self-made) mockup images using existing endpoints
- Influence: Used generated html files
- PR: #28

### Entry 7
- Student(s): Tom
- Artifact: tests/test_main.py
- Label: AI-GENERATED
- AI tool: Copilot
- Purpose: Create tests for the new frontend
- Influence: Used generated tests
- PR: #28

### Entry 8
- Student(s): Tom
- Artifact: tests/test_main.py
- Label: AI-GENERATED
- AI tool: Copilot
- Purpose: Create tests for item creation/updating 
- Influence: Used generated tests
- PR: #27

### Entry 9
- Student(s): Tom
- Artifact: README.md
- Label: AI-GENERATED
- AI tool: Copilot
- Purpose: Update the Repository Structure to match current state
- Influence: Adapted the generated markdown
- PR: #29

### Entry 10
- Student(s): Logan 
- Artifact: app/services/customer_service.py, tests/test_main.py
- Label: AI-GENERATED
- AI tool: ChatGPT
- Purpose: Customer registration and structure 
- Influence: Used and adapted generated registration code, password hashing & tests
- Validation: all the 21 Pytest cases passed 
- PR: #46

### Entry 11
- Student(s): Logan 
- Artifact: app/services/auth_service.py, app/core/security.py, tests/test_main.py
- Label: AI-GENERATED
- AI tool: ChatGPT
- Purpose: Implement the authentication and access restrictions for US-12
- Influence: Used and adapted generated authentication code & tests, reads locally set JWT secret key without storing in Git 
- Validation: checked using Pytest
- PR: #47

### Entry 12
- Student(s): [Your name]
- Artifact: README.md
- Label: AI-GENERATED
- AI tool: ChatGPT
- Purpose: Document authentication setup and usage
- Influence: Used and adapted instructions for the JWT secret key, sign-in, and local admin setup
- Validation: By comparing the instructions with the authentication implementation
- PR: #47




