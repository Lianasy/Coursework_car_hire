from typing import Optional
import copy
from Connect import connection

class CarDocument:
    def __init__(self, carId: int) -> None:
        """
        Initializes the CarDocument object with a car ID.

        Args:
            carId (int): Car ID.
        """
        self.carId: int = carId
        self.documentLocation: str | None = None

    def get_car_id(self, doc_id, doc_location) -> int:
        """
        Gets the car ID associated with the document.

        Returns:
            int: Car ID.
        """
        db = connection.couchdb_connection['car_hire']
        query = {
            "selector": {
                "documents": {
                    "$elemMatch": {
                        "documentId": doc_id
                    }
                }
            },
            "fields": ["documentLocation"],
        }
        res = db.find(query)
        car_id = next(res, {}).get('carId', None)
        print()
        return self.carId

    def get_document_location(self, doc_id) -> str | None:
        """
        Gets the location of the document.

        Returns:
            str | None: Document location.
        """
        try:
            db = connection.couchdb_connection['car_hire']
            query = {
                "selector": {
                    "documents": {
                        "$elemMatch": {
                            "documentId": doc_id
                        }
                    }
                },
             "fields": ["documents"],
            }
            result_list = list(db.find(query))
            document_locations = [doc['documentLocation'] for doc in result_list[0].get('documents', []) if
                                 doc['documentId'] == doc_id]

            if document_locations:
                document_location = document_locations[0]
                print(document_location)
                return self.documentLocation
            else:
                print(f"Місцезнаходження документа для ідентифікатора '{doc_id}' не знайдено.")
                return None

        except Exception as e:
            print(f"Помилка: {e}")
            return None



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
        try:
            cursor = connection.mysql_connection.cursor()
            insert_query = "INSERT INTO car (carId, carNumber, carModel, rentPrice, rentStatus, carType) VALUES (%s, %s, %s, %s, %s, %s)"
            car_data = (self.carId, self.carNumber, self.carModel, self.rentPrice, self.rentStatus, self.carType)
            cursor.execute(insert_query, car_data)
            connection.mysql_connection.commit()

        except Exception as e:
            print(f"Помилка при взаємоді з базою даних: {e}")



    def load_car_info(self) -> None:
        """
        Loads car information from the database.
        """
        if self.carId is not None:
            try:
                cursor = connection.mysql_connection.cursor()
                query = f"SELECT carNumber, carModel, rentPrice, rentStatus, carType FROM car WHERE carId = {self.carId}"
                cursor.execute(query)
                car_info = cursor.fetchone()

                if car_info:
                    self.carNumber, self.carModel, self.rentPrice, self.rentStatus, self.carType = car_info
                    print(f"Інформацію про автомобіль (ID {self.carId}) завантажено з бази даних.")
                else:
                    print(f"Автомобіль з ID {self.carId} не знайдено в базі даних.")

            except Exception as e:
                print(f"Помилка при взаємоді з базою даних: {e}")


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


carDoc = CarDocument(4)
#carDoc.get_document_location("CertifOfRegistrCar5")
car = Car(3)
car.load_car_info()
print(car.carNumber)
car1 = Car(10, "AA5011AA", "Nissan Micro", 200, True, "ECONOMY")
car1.upload_car_info()
print(car1.carModel + car1.carNumber)