
from flask import *
from flask import request
import pymongo
import time
from pathlib import Path

# Global Variables

app = Flask(__name__) 
DBACredentrials=["DBA","12"]
GenuineDBA=False
ip=""
loc=""
FailCount=0
myclient = pymongo.MongoClient("mongodb://0.0.0.0:27017/")
dblist = myclient.list_database_names()
original=[]
superoriginal=[]
makeinaccessable=False
mystr=""

def ComputeOriginal():
    myworkingdatabase=0
    if "MyBankCardsManagerDB" in dblist:
        myworkingdatabase=myclient["MyBankCardsManagerDB"]
        myoriginalcollection=myworkingdatabase["Original"]
        for record in myoriginalcollection.find():
            record=str(record)
            x=record.split(',')
            x[-1]=x[-1].replace('}','')
            del x[0]
            z=""
            for i in x:
                z+=i
            original.append(z)
def ComputeSuperOriginal():
    myworkingdatabase=0

    if "MyBankCardsManagerDB2" in dblist:
        myworkingdatabase=myclient["MyBankCardsManagerDB2"]
        mysuperoriginalcollection=myworkingdatabase["SuperOriginal"]
        for record in mysuperoriginalcollection.find():
            record=str(record)
            x=record.split(',')
            x[-1]=x[-1].replace('}','')
            del x[0]
            z=""
            for i in x:
                z+=i
            # original.append(z)
            superoriginal.append(z)
        
@app.route('/MyBankCardsManager') #ONE
def fun1():
    return render_template("1.EntryPage.html")


@app.route('/MyBankCardsManager/ThisIsDBA') #TWO
def home():
    return render_template("2.AuthenticateDBA.html")

@app.route('/MyBankCardsManager/Reset')
def home4():
    time.sleep(1)
    global GenuineDBA
    global makeinaccessable
    FailCount=0
    GenuineDBA=True
    makeinaccessable=False
    return render_template("1.EntryPage.html")

@app.route('/MyBankCardsManager/AuthenticateAgain') #THREE
def home2():
    time.sleep(1)
    return render_template("3.AuthenticateAgain.html")


@app.route('/MyBankCardsManager/DBAMenu') #Four
def home3():
    time.sleep(1)
    if GenuineDBA==True:
        return render_template("4.DBAMenu.html")
    else:
        return render_template("5.DBAMenufake.html")



@app.route('/MyBankCardsManager/ProcessDBAdata',methods = ['GET'])
def processthedata():
    DBACode=request.args.get('DBACode')  
    Password=request.args.get('Password')
    global FailCount
    global GenuineDBA
    if str(DBACode)==DBACredentrials[0]:
        if str(Password)==DBACredentrials[1]:
            if FailCount==0 or FailCount==1:
                GenuineDBA=True
                FailCount=0
            return redirect("/MyBankCardsManager/DBAMenu")
        else:
            FailCount+=1
            
            if FailCount==3:
                GenuineDBA=False
                global ip
                ip = requests.get('https://api.ipify.org?format=json').json()
                FailCount=0
                print(ip + "Line 134")
                return redirect("/MyBankCardsManager/DBAMenu")
            
            return redirect("/MyBankCardsManager/AuthenticateAgain")
    else:
        FailCount+=1
        if FailCount==3:
            GenuineDBA=False
            ip = request.remote_addr
            FailCount=0
            print(ip + "Line 144")
            return redirect("/MyBankCardsManager/DBAMenu")
        return redirect("/MyBankCardsManager/AuthenticateAgain")


@app.route('/MyBankCardsManager/DBAMenu/DropDB') # FIVE
def DropDB():
    global original
    global superoriginal
    time.sleep(2)
    original=['NULL']
    superoriginal=['NULL']
    return "<h1>Dropped the database</h1>"
@app.route('/MyBankCardsManager/DBAMenu/AddEntry') # SIX
def AddEntry():
    time.sleep(1)
    return render_template("6.AddEntry.html")

@app.route('/MyBankCardsManager/DBAMenu/ViewDatabase') # Seven
def ViewDatabase():
    time.sleep(1)
    global makeinaccessable
    global mystr
    mystr=''
    temp=''
    if GenuineDBA==True:
        mystr="<h1> ORIGINAL DATABASE </h1><br>"
        mystr+="<h5>"
        for i in original:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        if makeinaccessable:
            return "<h1> Database InAccessable!! </h1>"
        return temp
        
    else:
        mystr="<h1> HONEYPOT DATABASE </h1><br>"
        mystr+="<h5>"
        for i in superoriginal:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        makeinaccessable=True
        # GenuineDBA=False
        return temp

@app.route('/MyBankCardsManager/DBAMenu/ViewDatabase1')
def ViewDatabase1():
    time.sleep(1)
    global makeinaccessable
    global mystr
    global ip
    mystr=''
    temp=''
    if GenuineDBA==True:
        global loc
        mystr="<h1> HONEYPOT DATABASE </h1><br>"
        mystr+="<h5>"
        for i in superoriginal:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        return temp + "IP of Intruder : " + ip
        
    else:
        mystr="<h1> HONEYPOT DATABASE </h1><br>"
        mystr+="<h5>"
        for i in superoriginal:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        makeinaccessable=True
        return temp


@app.route('/MyBankCardsManager/DBAMenu/DownloadDB')
def DownloadDB():
    time.sleep(1)
    downloads_path = str(Path.home() / "Downloads")
    #return str(downloads_path)
    #return 'hello'
    p=downloads_path.replace('\\','/')
    # print(p)
    p+='/MyBankCardsManagerDatabase.txt'

    d=open(p,'w')
    data=[]
    if GenuineDBA:
        data=original+[]
    else:
        data=superoriginal+[]
    for i in data:
        i=str(i)+'\n'
        d.write(i)

    d.close()
    
    
    if GenuineDBA:
        return "<h1>Database Downloaded</h1>"
    else:
        return "<h1>Database Downloaded</h1>"
@app.route('/MyBankCardsManager/DBAMenu/AddEntryData',methods=['GET'])
def AddEntryData():
    time.sleep(1)
    CName=request.args.get('CName')
    CNumber=request.args.get('CNum')
    CExpiry=request.args.get('CExpiry')
    CCVV=request.args.get('CCVV')
    record={'username':'DBA707', 'CardName':str(CName), 'CardNumber':str(CNumber), 'Expiry':str(CExpiry), 'CVV':str(CCVV)}
    record=str(record)
    x=record.split(',')
    x[-1]=x[-1].replace('}','')
    x[0]=x[0].replace('{','')
    z=""
    for i in x:
        z+=i    
    if GenuineDBA:
        original.append(z)
    else:
        superoriginal.append(z)
    return render_template("9.EntrySuccessful.html")
    
def DBADone():
    return render_template("DBADone.html")
if __name__ =='__main__':
    ComputeOriginal()
    ComputeSuperOriginal()
    app.run(host='0.0.0.0', port=7000,debug = True)  
