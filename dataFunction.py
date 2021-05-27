

class suppliers:
    #constructor
    def __init__(self, conn):
        self._conn = conn

    def add(self, supplier):
        self._conn.execute("""INSERT INTO suppliers (id, name,logistic) VALUES (?, ?,?)""",
                           [supplier.id, supplier.name, supplier.logistic])


    def logisticName(self, name):
        this = self._conn.cursor()
        this.execute("SELECT logistic FROM suppliers WHERE suppliers.name=?", [name])
        output = this.fetchone()[0]

        return output

    def idName(self, name):
        this = self._conn.cursor()
        this.execute("SELECT id FROM suppliers WHERE suppliers.name=?", [name])
        output = this.fetchone()[0]

        return output


class logistics:
    # constructor
    def __init__(self, conn):
        self._conn = conn

    def add(self, logistic):
        self._conn.execute("""INSERT INTO logistics (id, name,count_sent,count_received) VALUES (?,?,?,?)""", [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])


    def receivedTotal(self):
        this = self._conn.cursor()
        this.execute("SELECT SUM(count_received) FROM logistics")
        total = this.fetchone()[0]

        return total

    def sendTotal(self):
        this = self._conn.cursor()
        this.execute("SELECT SUM(count_sent) FROM logistics")
        total = this.fetchone()[0]

        return total

    def updateReceived(self, id, num):
        this = self._conn.cursor()
        current = this.execute("SELECT count_received FROM logistics WHERE id=?", [id]).fetchone()[0]
        this.execute("UPDATE logistics set count_received = ? WHERE id=?", [num + current, id])


    def updateSent(self, id, num):
        this = self._conn.cursor()
        current = this.execute("SELECT count_sent FROM logistics WHERE id=?", [id]).fetchone()[0]
        this.execute("UPDATE logistics set count_sent = ? WHERE id=?", [num + current, id])






class vaccines:
    # constructor
    def __init__(self, conn):
        self._conn = conn


    def add(self, vaccine):
        self._conn.execute("""INSERT INTO vaccines (id, date,supplier,quantity) VALUES (?,?,?,?)""", [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])


    def nextId(self):
        this = self._conn.cursor()
        this.execute("SELECT MAX(id) FROM vaccines")
        output = this.fetchone()[0]

        return output+1

    def totalAmount(self):
        this = self._conn.cursor()
        this.execute("SELECT SUM(quantity) FROM vaccines")
        total = this.fetchone()[0]

        return total

    def reduceAmount(self, amountToReduce):
        this = self._conn.cursor()
        amount = amountToReduce
        check = True
        while check:
            quantity = this.execute("SELECT quantity FROM vaccines WHERE (SELECT MIN(date) FROM vaccines)=date").fetchone()[ 0]
            id = this.execute("SELECT id FROM vaccines WHERE (SELECT MIN(date) FROM vaccines)=date").fetchone()[0]
            this.execute("UPDATE vaccines SET quantity = ? WHERE id=?", [quantity - amount, id])
            if quantity - amount < 0:
                this.execute("DELETE FROM vaccines WHERE id=?", [id])
                amount = amount - quantity
            elif quantity - amount == 0:
                this.execute("DELETE FROM vaccines WHERE id=?",[id])
                self._conn.commit()
                check = False
            else:
                check = False


class clinics:
    # constructor
    def __init__(self, conn):
        self._conn = conn

    def add(self, clinic):
        self._conn.execute("""INSERT INTO clinics (id, location,demand,logistic) VALUES (?,?,?,?)""",
                           [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def demands(self):
        this = self._conn.cursor()
        this.execute("SELECT SUM(demand) FROM clinics")
        demand = this.fetchone()[0]

        return demand


    def sendDemand(self, city, num):
        this = self._conn.cursor()
        demand = this.execute("SELECT demand FROM clinics WHERE location=?", [city]).fetchone()[0]
        this.execute("UPDATE clinics set demand = ? WHERE location = ?", [demand - num, city])

    def logisticId(self, city):
        this = self._conn.cursor()
        this.execute("SELECT logistic FROM clinics WHERE clinics.location=?", [city])
        ID = this.fetchone()[0]

        return ID

