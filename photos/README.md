
The project has two entities modelled 
 * Photo
 * User      

The database used is sqlite populated with some test values


Two users have been created
``` 
user1:  {id: 1, username: "test_user_1"}
user2:  {id: 1, username: "test_user_2"}
``` 


Photo APIs supported:

( Deloyed on http://deepav88.pythonanywhere.com/ )

Get Jwt Token has to be called first to obtain a token
```
The username is used to obtain a jwt token

The api details are:

url: /get-token/?username=test_user_1
method: get

Token from the above response and username are to be sent as request headers
for every api call
{"token": <token>, "username": <user_name>"}
```

```

Request headers for all APIs
{"token": <token>, "username": <user_name>"}
```
(1) List photos 

```
Url: /photos/
method: GET
Query parameters:
    * published_on=<datetime> (eg of pub_date: 2020-08-02T12:31:27.365423Z)
    * user=<integer_user_id>
    * is_draft=<bool>           
    * order_by=<published_on>  
        (for ascending sort on date: order_by=-published_on
         for desscending sort on date: order_by=-published_on
        )
```

(2) Get Photos

```
Url: /photos/<id>/
method: GET 
```
(3) Create Photo:
 - Can be saved as draft by passing is_draft=true
 - The photo is saved to a folder /static/ locally which can be replaced by 
 uploading it to a service like aws s3 


```
Url: /photos/
method: POST
request type: multipart/form-data 

request body: 
{
"image": <file>,
"caption":<string>,
"is_draft": <bool>
"user": <integer_user_id>
}
```

(4) Delete Photo

```
Url: /photos/<photo_id>
method: DELETE
```

(5) Edit Photo ( captions )

```
Url: /photos/<id>/
method: PATCH

request type: 
{
"caption":<string>
}

```
(6) Post Photo 
    The api takes an image to be posted or the image id to be posted
    Using the image id, the image location(Example: s3) 
    is retrieved from the database
    
```
Url: /post-photo/
method: POST
request type: multipart/form-data 

request body: 
{
"image": <file>,
"photo_id": <id>
}
```


To run the application from within the photos directory
(Requires Python 3)

1. Install requirements 
    pip install requirements.txt
    
2. Runserver
    ./manage.py runserver 

3. Migrate:
    ./manage.py migrate
    
4. Tests
    ./manage.py test 
