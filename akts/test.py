from akts import db
from akts import models
#from akts.getfromfb import Fbticket
#import datetime

listmode = [{'val': actmode.id, 'name' : actmode.name} for actmode in models.Tickets.query.all()]

for act in listmode:
    print(act['name'])


