import sqlite3

from dataFunction import clinics
from dataFunction import logistics
from dataFunction import suppliers
from dataFunction import vaccines
from data import vaccine

class repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._suppliers = suppliers(self._conn)
        self._vaccines = vaccines(self._conn)
        self._logistics = logistics(self._conn)
        self._clinics = clinics(self._conn)

#create the tabels for SQL
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS logistics (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                count_sent INTEGER NOT NULL,
                count_received INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS clinics (
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                demand INTEGER NOT NULL,
                logistic INTEGER REFERENCES logistics(id)
            );
            CREATE TABLE IF NOT EXISTS vaccines (
                id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                supplier INTEGER REFERENCES suppliers(id),
                quantity INTEGER NOT NULL 
            );
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                logistic INTEGER REFERENCES logistics(id)
            );
        """)

    def addClinic(self, clinic):
        self._clinics.add(clinic)

    def addLogistic(self, logistic):
        self._logistics.add(logistic)

    def addSupplier(self, supplier):
        self._suppliers.add(supplier)

    def addVaccine(self, vaccine):
        self._vaccines.add(vaccine)



    def sendShipment(self, location, amount):
        self._clinics.sendDemand(location, amount)
        self._vaccines.reduceAmount(amount)
        logisticId = self._clinics.logisticId(location)
        self._logistics.updateSent(logisticId, amount)

    def receiveShipment(self, name, amount, date):
        supplier = self._suppliers.idName(name)
        vaccineId = self._vaccines.nextId()
        vaccine1 = vaccine(vaccineId, date, supplier, amount)
        self._vaccines.add(vaccine1)
        logisticId = self._suppliers.logisticName(name)
        self._logistics.updateReceived(logisticId, amount)


    def detail(self):
        output = str(self._vaccines.totalAmount()) + ','
        output = output + str(self._clinics.demands()) + ','
        output = output + str(self._logistics.receivedTotal()) + ','
        output = output + str(self._logistics.sendTotal())
        return output

    def _close(self):
        self._conn.commit()
        self._conn.close()
