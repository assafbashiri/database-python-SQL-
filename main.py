
import sqlite3
import sys
import datetime
from data import supplier
from data import vaccine
from data import clinic
from data import logistic

from repository import repository

if __name__ == '__main__':


    # CREATE THE TABLES IN REPOSITORY
    repository = repository()
    repository.create_tables()

    # READ THE config
    file1 = open(sys.argv[1], 'r')
    config = file1.read()
    lines = config.split("\n")
    line1 = lines[0].split(",")
    vaccinesNum = int(line1[0])
    supplierNum = int(line1[1])
    clinicsNum = int(line1[2])
    logisticsNum = int(line1[3])
    numOfLine=1

    #VACCINES
    for i in range(0,vaccinesNum):
        lineVaccines = lines[numOfLine].split(",")
        vaccine1 =vaccine(int(lineVaccines[0]),lineVaccines[1],int(lineVaccines[2]),int(lineVaccines[3]))
        repository.addVaccine(vaccine1)
        numOfLine = numOfLine+1

    #SUPPLIER
    for i in range(0,supplierNum):
        lineSupplier = lines[numOfLine].split(",")
        supplier1 =supplier(int(lineSupplier[0]),lineSupplier[1],int(lineSupplier[2]))
        repository.addSupplier(supplier1)
        numOfLine = numOfLine+1

    #CLINICS
    for i in range(0,clinicsNum):

        lineClinics = lines[numOfLine].split(",")
        clinic1 =clinic(int(lineClinics[0]),lineClinics[1],int(lineClinics[2]),int(lineClinics[3]))
        repository.addClinic(clinic1)
        numOfLine = numOfLine+1

    #LOGISTICS
    for i in range(0,logisticsNum):
        lineLogistics = lines[numOfLine].split(",")
        logistics1=logistic(int(lineLogistics[0]), lineLogistics[1], int(lineLogistics[2]),int(lineLogistics[3]))
        repository.addLogistic(logistics1)
        numOfLine = numOfLine+1

#END OF READING CONFIG
    file1.close()

#READ THE ORDERS
    toReturn = ""
    file2 = open(sys.argv[2], 'r')
    ordersLines = file2.read()

    ordersLines = ordersLines.split("\n")
    indexLine = 0

    #read orders from file
    numOfLines = len(ordersLines)
    for i in range(0, numOfLines):
        order_i = ordersLines[indexLine].split(",")
        # ReceiveShipment
        if len(order_i) == 3:
            repository.receiveShipment(order_i[0], int(order_i[1]), order_i[2])
            toReturn = toReturn + repository.detail() + '\n'
        # SendShipment
        elif len(order_i)==2:
            repository.sendShipment(order_i[0], int(order_i[1]))
            toReturn = toReturn + repository.detail()+'\n'

        indexLine = indexLine + 1

#WRITE TO THE OUTPUT FILE
    outputFile = open(sys.argv[3], 'w')
    outputFile.write(toReturn)
    outputFile.close()
    repository._close()
