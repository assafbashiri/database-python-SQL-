
#the classes

#supplier
class supplier:
    def __init__(self, ID, name, logistic):
        self.id = ID
        self.name = name
        self.logistic = logistic

#logistic
class logistic:
    def __init__(self, ID, name, countsent, countreceived):
        self.id = ID
        self.name = name
        self.count_sent = countsent
        self.count_received = countreceived

#vaccine
class vaccine:
    def __init__(self, ID, date, supplier, quantity):
        self.id = ID
        self.date = date
        self.supplier = supplier
        self.quantity = quantity

#clinic
class clinic:
    def __init__(self, ID, location, demand, logistic):
        self.id = ID
        self.location = location
        self.demand = demand
        self.logistic = logistic

