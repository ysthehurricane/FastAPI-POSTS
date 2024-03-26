# FastAPI-POSTS

# Project Structure

database.py : All configuration related to Database and schemas <br>
models.py : Database Pydantic Models User and Post <br>
main.py : Fast API main file (with all endpoints) <br>

End Pointa:

Sign Up Endpoint

Input:
Request Body: <br>
JSON object with fields:
- username (string): The username of the user.
- password (string): The password of the user.

Output:
JSON object with message:
- message (string): A message indicating successful user creation.

Login Endpoint

Input:
Request Body: <br>
JSON object with fields:
- username (string): The username of the user.
- password (string): The password of the user.

Output:
JSON object with authentication token:
- access_token (string): JWT token for authentication. ( valid 30 min )
- token_type (string): Type of token (Bearer).

Add Post Endpoint

Input:
Request Body:
JSON object with fields:

- title (string): Title of the post.
- content (string): Content of the post.

Authentication:
- Bearer token obtained from the login endpoint.

Output:
JSON object with post ID:
- postID (int or string): ID of the added post.

Get Posts Endpoint

Input:
- Authentication: Bearer token obtained from the login endpoint.

Output:

List of JSON objects representing posts:

Each JSON object contains fields:
- id (int): ID of the post.
- title (string): Title of the post.
- content (string): Content of the post.

Delete Post Endpoint

Input:

Path parameter:
- post_id (int): ID of the post to delete.

- Authentication: Bearer token obtained from the login endpoint.

Output:
JSON object with message:

- message (string): A message indicating successful deletion of the post.
