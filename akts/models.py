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
    lowcourtcode = db.Column(db.String(8))
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
    warranty = db.Column(db.Boolean)
    dead = db.Column(db.Boolean)

    #возвращает упорядоченный список номеров заявок в сц
    def serviceticketList(self):
        query = Tickets.query.with_entities(Tickets.serviceticket).filter(Tickets.serviceticket != 0).order_by(
            Tickets.serviceticket).group_by(Tickets.serviceticket).all()
        return [x.serviceticket for x in query]

    def shortlist(query):
        result = [{'localticket': x.localticket,
                   'hotlineticket': x.hotlineticket,
                   'lowcourtcode': x.lowcourtcode,
                   'serviceprovider': x.serviceprovider,
                   'location': x.location,
                   'name': x.name,
                   'inventnumder': x.inventnumder,
                   'serialnumber': x.serialnumber,
                   'serviceticket': x.serviceticket,
                   'serviceakt': x.serviceakt,
                   'serviceprice': x.serviceprice,
                   'warranty': x.warranty,
                   'dead': x.dead} for x in query]
        for item in result:
            currentLocation = Location.query.get(item['location'])
            currentServiceProvider = ServiceProvider.query.get(item['serviceprovider'])
            currentLowCourt = LowCourt.query.filter_by(code=item['lowcourtcode']).first()
            item['locationname'] = currentLocation.name
            item['serviceprovidername'] = currentServiceProvider.name
            item['lowcourtname'] = currentLowCourt.name
        return result


    #Возвращает все заявки по номеру заявки в СЦ и коду сервиса
    def tiketsByTicket(self, serviceticket, serviceprovider):
        query = Tickets.query.filter((Tickets.serviceticket == serviceticket) and (Tickets.serviceprovider == serviceprovider)).order_by(
            Tickets.serviceakt).all()
        return Tickets.fullListFromQuery(query)

    # Выбор по конкретному суду
    def byLow(self,lowcourtcode):
        query = Tickets.query.filter(Tickets.lowcourtcode == lowcourtcode).order_by(Tickets.localticket).all()
        return Tickets.fullListFromQuery(query)

    # По месту нахождения ПТС
    def byLocation(self,location):
        query = Tickets.query.filter(Tickets.location == location).order_by(Tickets.localticket).all()
        return Tickets.fullListFromQuery(query)

    # По коду сервиса все ремонты.
    def byServiceprovider(self,serviceprovider):
        query = Tickets.query.filter(Tickets.serviceprovider == serviceprovider).order_by(Tickets.localticket).all()
        return Tickets.fullListFromQuery(query)

    # Все заявки
    def allTickets(self):
        query = Tickets.query.order_by(Tickets.localticket).all()
        return Tickets.fullListFromQuery(query)

    # Из результата запроса получаем список справочников для передачи в HTML
    def fullListFromQuery(query):
        result = [{'localticket': x.localticket,
                 'hotlineticket': x.hotlineticket,
                 'aktco7mode': x.aktco7mode,
                 'aktco7date': x.aktco7date,
                 'aktco8mode': x.aktco8mode,
                 'aktco8date': x.aktco8date,
                 'aktco41mode': x.aktco41mode,
                 'aktco42mode': x.aktco42mode,
                 'lowcourtcode': x.lowcourtcode,
                 'serviceprovider': x.serviceprovider,
                 'serviceproviderdate': x.serviceproviderdate,
                 'location': x.location,
                 'locationdate': x.locationdate,
                 'name': x.name,
                 'inventnumder': x.inventnumder,
                 'serialnumber': x.serialnumber,
                 'serviceticket': x.serviceticket,
                 'serviceakt': x.serviceakt,
                 'serviceprice': x.serviceprice,
                 'remark': x.remark,
                 'warranty': x.warranty,
                 'dead': x.dead} for x in query]
        for item in result:
            currentAct7Mode = ActMode.query.get(item['aktco7mode'])
            currntAct8Mode = ActMode.query.get(item['aktco8mode'])
            currntAct41Mode = ActMode.query.get(item['aktco41mode'])
            currntAct42Mode = ActMode.query.get(item['aktco42mode'])
            currentLocation = Location.query.get(item['location'])
            currentServiceProvider = ServiceProvider.query.get(item['serviceprovider'])
            currentLowCourt = LowCourt.query.filter_by(code=item['lowcourtcode']).first()
            item['aktco7modename'] = currentAct7Mode.name
            item['aktco8modename'] = currntAct8Mode.name
            item['aktco41modename'] = currntAct41Mode.name
            item['aktco42modename'] = currntAct42Mode.name
            item['locationname'] = currentLocation.name
            item['serviceprovidername'] = currentServiceProvider.name
            item['lowcourtname'] = currentLowCourt.name
        return result

