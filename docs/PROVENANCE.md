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
- Student(s): Liu Shuai
- Artifact: app/schemas/item.py, app/services/item_service.py, app/api/routes/item_router.py, tests/test_main.py
- Label: AI-ASSISTED
- AI tool: ChatGPT
- Purpose: Fix syntax errors and improve menu item availability handling.
- Influence: I wrote the main logic for handling item availability. I mainly used ChatGPT to double-check my syntax and figure out a weird indentation error I was stuck on. It also helped me brainstorm how to ensure the availability state stays consistent during updates.
- Validation: Ran the item tests and made sure unavailable items stay unavailable unless explicitly changed. The initial 18 tests passed, and the latest full test run passed all 50 tests.
- PR: #52

### Entry 11
- Student(s): Liu Shuai
- Artifact: web/m2.html
- Label: No-AI
- AI tool: NA
- Purpose: Implement a Quick Test Login feature to reduce repetitive manual input during frontend testing.
- Influence: I got tired of typing the test account details every time I refreshed the page, so I searched online for some JS snippets to auto-fill them and trigger the login. I also fixed some broken HTML comment syntax so my dev notes wouldn't show up on the page.
- Validation: Tested the shortcut locally and confirmed that the test account could successfully sign in through the existing authentication process.
- PR: #53

### Entry 12
- Student(s): Liu Shuai
- Artifact: app/services/commerce_service.py, app/api/routes/commerce_router.py, app/schemas/commerce.py, app/repositories/commerce_repository.py
- Label: AI-ASSISTED
- AI tool: ChatGPT
- Purpose: Integrate customer accounts, shopping carts, checkout, and order persistence for Milestone 2.
- Influence: I did the primary implementation for linking customer accounts, carts, and orders. I used ChatGPT mainly as a rubber duck鈥攈aving it review my integration logic and check for potential edge cases in the checkout flow. It helped me verify that my Pydantic schemas matched the frontend payloads.
- Validation: Did a full manual run-through from adding to cart, to checkout, and checking saved orders. Also confirmed data persisted after restarting the app. The latest full test run passed all 50 tests.
- PR: #50, #51, #52

### Entry 13
- Student(s): Liu Shuai
- Artifact: app/repositories/json_storage.py, app/repositories/restaurant_repository.py, app/repositories/item_repository.py, tests/test_json_storage.py, tests/test_commerce_repository.py
- Label: AI-ASSISTED
- AI tool: Gemini
- Purpose: Improve the reliability of JSON data persistence and reduce the risk of incomplete file writes.
- Influence: I implemented the shared JSON storage function. When I was figuring out how to prevent partial file writes, I asked Gemini to review my approach. It pointed me towards the idea of using temporary files and os.replace, which I then integrated and tested myself.
- Validation: Wrote tests simulating write failures to make sure original JSON files didn't get overwritten or damaged. I tested the JSON saving behavior, including what happens when a write fails.
- PR: #49, #52

### Entry 14
- Student(s): Liu Shuai
- Artifact: app/core/auth.py, app/api/routes/restaurant_router.py, app/api/routes/item_router.py, tests/test_m2_api_integration.py
- Label: AI-ASSISTED
- AI tool: Grok
- Purpose: Implement role-based access control and provide a local administrator initialization method.
- Influence: I worked on the RBAC logic for the restaurant and menu endpoints. I used Grok to check my FastAPI dependency injection syntax for the Bearer token, and asked it to review my role-based access control dependencies to see if there were any security loopholes. It helped me confirm my 401 vs 403 handling was correct.
- Validation: Tested the auth flow鈥攇ot 401 when no token was provided, and 403 when logged in as a normal customer. Verified that failed requests didn't mess up the JSON data. The latest full test run passed all 50 tests.
- PR: #52

### Entry 15
- Student(s): Liu Shuai
- Artifact: app/schemas/item.py, tests/test_main.py, tests/test_commerce_m2.py
- Label: AI-ASSISTED
- AI tool: Deepseek
- Purpose: Strengthen menu item price validation and checkout regression testing.
- Influence: I wrote the new price validations and regression tests. I used Deepseek to brainstorm edge cases I might have missed (like restaurant mismatches or missing addresses) and to check if my test assertions were actually rigorous enough to catch those failures.
- Validation: Ran targeted pytest files to ensure bad checkouts failed gracefully without creating orders or clearing the cart. The latest full test run passed all 50 tests.
- PR: #51, #52

### Entry 16
- Student(s): Liu Shuai
- Artifact: web/index.html, web/m2.html
- Label: AI-ASSISTED
- AI tool: Claude
- Purpose: Connect the restaurant browsing page to the M2 ordering interface and improve frontend authentication and checkout feedback.
- Influence: I wrote the frontend JS to link the pages and handle the UI feedback. I asked Claude to review my DOM manipulation code and check for any syntax errors. During my own testing, I caught a bug where old login data wasn't clearing, and Claude helped me verify the fix was robust.
- Validation: Checked for JS syntax errors using Node.js, then tested manually in the browser. Went through login failures, successful checkout, and page refreshes to make sure the UI updated correctly. The latest full test run passed all 50 tests.
- PR: #53
