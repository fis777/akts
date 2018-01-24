from akts import app
from akts import models
from akts import db
from akts import getfromfb
from flask import render_template, flash, redirect, url_for, request
import datetime

#строку которую возвращает HTML форма конвертируем в datetime.date
def strToDate(str):
    return datetime.date(int(str[0:4]),int(str[5:7]),int(str[8:10]))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template("index.html")

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
        return redirect(url_for('list'))
    return render_template("addticket.html")

@app.route('/edit/<local>', methods=['GET', 'POST'])
def edit(local):
    actmode = models.ActMode()
    listmode = [{'val': actmode.id, 'name' : actmode.name} for actmode in models.ActMode.query.all()]
    ticket = models.Tickets.query.filter_by(localticket = local).first()
    if request.method == 'POST':
        ticket.hotlineticket = request.form['hotlineticket']
        ticket.aktco7mode = request.form.get('aktco7mode')
        ticket.aktco7date = strToDate(request.form['aktco7date'])
        db.session.commit()
        return redirect(url_for('list'))
    return render_template("edit.html",ticket = ticket,listmode = listmode)

@app.route('/getticket', methods=['GET', 'POST'])
def getticket():
    if request.method == 'POST':
        localticket = request.form['localticket']
        return redirect(url_for('edit', local = localticket))
    return render_template("get_ticket_for_edit.html")

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
             'remark': x.remark} for x in models.Tickets.query.all()]
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
    return render_template('list.html',list=list)

