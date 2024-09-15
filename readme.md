Immediate Search:
The system will start searching as soon as the query is received.

Cache Results:
The search results are saved so that future searches for the same query will be faster.

API Status:
There's a feature to check if the API is working, and it will return a "200 OK" status if everything is fine.

User Handling:
If the user already exists, the system increases their query count. If they are new, it creates a user and sets their query count to 1.

Text Box for Query:
A text box is provided where users can enter their search query.

Top Search Results:
The system will return the top results based on the search query, showing a certain number of results.

Threshold Score:
It also shows how relevant the results are based on a threshold score.

Limit on Queries:
If a user makes more than 5 queries in a row, they will get an error message with a 429 status, meaning "Too Many Requests."

Error Handling:
Even when there’s an error, the system still returns a 200 OK status code, but it will explain what went wrong so the user can fix it.








