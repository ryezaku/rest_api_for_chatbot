# rest_api_for_chatbot
rest_api_chatbot

# Running The Docker
1.to run the fast api service,go to the directory path and type 
```
docker-compose up --build
```

After the message below is shown on the console, we may start to send the POST request
```
chatbot-fastapi-2 | INFO:     Waiting for application startup.
chatbot-fastapi-2 | INFO:     Application startup complete.
chatbot-fastapi-2 | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
- The POST request was tested using Postman
- The json body is shown below:

We require the access token to  be included in the postman in order to use the api
send the request to here to register the user:
```
http://localhost:8000/v1/hooli/message
```
##  example for registration of user
```
    {   "sender": "+444",
        "receiver": "921008145383",
        "text" :"hello Vox"

    }
```
- the response would be like:
```
{
    "msg": "Yes I am inspired by commander Data's artificial personality."
}
```

## For update database:
```
http://localhost:8000/v1/hooli/message/{restaurant_id}
```

```
{
"hooli_number":"11223", 
"name":"haha1dasd1", 
"contact_phone":"contact_nasdumber"
}
```
- for the restaurant id we can use the restaurant id inside the database which is in side the database.sqlite below:

```
                id  hooli_number           name contact_phone
0  sliceline_pizza         11223     haha1dasd1  +60011234567
1    drunken_dough  +12207654321  Drunken Dough  +60012345678
2        pizza_but  +12002468246      Pizza But  +60013693693
```
- the response would be like:
```
chatbot-fastapi-2 | INFO:     172.20.0.1:44014 - "PUT /v1/hooli/message/sliceline_pizza HTTP/1.1" 202 Accepted
```
