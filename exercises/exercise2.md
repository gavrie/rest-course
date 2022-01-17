# Exercise 2

Branch: `lesson_065_hateoas_pagination`

- Generate the correct links for paging (the current code contains placeholder numbers for the `offset` and `limit` parameters; your code should include the correct numbers)
   - Note: not all pages necessarily need to include all 4 links, but only the relevant ones.
   - Be sure that your code is efficient in that it only pulls the minimal required data from Redis.
- Implement a test that verifies that everything works. 
  - The "ideal" test would get the URL of the first page, and automatically follow the links to retrieve all pages.
