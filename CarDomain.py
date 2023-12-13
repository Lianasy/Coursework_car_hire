class Car:
    def __init__(self, carId):
        self.carId = None
        self.carNumber = None
        self.carModel = None
        self.rentPrice = None
        self.rentStatus = None
        self.carType = None
        self.documents = None

    def getId(self):
        return self.carId

    def setRentStatus(self, newRentStatus):
        self.rentStatus = newRentStatus

    def addDocument(self, document):
        self.documents.append(document)


class CarDocument:
    def __init__(self, carId):
        self.carId = carId
        self.documentLocation = None

    def getCarId(self):
        return self.carId

    def getDocumentLocation(self):
        return self.documentLocation