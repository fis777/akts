from akts import db
from akts import models
#from akts.getfromfb import Fbticket
#import datetime
inventnumder ='1321401'
s =  models.Tickets.query.filter(models.Tickets.inventnumder.contains('1321401')).all()
print(s)
