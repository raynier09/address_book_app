from database import create_db_and_tables, engine
from models import Address, AddressCreate, AddressRead
from geopy.distance import geodesic
from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException, Depends
from typing import List

app = FastAPI()

def get_db():
    """
        Context manager to get a database session.

        Yields:
            Session: The database session.
    """
    with Session(engine) as session:
        yield session

@app.post("/addresses/", response_model=AddressRead)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    """
        Create a new address.

        Args:
            address (AddressCreate): The address data to create.
            db (Session): The database session.

        Returns:
            AddressRead: The created address.
    """
    db_address = Address.model_validate(address)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/", response_model=List[AddressRead])
def read_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        Retrieve a list of addresses.

        Args:
            skip (int): The number of records to skip.
            limit (int): The maximum number of records to return.
            db (Session): The database session.

        Returns:
            List[AddressRead]: A list of addresses.
    """
    addresses = db.exec(select(Address).offset(skip).limit(limit)).all()
    return addresses

@app.get("/addresses/{address_id}", response_model=AddressRead)
def read_address(address_id: int, db: Session = Depends(get_db)):
    """
        Retrieve a single address by its ID.

        Args:
            address_id (int): The ID of the address to retrieve.
            db (Session): The database session.

        Returns:
            AddressRead: The retrieved address.
    """
    address = db.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.put("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: int, address_update: AddressCreate, db: Session = Depends(get_db)):
    """
        Update an existing address.

        Args:
            address_id (int): The ID of the address to update.
            address_update (AddressCreate): The updated address data.
            db (Session): The database session.

        Returns:
            AddressRead: The updated address.
    """
    address = db.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address_data = address_update.dict(exclude_unset=True)
    for key, value in address_data.items():
        setattr(address, key, value)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

@app.delete("/addresses/{address_id}", response_model=AddressRead)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
        Delete an address by it's ID.

        Args:
            address_id (int): The ID of the address to delete.
            db (Session): The database session.

        Returns:
            AddressRead: The deleted address.
    """
    address = db.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return address

@app.get("/addresses/search/", response_model=List[AddressRead])
def search_addresses(latitude: float,
                     longitude: float,
                     distance: float,
                     db: Session = Depends(get_db)):
    """
        Search for addresses within a given distance from specified coordinates.

        Args:
            latitude (float): The latitude of the search center.
            longitude (float): The longitude of the search center.
            distance (float): The maximum distance in kilometers from the search center.

        Returns:
            List[AddressRead]: A list of addresses within the specified distance.
    """

    addresses = db.exec(select(Address)).all()
    result = []
    for address in addresses:
        if geodesic((latitude, longitude), (address.latitude, address.longitude)).km <= distance:
            result.append(address)
    return result

@app.on_event("startup")
async def on_startup():
    """
        Function to perform actions when the application starts up.
    """
    create_db_and_tables()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
