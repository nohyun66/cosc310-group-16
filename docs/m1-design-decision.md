# M1 Design Decision: Empty Search Results

## Decision

Restaurant searches return 200 OK with an empty list when no
restaurants match. Requests for a specific restaurant ID return
404 Not Found when that restaurant does not exist.

## Reason

A search can complete successfully without finding any matches.
Returning a list gives the frontend a consistent response format
for successful searches.

A request for a specific ID asks for one existing restaurant.
If that restaurant does not exist, the API returns 404.

## Alternative considered

Return 404 whenever a search finds no matches.

We chose an empty list because no search results is an expected
outcome that the frontend can display to the customer.

## Tradeoff

The frontend must check whether the returned list is empty and
display a suitable message, such as "No restaurants found."

## Validation

Automated tests check that searches with no matches return
200 OK and an empty list, and that a missing restaurant ID
returns 404.