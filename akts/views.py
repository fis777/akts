from akts import app
from akts import models
from akts import db
from akts import getfromfb
from flask import render_template, flash, redirect, url_for, request
import datetime

#строку содержащую дату, которую возвращает HTML форма, конвертируем в datetime.date
def strToDate(str):
    return datetime.date(int(str[0:4]),int(str[5:7]),int(str[8:10]))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        localticket = request.form['ticket']
        fbTicket = getfromfb.Fbticket()
        if fbTicket.getbylocalticket(localticket):
            db.session.add(models.Tickets(localticket=fbTicket.ticket['localticket'],
                                          hotlineticket=fbTicket.ticket['hotlineticket'],
                                          aktco7mode=fbTicket.ticket['aktco7mode'],
                                          aktco7changedate = fbTicket.ticket['aktco7changedate'],
                                          aktco7date = fbTicket.ticket['aktco7date'],
                                          aktco8mode = fbTicket.ticket['aktco8mode'],
                                          aktco8changedate = fbTicket.ticket['aktco8changedate'],
                                          aktco8date = fbTicket.ticket['aktco8date'],
                                          aktco41mode = fbTicket.ticket['aktco41mode'],
                                          aktco42mode = fbTicket.ticket['aktco42mode'],
                                          lowcourtcode = fbTicket.ticket['lowcourtcode'],
                                          serviceprovider = fbTicket.ticket['serviceprovider'],
                                          serviceproviderdate = fbTicket.ticket['serviceproviderdate'],
                                          location = fbTicket.ticket['location'],
                                          locationdate = fbTicket.ticket['locationdate'],
                                          name = fbTicket.ticket['name'],
                                          inventnumder=fbTicket.ticket['inventnumder'],
                                          serialnumber=fbTicket.ticket['serialnumber'],
                                          serviceticket = fbTicket.ticket['serviceticket'],
                                          serviceakt = fbTicket.ticket['serviceakt'],
                                          serviceprice = fbTicket.ticket['serviceticket'],
                                          remark=fbTicket.ticket['remark']))
            db.session.commit()
        return redirect(url_for('lst'))
    return render_template("addticket.html")

@app.route('/edit/<local>', methods=['GET', 'POST'])
def edit(local):
    listlocation = [{'val': location.id, 'name' : location.name} for location in models.Location.query.all()]
    listmode = [{'val': actmode.id, 'name' : actmode.name} for actmode in models.ActMode.query.all()]
    listprovider = [{'val': provider.id, 'name' : provider.name} for provider in models.ServiceProvider.query.all()]
    listlow = [{'val': low.code, 'name' : low.name} for low in models.LowCourt.query.all()]
    ticket = models.Tickets.query.filter_by(localticket = local).first()
    if request.method == 'POST':
        ticket.aktco7mode = request.form.get('aktco7mode')
        ticket.aktco7date = strToDate(request.form['aktco7date'])
        ticket.aktco41mode = request.form.get('aktco41mode')
        ticket.aktco8mode = request.form.get('aktco8mode')
        ticket.aktco8date = strToDate(request.form['aktco8date'])
        ticket.aktco42mode = request.form.get('aktco42mode')
#        ticket.lowcourtcode = request.form.get('lowcourtcode')
        ticket.serviceprovider = request.form.get('serviceprovider')
        ticket.location = request.form.get('location')
        ticket.name = request.form['name']
#        ticket.inventnumder = request.form['inventnumder']
#        ticket.serialnumber = request.form['serialnumber']
        ticket.serviceticket = int(request.form['serviceticket'])
        ticket.serviceakt = int(request.form['serviceakt'])
        ticket.serviceprice = float(request.form['serviceprice'])
#        ticket.remark = request.form['remark']
        db.session.commit()
        return redirect(url_for('lst'))
    return render_template("edit.html",ticket = ticket,listmode = listmode,listlow = listlow,listprovider = listprovider,listlocation = listlocation)

@app.route('/getticket', methods=['GET', 'POST'])
def getticket():
    if request.method == 'POST':
        localticket = request.form['localticket']
        return redirect(url_for('edit', local = localticket))
    return render_template("get_ticket_for_edit.html")

