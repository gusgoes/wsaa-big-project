# Books API

Base URL (local):
http://127.0.0.1:5000

## Response Envelope

All responses follow a consistent shape:

**Success:**
```json
{ "status": "success", "data": <payload> }
```

**Error:**
```json
{ "status": "error", "message": "<description>" }
```

## Endpoints

### GET /books
Returns all books.

Response 200 example:
```json
{
	"status": "success",
	"data": [
		{ "id": 1, "title": "1984", "author": "George Orwell", "price": 10.5 }
	]
}
```

### GET /books/{id}
Returns one book by id.

Response 200 example:
```json
{
	"status": "success",
	"data": { "id": 1, "title": "1984", "author": "George Orwell", "price": 10.5 }
}
```

Response 404 example:
```json
{
	"status": "error",
	"message": "Not found"
}
```

### POST /books
Creates a new book.

Request body example:
```json
{
	"title": "1984",
	"author": "George Orwell",
	"price": 10.5
}
```

Response 201 example:
```json
{
	"status": "success",
	"data": { "id": 1 }
}
```

Response 400 examples:
```json
{
	"status": "error",
	"message": "title is required and must be a non-empty string"
}
```

```json
{
	"status": "error",
	"message": "price must be greater than or equal to 0"
}
```

### PUT /books/{id}
Updates an existing book.

Request body example:
```json
{
	"title": "1984",
	"author": "George Orwell",
	"price": 8.99
}
```

Response 200 example:
```json
{
	"status": "success",
	"data": { "updated": 1 }
}
```

Response 400 example:
```json
{
	"status": "error",
	"message": "price is required and must be numeric"
}
```

Response 404 example:
```json
{
	"status": "error",
	"message": "Not found"
}
```

### DELETE /books/{id}
Deletes a book by id.

Response 200 example:
```json
{
	"status": "success",
	"data": { "deleted": 1 }
}
```

Response 404 example:
```json
{
	"status": "error",
	"message": "Not found"
}
```

## Validation Rules

For POST and PUT:
- title: required, string, not empty
- author: required, string, not empty
- price: required, numeric, must be greater than or equal to 0
