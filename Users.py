from datetime import datetime
from typing import Dict
from Connect import connection
import json


class BaseInfo:
    def __init__(self, id: int, firstName: str = None, lastName: str = None, birthDate: datetime = None) -> None:
        """
        Initializes the BaseInfo object with optional parameters.

        Args:
            id (int): The user ID.
            firstName (str): First name of the user.
            lastName (str): Last name of the user.
            birthDate (datetime): Birthdate of the user.
        """
        self.id: int = id
        self.firstName: str | None = firstName
        self.lastName: str | None = lastName
        self.birthDate: datetime | None = birthDate

    def upload_to_database_new(self) -> bool:
        """
        Uploads user's base information to the database for new user.

        Returns:
            bool: True if the upload was successful, False otherwise.
        """
        try:
            cursor = connection.mysql_connection.cursor()
            insert_query = "INSERT INTO baseUserInfo (userId, firstName, lastName, birthDate) VALUES (%s, %s, %s, %s)"
            user_data = (self.id, self.firstName, self.lastName, self.birthDate)
            cursor.execute(insert_query, user_data)
            connection.mysql_connection.commit()
            # Якщо вивантаження в базу пройшло успішно, повертаємо True
            return True
        except Exception as e:
            # Якщо сталася помилка, повертаємо False
            print(f'Failed to upload base info for user {self.id} to db. Error: {e}')
            return False

    def upload_to_database_existing(self) -> bool:
        """
        Uploads user's base information to the database for existing user.

        Returns:
            bool: True if the upload was successful, False otherwise.
        """
        try:
            cursor = connection.mysql_connection.cursor()
            insert_query = "UPDATE baseUserInfo SET firstName = %s, lastName = %s, birthDate = %s WHERE userId = %s"
            user_data = (self.firstName, self.lastName, self.birthDate, self.id)
            cursor.execute(insert_query, user_data)
            connection.mysql_connection.commit()
            # Якщо вивантаження в базу пройшло успішно, повертаємо True
            print('base info for user ', self.id, 'load to db')
            return True
        except Exception as e:
            # Якщо сталася помилка, повертаємо False
            print(f'Failed to upload base info for user {self.id} to db. Error: {e}')
            return False

    def load_from_database(self) -> None:
        """
        Loads user's base information from the database.
        """
        if self.id is not None:
            try:
                cursor = connection.mysql_connection.cursor()
                query = f"SELECT firstName, lastName, birthDate FROM baseUserInfo WHERE userId = {self.id}"
                cursor.execute(query)
                base_info = cursor.fetchone()

                if base_info:
                    self.firstName, self.lastName, self.birthDate = base_info
                    print(f"Базова інформація користувача (ID {self.id}) завантажена з бази даних.")
                else:
                    print(f"Юзера з ID {self.id} не знайдено в базі даних.")
                    pass

            except Exception as e:
                print(f"Помилка при взаємодії з базою даних: {e}")


