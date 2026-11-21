Item 1
Menu Item Availability and State Preservation 
Feature Integration

Problem:
The original menu-item model did not support an availability field. This prevented the application from reliably distinguishing between available and unavailable menu items.
During integration, I found another potential issue: updating an unavailable item's information could unintentionally reset its availability to True.

Implementation:
Modified files:
app/schemas/item.py: Added the availability field and non-negative price validation.
app/services/item_service.py: Added availability handling when creating and updating menu items.
app/api/routes/item_router.py: Passed availability information to the service layer and distinguished omitted values from explicit updates.
tests/test_main.py: Added regression coverage for availability preservation and explicit reactivation.

Idea:
The update operation preserves the existing availability state when the request does not explicitly specify a new value. This can prevent an unavailable item from being unintentionally reactivated when other properties are updated.

Testing and Validation:
1 Existing tests remained operational.
2 Added an availability regression test.
3 Verified that availability remains False when a price update omits the field.
4 Verified that explicitly setting availability to True allows reactivation.
Latest pytest result: 18 passed, 1 warning, 0 failed.

AI Assistance:
Used ChatGPT for correcting syntax error.

PR: #52

Item 2
Testing Efficiency 
Developer Experience

Problem:
When testing the customer registration, shopping cart, and checkout features, I found that after every page refresh or debug frontend changes, it is very troublesome to enter(or copy and paste) login credentials.

Improvement:
I added a Quick Test Login button to web/m2.html to automatically fill in predefined test customer information and sign in through the existing login function.
This allows me to access the application more quickly during repeated manual testing without changing the backend authentication process.
I also corrected the HTML comment syntax to keep development notes (for my teammates to delete after we done all the testing in the future) in the source code without displaying them on the webpage.

Testing:
Firstly I Verified that the test customer could successfully sign in using the shortcut. Secondly, IConfirmed that the login status displayed "Signed in". Lastly, I Confirmed that the shortcut uses the existing authentication flow.

Reflection:
Although this is a small feature, I wanted to improve the development workflow, increase efficiency. So that we don't need to repeatedly performing the same manual steps. This makes future testing of the cart, checkout, and order features more convenient.
The shortcut is intended for local development only. In the future, it will be removed or replaced before the final public submission.

AI Assistance:
I googled necessary code to implement this small function. No AI assisted

GitHub Evidence:
File: web/m2.html
Commit: e21c6ae
PR: #53

Item 3
Improving JSON Data Persistence  
Architecture Improvement and Decision Receipt

Problem:
During M2 integration, I noticed that the restaurant and menu repositories were saving data directly to JSON files. If something went wrong during saving, the original file could potentially be damaged.

Implementation:
I have two ideas:
1 Keep the existing file-writing method because it was simple and already working.
2 Use a temporary file and replace the original file after the new data was written successfully.
I chose the second option because it provided better protection for our stored data without making major changes to the existing project.
I added app/repositories/json_storage.py and updated the restaurant and item repositories to use the shared JSON saving function.
The function writes data to a temporary file first, then replaces the original file. This reduces the risk of leaving a partially written JSON file if saving fails.
I also added tests to check that JSON files could be created, updated, and preserved when replacement failed.

Testing:
I ran the repository tests and the full automated test suite. In my latest full test run on November 20, 2026, all 50 tests passed.
I also confirmed that the GitHub Actions test workflow completed successfully.

Reflection:
This change helped make the data storage more reliable. It also reduced repeated file-saving code between repositories. I think it was a useful improvement because the M2 system depends on keeping customer orders and menu data consistent.

AI Assistance:
I used Gemini for implementation suggestions and debugging. I integrated the changes and verified the results.

GitHub Evidence:
Files: app/repositories/json_storage.py, app/repositories/item_repository.py, app/repositories/restaurant_repository.py, tests/test_json_storage.py  
PR: #49, #52

Item 4
Customer, Cart, and Checkout Integration
Feature Integration

Problem:
M2 required the customer, restaurant, menu, cart, and order features to work together. It was important to make sure the system could complete an order rather than having separate features that only worked individually.

