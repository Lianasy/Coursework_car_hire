from typing import Optional
import copy


class CarDocument:
    def __init__(self, carId: int) -> None:
        """
        Initializes the CarDocument object with a car ID.

        Args:
            carId (int): Car ID.
        """
        self.carId: int = carId
        self.documentLocation: str | None = None

    def get_car_id(self) -> int:
        """
        Gets the car ID associated with the document.

        Returns:
            int: Car ID.
        """
        return self.carId

    def get_document_location(self) -> str | None:
        """
        Gets the location of the document.

        Returns:
            str | None: Document location.
        """
        return self.documentLocation


class Car:
    def __init__(self, carId: int, carNumber: str | None = None, carModel: str | None = None,
                 rentPrice: float | None = None, rentStatus: bool | None = None,
                 carType: str | None = None, documents: list[CarDocument] | None = None) -> None:
        """
        Initializes the Car object with optional parameters.

        Args:
            carId (int): The unique identifier for the car.
            carNumber (str | None): Car registration number.
            carModel (str | None): Car model.
            rentPrice (float | None): Rental price per day.
            rentStatus (bool | None): Rental status of the car.
            carType (str | None): Type or category of the car.
            documents (list[CarDocument] | None): List of documents associated with the car.
        """
        self.carId: int = carId
        self.carNumber: str | None = carNumber
        self.carModel: str | None = carModel
        self.rentPrice: float | None = rentPrice
        self.rentStatus: bool | None = rentStatus
        self.carType: str | None = carType
        self.documents: list[CarDocument] | None = documents

    def upload_car_info(self) -> None:
        """
        Uploads car information to the database.
        """
        # Placeholder for actual implementation

    def load_car_info(self) -> None:
        """
        Loads car information from the database.
        """
        if self.carId is not None:
            # Placeholder for actual implementation
            pass

    def get_id(self) -> int:
        """
        Gets the unique identifier for the car.

        Returns:
            int: Car ID.
        """
        return self.carId

    def set_rent_status(self, new_rent_status: str) -> None:
        """
        Sets the rental status of the car.

        Args:
            new_rent_status (bool): New rental status.
        """
        self.rentStatus = new_rent_status

    def add_document(self, document: CarDocument) -> None:
        """
        Adds a document to the list of documents associated with the car.

        Args:
            document (CarDocument): Document object to be added.
        """
        self.documents.append(document)
