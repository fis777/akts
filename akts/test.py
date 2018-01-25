from akts import db
from akts import models
#from akts.getfromfb import Fbticket
#import datetime

listlow = [{'val': low.code, 'name': low.name} for low in models.LowCourt.query.all()]

for act in listlow:
    print(act['val'] + act['name'])