class Credential:
    def __init__(self, login: str | None = None, password: str | None = None) -> None:
        """
        Initializes the Credential object with login and password.

        Args:
            login (str): User's login.
            password (str): Password which user writes when logging in.
        """
        self.login: str | None = login
        self.password_to_validate: str | None = password

    def load_from_database(self) -> bool:
        """
        Gets login from database by user_id

        Args:
            user_id (int): User's id.

        Returns:
            bool: True if loading is successful
        """
        try:
            if self.login is not None:
                user_data = connection.redis_connection.get(str(self.login))
                print('Login for user', self.login, 'loaded from Redis', user_data)
                return True
            else:
                print('User not found in Redis')
                return False
        except Exception as e:
            # Якщо сталася помилка, повертаємо False
            print(f'Failed to load from db login for user {self.login}. Error: {e}')
            return False

    def get_id(self) -> int | None:
        """
        Gets the user ID if the password is valid.

        Returns:
            int | None: User ID or None if the password is invalid.
        """
        if self.__to_valid_password():
            user_data = connection.redis_connection.get(str(self.login))
            user_id = json.loads(user_data)[1]
            return user_id
        else:
            return None

    def __get_password(self) -> str:
        """
        Retrieves the password from the database based on the login.

        Returns:
            str: User's password.
        """
        # Placeholder for actual implementation
        try:
            user_data = connection.redis_connection.get(str(self.login))
            if user_data:
                password = json.loads(user_data)[0]
                return password

        except Exception as e:
            print(f'Failed to retrieve password from Redis. Error: {e}')
            return ''

    def __to_valid_password(self) -> bool:
        """
        Validates if the provided password matches the stored password.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        return self.__get_password() == self.password_to_validate

    def update_login(self, new_login: str) -> bool:
        """
        Updates the user's login and reflects the change in the database.

        Args:
            new_login (str): New login for the user.
        """
        try:
            if new_login is None:
                raise ValueError("New login cannot be None.")

            old_user_data = connection.redis_connection.get(str(self.login))
            if old_user_data is not None:
                connection.redis_connection.delete(str(self.login))
                self.login = new_login
                connection.redis_connection.set(new_login, old_user_data)
            return True
        except Exception as e:
            print(f'Failed to update login. Error: {e}')
            return False

    def update_password(self, new_password: str) -> bool:
        """
        Updates the user's password and reflects the change in the database.

        Args:
            new_password (str): New password for the user.
        """
        try:
            if new_password is None:
                raise ValueError("New password cannot be None.")

            user_data = connection.redis_connection.get(str(self.login))
            user_id = json.loads(user_data)[1]
            connection.redis_connection.set(str(self.login), json.dumps([new_password, user_id]))
            return True
        except Exception as e:
            print(f'Failed to update password for user {self.login}. Error: {e}')
            return False

    def upload_to_database_new(self, password: str, user_id: int) -> bool:
        """
                Updates the user's password and reflects the change in the database.

                Args:
                    new_password (str): New password for the user.
                """
        try:
            if self.login is None:
                raise ValueError("Login cannot be None.")
            if password is None:
                raise ValueError("Password cannot be None.")
            if user_id is None:
                raise ValueError("User id cannot be None.")

            connection.redis_connection.set(self.login, json.dumps((password, user_id)))
            return True
        except Exception as e:
            print(f'Failed to update password for user {user_id} in Redis. Error: {e}')
            return False


class PrivateInfo:
    def __init__(self, id: int | None = None) -> None:
        """
        Initializes the PrivateInfo object with a user ID.

        Args:
            id (int): User ID. If not provided, upload given privateInfo to the database by method `upload_private_info`
            and get id for new user
        """
        self.id: int | None = id

    def load_from_database(self) -> Dict[str, str | None]:
        """
        Retrieves private information of the user from the database.

        Returns:
            Dict[str, str | None]: Dictionary containing private information.
        """
        info: Dict[str, str | None] = None
        try:
            cursor = connection.mysql_connection.cursor(dictionary=True)

            # Виконуємо SQL-запит для отримання приватної інформації про користувача
            query = "SELECT photo, passportID, phoneNumber, driverLicence, email FROM privateInfo WHERE userId = %s"
            cursor.execute(query, (self.id,))
            result = cursor.fetchone()

            if result:
                print(result)
                return result
            else:
                print(f'Private information not found in MySQL for user {self.id}')
                return {}

        except Exception as e:
            # Обробка винятку при завантаженні інформації з бази даних
            print(f'Failed to load private info from MySQL. Error: {e}')
            return {}

    def upload_to_database_new(self, args: Dict[str, str | None]) -> int:

        """
        Uploads private information of the user to the database for new user.

        Args:
            args (Dict[str, str | None]): Dictionary containing private information.

        Returns:
            int: User id
        """
        try:
            cursor = connection.mysql_connection.cursor()
            insert_query = "INSERT INTO privateInfo (photo, passportID, phoneNumber, driverLicence, email) " \
                           "VALUES (%s, %s, %s, %s, %s)"
            user_data = (args.get('photo'), args.get('passportID'), args.get('phoneNumber'),
                         args.get('driverLicence'), args.get('email'))
            cursor.execute(insert_query, user_data)
            connection.mysql_connection.commit()
            # Якщо вивантаження в базу пройшло успішно, повертаємо id
            user_id = cursor.lastrowid
            if user_id is None:
                raise ValueError('Error occured when uploading private info for new user')
            self.id = user_id
            del args
            return self.id
        except Exception as e:
            # Якщо сталася помилка, повертаємо -1
            print(f'Failed to upload private info for user to db. Error: {e}')
            return -1

    def upload_to_database_existing(self, args: Dict[str, str | None]) -> bool:
        """
        Uploads private information of the user to the database for new user.

        Args:
            args (Dict[str, str | None]): Dictionary containing private information.

        Returns:
            int: User id
        """
        try:
            cursor = connection.mysql_connection.cursor()
            query = "UPDATE privateInfo " \
                    "SET photo = %s, passportID = %s, phoneNumber = %s, driverLicence = %s, email = %s" \
                    " WHERE userId = %s"

            # Виконання запиту UPDATE
            user_data = (args.get('photo'), args.get('passportID'), args.get('phoneNumber'), args.get('driverLicence'),
                         args.get('email'), self.id)
            cursor.execute(query, user_data)
            connection.mysql_connection.commit()
            # Якщо вивантаження в базу пройшло успішно, повертаємо True
            del args
            return True
        except Exception as e:
            # Якщо сталася помилка, повертаємо False
            print(f'Failed to upload private info for user to db. Error: {e}')
            return False


class User:
    def __init__(self, id: int | None = None, creds: Credential | None = None) -> None:
        """
        Initializes the User object with optional parameters.

        Args:
            id int: User ID.
        """
        self.id: int = id
        self.baseInfo: BaseInfo | None = None
        self.privateInfo: PrivateInfo | None = None
        self.creds: Credential | None = creds

    def load_private_info(self) -> None:
        """
        Loads user's private information from the database.
        """
        if self.id is not None:
            self.privateInfo = PrivateInfo(self.id)
        else:
            self.privateInfo = None

    def load_base_info(self) -> None:
        """
        Loads user's base information from the database.
        """
        if self.id is not None:
            self.baseInfo = BaseInfo(self.id)
            self.baseInfo.load_from_database()
        else:
            self.baseInfo = None

    def change_base_info(self, new_info: Dict[str, str | None]) -> bool:
        """
        Changes user's base information and updates it in the database.

        Args:
            new_info (Dict[str, str | None]): Dictionary containing new base information
                                               in format {'firstName': str, 'lastName': str, 'birthDate': datetime}.

        Returns:
            bool: True if uploading is successful
        """
        self.baseInfo.firstName = new_info['firstName']
        self.baseInfo.lastName = new_info['lastName']
        self.baseInfo.birthDate = new_info['birthDate']
        return self.baseInfo.upload_to_database_existing()

    def change_private_info(self, new_info: Dict[str, str | None]) -> bool:
        """
        Changes user's private information and updates it in the database.

        Args:
            new_info (Dict[str, str | None]): Dictionary containing new private information.

        Returns:
            bool: True if uploading is successful
        """
        return self.privateInfo.upload_to_database_existing(new_info)

    def change_credentials(self, new_info: Dict[str, str]) -> bool:
        """
        Changes user's credentials (login and password) and updates them in the database.

        Args:
            new_info (Dict[str, str]): Dictionary containing new credentials.

        Returns:
            bool: True if changing both login and password is successful
        """
        result_login = self.creds.update_login(new_info['login'])
        if result_login:
            result_password = self.creds.update_password(new_info['password'])
            return result_password
        return False


class Renter(User):
    def __init__(self, id: int | None = None, creds: Credential | None = None) -> None:
        """
        Initializes the Renter object with additional attributes.

        Args:
            id (int): Renter id.
        """
        super().__init__(id, creds)
        self.registrationDate: datetime | None = None
        self.driverLicenseDate: datetime | None = None
        self.canRent: bool = True

    def load_from_database(self) -> None:
        """
        Loads renter's information from the database.
        """
        if self.id is not None:

            cursor = connection.mysql_connection.cursor()
            self.load_base_info()
            self.load_private_info()
            query = f"SELECT registrationDate, driverLicenceDate FROM renter WHERE userId = {self.id}"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                self.registrationDate, self.driverLicenceDate = result
            else:
                print(f'Renter with id {self.id} not found in the database.')
            self.registrationDate = datetime.now().date()
            self.driverLicenceDate = datetime.now().date()

    def register(self, args: Dict[str, Dict[str, str]]) -> bool:
        """
        Registers a new renter and inserts their information into the database.

        Args:
            args (Dict[str, Dict[str, str]]): Dictionary containing information for registration.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        try:
            self.privateInfo = PrivateInfo()
            id = self.privateInfo.upload_to_database_new(args['privateInfo'])
            if id == -1:
                self.privateInfo = None
                raise ConnectionError("Error occurred when trying to add a new user to PrivateInfo table")

            self.id = id

            self.baseInfo = BaseInfo(
                self.id, args['baseInfo']['firstName'], args['baseInfo']['lastName'], args['baseInfo']['birthDate']
            )
            if not self.baseInfo.upload_to_database_new():
                raise ConnectionError("Error occurred when trying to add a new user to BaseInfo table")

            self.registrationDate = datetime.now().date()
            self.driverLicenseDate = args['driverLicenseDate']
            self.creds = Credential(args['credentials']['login'])
            if not self.creds.upload_to_database_new(args['credentials']['password'], self.id):
                raise ConnectionError("Error occurred when trying to add a new user to Credentials table")
            return True
        except Exception as e:
            print(f'Failed to load renter information from the database. Error: {e}')
            return False

    def count_driver_experience(self) -> datetime:
        """
        Calculates the driver's experience based on the current date and driver's license date.

        Returns:
            datetime: Driver's experience duration.
        """
        return datetime.now().date() - self.driverLicenseDate

    def count_time_in_system(self) -> int:
        """
        Calculates the time spent in the system based on the current date and registration date.

        Returns:
            datetime: Time in the system duration.
        """
        return datetime.now().date() - self.registrationDate

    def get_agreements(self) -> None:
        """
        Retrieves agreements from the Agreement document based on the user ID.
        """
        # Placeholder for actual implementation
        pass

    def set_rent_ability(self, val: bool) -> None:
        """
        Sets the rent ability status for the renter.

        Args:
            val (bool): Rental status.
        """
        self.canRent = val


