import fdb
import datetime



class Fbticket():
    con = None
    today = datetime.date.today()
    ticket ={'localticket' : 1,
             'hotlineticket': '',
             'aktco7mode' : 1,
             'aktco7modename' : '',
             'aktco7changedate' : today,
             'aktco7date' : today,
             'aktco8mode': 1,
             'aktco8modename': '',
             'aktco8changedate': today,
             'aktco8date': today,
             'aktco41mode' : 1,
             'aktco42mode' : 1,
             'lowcourtcode' : '',
             'lowcourtname': '',
             'serviceprovider' : 1,
             'serviceproviderdate' : today,
             'location' : 1,
             'locationdate' : today,
             'name' : '',
             'inventnumder': '',
             'serialnumber': '',
             'serviceticket' : 0,
             'serviceakt' : 0,
             'serviceprice' : 0,
             'remark': ''
             }

    def __init__(self,regnum = 0,hotlineregnum ='', name = '', invnumber ='',sernumber = '',remark = '',institutionid = 0,equipmentid = 0):
        self.con = fdb.connect(dsn='192.168.10.10:cia',user='SYSDBA',password='m')
        self.localticket = regnum
        self.hotlineticket = hotlineregnum
        self.inventnumder = invnumber
        self.serialnumber = sernumber
        self.remark = remark
        self.institutionid = institutionid
        self.equipmentid = equipmentid
        self.name = name
        self.servicerequestid = 0
        self.problemdescription = ''

    def getbyhotlinenum(self,hotlinenumber):
        #Получаем данные из ис иац по номеру заявки на ГЛ
        self.hotlineticket = str(hotlinenumber)
        if self.con is not None:
            SELECT = 'select servicerequest.regnum, servicerequest.invnumber, servicerequest.sernumber, '
            SELECT = SELECT + 'servicerequest.remark, servicerequest.institutionid,servicerequest.equipmentid'
            SELECT = SELECT + ' from servicerequest'
            SELECT = SELECT + ' where servicerequest.hotlineregnum = ' + self.hotlineticket
            cursor = self.con.cursor()
            cursor.execute(SELECT)
            s = cursor.fetchone()
            self.localticket = s[0]
            self.inventnumder = s[1]
            self.serialnumber = s[2]
            self.remark = s[3]
            self.institutionid = s[4]
            self.equipmentid = s[5]
            return True
        else:
            print('No connect to databse')

    def getbylocalticket(self,localtiket):
        #Получаем данные из ис иац по номеру заявки в филиале
        if self.con is not None:
            SELECT = 'select servicerequest.hotlineregnum, servicerequest.invnumber, servicerequest.sernumber, '
            SELECT = SELECT + 'servicerequest.remark, servicerequest.institutionid,servicerequest.equipmentid,servicerequest.id'
            SELECT = SELECT + ' from servicerequest'
            SELECT = SELECT + ' where (servicerequest.regnum=' + str(localtiket) +'and servicerequest.REGYEAR=2018)'
            cursor = self.con.cursor()
            cursor.execute(SELECT)
            result = cursor.fetchone()
            self.ticket['localticket'] = localtiket
            self.ticket['hotlineticket'] = result[0]
            self.ticket['inventnumder'] =  result[1]
            self.ticket['serialnumber'] = result[2]
            self.ticket['remark'] = result[3]
            self.institutionid = result[4]
            self.equipmentid = result[5]
            self.servicerequestid = result[6]

            SELECT = 'SELECT SERVICEREQUESTFAULT.FAULTID FROM SERVICEREQUESTFAULT WHERE SERVICEREQUESTFAULT.REQUESTID =' + str(self.servicerequestid)
            cursor = self.con.cursor()
            cursor.execute(SELECT)
            try:
                if cursor.fetchone()[0] != 540001:
                    # Код неисправности не аппаратная проблема
                    print('Software problem. Not hardware')
                    return False
            except TypeError:
                #Не заполнены необходимые поля в ИС ИАЦ
                print('Not filled type of problem')
                return False

            SELECT = 'SELECT SERVICEREQUESTEQPMNTCHECK.PROBLEMDSCRPTN FROM SERVICEREQUESTEQPMNTCHECK WHERE SERVICEREQUESTEQPMNTCHECK.REQUESTID =' + str(self.servicerequestid)
            cursor = self.con.cursor()
            cursor.execute(SELECT)
            try:
                self.problemdescription = cursor.fetchone()[0]
            except:
                #Не заполнено поле в ИС ИАЦ Описание проявления неисправности
                print('Not filled problem description')
                return False

            SELECT = "SELECT TERMINALEQUIPMENT.DTLEQTYPEIDSTR FROM TERMINALEQUIPMENT WHERE  TERMINALEQUIPMENT.ID =" + str(self.equipmentid)
            cursor = self.con.cursor()
            cursor.execute(SELECT)
            result = cursor.fetchone()
            self.ticket['name'] = result[0]
            SELECT = "SELECT INSTITUTION.VN_CODE, INSTITUTION.NAME FROM INSTITUTION WHERE  INSTITUTION.ID =" + str(self.institutionid)
            cursor = self.con.cursor()
            cursor.execute(SELECT)
            result = cursor.fetchone()
            self.ticket['lowcourtcode'] = result[0]
            self.ticket['lowcourtname'] = result[1]

            return True
        else:
            print('No connect to databse')
