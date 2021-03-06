import datetime
from sqlalchemy import desc
from .akts import db
from akts.getfromfb import Fbticket

class Typeofequipment(object):
    types = {1:"Монитор",
                2:"ИБП",
                3:"Принтер",
                4:"Сканер",
                5:"МФУ",
                6:"Копир",
                7:"Факс",
                8:"АРМ",
                9:"Сервер",
                10:"Киоск",
                11:"АВФ",
                12:"Сетевое"}
    
    def get_type(self,id):
        return self.types[id]

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
    serviceprice = db.Column(db.Float)
    remark = db.Column(db.String(50))
    typeofequipment = db.Column(db.Integer)
    dead = db.Column(db.Boolean)
    akt_priemki = db.Column(db.Integer)

    # возвращает упорядоченный список номеров заявок в сц
    def serviceticketList(self):
        query = Tickets.query.with_entities(Tickets.serviceticket).\
            filter(Tickets.serviceprovider == 8).\
            order_by(Tickets.serviceticket).\
            group_by(Tickets.serviceticket).all()
        return [x.serviceticket for x in query]

        # возвращает упорядоченный список номеров актов премки
    def by_akt_priemki(self):
        query = Tickets.query.filter(Tickets.serviceprovider == 8).\
            filter(Tickets.akt_priemki != 0).\
            filter(Tickets.akt_priemki != None).\
            order_by(Tickets.akt_priemki).\
            group_by(Tickets.akt_priemki).all()
        return [item.akt_priemki for item in query]

    def shortlist(self, query):
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
                   'dead': x.dead} for x in query]
        for item in result:
            current_Location = Location.query.get(item['location'])
            current_Service_Provider = ServiceProvider.query.get(item['serviceprovider'])
            current_LowCourt = LowCourt.query.filter_by(code=item['lowcourtcode']).first()
            item['locationname'] = current_Location.name
            item['serviceprovidername'] = current_Service_Provider.name
            item['lowcourtname'] = current_LowCourt.name
        return result

    # Возвращает все заявки по номеру заявки в СЦ и коду сервиса
    def tiketsByTicket(self, serviceticket, serviceprovider):
        query = Tickets.query.filter((Tickets.serviceticket == serviceticket) and (Tickets.serviceprovider == serviceprovider)).order_by(
            Tickets.serviceakt).all()
        return Tickets.fullListFromQuery(query)

    # Возвращает все заявки по номеру акта премки
    def tiketsByAktPriemki(self, akt, serviceprovider):
        query = Tickets.query.filter((Tickets.akt_priemki == akt) and (Tickets.serviceprovider == serviceprovider)).\
            order_by(Tickets.akt_priemki).all()
        return Tickets.fullListFromQuery(query)

    def sumByAktPriemki(self, akt, serviceprovider):
        query = Tickets.query.filter((Tickets.akt_priemki == akt) and (Tickets.serviceprovider == serviceprovider)).\
            order_by(Tickets.akt_priemki).all()
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

    # По коду сервиса все выполненные ремонты.
    def byServiceproviderDone(self,serviceprovider):
        query = Tickets.query.filter(Tickets.serviceprovider.like(serviceprovider) & Tickets.aktco8mode.notilike(1) & Tickets.aktco8mode.notilike(7)).all()
        return Tickets.fullListFromQuery(query)

    # Все ремонты через ЗИП
    def bySpareParts(self):
        query = Tickets.query.filter(Tickets.serviceprovider.in_((2,3,4,5))).order_by(Tickets.localticket).all()
        return Tickets.fullListFromQuery(query)
    # Все ремонты через ЗИП выполненные
    def bySparePartsDone(self):
        query = Tickets.query.filter(Tickets.serviceprovider.in_((2,3,4,5)) & Tickets.aktco8mode.notilike(1) & Tickets.aktco8mode.notilike(7)).order_by(Tickets.localticket).all()
        return Tickets.fullListFromQuery(query)

    #Поиск по инв номеру или номеру заявки в филиале
    def seek(self,value):
        query = Tickets.query.filter(Tickets.localticket.contains(value) | Tickets.inventnumder.contains(value)).all()
        return Tickets.fullListFromQuery(query)

    def isLocalTicketExist(self, localticket):
        query = Tickets.query.filter(Tickets.localticket.like(localticket)).first()
        if query is None:
            return False
        else:
            return True
    def quantityofequipmenttype(self,typeofeq):
        query = Tickets.query.filter(Tickets.typeofequipment.like(typeofeq)  & Tickets.aktco8mode.notilike(1) & Tickets.aktco8mode.notilike(7)).count()
        return query

    # Все заявки
    def allTickets(self):
        query = Tickets.query.order_by(Tickets.localticket.desc()).all()
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
                 'dead': x.dead,
                 'akt_priemki': x.akt_priemki} for x in query]
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

def write_off(self):
    ''' Возвращает заявки по которым было списание '''
    pass
