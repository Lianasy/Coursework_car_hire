from datetime import datetime, timedelta
from CarDomain import Car
from Users import Renter, CompanyWorker
from typing import Dict
from Connect import connection
import json


class Rent:
    def __init__(self, rent_id: int | None = None, user_id: int | None = None, car_id: int | None = None,
                 price: float | None = None, discount: int | None = None, deposit: float | None = None,
                 start_time: datetime | None = datetime.now().date(), end_time: datetime | None = datetime.now().date(),
                 agreement: str | None = None, agreement_description: str | None = None,
                 isRentFinished: bool | None = False) -> None:
        """
        Initializes the Rent object with optional parameters.

        Args:
            rent_id (int | None): Unique identifier for the rent.
            user_id (int | None): User ID associated with the rent.
            car_id (int | None): Car ID associated with the rent.
            car_price (float | None): Rental price per day for the car.
            discount (int | None): Discount applied to the rental price.
            deposit (float | None): Deposit amount for the rent.
            days_for_rent (int | None): Number of days the car is rented.
            agreement (str | None): Agreement details for the rent.
            agreement_description (str | None): Description of the rent agreement.

        Note:
            If `rent_id` is not provided, it generates a new agreement and description.
            Otherwise, it uses the provided `agreement` and `agreement_description`.
        """
        self.rent_id: int | None = rent_id
        self.user_id: int | None = user_id
        self.car_id: int | None = car_id
        self.price: float | None = price
        self.discount: int | None = discount
        self.deposit: float | None = deposit
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.agreement: str | None = agreement
        self.agreement_description: str | None = agreement_description
        self.isRentFinished: bool = isRentFinished

    def generate_agreement(self) -> str:
        """
        Generates a new agreement for the rent.

        Returns:
            str: Agreement details.
        """
        pass

    def generate_agreement_description(self) -> str:
        """
        Generates a description for the rent agreement.

        Returns:
            str: Agreement description.
        """
        pass

    def upload_to_database_new(self):
        """
        Uploads new rent details to the database.
        """
        try:
            cursor = connection.mysql_connection.cursor()
            insert_query = "INSERT INTO rent" \
                           " (userId, shortTermAgreement, carId, price, deposit, " \
                           "startTime, endTime, isFinish, discount)" \
                           " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            user_data = (self.user_id, self.agreement, self.car_id,
                         self.price, self.deposit, self.start_time,
                         self.end_time, self.isRentFinished, self.discount)
            cursor.execute(insert_query, user_data)
            connection.mysql_connection.commit()
            rent_id = cursor.lastrowid
            if rent_id is not None:
                self.rent_id = rent_id
            # Якщо вивантаження в базу пройшло успішно, повертаємо True
            return True
        except Exception as e:
            # Якщо сталася помилка, повертаємо False
            print(f'Failed to upload rent info to MySQL. Error: {e}')
            return False

        #db = connection.couchdb_connection['car_hire']
        #document_id = f"Agreement_{str(self.rent_id)}"
        #document_location = f"Agreement_{str(self.rent_id)}.doc"
        #new_document = {
        #    "_id": document_id,
        #    "documentLocation": document_location,
        #    "rentId": self.rent_id
        #}
        #response = db.save(new_document)
        #if response:
        #    print("Document added to CouchDB successfully.")
        #else:
        #    print(f'Failed to add document to CouchDB. Response: {response}')

    def upload_to_database_existing(self):
        """
        Uploads existing rent details to the database.
        """
        try:
            cursor = connection.mysql_connection.cursor()
            update_query = "UPDATE rent SET userId = %s, shortTermAgreement = %s, carId = %s, " \
                           "price = %s, deposit = %s, startTime = %s, endTime = %s, " \
                           "isFinish = %s, discount = %s WHERE rent_id = %s"
            user_data = (self.user_id, self.agreement, self.car_id,
                         self.price, self.deposit, self.start_time,
                         self.end_time, self.isRentFinished, self.discount,
                         self.rent_id)
            cursor.execute(update_query, user_data)
            connection.mysql_connection.commit()
            # Якщо оновлення в базі пройшло успішно, повертаємо True
            return True
        except Exception as e:
            # Якщо сталася помилка, повертаємо False
            print(f'Failed to update rent details for rent {self.rent_id} in db. Error: {e}')
            return False
    def load_from_database(self) -> None:
        """
        Loads rent details from the database.
        """
        if self.rent_id is not None:
            try:
                cursor = connection.mysql_connection.cursor()
                select_query = "SELECT userId, shortTermAgreement, carId, price, deposit, " \
                               "startTime, endTime, isFinish, discount FROM rent WHERE rentId = %s"
                cursor.execute(select_query, (self.rent_id,))
                result = cursor.fetchone()

                if result:
                    (self.user_id, self.agreement, self.car_id, self.price,
                     self.deposit, self.start_time, self.end_time,
                     self.isRentFinished, self.discount) = result

            except Exception as e:
                print(f'Failed to load rent details from MySQL. Error: {e}')

    def set_rent_finished(self, set_finished: bool = True) -> None:
        """
        Marks the rent as set_finished and updates the database.

        Args:
            set_finished (bool): Indicates whether the rent is finished or not.
        """

        if self.rent_id is not None:
            try:
                cursor = connection.mysql_connection.cursor()
                update_query = "UPDATE rent SET isFinish = %s WHERE rentId = %s"
                cursor.execute(update_query, (set_finished, self.rent_id))
                connection.mysql_connection.commit()

                # Оновлення атрибута об'єкту
                self.isRentFinished = set_finished

            except Exception as e:
                print(f'Failed to update rent status in MySQL. Error: {e}')


