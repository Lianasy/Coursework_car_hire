import copy
from datetime import datetime


class BaseInfo:
    def __init__(self, id, firstName=None, lastName=None, birthDate=None):
        self.userId = id
        self.firstName = firstName
        self.lastName = lastName
        self.birthDate = birthDate

    def upload_base_info(self):
        # Загрузка данных в бд
        pass


class Credential:
    def __init__(self, login, password):
        self.login = login
        self.password_to_validate = password

    def get_id(self):
        if self.__to_valid_password():
            # Получить ID по логину
            pass
        else:
            return None

    def __get_password(self):
        # Найти пароль по логину
        pass

    def __to_valid_password(self):
        return self.__get_password() == self.password_to_validate


class PrivateInfo:
    def __init__(self, id):
        self.__id = id
        self.__photo = None
        self.__passportId = None
        self.__phoneNumber = None
        self.__email = None
        self.__driverLicence = None

    def get_private_info(self):
        # Загрузка приватной информации из privateInfo table по id
        return copy.deepcopy(self.__dict__)

    def upload_private_info(self, args):
        # Загрузка args в бд
        del args


class User:
    def __init__(self):
        self.id = None
        self.baseInfo = None
        self.privateInfo = None
        self.creds = None

    def enter_system(self, login, password):
        self.creds = Credential(login, password)
        id = self.creds.get_id()
        if id is not None:
            self.id = id
            self.load_private_info()
            self.load_base_info()

    def load_private_info(self):
        if self.id is not None:
            self.privateInfo = PrivateInfo(self.id)

    def load_base_info(self):
        if self.id is not None:
            self.baseInfo = BaseInfo(self.id)


class Renter(User):
    def __init__(self):
        super().__init__()
        self.registrationDate = None
        self.driverLicenseDate = None

    def enter_system_as_renter(self, login, password):
        self.enter_system(login, password)
        # Получение registrationDate, driverLicenseDate из таблицы Renter по id

    def register(self, args):
        # Внесение введенных данных в таблицы
        # Получение id как хз
        # self.baseInfo = BaseInfo(self.id, firstName, lastName, birthDate) - из args или BaseInfo(self.id) из бд
        self.privateInfo = PrivateInfo(self.id)
        self.registrationDate = datetime.now().date()
        # self.driverLicenceDate взять из args

    def count_driver_experience(self):
        return datetime.now().date() - self.driverLicenseDate

    def count_time_in_system(self):
        return datetime.now().date() - self.registrationDate

    def get_agreements(self):
        # Получение договоров из Agreement doc по id
        pass


class CompanyWorker(User):
    def __init__(self):
        super().__init__()
        self.position = None
        self.isActive = None

    def enter_system_as_worker(self, login, password):
        self.enter_system(login, password)
        # Получение position, isActive из таблицы companyWorker по id


class Driver(Renter):
    def get_rent_controller(self):
        # Логика для возврата экземпляра RentController
        pass


class UnverifiedDriver(Renter):
    pass
