from akts import db
from akts import models
from akts.getfromfb import Fbticket
import datetime

db.create_all()

list = ['Не определен', 'Подготовлен в эл. виде', 'На подписании в ОА', 'На подписании в УСД ',
        'На подписании в филиале', 'Полностью подписан']
for item in list:
    itemname = models.ActMode(name=item)
    db.session.add(itemname)

list = ['Не определено', 'На ОА, еще не привезли', 'В филиале на диагностике', 'В сервисном центре',
        'Отремонтирован находится в филиале', 'Отремонтирован отдан на ОА', 'Отдан неотремонтированным']
for item in list:
    itemname = models.Location(name=item)
    db.session.add(itemname)

list = ['Не определен', 'ЗИП 2015', 'ЗИП 2016', 'ЗИП 2017', 'ЗИП 404 договор', 'без затрат', 'Корекс', 'Актион 751']
for item in list:
    itemname = models.ServiceProvider(name=item)
    db.session.add(itemname)

list = [['', 'Не определен'],
        ['45RS0001', 'Альменевский районный суд'],
        ['45RS0002', 'Белозерский районный суд'],
        ['45RS0003', 'Варгашинский районный суд'],
        ['45RS0004', 'Далматовский районный суд'],
        ['45RS0005', 'Звериноголовский районный суд'],
        ['45RS0006', 'Каргапольский районный суд'],
        ['45RS0007', 'Катайский районный суд'],
        ['45RS0008', 'Кетовский районный суд'],
        ['45RS0009', 'Куртамышский районный суд'],
        ['45RS0010', 'Лебяжьевский районный суд'],
        ['45RS0011', 'Макушинский районный суд'],
        ['45RS0012', 'Мишкинский районный суд'],
        ['45RS0013', 'Мокроусовский районный суд'],
        ['45RS0014', 'Притобольный районный суд'],
        ['45RS0015', 'Петуховский районный суд'],
        ['45RS0016', 'Половинский районный суд'],
        ['45RS0017', 'Сафакулевский районный суд'],
        ['45RS0018', 'Целинный районный суд'],
        ['45RS0021', 'Шадринский районный суд'],
        ['45RS0022', 'Шатровский районный суд'],
        ['45RS0023', 'Шумихинский районный суд'],
        ['45RS0024', 'Щучанский районный суд'],
        ['45RS0025', 'Юргамышский районный суд'],
        ['45RS0026', 'Курганский городской суд'],
        ['45UD0000', 'УСД в Курганской области'],
        ['45OS0000', 'Курганский областной суд'],
        ['45AS0034', 'Арбитражный суд Курганской области'],
        ['45IC0000', 'филиал ФГБУ ИАЦ Судебного департамента в Курганской области']
        ]
for item in list:
    db.session.add(models.LowCourt(code=item[0], name=item[1]))

fbTicket = Fbticket()
if fbTicket.getbylocalticket(4):
        db.session.add(models.Tickets(localticket=fbTicket.ticket['localticket'],
                                      hotlineticket=fbTicket.ticket['hotlineticket'],
                                      aktco7mode=fbTicket.ticket['aktco7mode'],
                                      aktco7changedate=fbTicket.ticket['aktco7changedate'],
                                      aktco7date=fbTicket.ticket['aktco7date'],
                                      aktco8mode=fbTicket.ticket['aktco8mode'],
                                      aktco8changedate=fbTicket.ticket['aktco8changedate'],
                                      aktco8date=fbTicket.ticket['aktco8date'],
                                      aktco41mode=fbTicket.ticket['aktco41mode'],
                                      aktco42mode=fbTicket.ticket['aktco42mode'],
                                      lowcourtcode=fbTicket.ticket['lowcourtcode'],
                                      serviceprovider=fbTicket.ticket['serviceprovider'],
                                      serviceproviderdate=fbTicket.ticket['serviceproviderdate'],
                                      location=fbTicket.ticket['location'],
                                      locationdate=fbTicket.ticket['locationdate'],
                                      name=fbTicket.ticket['name'],
                                      inventnumder=fbTicket.ticket['inventnumder'],
                                      serialnumber=fbTicket.ticket['serialnumber'],
                                      serviceticket=fbTicket.ticket['serviceticket'],
                                      serviceakt=fbTicket.ticket['serviceakt'],
                                      serviceprice=fbTicket.ticket['serviceticket'],
                                      remark=fbTicket.ticket['remark']))

db.session.commit()