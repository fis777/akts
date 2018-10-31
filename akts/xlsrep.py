import xlrd
import sqlite3

rb = xlrd.open_workbook('111.xlsx')

def foo():
    for rownum in range(sheet.nrows):
        yield sheet.row_values(rownum)

#Суды общей юрисдикцмм
sheet = rb.sheet_by_index(0)
iac = {int(row[7].split("-")[2]): {"ticket": row[7].split("-")[2], "oa": row[2],"name": row[3], "invent": row[4].split("\n")} for row in foo()}

#Областной суд
sheet = rb.sheet_by_index(1)
for row in foo():
    iac[int(row[7].split("-")[2])] = {"ticket": row[7].split("-")[2], "oa": row[2],"name": row[3], "invent": row[4].split("\n")}

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('SELECT localticket, name, serialnumber FROM tickets')
result = cursor.fetchall()
conn.close()
rem = {row[0]:{"ticket": row[0], "name": row[1],"serial": row[2]} for row in result}

print("not in rem")
for key in iac.keys():
    if key not in rem.keys():
        print(iac[key]) 

print("not in iac")
for key in rem.keys():
    if key not in iac.keys():
        print(rem[key])
