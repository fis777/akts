import datetime
from akts import db
from akts.getfromfb import Fbticket

class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

class ActMode(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

class ServiceProvider(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

class LowCourt(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(8))

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localticket = db.Column(db.Integer)
    hotlineticket = db.Column(db.Integer)
    aktco7mode = db.Column(db.Integer)
    aktco7changedate = db.Column(db.Date)
    aktco7date = db.Column(db.Date)
    aktco8mode = db.Column(db.Integer)
    aktco8changedate = db.Column(db.Date)
    aktco8date = db.Column(db.Date)
    aktco41mode = db.Column(db.Integer)
    aktco42mode = db.Column(db.Integer)
    lowcourtcode = db.Column(db.Integer)
    serviceprovider = db.Column(db.Integer)
    serviceproviderdate = db.Column(db.Date)
    location = db.Column(db.Integer)
    locationdate = db.Column(db.Date)
    name = db.Column(db.String(50))
    inventnumder = db.Column(db.String(12))
    serialnumber = db.Column(db.String(12))
    serviceticket = db.Column(db.Integer)
    serviceakt = db.Column(db.Integer)
    serviceprice =  db.Column(db.Float)
    remark = db.Column(db.String(50))