class RenterController:
    def __init__(self, renter: Renter) -> None:
        """
        Initializes the RenterController object.

        Args:
            renter (Renter): Renter from LogIn.user or Registration.user
        """
        self.renter: Renter = renter

    def calculate_discount(self) -> int:
        """
        Calculates the discount based on the time a user has spent in the system.

        Returns:
            int: Discount percentage.
        """
        time_in_system = self.renter.count_time_in_system()
        if time_in_system >= 365:
            return 10
        elif time_in_system >= 180:
            return 5
        elif time_in_system >= 90:
            return 3
        elif time_in_system >= 30:
            return 1
        else:
            return 0

    def calculate_deposit(self) -> float:
        """
        Calculates the deposit amount based on user information.

        Returns:
            float: Deposit amount.
        """

        pass

    def get_available_cars(self) -> list[Car]:
        """
        Retrieves available cars from the Car table in the database.

        Returns:
            list[Car]: List of available cars.
        """
        available_cars = []

        try:
            cursor = connection.mysql_connection.cursor()

            query = """
                            SELECT *
                            FROM car
                            WHERE rentStatus = 'AVAILABLE'
                        """

            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                car = Car(
                    carId=row[0],
                    carNumber=row[1],
                    carModel=row[2],
                    rentPrice=row[3],
                    rentStatus=row[4],
                    carType=row[5],
                )
                available_cars.append(car)

            return available_cars

        except Exception as e:
            print(f'Failed to retrieve available cars. Error: {e}')



    def rent_car(self, car: Car, days_for_rent: int) -> None:
        """
        Rents a car for a specified number of days and updates the database.

        Args:
            car (Car): Car object to be rented.
            days_for_rent (int): Number of days for the rent.
        """
        rent = Rent(user_id=self.renter.id, car_id=car.carId, price=car.rentPrice * days_for_rent,
                    discount=self.calculate_discount(), deposit=self.calculate_deposit(), start_time=datetime.now().date(),
                    end_time=datetime.now().date() + timedelta(days=days_for_rent))
        rent.generate_agreement()
        rent.generate_agreement_description()
        rent.upload_to_database_new()
        car.set_rent_status('IN_RENT')
        car.upload_car_info()
        self.renter.set_rent_ability(False)



