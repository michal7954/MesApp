def printTable(table, total, decimal):
    for row in table:
        rowPrintable = ""
        for element in row:
            rowPrintable += "{:{:}.{:}f}".format(element, total, decimal)
        print(rowPrintable)
