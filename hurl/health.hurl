GET {{base_url}}/healthz
HTTP 200
[Asserts]
jsonpath "$.status" == "ok"

GET {{base_url}}/readyz
HTTP 200
[Asserts]
jsonpath "$.status" == "ready"