@app.route('/seek',methods=['GET', 'POST'])
def seek():
    if request.method == 'POST':
        inventnumder = request.form['inventnumder']
        list = [{'localticket': x.localticket,
                 'hotlineticket': x.hotlineticket,
                 'aktco7mode': x.aktco7mode,
                 'aktco7changedate': x.aktco7changedate,
                 'aktco7date': x.aktco7date,
                 'aktco8mode': x.aktco8mode,
                 'aktco8changedate': x.aktco8changedate,
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
                 'remark': x.remark} for x in models.Tickets.query.filter(models.Tickets.inventnumder.contains(inventnumder)).all()]
        for item in list:
            currentAct7Mode = models.ActMode.query.get(item['aktco7mode'])
            currntAct8Mode = models.ActMode.query.get(item['aktco8mode'])
            currntAct41Mode = models.ActMode.query.get(item['aktco41mode'])
            currntAct42Mode = models.ActMode.query.get(item['aktco42mode'])
            currentLocation = models.Location.query.get(item['location'])
            currentServiceProvider = models.ServiceProvider.query.get(item['serviceprovider'])
            currentLowCourt = models.LowCourt.query.filter_by(code=item['lowcourtcode']).first()
            item['aktco7modename'] = currentAct7Mode.name
            item['aktco8modename'] = currntAct8Mode.name
            item['aktco41modename'] = currntAct41Mode.name
            item['aktco42modename'] = currntAct42Mode.name
            item['locationname'] = currentLocation.name
            item['serviceprovidername'] = currentServiceProvider.name
            item['lowcourtname'] = currentLowCourt.name
        return render_template('list.html',list = list)
    return render_template("seek.html")


@app.route('/')
@app.route('/list')
def list():
    list = [{'localticket' : x.localticket,
             'hotlineticket': x.hotlineticket,
             'aktco7mode': x.aktco7mode,
             'aktco7changedate': x.aktco7changedate,
             'aktco7date': x.aktco7date,
             'aktco8mode': x.aktco8mode,
             'aktco8changedate': x.aktco8changedate,
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
             'remark': x.remark} for x in models.Tickets.query.order_by('localticket').all()]
    for item in list:
        currentAct7Mode = models.ActMode.query.get(item['aktco7mode'])
        currntAct8Mode = models.ActMode.query.get(item['aktco8mode'])
        currntAct41Mode = models.ActMode.query.get(item['aktco41mode'])
        currntAct42Mode = models.ActMode.query.get(item['aktco42mode'])
        currentLocation = models.Location.query.get(item['location'])
        currentServiceProvider = models.ServiceProvider.query.get(item['serviceprovider'])
        currentLowCourt = models.LowCourt.query.filter_by(code = item['lowcourtcode']).first()
        item['aktco7modename'] = currentAct7Mode.name
        item['aktco8modename'] = currntAct8Mode.name
        item['aktco41modename'] = currntAct41Mode.name
        item['aktco42modename'] = currntAct42Mode.name
        item['locationname'] = currentLocation.name
        item['serviceprovidername'] = currentServiceProvider.name
        item['lowcourtname'] =  currentLowCourt.name
    return render_template('list.html',list = list)


@app.route('/lst')
def lst():
    tickets = models.Tickets()
    lst = tickets.allTickets()
    return render_template('lst.html',list = lst)


@app.route('/reportservice')
def reportservice():
    tickets = models.Tickets()
    result = []  # Полный список заявок в СЦ для вывода в HTML
    resultsum = []
    resultsumall = 0
    # Получаем номера всех заявок
    slist = tickets.serviceticketList()
    for item in slist:
        # Получаем все акты тс по одной заявке
        stlist = tickets.tiketsByTicket(item, 8)
        summa = 0
        for s in stlist:
            result.append(s)
            summa += s['serviceprice']
        resultsumall += summa
        resultsum.append({'serviceticket': item, 'summa': summa})
    return render_template('reportservice.html',result = result, resultsum = resultsum, resultsumall = resultsumall)

@app.route('/reportbyservice')
def reportbyservice():
    tickets = models.Tickets()
    report = {}

    #Актион 751
    result = tickets.byServiceprovider(8)
    report['action751'] = result.__len__()
    itog = 0
    for foo in result:
        if foo['aktco8mode'] != 1:
            itog += 1
    report['action751done'] = itog

    #Без денег
    result = tickets.byServiceprovider(6)
    report['nomoney'] = result.__len__()
    itog = 0
    for foo in result:
        if foo['aktco8mode'] != 1:
            itog += 1
    report['nomoneydone'] = itog

    # ЗИП 15
    result = tickets.byServiceprovider(2)
    report['zip'] = result.__len__()
    itog = 0
    for foo in result:
        if foo['aktco8mode'] != 1:
            itog += 1
    report['zipdone'] = itog

    # ЗИП 16
    result = tickets.byServiceprovider(3)
    report['zip'] += result.__len__()
    itog = 0
    for foo in result:
        if foo['aktco8mode'] != 1:
            itog += 1
    report['zipdone'] += itog

    # ЗИП 17
    result = tickets.byServiceprovider(4)
    report['zip'] += result.__len__()
    itog = 0
    for foo in result:
        if foo['aktco8mode'] != 1:
            itog += 1
    report['zipdone'] += itog

    # ЗИП 404
    result = tickets.byServiceprovider(5)
    report['zip'] += result.__len__()
    itog = 0
    for foo in result:
        if foo['aktco8mode'] != 1:
            itog += 1
    report['zipdone'] += itog

    #Без денег
    result = tickets.byServiceprovider(1)
    report['nodefine'] = result.__len__()

    return render_template('byservice.html',report = report)




