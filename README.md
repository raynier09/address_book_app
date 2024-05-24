# Address Book Application

Recommended to install this on a virtual environment. To avoid conflicts on the dependencies
with other projects.

To install all the dependencies. run the command

``` 
pip install -r requirements.txt
```

Start the application
```
uvicorn main:app --reload
```

### Open Swagger UI
127.0.0.1:8000/docs

### API Endpoints

```
   /addresses/ - POST - Create New Address
   /addresses/ - GET  - Retrieve List of Address
   /addresses/{address_id} - GET - Retrieve a single address by its ID.
   /addresses/{address_id} - PUT - Update an existing address
   /addresses/{address_id} - DELETE - Delete an address using it's ID.
   /addresses/search/ - GET - Search for Addresses within a given distance from specified coordinates
```