class CompanyWorker(User):
    def __init__(self, id: int, creds: Credential | None = None) -> None:
        """
        Initializes the CompanyWorker object.
        """
        super().__init__(id, creds)
        self.position: str | None = None
        self.isActive: bool = True

    def load_from_database(self) -> None:
        """
        Loads worker's information from the database.
        """
        if self.id is not None:
            self.load_base_info()
            self.load_private_info()
            cursor = connection.mysql_connection.cursor()
            query = f"SELECT position, isActive FROM companyWorker WHERE userId = {self.id}"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                print(result)
                self.position, self.isActive = result
            self.position = 'MANAGER'


class LogIn:
    def __init__(self, login: str, password: str) -> None:
        """
        Enters the system by validating user credentials and loads information.

        Args:
            login (str): User login.
            password (str): Entered password.
        """
        self.creds: Credential = Credential(login, password)
        self.successful = False
        id: int | None = self.creds.get_id()
        if id is not None:
            self.successful = True
            # Determine the user type - client or employee
            if True:  # For now, all are clients
                self.user: Renter = Renter(id)
                self.user.load_from_database()
            else:
                self.user: CompanyWorker = CompanyWorker(id)
                self.user.load_from_database()



class Registration:
    def __init__(self, args: Dict[str, str]) -> None:
        """
        Initializes the Registration object with user information.

        Args:
            args (Dict[str, str]): Dictionary containing information for registration.
        """
        self.user: Renter = Renter()
        self.successful = False
        try:
            if not self.user.register(args):
                del self.user
                raise Exception
            self.successful = True
        except Exception as err:
            print(f'Can`t register.')


#user_birthdate = datetime(1990, 5, 15)
#base = BaseInfo(8)
#base.load_from_database()
#print(base.lastName)
#private = PrivateInfo(2)
#renter = Renter(3)
#renter.load_from_database()
#com = CompanyWorker(1)
#com.load_from_database()


