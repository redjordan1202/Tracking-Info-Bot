from simple_salesforce import Salesforce
import datetime
import gspread
from gspread.models import Worksheet
from db import DataStructure
from decouple import config

sf = None

class Case:
        caseNumber = None
        orderNumber = None
        rmaType = None
        caseCreator = None
        repairNotes = None
        caseOrigin = None
        trackingNumber = None
        trackingLength = None
        trackingCarrier = None
        trackingMessage = None
        status = None
        part = None

def start_up():
    print('Logging into Salesforce...')
    global sf
    sf_user = config("sf_user")
    sf_passwd = config("sf_passwd")
    sf_token = config("sf_token")
    sf = Salesforce(password=sf_passwd, username=sf_user, security_token=sf_token)
    print('Logged In!\n')

def find_case(case_number):
    global sf

    if case_number.isalnum() != True:
        print('{} is not a Valid Case Number' % (case_number)) 
    if len(case_number) < 6:
        Case.caseNumber = case_number.zfill(6)
    else:
        Case.caseNumber = case_number

    print('Finding Case %s\n---------------' % (case_number))

    query= sf.query_all_iter(
        "SELECT Order_ID__c, RMA_Type__c, Outgoing_Parts_Number__c, Tracking_Number_2__c, Case_Created_By__c, Repairs_Performed__c, Origin, Parts_Needed__c FROM Case WHERE CaseNumber = '{}'".format(Case.caseNumber)
        )
    for i in query:
        Case.orderNumber = i.get('Order_ID__c')
        Case.rmaType = i.get('RMA_Type__c')
        Case.caseCreator = i.get('Case_Created_By__c')
        Case.repairNotes = i.get('Repairs_Performed__c')
        Case.caseOrigin = i.get('Origin')
        Case.part = i.get('Parts_Needed__c')
        
        if i.get('Tracking_Number_2__c') != None:
            Case.trackingNumber = i.get('Tracking_Number_2__c')
        else:
            Case.trackingNumber = i.get('Outgoing_Parts_Number__c')
        
        try: 
            Case.trackingLength = len(Case.trackingNumber)
            Case.trackingCarrier = ''
        except:
            Case.trackingCarrier = 'Check Tracking'

        if Case.trackingCarrier != 'Check Tracking':
            if Case.trackingLength != 18 or 22 or 12:
                    Case.trackingCarrier = 'Other'
            if Case.trackingLength == 18:
                    Case.trackingCarrier = 'UPS'
            if Case.trackingLength == 22:
                    Case.trackingCarrier = 'USPS'   
            if Case.trackingLength == 12:
                    Case.trackingCarrier = 'Fedex'

def write_to_db():
    active_col = 1
    today = datetime.date.today()
    date_str = today.strftime('%m/%d/%Y')
    db_data = [
            Case.caseNumber,
            Case.orderNumber,
            Case.rmaType,
            Case.part,
            Case.trackingNumber,
            Case.trackingCarrier,
            Case.status,
            Case.trackingMessage
        ]
    
    print('Writting to DB\n---------------')
    
    DataStructure.write_data(
            DataStructure.active_row, active_col, date_str
        )
    for i in db_data:
        active_col += 1
        DataStructure.write_data(
            DataStructure.active_row, active_col, i
        )
    
    DataStructure.update_last_edited()
    sf.Case.upsert(
        f"CaseNumber/{Case.caseNumber}", {'Tracking_Number_Sent__c': 'Yes'}
    )

    print('Write Complete\n---------------')

def generate_tracking(case_number):
    DataStructure.generate_data_structure("Case Tracking Template",'A2')

    
    find_case(case_number)
    print('Case %s Found\nCreating Message\n---------------' % (case_number)) 
    if Case.caseCreator == 'Court Smith':
            Case.status = '***Send to Court***'
    if Case.caseCreator == 'Dani Vo':
            Case.status = '***Send to Dani***'
    if Case.caseOrigin != "Amazon Messages":
            Case.status = '***Send to {}***'.format(Case.caseCreator)
    else:
            Case.status = 'Tracking Sent'

    if Case.rmaType == 'Part':
        DataStructure.pull_data('D2')
        Case.trackingMessage = DataStructure.data % (
            Case.part,
            Case.trackingCarrier,
            Case.trackingNumber
        )
    if Case.rmaType == 'Repair':
        DataStructure.pull_data('E2')
        Case.trackingMessage = DataStructure.data % (
            Case.trackingCarrier,
            Case.trackingNumber,
            Case.repairNotes
        )
    if Case.rmaType == 'Replace':
        DataStructure.pull_data('f2')
        Case.trackingMessage = DataStructure.data % (
            Case.trackingCarrier,
            Case.trackingNumber
        )
    
    write_to_db()

def Main():
    start_up()

    while True:
        user_input = input(
            'Please Enter a Case Numbers Separated by Space\nor Type Exit to Exit: '
        )
        if user_input == 'Exit':
            quit()
        if user_input == '':
            print('Please Enter a Case Number or Exit')
        else:
            case_list = list(user_input.split())

        for case in case_list:
            generate_tracking(case)



Main()





