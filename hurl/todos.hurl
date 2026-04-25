POST {{base_url}}/api/v1/auth/register
Content-Type: application/json
{
  "email": "{{email}}",
  "name": "Hurl Todo User",
  "password": "{{password}}"
}
HTTP 200

POST {{base_url}}/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded
username={{email}}&password={{password}}
HTTP 200
[Captures]
token: jsonpath "$.access_token"

POST {{base_url}}/api/v1/todos
Content-Type: application/json
Authorization: Bearer {{token}}
{
  "title": "Hurl todo",
  "description": "Created by hurl API test",
  "priority": 3,
  "tags": ["ci", "hurl"]
}
HTTP 201
[Captures]
todo_id: jsonpath "$.id"
[Asserts]
jsonpath "$.title" == "Hurl todo"
jsonpath "$.status" == "open"
jsonpath "$.priority" == 3

GET {{base_url}}/api/v1/todos
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.total" == 1
jsonpath "$.items[0].title" == "Hurl todo"

PATCH {{base_url}}/api/v1/todos/{{todo_id}}
Content-Type: application/json
Authorization: Bearer {{token}}
{
  "title": "Updated hurl todo",
  "status": "done"
}
HTTP 200
[Asserts]
jsonpath "$.title" == "Updated hurl todo"
jsonpath "$.status" == "done"

DELETE {{base_url}}/api/v1/todos/{{todo_id}}
Authorization: Bearer {{token}}
HTTP 204
