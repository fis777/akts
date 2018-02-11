#from akts import db
from akts.models import Tickets
#from akts.getfromfb import Fbticket
#import datetime

#def factory(aClass, *args):
#    return aClass(*args)

#query = Tickets.query.filter((Tickets.serviceticket == 1) and (Tickets.serviceprovider == 8)).order_by(
#            Tickets.serviceakt).all()

tickets = Tickets()
res = tickets.allTickets()
print(res)

'''
tickets = Tickets()
result=[] # Полный список заявок в СЦ для вывода в HTML
resultsum=[]
resultsumall = 0
#Получаем номера всех заявок
slist = tickets.serviceticketList()

for item in slist:
    #Получаем все акты тс по одной заявке
    stlist = tickets.tiketsByTicket(item,8)
    summa = 0
    for s in stlist:
        result.append(s)
        summa += s['serviceprice']
    resultsumall += summa
    resultsum.append({'serviceticket': item, 'summa': summa})

for xlist in result:
    print(xlist['inventnumder'],xlist['serviceakt'],xlist['serviceticket'],xlist['serviceprice'])
for s in resultsum:
    print(s['serviceticket'],s['summa'])
print(resultsumall)

#for x in query:
#    if x.serviceticket not in serviceticketlist:
#        serviceticketlist.append(x.serviceticket)
#    index = serviceticketlist.index(x.serviceticket)
#    serviceticketlist[index][] = {'name': x.name ,
#                                'inventnumder': x.inventnumder,
#                                'serialnumber': x.serialnumber,
#                                'serviceticket': x.serviceticket,
#                                'serviceakt': x.serviceakt,
#                                'serviceprice': x.serviceprice}



#for i in serviceticketlist:
#    print(i['name'] + ' ' + i['inventnumder'] + ' ' + str(i['serviceticket']) +' ' + str(i['serviceakt']) +' ' + str(i['serviceprice']))

'''