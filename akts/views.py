import datetime
from flask import render_template, redirect, url_for, request
from akts import getfromfb
from akts import models
from .akts import db
from .akts import app


#строку содержащую дату, которую возвращает HTML форма, конвертируем в datetime.date
def strToDate(st):
    return datetime.date(int(st[0:4]), int(st[5:7]), int(st[8:10]))


@app.route('/add', methods=['GET', 'POST'])
#добавляем заявку из ИС ИАЦ
def add():
    if request.method == 'POST':
        localticket = request.form['ticket']
        #Проверяем есть ли уже такая заявка
        ticket = models.Tickets()
        if ticket.isLocalTicketExist(localticket):
            return redirect(url_for('lst'))
        fbTicket = getfromfb.Fbticket()
        if fbTicket.getbylocalticket(localticket):
            db.session.add(models.Tickets(localticket=fbTicket.ticket['localticket'],
                                          hotlineticket=fbTicket.ticket['hotlineticket'],
                                          aktco7mode=fbTicket.ticket['aktco7mode'],
                                          aktco7changedate=fbTicket.ticket['aktco7changedate'],
                                          aktco7date=fbTicket.ticket['aktco7date'],
                                          aktco8mode=fbTicket.ticket['aktco8mode'],
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
        ticket.serviceprovider = request.form.get('serviceprovider')
        ticket.location = request.form.get('location')
        ticket.name = request.form['name']
        ticket.serviceticket = int(request.form['serviceticket'])
        ticket.serviceakt = int(request.form['serviceakt'])
        ticket.serviceprice = float(request.form['serviceprice'])
        db.session.commit()
        return redirect(url_for('lst'))
    return render_template("edit.html",ticket = ticket,listmode = listmode,listlow = listlow,listprovider = listprovider,listlocation = listlocation)

@app.route('/',methods=['GET', 'POST'])
@app.route('/lst',methods=['GET', 'POST'])
def lst():
    if request.method == 'POST':
        value = request.form['seek']
        tickets = models.Tickets()
        lst = tickets.seek(value)
        return render_template('list2.html', lst=lst)
    tickets = models.Tickets()
    lst = tickets.allTickets()
    return render_template('list2.html', lst = lst)

@app.route('/ust')
def ust():
    tickets = models.Tickets.query.all()
    for tic in tickets:
        if tic.name.find("Источ") != -1:
            tic.typeofequipment = 2
        elif tic.name.find("ИБП") != -1:
            tic.typeofequipment = 2
        elif tic.name.find("1000-07") != -1:
            tic.typeofequipment = 2
        elif tic.name.find("ринтер") != -1:
            tic.typeofequipment = 3
        elif tic.name.find("канер") != -1:
            tic.typeofequipment = 4
        elif tic.name.find("МФУ") != -1:
            tic.typeofequipment = 5
        elif tic.name.find("1028") != -1:
            tic.typeofequipment = 5
        elif tic.name.find("опир") != -1:
            tic.typeofequipment = 6
        elif tic.name.find("КМА") != -1:
            tic.typeofequipment = 6
        elif tic.name.find("Факс") != -1:
            tic.typeofequipment = 7
        elif tic.name.find("блок") != -1:
            tic.typeofequipment = 8
        elif tic.name.find("иоск") != -1:
            tic.typeofequipment = 10
        elif tic.name.find("мутатор") != -1:
            tic.typeofequipment = 12
        elif tic.name.upper().find("INELT") != -1:
            tic.typeofequipment = 2
        elif tic.name.find("онитор") != -1:
            tic.typeofequipment = 1
        elif tic.name.find("аудио") != -1:
            tic.typeofequipment = 11
    db.session.commit()
    return render_template("addticket.html")

@app.route('/otch_typeof')
def otch_typeof():
    typeofeq = models.Typeofequipment()
    tic = models.Tickets()
    otch = [{"cnt": tic.quantityofequipmenttype(x), "name": typeofeq.get_type(x)} for x in range(1,12)]
    return render_template("otch_typeof.html",otch = otch)

@app.route('/repair_not_defined')
def rep_type_of_repair_not_defined():
    '''Отчет по  заявкам у которых тип ремонта - не определен'''
    SERVICE_TYPE = 1 # Не определен вариант ремонта
    result = models.Tickets.byServiceprovider(SERVICE_TYPE)
    return render_template('list2.html', lst = result)


@app.route('/report_akt_priemki')
def report_akt_priemki():
    tikets = models.Tickets()
    result = []
    resultsum = []
    resultsumall = 0
    akts = tikets.by_akt_priemki()
    for akt in akts:
        tikets_list = tikets.tiketsByAktPriemki(akt, 8)
        summa = 0
        for item in tikets_list:
            result.append(item)
            summa += item['serviceprice']
        resultsumall += summa
        resultsum.append({'akt_priemki': akt, 'summa': summa})
    return render_template('rep_by_akt_priemki.html', result=result, resultsum=resultsum, resultsumall=resultsumall)

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
    return render_template('reportservice.html', result=result, resultsum=resultsum, resultsumall=resultsumall)

@app.route('/reportbyservice')
def reportbyservice():
    tickets = models.Tickets()
    report = {}
    #Актион 751
    report['action751'] = tickets.byServiceprovider(8).__len__()
    report['action751done'] = tickets.byServiceproviderDone(8).__len__()
    #Без денег
    report['nomoney'] = tickets.byServiceprovider(6).__len__()
    report['nomoneydone'] = tickets.byServiceproviderDone(6).__len__()
    # ЗИП
    report['zip'] = tickets.bySpareParts().__len__()
    report['zipdone'] = tickets.bySparePartsDone().__len__()
    #Не определен способ ремонта
    report['nodefine'] = tickets.byServiceprovider(1).__len__()
    return render_template('byservice.html',report = report)

@app.route('/write-off')
def writу_off():
    ''' Отчет по списанию техники  '''
    pass