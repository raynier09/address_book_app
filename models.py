from sqlmodel import SQLModel, Field
from pydantic import field_validator

class AddressBase(SQLModel):
    """
    Base model for representing address data.

    Attributes:
        name (str): The name associated with the address.
        street (str): The street or street address.
        city (str): The city or locality.
        state (str): The state or region.
        country (str): The country.
        latitude (float): The latitude coordinate of the address.
        longitude (float): The longitude coordinate of the address.
    """

    name: str
    street: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float

    @field_validator('latitude')
    def validate_latitude(cls, value) -> float:
        """
        Validator for latitude coordinate.

        Args:
            value (float): The latitude value to validate.

        Returns:
            float: The validated latitude value.

        Raises:
            ValueError: If the latitude is not within the valid range (-90 to 90 degrees).
        """

        if not -90 <= value <= 90:
            raise ValueError('Latitude must be between -90 and 90 degrees.')
        return value

    @field_validator('longitude')
    def validate_longitude(cls, value) -> float:
        """
            Validator for longitude coordinate.

            Args:
                value (float): The longitude value to validate.

            Returns:
                float: The validated longitude value.

            Raises:
                ValueError: If the longitude is not within the valid range (-180 to 180 degrees).
        """

        if not -180 <= value <= 180:
            raise ValueError('Longitude must be between -180 and 180 degrees.')
        return value

class Address(AddressBase, table=True):
    """ Model for representing an address entity """
    id: int = Field(default=None, primary_key=True)

class AddressCreate(AddressBase):
    """ Model for creating a new address """

class AddressRead(AddressBase):
    """ Model for reading an address """
    id: int
