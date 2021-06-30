# some resource: https://wiki.postgresql.org/wiki/Psycopg2_Tutorial
# was renamed from psycopg
# todo: add the alter table to add new columns, if they not in colnames
import psycopg2 as pg2
from api_pull import pullData


def colSlug(preCol):
    out = ""
    preCol = str(preCol)
    for i in preCol:
        if i==" ":
            out += "_"
        elif i=="-":
            out += "_"
        else:
            out += i
    return out


secret = 'password'

conn = pg2.connect(database='nutrition', user='postgres', password=secret)

cur = conn.cursor()

cur.execute("Select * FROM nutrition_facts LIMIT 0")
colnames = [desc[0] for desc in cur.description]


# Get the data
productName, productBrand, barcode, productNutrients = pullData()
productName = colSlug(productName)
productBrand = colSlug(productBrand)
print("product name: " + productName)

# Update if any new columns
for col in productNutrients:
    col = colSlug(col)  # new
    if ("100g" in col) and (col not in colnames) and ('kcal' not in col) and ('kj' not in col):
        new_query = "ALTER TABLE nutrition_facts ADD COLUMN {} VARCHAR(10)".format(col)
        # print(new_query)
        # test for alter table.. .
        cur.execute(new_query)
        print("column added")

# update the table
conn.commit()

# Insert the data
constantInsert = "INSERT INTO nutrition_facts(product_name, brand, barcode) VALUES('{}', '{}', '{}');".format(productName, productBrand, barcode)
cur.execute(constantInsert)

# update the table
conn.commit()

variableInsert = "UPDATE nutrition_facts SET {} ='{}' WHERE product_name='{}'"
for col in productNutrients.keys():
    #print("main.py: line54: " +col)
    tempSlug = colSlug(col)  # new
    if ("100g" in col) and ("kcal" not in col) and ("kj" not in col):
        #print(col)  # test 5
        #print(tempSlug)  # test 4
        theSplits = tempSlug.split("_")

        unit = ""

        for j in productNutrients.keys():
            if (theSplits[0] in j) and ("unit" in j):
                unit = productNutrients[j]
            else:
                pass

        tempNutrients = str(productNutrients[col])
        #print(type(tempNutrients))  # test 3
        slugNutrients = colSlug(tempNutrients) + unit
        #print("main.py: line66: "+productName)
        #print("tempSlug: " + tempSlug)
        #print("slugNutrients: " + slugNutrients)
        #print("productName: " + productName)
        tempInsert = variableInsert.format(tempSlug, slugNutrients, productName)  # slugNutrients vs
        cur.execute(tempInsert)
        # update the table
conn.commit()

cur.close()
conn.close()




# -------------------------------------------------------------
# Deprecated                                                  |
# -------------------------------------------------------------
# test for colnames: for col in colnames: print(type(col))

# cur.execute('SELECT * FROM nutrition_facts')
#cur.fetchone()
#for row in cur.fetchmany(3):
#    print("")
#    print(row)
#-----------------------------------------------------------