class ManagerController:
    def __init__(self, manager: CompanyWorker) -> None:
        """
        Initializes the ManagerController object.

        Args:
            manager (CompanyWorker): Manager object from LogIn.user.
        """
        self.manager: CompanyWorker = manager

    def end_rent(self, rent: Rent) -> None:
        """
        Ends the specified rent and updates the database.

        Args:
            rent (Rent): Rent to be ended
        """
        rent.set_rent_finished()
        rent.upload_to_database_existing()

    def change_user_info(self, user: Renter, new_info: Dict[str, str]) -> None:
        """
        Changes user information and updates the database.

        Args:
            user (User): User object.
            new_info (Dict[str, str]): Dictionary containing new user information.
        """
        try:
            if not user.change_base_info(new_info):
                raise Exception
        except Exception as e:
            print('Changing user info failed')

    def get_users(self) -> list[Renter]:
        """
        Retrieves a list of users from the User table in the database.

        Returns:
            list[Renter]: List of users.
        """
        try:
            cursor = connection.mysql_connection.cursor()

            query = """
                    SELECT * FROM renter
                """

            cursor.execute(query)
            results = cursor.fetchall()

            renters = []
            for row in results:

                renter = Renter(row[0], None)
                renter.registrationDate = row[1]
                renter.driverLicenseDate = row[2]
                renter.canRent = True

                renters.append(renter)

            return renters

        except Exception as e:
            print(f'Failed to retrieve users from the database. Error: {e}')
            return []

    def get_cars(self) -> list[Car]:
        """
        Retrieves a list of cars from the Car table in the database.

        Returns:
            list[Car]: List of cars.
        """
        cars = []

        try:
            cursor = connection.mysql_connection.cursor()

            query = """
                            SELECT * FROM car
                        """

            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                car = Car(
                    carId=row[0],
                    carNumber=row[1],
                    carModel=row[2],
                    rentPrice=row[3],
                    rentStatus=row[4],
                    carType=row[5],
                )
                cars.append(car)

            return cars

        except Exception as e:
            print(f'Failed to retrieve available cars. Error: {e}')


    def get_rented_cars(self) -> list[Car]:
        """
        Retrieves a list of rented cars from the Rent table in the database.

        Returns:
            list[Car]: List of rented cars.
        """
        rented_cars = []

        try:
            cursor = connection.mysql_connection.cursor()

            query = """
                                   SELECT *
                                   FROM car
                                   WHERE rentStatus = 'IN_RENT'
                               """

            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                car = Car(
                    carId=row[0],
                    carNumber=row[1],
                    carModel=row[2],
                    rentPrice=row[3],
                    rentStatus=row[4],
                    carType=row[5],
                )
                rented_cars.append(car)

            return rented_cars

        except Exception as e:
            print(f'Failed to retrieve available cars. Error: {e}')

    def get_expired_rents(self) -> list[Rent]:
        """
        Retrieves a list of expired rents from the Rent table in the database.

        Returns:
            list[Rent]: List of expired rents.
        """
        try:
            cursor = connection.mysql_connection.cursor()

            query = """
                        SELECT * FROM rent
                        WHERE endTime < NOW() AND isFinish = 0
                    """

            cursor.execute(query)
            results = cursor.fetchall()

            expired_rents = []
            for row in results:
                rent = Rent(
                    rent_id=row[0],
                    user_id=row[1],
                    car_id=row[2],
                    price=row[3],
                    deposit=row[4],
                    start_time=row[5],
                    end_time=row[6],
                    isRentFinished=row[7],
                    discount=row[8],
                    # Інші атрибути, які можна отримати з результатів запиту
                )

                expired_rents.append(rent)

            return expired_rents

        except Exception as e:
            print(f'Failed to retrieve expired rents from the database. Error: {e}')
            return []


