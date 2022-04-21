from simple_salesforce import Salesforce
from tkinter import filedialog as fd
import datetime
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog as fd
from os.path import expanduser
from decouple import config

class MainApplication:
        def __init__(self, master):
                self.master = master 
                master.title('Tracking')

                
                print('Logging into Salesforce...')
                self.sf_user = config("sf_user")
                self.sf_passwd = config("sf_passwd")
                self.sf_token = config("sf_token")
                self.sf = Salesforce(password=self.sf_passwd, username=self.sf_user, security_token=self.sf_token)

                self.saveFolder = None
                self.caseNumberList = []

                #User Input section
                self.frm_userInput = Frame(master)
                self.lbl_caseNumberInput = Label(master = self.frm_userInput, text = 'Enter Case Number', width = 15)
                self.ent_caseNumberInput = Entry(master = self.frm_userInput, text = 'Case Number',width = 15)
                self.btn_caseLookup = Button(master = self.frm_userInput, text = 'Look Up Case',width = 15, command = self.lookupCase)
                self.btn_sendTracking = Button(master = self.frm_userInput, text = 'Add to Tracking List',width = 15, command = self.trackingList)

                self.frm_userInput.pack()
                self.frm_userInput.pack_propagate(0)
                self.lbl_caseNumberInput.grid(column = 1, row = 0, pady = 5)
                self.ent_caseNumberInput.grid(column = 1, row = 1, pady = 15)
                self.btn_caseLookup.grid(column = 0, row = 3)
                self.btn_sendTracking.grid(column = 2, row = 3)

                #case info section
                self.frm_caseInfo = Frame(master, borderwidth = 2, relief = 'solid', height = 400)
                self.ent_caseNumber = Entry(master = self.frm_caseInfo, state = DISABLED, width = 15)
                self.ent_orderNumber = Entry(master = self.frm_caseInfo, state = DISABLED, width = 30)
                self.ent_rmaType = Entry(master = self.frm_caseInfo, state = DISABLED, width = 15)
                self.ent_trackingNumber = Entry(master = self.frm_caseInfo, state = DISABLED, width = 15)
                self.ent_trackingCarrier = Entry(master = self.frm_caseInfo, state = DISABLED, width = 15)
                self.ent_caseCreator = Entry(master = self.frm_caseInfo, state = DISABLED, width = 15)

                #case info labels
                self.lbl_caseNumber = Label(master = self.frm_caseInfo, text = 'Case Number')
                self.lbl_orderNumber = Label(master = self.frm_caseInfo, text = 'Order Number')
                self.lbl_rmaType = Label(master = self.frm_caseInfo, text = 'RMA Type')
                self.lbl_trackingNumber = Label(master = self.frm_caseInfo, text = 'Tracking Number')
                self.lbl_trackingCarrier = Label(master = self.frm_caseInfo, text = 'Tracking Carrier')
                self.lbl_caseCreator = Label(master = self.frm_caseInfo, text = 'Case Creator')

                self.frm_caseInfo.pack(pady = 15)
                self.frm_caseInfo.pack_propagate(0)
                self.ent_caseNumber.grid(column = 0, row = 1, padx = 10)
                self.ent_orderNumber.grid(column = 1, row = 1, padx = 10)
                self.ent_rmaType.grid(column = 2, row = 1, padx = 10)
                self.ent_trackingNumber.grid(column = 0, row = 3, padx = 10)
                self.ent_trackingCarrier.grid(column = 1, row = 3, padx = 10)
                self.ent_caseCreator.grid(column = 2, row = 3, padx = 10, pady = (0,15))

                self.lbl_caseNumber.grid(column = 0, row = 0, padx = 10, pady = (15,0))
                self.lbl_orderNumber.grid(column = 1, row = 0, padx = 10, pady = (15,0))
                self.lbl_rmaType.grid(column = 2, row = 0, padx = 10)
                self.lbl_trackingNumber.grid(column = 0, row = 2, padx = 10)
                self.lbl_trackingCarrier.grid(column = 1, row = 2, padx = 10)
                self.lbl_caseCreator.grid(column = 2, row = 2, padx = 10)

                #log area
                self.frm_log = Frame(master)
                self.txt_log = scrolledtext.ScrolledText(master = self.frm_log, wrap = WORD, width = 55, height = 8, state = DISABLED, font = ('Monospace', 10))

                self.frm_log.pack()
                self.frm_log.pack_propagate(0)
                self.txt_log.grid(row = 0, column = 0)

                #other functions
                self.frm_functions = Frame(master)
                self.btn_trackingMessage = Button(master = self.frm_functions, text = 'Create Tracking Messages', command = self.createTracking)
                self.btn_saveLocation = Button(master = self.frm_functions, text = 'Save Location...', command = self.saveLocation)

                self.frm_functions.pack()
                self.frm_functions.pack_propagate(0)
                self.btn_trackingMessage.grid(column = 0, row = 0, pady = 10, padx = 15)
                self.btn_saveLocation.grid(column = 1, row = 0, pady = 10, padx = 15)

        def writeLog(self,text):
                self.txt_log.configure(state = NORMAL)
                self.txt_log.insert(END, str(text))
                self.txt_log.configure(state = DISABLED)
                self.txt_log.see(END)

        def writeEntry(self,entry,text):
                entry.config(state = NORMAL)
                entry.delete(0,'end')
                entry.insert(0, str(text))
                entry.configure(state = DISABLED)

        def findCase(self, caseNumber):                     
                i = caseNumber
                query = self.sf.query_all_iter("SELECT Order_ID__c, RMA_Type__c, Outgoing_Parts_Number__c, Tracking_Number_2__c, Case_Created_By__c, Repairs_Performed__c, Origin FROM Case WHERE CaseNumber = '{}'".format(i))
                for i in query:
                        self.orderNumber = i.get('Order_ID__c')
                        self.rmaType = i.get('RMA_Type__c')
                        self.caseCreator = i.get('Case_Created_By__c')
                        self.repairNotes = i.get('Repairs_Performed__c')
                        self.caseOrigin = i.get('Origin')
                        if i.get('Outgoing_Parts_Number__c') != None:
                                self.trackingNumber = i.get('Outgoing_Parts_Number__c')
                        else:
                                self.trackingNumber = i.get('Tracking_Number_2__c')
                                
                        try: 
                                self.trackingLength = len(self.trackingNumber)
                                self.trackingCarrier = ''
                        except:
                                self.trackingCarrier = 'Check Tracking'

                        if self.trackingCarrier != 'Check Tracking':
                                if self.trackingLength != 18 or 22:
                                        self.trackingCarrier = 'Other'
                                if self.trackingLength == 18:
                                        self.trackingCarrier = 'UPS'
                                if self.trackingLength == 22:
                                        self.trackingCarrier = 'USPS'   
                                if self.trackingLength == 12:
                                        self.trackingCarrier = 'Fedex'

        def lookupCase(self):
                self.caseNumber = self.ent_caseNumberInput.get()

                self.findCase(self.caseNumber)

                self.writeEntry(self.ent_caseNumber,self.caseNumber)
                self.writeEntry(self.ent_orderNumber,self.orderNumber)
                self.writeEntry(self.ent_rmaType,self.rmaType)
                self.writeEntry(self.ent_trackingNumber,self.trackingNumber)
                self.writeEntry(self.ent_trackingCarrier,self.trackingCarrier)
                self.writeEntry(self.ent_caseCreator,self.caseCreator)

        def trackingList(self):
                self.caseNumberList.append(self.ent_caseNumberInput.get())
                self.lookupCase()
                self.writeLog('Case Number {} added to Tracking List\n'.format(self.ent_caseNumberInput.get()))

        def saveLocation(self):
                self.saveFolder = fd.askdirectory()
                self.writeLog('Save Location Updated\n')

        def createTracking(self):
                self.date = datetime.date.today()
                if self.saveFolder == None:
                        self.saveFolder = expanduser('~')
                self.trackingFile = open('%s/%s.txt' % (self.saveFolder,self.date), 'a+')

                self.writeLog('Generating Tracking Messages......\n')

                if len(self.caseNumberList) != 0:
                        for i in self.caseNumberList:
                                self.caseNumber = i
                                self.findCase(self.caseNumber)
                                self.trackingFile.write("Case Number: {}\n".format(self.caseNumber))
                                self.trackingFile.write("Order Number: {}\n".format(self.orderNumber))
                                self.trackingFile.write("RMA Type: {}\n\n".format(self.rmaType))
                                if self.caseCreator == 'Court Smith':
                                        self.trackingFile.write('Tracking Number: {}\n'.format(self.trackingNumber))
                                        self.trackingFile.write('***Send Tracking to Court***')
                                        self.trackingFile.write("\n==========================\n\n")
                                        continue
                                if self.caseCreator == 'Dani Vo':
                                        self.trackingFile.write('Tracking Number: {}\n'.format(self.trackingNumber))
                                        self.trackingFile.write('***Send Tracking to Dani***')
                                        self.trackingFile.write("\n==========================\n\n")
                                        continue
                                if self.caseOrigin != "Amazon Messages":
                                        self.trackingFile.write('Tracking Number:{}\n'.format(self.trackingNumber))
                                        self.trackingFile.write('***Send Tracking to {}\n'.format(self.caseCreator))
                                        self.trackingFile.write("\n==========================\n\n")
                                        continue
                                else:
                                        if self.trackingCarrier != 'Other':
                                                if self.rmaType == 'Part':
                                                        self.trackingFile.write(
                                                                """Hello,
This is to let you know that your parts have shipped.
Your %s tracking number is: %s
Please allow up to 48 hours for the tracking to fully update.
Best Regards,
Customer Support
Skytech Gaming\n""" % (self.trackingCarrier, self.trackingNumber)
                                                        )

                                                if self.rmaType == 'Repair':
                                                        self.trackingFile.write(
                                                                """Hello,
This is to let you know that your repaired Computer has shipped.
Your %s tracking number is: %s
Our Repair team performed the following Repairs:
'%s'
Please allow up to 48 hours for the tracking to fully update.
Best Regards,
Customer Support
Skytech Gaming\n""" % (self.trackingCarrier, self.trackingNumber, self.repairNotes)
                                                        )

                                                if self.rmaType == 'Replace':
                                                        self.trackingFile.write(
                                                                """Hello,
This is to let you know that your replacement Computer has shipped.
Your %s tracking number is: %s
Please allow up to 48 hours for the tracking to fully update.
Best Regards,
Customer Support
Skytech Gaming\n""" % (self.trackingCarrier, self.trackingNumber)
                                                        )

                                        else:
                                                self.trackingFile.write('***Check Tracking***')
                                                        
                                        self.trackingFile.write("\n==========================\n\n")

                else:
                        self.writeLog('Please add a Case to the List\n')

                self.trackingFile.close()
                self.writeLog('Tracking Messages Complete\nTracking Messages can be found at:\n%s/%s.txt' % (self.saveFolder,self.date))


root = Tk()
root.geometry('500x500')
mainApp = MainApplication(root)
root.mainloop()