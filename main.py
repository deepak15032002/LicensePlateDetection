import mysql.connector
import time
res2 = []
count = 0

def fun2(s):
    res = []
    String = ""
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="license_plate"
    )


    query = "select * from license_plate.new_table where license_number = '{qu}';".format(qu=s)
    print(query)
    cur = mydb.cursor()
    cur.execute(query)

    for col in cur:
        res.append(col[0])
        res.append(col[1])
        res.append(col[2])
        res.append(col[3])
        res.append(col[4])
        res.append(col[5])
        res.append(col[6])
        res.append(col[7])
        datetime_year = col[3]
        datetime_month = col[3]
        year = datetime_year.year
        month = datetime_month.month
        if year < time.gmtime().tm_year:
            print("Registration Expired : challan is processing on " + col[6])
            String += "Registration Expired : challan is processing on " + col[6] + ", "
        if year == time.gmtime().tm_year:
            if month < time.gmtime().tm_mon:
                print("Registration Expired : challan is processing on " + col[6])
                String += "Registration Expired : challan is processing on " + col[6] + ", "

        if col[4] == 0:
            print("PUC Expired : challan is processing on " + col[6])
            String += "PUC Expired : challan is processing on " + col[6] + ", "

        if col[7] == 0:
            print("Insurence Expired : challan is processing on " + col[6])
            String += "Insurence Expired : challan is processing on " + col[6] + ", "

        res.append(String)
        res2.append(res)