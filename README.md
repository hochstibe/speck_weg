# speck_weg
web app

```
# GET -> assumes, that it is a GET request
curl localhost:5000/
# Send Data (POST) -> specify header
curl -d '{json}' -H 'Content-Type: application/json' localhost:5000/
# Force a HTTP verb
curl localhost:5000 -X DELETE
```