Implementation:
I worked on integrating the customer registration and login process with the shopping cart and checkout system.
The cart supports adding items, changing quantities, removing items, and clearing the cart. I also checked that customers could only add items from one restaurant at a time.
During checkout, the system checks the customer information, restaurant status, and menu item availability before creating an order.
After checkout, the order is saved and the customer's cart is cleared.

Testing and Validation:
I tested the complete workflow through the frontend, starting from registration and login.
I added a menu item to the cart, changed its quantity, completed checkout, and checked the saved order.
I also restarted the application and confirmed that the previous order could still be retrieved.

Reflection:
This was an important part of M2 because it connected several features into one working system. Testing the full process helped me understand how the different parts of the backend interact.

AI Assistance:
I used ChatGPT for implementation examples and debugging.

GitHub Evidence:
Files: app/services/commerce_service.py, app/api/routes/commerce_router.py, app/schemas/commerce.py
PR: #50, #51, #52

Item 5
Role-Based Access Control
Security Improvement / Decision Receipt

Problem:
The system has different types of users. Regular customers should be able to browse restaurants and place orders, but they should not be able to create or modify restaurant and menu information.

Options Considered:
Allow all authenticated users to access the existing management endpoints.
Restrict restaurant and menu modifications to users with the admin role.
I chose the second approach because it provides a clear separation between customers and administrators.

Implementation:
I worked on integrating authentication and role checks into the API.
Requests without a valid login token are rejected. Customers who are logged in but do not have administrator permissions cannot access the restaurant and menu modification endpoints.
The system also uses different HTTP status codes for authentication and permission errors.

Testing and Validation:
I tested unauthenticated requests and requests made using a regular customer account.
I verified that unauthenticated requests returned 401 and regular customers received 403 when accessing protected management endpoints.
I also added checks to confirm that rejected requests did not modify the restaurant or menu JSON files.

Reflection:
This improvement helped make the system more secure and made the API behaviour easier to understand.

AI Assistance:
I used Grok for implementation suggestions and test guidance.

GitHub Evidence:
Files: app/core/auth.py, app/api/routes/restaurant_router.py, app/api/routes/item_router.py, tests/test_m2_api_integration.py
PR: #52

Item 6
Shared Authentication 
Architecture Improvement / Decision Receipt

Problem:
Authentication checks were duplicated in the commerce router and security module. Security code also depended on the router to access the shared service.

Options Considered:
Keep the separate authentication checks and access the service through the router.
Move the shared service into a separate module and use one authentication check.
I chose the second approach to reduce duplication and also the separation of responsibilities.

Implementation:
Removed the duplicate authentication dependency from auth_router.py. Customer, cart, and order routers now import current_user from app/core/auth.py, which admin checks also use. Reused the shared services introduced in PR #56.

Testing and Validation:
I added tests/test_shared_authentication.py to check registration, login, menu retrieval, cart operations, admin permissions, and checkout using the same token.
The test uses temporary storage.
All 51 tests passed.

Reflection:
This change makes authentication easier to maintain because the shared check only needs to be updated in one place. It adds one small module while preserving existing functionality and login sessions.

AI Assistance:
I used ChatGPT for implementation suggestions, integration tests, and debugging guidance. 

GitHub Evidence:
Files: app/core/dependencies.py, app/core/auth.py, app/api/routes/commerce_router.py, tests/test_shared_authentication.py
PR: #57

Final Integration Check November 20, 2026
After splitting the M2 work into smaller PRs, I ran the full test suite again and got 50 passed with one warning.
I also tested the ordering flow in the browser. Login, restaurant browsing, adding items to the cart, checkout, and order history all worked. Checkout returned 201 and the order appeared in the order history.
The work was split across PRs #49–#53 for review.

Final M2 Check November 20, 2026
I split my M2 changes into five PRs (#49-#53) so the team could review them separately.
After finishing the frontend, I ran pytest again and got 50 passed with one warning.
I also tried the ordering flow in the browser. I logged in, picked a restaurant, added food to the cart, checked out, and viewed the order afterward. Checkout returned 201 and the order showed up in my order history.
The PRs are uploaded, but they still need to be reviewed and merged into the main branch.