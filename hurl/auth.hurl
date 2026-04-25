POST {{base_url}}/api/v1/auth/register
Content-Type: application/json
{
  "email": "{{email}}",
  "name": "Hurl Test User",
  "password": "{{password}}"
}
HTTP 200
[Asserts]
jsonpath "$.email" == "{{email}}"
jsonpath "$.name" == "Hurl Test User"

POST {{base_url}}/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded
[FormParams]
username: {{email}}
password: {{password}}
HTTP 200
[Captures]
token: jsonpath "$.access_token"
[Asserts]
jsonpath "$.token_type" == "bearer"

GET {{base_url}}/api/v1/auth/me
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.email" == "{{email}}"
