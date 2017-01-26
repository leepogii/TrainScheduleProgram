import urllib.request
import pymysql
from tkinter import *
from tkinter import ttk
from re import findall
import base64
import math
import time
from datetime import date
from datetime import *
class Phasetres:
    def __init__(self,rootWin):

        self.rootWin= rootWin
        
        url = "http://faculty.gatech.edu/hg/image/276841/200xX_scale"
        
        val = urllib.request.urlopen(url)
        
        myPic = val.read()
        
        self.resList=[]
        self.student = False
        b64data = base64.encodebytes(myPic)
        self.photo = PhotoImage(data = b64data)
        self.totalCost = 0
        self.login()

    def login(self):


        self.rootWin.title("Login")
        self.center = Label(self.rootWin, text = "Login", font = ("Helvetica", 16))
        self.center.grid(row = 0, column = 2)
        self.username=Label(self.rootWin,text="Username")
        self.username.grid(row=1,column=0,sticky=W, padx = 25, pady = 5)
        self.stvar=StringVar()
        self.ue=Entry(self.rootWin,textvariable=self.stvar, width = 40)
        self.ue.grid(row=1,column=2,columnspan = 3, padx = 25, pady = 5)
        self.password=Label(self.rootWin,text="Password")
        self.password.grid(row=2,column=0,sticky=W, padx =25, pady = 5)
        self.stvar1=StringVar()
        self.ent=Entry(self.rootWin,textvariable=self.stvar1, width = 40)
        self.ent.grid(row=2,column=2,columnspan = 3, padx = 25, pady = 5)
        self.login = Button(self.rootWin, text = "Login", width = 20, command = self.Login_Check)
        self.login.grid(row = 3, column = 1, columnspan = 2)
        
        
        self.register = Button(self. rootWin, text = "Register", width = 20, command = self.New_User)
        self.register.grid(row = 3, column = 3, columnspan =2, padx =5)

        


    def Connect(self):
        try:
            self.database= pymysql.connect(host = "academic-mysql.cc.gatech.edu",user = "cs4400_Team_4", passwd = "3Pnh70jY", db = 'cs4400_Team_4')
            self.Curs = self.database.cursor()
            return self.database
        except:
            messagebox.showwarning("Connection Error! :(", "Check your internet connection and try again")
#connects to database

    def Login_Check(self):

        username = self.stvar.get()
        self.username= username
        password = self.stvar1.get()

        self.Connect()

        if len(username) != 0 and len(password)!=0:
            Q1 =  'SELECT * FROM USER WHERE Username= "'+ str(username)+'" and Password="'+str(password)+'"'
            self.Curs.execute(Q1)
            data = self.Curs.fetchall()
            print (data[0][0])
            if data and username == data[0][0] and password == data[0][1]:
                Q1 = 'SELECT * FROM CUSTOMER WHERE Username= "'+ str(username)+'"'
                self.Curs.execute(Q1)
                data = self.Curs.fetchall()
                if data:
                    self.Ch_Funct()
                else:
                    self.Man_Ch_Func()
            else :
                messagebox.showwarning("Invalid", "The entered username or password not found, check for error")
        else:
            messagebox.showwarning("Empty Field", "Please fill required fields")
                


    def New_User(self):

        self.windN_U = Toplevel()
        self.rootWin.withdraw()

        self.l0 = Label(self.windN_U, text= "New User Registration", font = ("Helvetica",16))
        self.l0.grid(row = 0, column = 1, pady = 50)
        
        self.l = Label(self.windN_U, image=self.photo)
        self.l.grid(row = 5, column = 2, columnspan= 2)

        self.l2= Label(self.windN_U, text="Username")
        self.l2.grid(row=1,column=0, sticky=E)

        self.l3= Label(self.windN_U, text= "Email Address")
        self.l3.grid(row=2,column=0, sticky= E)

        self.l4= Label(self.windN_U, text= "Password")
        self.l4.grid(row=3,column=0, sticky= E)

        self.l3= Label(self.windN_U, text= " Confirm Password")
        self.l3.grid(row=4,column=0, sticky= E)

        self.sv = StringVar()
        self.sv2= StringVar()
        self.sv3= StringVar()
        self.sv4= StringVar()

        self.e1= Entry(self.windN_U, textvariable= self.sv, width = 30, state= "normal",bg="gold")
        self.e1.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)
        self.e2= Entry(self.windN_U, textvariable= self.sv2, width = 30, state= "normal", bg="gold")
        self.e2.grid(row=2,column=1, pady= 5, padx = 20, sticky=W)
        self.e3= Entry(self.windN_U, textvariable= self.sv3, width = 30, state= "normal",bg="gold")
        self.e3.grid(row=3,column=1, pady= 5, padx = 20, sticky=W)
        self.e4= Entry(self.windN_U, textvariable= self.sv4, width = 30, state= "normal", bg="gold")
        self.e4.grid(row=4,column=1, pady= 5, padx = 20,sticky=W)

        self.b1= Button(self.windN_U, text= "Create", width=12, bg="white", command= self.RegisterNew)
        self.b1.grid(row=5, column=1,  pady = 20)

        self.b1= Button(self.windN_U, text= "Back", width=12, bg="white", command= self.BackToLogin)
        self.b1.grid(row=5, column=0,  pady = 20)

    def RegisterNew(self):

        username = self.sv.get()
        email = self.sv2.get()
        password = self.sv3.get()
        cpassword = self.sv4.get()

        query = 'SELECT Username FROM CUSTOMER'


        self.Connect()
        if password != cpassword:
            messagebox.showwarning("Error", "Passwords don't match")
#how to check validity of email?
        if len(username)!=0 and len(email)!=0 and len(password) !=0 and len(cpassword) !=0:
            QUsername = 'SELECT Username FROM CUSTOMER WHERE Username= "'+ (username) + '"'
            print(QUsername)
            QEmail = 'SELECT Email FROM CUSTOMER WHERE Username= "'+ email + '"'
            self.Curs.execute(QUsername)
            dataUsername = self.Curs.fetchall()
            self.Curs.execute(QEmail)
            dataEmail = self.Curs.fetchall()
            if dataUsername:
                print(dataUsername)
                messagebox.showwarning("Sorry", "Username already exists")
            elif dataEmail:
                print(dataEmail)
                messagebox.showwarning("Sorry", "Email Address already exists")
            else:
                QRN3 = 'INSERT INTO CUSTOMER VALUES("' + username + '", "' + email + '",' + str(0) + ')'
                QRN4 = 'INSERT INTO USER VALUES("' + username + '", "' + password + '")'
                self.Curs.execute(QRN3)
                self.Curs.execute(QRN4)
                messagebox.showwarning("Success", "Successfully Created")  
        
        else:
            messagebox.showwarning("Sorry", "Please fill all fields")

    def BackToLogin(self):
        self.windN_U.withdraw()
        self.rootWin.deiconify()

    def LogOutB2L (self):
        self.windCF.withdraw()
        self.rootWin.deiconify()
        

    def Stu_Disc(self):

        self.windStD = Toplevel()
        self.windCF.withdraw()
        
                
        self.l0SD = Label(self.windStD, text= "Add School Info", font = ("Helvetica",16))
        self.l0SD.grid(row = 0, column = 1, pady = 50)
        
        self.lSD = Label(self.windStD, image=self.photo)
        self.lSD.grid(row = 3, column = 2, columnspan= 2)

        self.l2SD= Label(self.windStD, text="School Email Address")
        self.l2SD.grid(row=1,column=0, padx = 25, sticky=E)

        self.svSD = StringVar()

        self.e1= Entry(self.windStD, textvariable= self.svSD, width = 30, state= "normal",bg="gold")
        self.e1.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)
        

        self.l3SD= Label(self.windStD, text= "Your school email address ends with .edu", font = ("Helvetica", 8))
        self.l3SD.grid(row=2,column=0, sticky= E)
        
        
        self.b1SD= Button(self.windStD, text= "Back", width=12, bg="white", command= self.DisctoMF)
        self.b1SD.grid(row=3, column=1,  pady = 10, sticky = W)

        self.b2SD= Button(self.windStD, text= "Submit", width=12, bg="white", command=self.isStudent)
        self.b2SD.grid(row=3, column=1,  pady = 10, sticky = E)

    def isStudent(self):
        emailAddr = self.svSD.get()
        if emailAddr.endswith(".edu"):
            Q = "UPDATE CUSTOMER SET isStudent = 1 WHERE Username = '" + self.username + "'"
            print(Q)
            self.Curs.execute(Q)
            messagebox.showwarning("Student Verified", "20% Discount will be applied.")
            self.student = True
        else:
            messagebox.showwarning("ERROR","Invalied Student Email Address")

    def DisctoMF(self):
        self.windStD.withdraw()
        self.windCF.deiconify()

    def View_Train_Sch(self):

        self.windVTS = Toplevel()
        self.windCF.withdraw()
        
        self.l0VTS = Label(self.windVTS, text= "View Train Schedule", font = ("Helvetica",16))
        self.l0VTS.grid(row = 0, column = 1, pady = 50)

        self.svVTS = StringVar()

        self.l2VTS= Label(self.windVTS, text="Train Number")
        self.l2VTS.grid(row=1,column=0, padx = 25, sticky=E)

        self.e1= Entry(self.windVTS, textvariable= self.svVTS, width = 30, state= "normal",bg="gold")
        self.e1.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)

        self.b2VTS = Button(self.windVTS, text= "Back", width=12, bg="white", command = self.VTStoCF)
        self.b2VTS.grid(row=2, column=0,  pady = 10, sticky = W)
        
        self.b1VTS= Button(self.windVTS, text= "Search", width=12, bg="white", command = self.View_Train_Sch2)
        self.b1VTS.grid(row=2, column=1,  pady = 10, sticky = W)

        
        self.lVTS = Label(self.windVTS, image=self.photo)
        self.lVTS.grid(row = 2, column = 2, columnspan= 2)

    def VTStoCF(self):
        self.windVTS.withdraw()
        self.windCF.deiconify()


    
    def getTrainTree(self, frame):
        tree = ttk.Treeview(frame)
        tree.pack()
        tree["show"] = "headings"
        tree["columns"] = ("train", "station", "arrive","dept")
        tree.heading("train", text = "Train Number")
        tree.heading("station", text = "Station")
        tree.heading("arrive", text = "Arrival Time")
        tree.heading("dept", text = "Departure Time")
        
        
        
        return tree
    def View_Train_Sch2(self): 
        self.Connect()
        userinput = self.svVTS.get()
        Query =  'SELECT * FROM TRAINSTOPSATSTATION WHERE trainNo= "'+ str(userinput)+'"'
        
        self.Curs.execute(Query)
        L = []
        for i in self.Curs:
            L.append(i)
        if (len(L) != 0):
            self.window3 = Toplevel()
            self.rootWin.withdraw() 
            
            
            frame1 = Frame(self.window3)
            frame1.pack()
            self.l0VTS2 = Label(frame1, text= "View Train Schedule")
            self.l0VTS2.pack(side = TOP)
            tree = self.getTrainTree(frame1)
            tree.pack(side = TOP)
    
            for row in L:
                tree.insert("", 0, text = "Line 1", values = (row[0], row[1],  str(row[2]), str(row[3])))
        else:
            messagebox.showwarning("Inccorect Train Number","Enter Correct Train Number")
            
            
        
        
        
    def Ch_Funct(self):

         self.windCF = Toplevel()
         self.rootWin.withdraw()

         self.l0CF = Label(self.windCF, text= "Choose Functionality", font = ("Helvetica",16))
         self.l0CF.grid(row = 0, column = 1, pady = 50)

         self.b1CF= Button(self.windCF, text= "View Train Schedule", width=40, bg="white", command = self.View_Train_Sch)
         self.b1CF.grid(row=1, column=1,  pady = 10, sticky = W)

         self.b2CF= Button(self.windCF, text= "Make a new Reservation", width=40, bg="white", command = self.Search_Trn)
         self.b2CF.grid(row=2, column=1,  pady = 10, sticky = W)

         self.b3CF= Button(self.windCF, text= "Update a Reservation", width=40, bg="white", command= self.Upd_Resv)
         self.b3CF.grid(row=3, column=1,  pady = 10, sticky = W)

         self.b4CF= Button(self.windCF, text= "Cancel a Reservation", width=40, bg="white", command =self.Canc_Resv)
         self.b4CF.grid(row=4, column=1,  pady = 10, sticky = W)

         self.b5CF= Button(self.windCF, text= "Give Review", width=40, bg="white", command= self.Write_Rev)
         self.b5CF.grid(row=5, column=1,  pady = 10, sticky = W)

         self.b5CF= Button(self.windCF, text= "View Review", width=40, bg="white", command=self.Find_Rev)
         self.b5CF.grid(row=6, column=1,  pady = 10, sticky = W)

         self.b6CF= Button(self.windCF, text= "Add School Information (student discount)", width=40, bg="white", command= self.Stu_Disc)
         self.b6CF.grid(row=7, column=1,  pady = 10, sticky = W)

         self.b7CF= Button(self.windCF, text= "Log Out", width=12, bg="gold", command = self.LogOutB2L)
         self.b7CF.grid(row=8, column=1,  pady = 10, sticky = W)


#Dynamic Part needs to be done

    def Search_Trn(self):
        self.windSet = Toplevel()
        self.windCF.withdraw()
        self.windSet.title("Search Train")

        self.lST = Label(self.windSet, text= "Search Train", font = ("Helvetica",16))
        self.lST.grid(row = 0, column = 1, pady = 50)

        self.l1ST= Label(self.windSet, text= "Departs From", font = ("Helvetica", 8))
        self.l1ST.grid(row=1,column=0, sticky= E)

        self.l2ST= Label(self.windSet, text= "Arrives At", font = ("Helvetica", 8))
        self.l2ST.grid(row=2,column=0, sticky= E)

        self.l3ST= Label(self.windSet, text= "Departure Date", font = ("Helvetica", 8))
        self.l3ST.grid(row=3,column=0, sticky= E)

        self.svST = StringVar()
        self.svST.set("")
        w1ST = OptionMenu(self.windSet, self.svST, "Braves", "Dodgers", "Marlins","Rangers", "Red Sox", "Yankees")
        w1ST.grid(row=1,column=2)
        
        self.sv2ST= StringVar()
        w2ST = OptionMenu(self.windSet, self.sv2ST, "Braves", "Dodgers", "Marlins","Rangers", "Red Sox", "Yankees")
        w2ST.grid(row=2,column=2)
        
        self.sv3ST= StringVar()

        self.e1ST= Entry(self.windSet, textvariable= self.svST, width = 30, state= "disabled",bg="gold")
        self.e1ST.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)

        self.e2ST= Entry(self.windSet, textvariable= self.sv2ST, width = 30, state= "disabled",bg="gold")
        self.e2ST.grid(row=2,column=1, pady= 5, padx = 20, sticky=W)

        self.e3ST= Entry(self.windSet, textvariable= self.sv3ST, width = 30, state= "normal",bg="gold")
        self.e3ST.grid(row=3,column=1, pady= 5, padx = 20, sticky=W)

        self.l4ST= Label(self.windSet, text="Enter in the form YY/MM/DD")
        self.l4ST.grid(row=4,column=1, padx = 25, sticky=E)

        self.bST= Button(self.windSet, text= "Find Trains", width=12, bg="gold", command = self.find)
        self.bST.grid(row=5, column=1,  pady = 10, sticky = W)

        self.bST2= Button(self.windSet, text= "Back", width=12, bg="gold", command = self.STbacktoCF)
        self.bST2.grid(row=5, column=0,  pady = 10, sticky = W)

        #departure date format check

    def STbacktoCF(self):
        self.windSet.withdraw()
        self.windCF.deiconify()
        
        
    def treeFind(self,frame):
        tree2 = ttk.Treeview(frame)
        tree2.pack()
        tree2["show"] = "headings"
        tree2["columns"] = ("Train", "Duration","Arrival", "Departure", "Price","Class")
        tree2.heading("Train", text = "Train")
        tree2.heading("Duration", text = "Duration")
        tree2.heading("Departure", text = "Departure Time")
        tree2.heading("Arrival", text = "Arrival Time")
        tree2.heading("Price", text = " 1st Price")
        tree2.heading("Class", text = "2nd Price")
        
        
        
        return tree2
        
    def find(self): #Looks for trains
        self.departs = self.svST.get()
        self.arrives = self.sv2ST.get()
        self.date = self.sv3ST.get()
        try:
            new = datetime.strptime(self.date, "%y/%m/%d").date()
            #frame2 = Frame(self.findwin)
            #frame2.pack()
            #tree2 = self.treeFind(frame2)
            #tree2.pack(side=TOP)
            a = new.timetuple()
            print(a)
            year = int(a[0])
            month = int(a[1])
            day = int(a[2])
            print(year)
            print(month)
            n = datetime.now()
            t = n.timetuple()
            cyear = int(t[0])
            cmonth = int(t[1])
            cday = int(t[2])
            print (cyear,cmonth)
            self.Connect()
            beast = 'SELECT S.TrainNo, TRAINROUTE.FirstClassPrice, TRAINROUTE.SecondClassPrice, S.Arrival, S.Departure, TIMEDIFF(S.Arrival, S.Departure) AS Duration FROM (SELECT X.TrainNo, X.DepTime as Departure, Y.ArrivalTime as Arrival, X.StationName as DepartStation, Y.StationName as ArrStation FROM (SELECT TrainNo, DepTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+self.departs+'") AS X JOIN (SELECT TrainNo, ArrivalTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+self.arrives+'") AS Y on (X.TrainNo = Y.TrainNo) WHERE (X.DepTime < Y.ArrivalTime)) as S JOIN TRAINROUTE ON (S.TrainNo = TRAINROUTE.TrainNo)'
            self.Curs.execute(beast)
            details = self.Curs.fetchall()
            validDate = False
            if cyear < year:
                validDate = True
            elif cyear == year:
                print("cyear == year")
                print("cyear < year")
                print("Today: ", cyear, cmonth)
                print("Booked: ", year, month)
                if cmonth < month:
                    print("cmonth < month")
                    validDate = True
                elif cmonth == month:
                    print("cmonth < month")
                    if cday <= day:
                        print("cday <= day")
                        validDate = True
            print("this")
            if validDate:
                if self.departs and self.arrives:
                    if details:
                        self.findwin = Toplevel()
                        self.rootWin.withdraw()
                        print(details)
                        Label(self.findwin, text="Train Number", anchor="w").grid(row=0, column=0,columnspan = 2, sticky="ew")
                        Label(self.findwin, text="Duration", anchor="w").grid(row=0, column=2, columnspan =2, sticky="ew")
                        Label(self.findwin, text="Departure", anchor="w").grid(row=0, column=4, columnspan = 2, sticky="ew")
                        Label(self.findwin, text="Arrival", anchor="w").grid(row=0, column=6, columnspan = 2, sticky="ew")
                        Label(self.findwin, text="1st Class Price", anchor="w").grid(row=0, column=8, columnspan = 2, sticky="ew")
                        Label(self.findwin, text="2nd Class Price", anchor="w").grid(row=0, column=10, columnspan = 2, sticky="ew")


                        aList = []
                        for i in details:
                            aList.append(i)
                        i = 1
                        j = 1
                        k = 2
                        self.v = IntVar()
                        for r in aList:

                            Label(self.findwin, text=r[0], anchor="w").grid(row=i, column=0, sticky="ew")
                            Label(self.findwin, text = str(r[5]), anchor = "w").grid(row = i, column = 2, sticky = "ew")
                            Label(self.findwin, text=str(r[4]), anchor="w").grid(row=i, column=4, sticky="ew")
                            Label(self.findwin, text = str(r[3]), anchor = "w").grid(row = i, column = 6, sticky = "ew")
                            Radiobutton(self.findwin, text=str(r[1]), variable = self.v, value = j, anchor="w").grid(row=i, column=8, sticky="ew")
                            Radiobutton(self.findwin, text=str(r[2]), variable = self.v, value = k, anchor="w").grid(row=i, column=10, sticky="ew")
                            j = j + 2
                            k = k + 2
                            i = i + 1

                        n = Button(self.findwin, text = "Next", command = self.Extras)
                        n.grid(row = i + 3, column = 6, sticky = "EW")
                    else:
                        messagebox.showwarning("Inccorect Train Number","There is no Train Route from " + self.departs + " to " + self.arrives)
                else:
                    messagebox.showwarning("Error","You should fill out the form")
            else:
                messagebox.showwarning("Error","Departure Date cannot be past date")
        except:
            messagebox.showwarning("Error", "Enter Date in correct format")


    def makeRes(self):
        print("make rev reached")
        self.departs = self.svST.get()
        self.arrives = self.sv2ST.get()
        self.date = self.sv3ST.get()
        rbvalue = self.v.get()
        self.Connect()
        beast = 'SELECT S.TrainNo, TRAINROUTE.FirstClassPrice, TRAINROUTE.SecondClassPrice, S.Arrival, S.Departure, TIMEDIFF(S.Arrival, S.Departure) AS Duration FROM (SELECT X.TrainNo, X.DepTime as Departure, Y.ArrivalTime as Arrival, X.StationName as DepartStation, Y.StationName as ArrStation FROM (SELECT TrainNo, DepTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+self.departs+'") AS X JOIN (SELECT TrainNo, ArrivalTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+self.arrives+'") AS Y on (X.TrainNo = Y.TrainNo) WHERE (X.DepTime < Y.ArrivalTime)) as S JOIN TRAINROUTE ON (S.TrainNo = TRAINROUTE.TrainNo)'
        self.Curs.execute(beast)
        details = self.Curs.fetchall()
        aList = []
        for i in details:
            aList.append(i)
        pos = math.ceil(rbvalue/2)
        tup = aList[pos-1]
        for data in tup:
            self.train = tup[0]
            self.dep = tup[4]
            self.arr = tup[3]
            self.dur = tup[5]
            if (rbvalue % 2 == 0):
                self.price = float(tup[2])
                self.c = "2nd Class"
            else:
                self.price = float(tup[1])
                self.c = "1st Class"
        self.numbags = self.svEX.get()
        
        self.name = self.sv1EX.get()
        if (len(self.name) == 0):
            messagebox.showwarning("Error", "Please enter Passenger Name.")
            return
        if (int(self.numbags) > 2):
                self. transaction = self.price + (int(self.numbags) - 2)*30

        else:
                self.transaction = self.price
        if (self.student):
            self.transaction = 0.8 * self.transaction

        tup1 = ()

        tup1 = tup1 + (self.train,)+(self.dep,)+(self.arr,)+(self.dur,)+(self.price,)+(self.numbags,)+(self.name,)+ (self.departs,)+(self.arrives,)+(self.c,)+(self.transaction,)+(self.date,)
        print(tup1, len(tup1))
        self.resList.append(tup1)
        self.makeResGui()

    def makeResGui(self):
            self.makeRev = Toplevel()
            self.extras.withdraw()
            self.makeRev.title("Make Reservation")
            print("this")
            Label(self.makeRev, text="Train Number", anchor="w").grid(row=0, column=0,columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Duration", anchor="w").grid(row=0, column=2, columnspan =2, sticky="ew")
            Label(self.makeRev, text="Departure", anchor="w").grid(row=0, column=4, columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Arrival", anchor="w").grid(row=0, column=6, columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Class", anchor="w").grid(row=0, column=8, columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Price", anchor="w").grid(row=0, column=10, columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Bags", anchor="w").grid(row=0, column=12, columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Passenger Name", anchor="w").grid(row=0, column=14, columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Depart Station", anchor="w").grid(row=0, column=16, columnspan = 2, sticky="ew")
            Label(self.makeRev, text="Arrive Station", anchor="w").grid(row=0, column=18, columnspan = 2, sticky="ew")
            Label(self.makeRev, text = "Remove?", anchor = "w").grid(row = 0, column = 20, columnspan = 2, sticky = "ew")
            i = 1
            x = 0
            self.val = IntVar()
            self.totalCost = 0
            for res in self.resList:
                Label(self.makeRev, text=res[0], anchor="w").grid(row=i, column=0,columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[3], anchor="w").grid(row=i, column=2, columnspan =2, sticky="ew")
                Label(self.makeRev, text=res[1], anchor="w").grid(row=i, column=4, columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[2], anchor="w").grid(row=i, column=6, columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[9], anchor="w").grid(row=i, column=8, columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[4], anchor="w").grid(row=i, column=10, columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[5], anchor="w").grid(row=i, column=12, columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[6], anchor="w").grid(row=i, column=14, columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[7], anchor="w").grid(row=i, column=16, columnspan = 2, sticky="ew")
                Label(self.makeRev, text=res[8], anchor="w").grid(row=i, column=18, columnspan = 2, sticky="ew")
                b = Radiobutton(self.makeRev, text = "Remove", variable = self.val, value = x)
                b.grid(row = i, column =20, columnspan = 2, sticky = "ew")
                b.deselect()
                self.totalCost = self.totalCost + res[10]
                
                x = x + 1
                i = i + 1
            
            self.val.set(100)
                
            if (self.student):
                Label(self.makeRev, text = "Student Discount Applied").grid(row = i + 3, column = 0, columnspan = 4, sticky = "ew")
            
            Label(self.makeRev, text = "Total Cost").grid(row = i + 5, column = 0, columnspan = 2, sticky = "ew")
            Label(self.makeRev, text = str(self.totalCost)).grid(row = i + 5, column = 4, columnspan = 4, sticky = "ew")
            delete = Button(self.makeRev, text = "Remove Selected Reservation", command = self.remove)
            delete.grid(row = i + 5, column = 8, columnspan = 4, sticky = "ew")
            add = Button(self.makeRev, text = "Continue Adding Train", command = self.dissimate)
            add.grid(row = i + 5, column = 12, columnspan = 2, sticky = "ew")
            self.Connect()
            Q = "SELECT CardNo FROM PAYMENTINFO WHERE Username = '" + self.username + "'"
            self.Curs.execute(Q)
            owned = self.Curs.fetchall()
            self.caslt = StringVar()
            last4dig = []
            i = 0
            if owned:

                for card in owned:
                    card = ''.join(card)
                    last4dig.insert(i, card[12:16])
                    i += 1
                self.caslt.set(last4dig[0])
                self.wAC = OptionMenu(self.makeRev, self.caslt, *last4dig)
                self.wAC.grid(row=i + 10,column=4)
            else:
                self.caslt.set("No Cards")
                self.wDC = OptionMenu(self.makeRev, self.caslt, "You must have registered cards first")
                self.wDC.grid(row=i + 10,column=10)
            submit = Button(self.makeRev, text = "Submit", command = self.submit)
            submit.grid(row = i + 10, column = 12, columnspan = 2, sticky = "ew")
            paymentInfo = Button(self.makeRev, text = "Add Card", command = self.Payment_Info)
            paymentInfo.grid(row = i + 5, column = 20, columnspan = 2, sticky = "ew")
        
    def backtoSrchTn(self):
        self.makeRev.withdraw()
        self.windSet.deiconify()
        
    def submit(self):
        cardNum = self.caslt.get()
        QCards = "SELECT CardNo FROM PAYMENTINFO WHERE Username = '" + self.username + "'"
        self.Connect()
        self.Curs.execute(QCards)
        owned = self.Curs.fetchall()
        for card in owned:
            card = ''.join(card)
            if cardNum in card:
                cardNum = card
                print(cardNum)
        qsubmit = "INSERT INTO RESERVATION(CardNo, IsCancelled, Username, TotalCost) VALUES('" + cardNum + "', '" + "0" + "', '" + self.username + "', '" + str(self.totalCost) + "')"
        self.Curs.execute(qsubmit)
        maxresid = "SELECT MAX(ReservationID) FROM RESERVATION"
        self.Curs.execute(maxresid)
            
        maxres = self.Curs.fetchall()
        self.resid = maxres[0][0]
        print(self.resid)
        for tup in self.resList:
            qrr = """INSERT INTO RESERVATIONRESERVESTRAINROUTE (ReservationID, TrainNo, Class, DepartDate, PassengerName, NoOfBags, DepartsFrom, ArrivesAt)
        VALUES('""" + str(self.resid) + "','" + tup[0] + "','" + tup[9] + "','" + tup[11] + "','" + tup[6] + "'," + str(tup[5]) + ",'" + tup[7] + "','" + tup[8] + "')"
            self.Curs.execute(qrr)
            print("sccs")
        self.Conf()
        
    def dissimate(self):
        self.windSet.withdraw()
        self.makeRev.withdraw()
        self.windCF.deiconify()




    def remove(self):
        r = self.val.get()
        if r != 100 :
            myList = self.resList[r]

            self.totalCost = self.totalCost -(myList[10])
            del self.resList[r]
            self.makeRev.destroy()

        self.makeResGui()

#Select Departure goes here

    def Extras(self):
        self.extras = Toplevel()
        self.findwin.withdraw()
        self.extras.title("Travel Extras and Passenger Info")

        self.lEX = Label(self.extras, text= "Travel Extras and Passenger Info", font = ("Helvetica",16))
        self.lEX.grid(row = 0, column = 0, pady = 50)

        self.l1EX= Label(self.extras, text= "Number of Bags", font = ("Helvetica", 8))
        self.l1EX.grid(row=1,column=0, sticky= E)

        self.l2EX= Label(self.extras, text= "Up to 4 bags per passenger, 2 free, 2 at $30 per bag", font = ("Helvetica", 8))
        self.l2EX.grid(row=2,column=1, sticky= E)

        self.l3EX= Label(self.extras, text= "Passenger Name", font = ("Helvetica", 8))
        self.l3EX.grid(row=3,column=0, sticky= E)

        self.svEX = StringVar()
        self.svEX.set("")
        w1EX = OptionMenu(self.extras, self.svEX, "0", "1", "2","3", "4")
        w1EX.grid(row=1,column=2)

        self.sv1EX= StringVar()

        self.e1ST= Entry(self.extras, textvariable= self.svEX, width = 30, state= "disabled",bg="gold")
        self.e1ST.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)

        self.e2ST= Entry(self.extras, textvariable= self.sv1EX, width = 30, state= "normal",bg="gold")
        self.e2ST.grid(row=3,column=1, pady= 5, padx = 20, sticky=W)

        self.bST= Button(self.extras, text= "Back", width=12, bg="gold", command = self.Back2ST)
        self.bST.grid(row=4, column=1,  pady = 10, sticky = W)
        print("doing extras")
        Button(self.extras, text= "Next", width=12, bg="gold", command = self.makeRes).grid(row=4, column=2,  pady = 10, sticky = W)

#Make Reservation goes here

#Make Reservation goes here
    def Back2ST (self):
        self.extras.withdraw()
        self.windSet.deiconify()

    def Payment_Info(self):

        self.windPI =Toplevel()

        self.Connect()
        #Get Card Info
        QGetCards = "SELECT CardNo FROM PAYMENTINFO WHERE Username = '" + self.username +"'"
        self.Curs.execute(QGetCards)
        self.cards = self.Curs.fetchall()

        self.lPI = Label(self.windPI, text= "Payment Info", font = ("Helvetica",16))
        self.lPI.grid(row = 0, column = 1, pady = 50)

        #Add Card

        self.l1PI= Label(self.windPI, text= "Add Card", font = ("Helvetica", 12))
        self.l1PI.grid(row=1,column=0, sticky= E)

        self.l2PI= Label(self.windPI, text= "Name on Card", font = ("Helvetica", 8))
        self.l2PI.grid(row=2,column=0, sticky= E)

        self.l3PI= Label(self.windPI, text= "Card Number", font = ("Helvetica", 8))
        self.l3PI.grid(row=3,column=0, sticky= E)

        self.l4PI= Label(self.windPI, text= "CVV", font = ("Helvetica", 8))
        self.l4PI.grid(row=4,column=0, sticky= E)

        self.l5PI= Label(self.windPI, text= "Expiration Date", font = ("Helvetica", 8))
        self.l5PI.grid(row=5,column=0, sticky= E)

        self.lzPI= Label(self.windPI, text= "Format YYYY/MM/DD", font = ("Helvetica", 8))
        self.lzPI.grid(row=6,column=1, sticky= E)



        #Confirm Format

        self.svPI = StringVar()
        self.sv2PI = StringVar()
        self.sv3PI = StringVar()
        self.sv4PI = StringVar()

        self.e1PI= Entry(self.windPI, textvariable= self.svPI, width = 30, state= "normal",bg="gold")
        self.e1PI.grid(row=2,column=1, pady= 5, padx = 20, sticky=W)

        self.e2PI= Entry(self.windPI, textvariable= self.sv2PI, width = 30, state= "normal",bg="gold")
        self.e2PI.grid(row=3,column=1, pady= 5, padx = 20, sticky=W)

        self.e3PI= Entry(self.windPI, textvariable= self.sv3PI, width = 30, state= "normal",bg="gold")
        self.e3PI.grid(row=4,column=1, pady= 5, padx = 20, sticky=W)

        self.e4PI= Entry(self.windPI, textvariable= self.sv4PI, width = 30, state= "normal",bg="gold")
        self.e4PI.grid(row=5,column=1, pady= 5, padx = 20, sticky=W)

        self.bPI= Button(self.windPI, text= "Submit", width=12, bg="gold", command=self.Add_Card)
        self.bPI.grid(row=7, column=1,  pady = 10, sticky = W)

        #Delete Card

        self.l6PI= Label(self.windPI, text= "Delete Card", font = ("Helvetica", 12))
        self.l6PI.grid(row=1,column=2, sticky= E)

        self.l6PI= Label(self.windPI, text= "Card Number", font = ("Helvetica", 8))
        self.l6PI.grid(row=2,column=2, sticky= E)

        self.sv5PI = StringVar()
        last4dig = []
        i = 0
        if self.cards:
            for card in self.cards:
                print(card)
                card = ''.join(card)
                print(card)
                last4dig.insert(i, card[12:16])
                i += 1
            self.sv5PI.set(last4dig[0])
            self.wDC = OptionMenu(self.windPI, self.sv5PI, *last4dig)
            self.wDC.grid(row=2,column=4)
        else:
            self.sv5PI.set("No Cards")
            self.wDC = OptionMenu(self.windPI, self.sv5PI, "You must have registered cards first")
            self.wDC.grid(row=2,column=4)
        self.b2PI= Button(self.windPI, text= "Submit", width=12, bg="gold", command=self.Delete_Card)
        self.b2PI.grid(row=7, column=3,  pady = 10, sticky = W)
##        cardQ = 'SELECT CardNo FROM RESERVATION WHERE Username="'+self.username+'" AND IsCancelled = 0'
##        self.Curs.execute(cardQ)
##        reserved = self.Curs.fetchall()
##        print(reserved)
##        noDelete = []
##        for item in reserved:
##            if item[0] not in noDelete:
##                noDelete.append(item[0])
##        print(noDelete)
    def Add_Card(self):
        nameOnCard = self.svPI.get()
        cardNum = self.sv2PI.get()
        cvv = self.sv3PI.get()
        expDate = self.sv4PI.get()
        
        yearMonthDate = expDate.split("/")

        self.Connect()
        
        n = datetime.now()
        t = n.timetuple()
        year = int(t[0])
        month = int(t[1])
        day = int(t[2])
        QGetCards = "SELECT CardNo FROM PAYMENTINFO WHERE Username = '" + self.username +"'"
        self.Curs.execute(QGetCards)
        self.cards = self.Curs.fetchall()
        QGetAllCards = "SELECT CardNo FROM PAYMENTINFO"
        self.Curs.execute(QGetAllCards)
        self.allCards = self.Curs.fetchall()
        cardList = []
        for card in self.allCards:
            cardList.append(card[0])
        if(cardNum in cardList):
            messagebox.showwarning("Error", "Card with Card Number already exists")
            return
        isIn = False
        for card in self.cards:
            if cardNum == card:
                isIn = True
        print(cardNum)
        print(len(cardNum))
        if len(cardNum) != 16:
            messagebox.showwarning("Invalid CardNo","Card should have 16 numbers")
        elif len(cvv) != 3:
            messagebox.showwarning("Invalid CVV","CVV should be 3 numbers")
        else:
            if not isIn:
                print(yearMonthDate[0])
                print(yearMonthDate[1])
                print(year)
                print(month)
                if int(yearMonthDate[0]) >= year:
                    if int(yearMonthDate[0]) == year:
                        if int(yearMonthDate[1]) >= month:
                            if nameOnCard and cardNum and cvv and expDate:
                                QInsert = "INSERT INTO PAYMENTINFO VALUES('"+cardNum+"',"+cvv+","+"'"+expDate+"','"+nameOnCard+"','"+self.username+"')"
                                self.Curs.execute(QInsert)
                                messagebox.showwarning("Success Adding Card","The Card is Added Successfully")
                            else:
                                messagebox.showwarning("Invalid Card Info","Please Fill Out All Card Information")
                        else:
                            messagebox.showwarning("Invalid Exp Date","This card has been expired")
                    else:
                        if nameOnCard and cardNum and cvv and expDate:
                            QInsert = "INSERT INTO PAYMENTINFO VALUES('"+cardNum+"',"+cvv+","+"'"+expDate+"','"+nameOnCard+"','"+self.username+"')"
                            self.Curs.execute(QInsert)
                            messagebox.showwarning("Success Adding Card","The Card is Added Successfully")
                else:
                    messagebox.showwarning("Invalid Exp Date","This card has been expired")
            else:
                messagebox.showwarning("Duplicated Card Info","This card already exists in your account")


    def Delete_Card(self):
        cardNum = self.sv5PI.get()
        found = False
        for card in self.cards:
            card = ''.join(card)
            if cardNum in card:
                cardNum = card
                found = True
        cardQ = 'SELECT CardNo FROM RESERVATION WHERE Username="'+self.username+'" AND IsCancelled = 0'
        self.Curs.execute(cardQ)
        reserved = self.Curs.fetchall()
        print(reserved)
        noDelete = []
        for item in reserved:
            if item[0] not in noDelete:
                noDelete.append(item[0])
        if(cardNum in noDelete):
            messagebox.showwarning("Error", "Card is being used for a reservation yo.")
            return
            
        if found:
            self.Connect()
            QGetCard = "SELECT CardNo FROM PAYMENTINFO WHERE CardNo = '"+cardNum+"'"
            self.Curs.execute(QGetCard)
            data = self.Curs.fetchall()
            if data:
                QDelete = "DELETE FROM PAYMENTINFO WHERE CardNo = '"+cardNum+"'"
                self.Curs.execute(QDelete)
                messagebox.showwarning("Removed","Card has been deleted.")
            else:
                messagebox.showwarning("Removed Card","This Card has been already removed")
        else:
            messagebox.showwarning("No Card","You should add card first")

    def Conf (self):
        self.makeRev.withdraw()
        self.winConf = Toplevel()
        self.winConf.title("Confirmation")

        self.lCf = Label(self.winConf, text= "Confirmation", font = ("Helvetica",16))
        self.lCf.grid(row = 0, column = 1, pady = 50)

        self.l1Cf= Label(self.winConf, text= "Reservation ID", font = ("Helvetica", 12))
        self.l1Cf.grid(row=1,column=0, sticky= E)

        self.l2Cf= Label(self.winConf, text= "Thanks! Save the R.ID", font = ("Helvetica", 8))
        self.l2Cf.grid(row=2,column=0, sticky= E)

        self.svCf = StringVar()
        #Add query for Res ID
        self.svCf.set(self.resid)

        self.e1Cf= Entry(self.winConf, textvariable= self.svCf, width = 30, state= "normal",bg="gold")
        self.e1Cf.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)

        self.b1Cf= Button(self.winConf, text= "Go back to choose Functionality", width=40, bg="gold", command = self.ConftoCF)
        self.b1Cf.grid(row=3, column=1,  pady = 10, sticky = W)

    def ConftoCF(self):
        self.winConf.withdraw()
        self.windCF.deiconify()

    def Upd_Resv (self):

        self.windUpdRes = Toplevel()
        

        
        self.windUpdRes.title("Update Reservation")

        self.lUR = Label(self.windUpdRes, text= "Update Reservation", font = ("Helvetica",16))
        self.lUR.grid(row = 0, column = 1, pady = 50)

        self.l1UR= Label(self.windUpdRes, text= "Reservation ID", font = ("Helvetica", 8))
        self.l1UR.grid(row=1,column=0, sticky= E)

        self.svUR = StringVar()

        self.e1UR= Entry(self.windUpdRes, textvariable= self.svUR, width = 20, state= "normal",bg="gold")
        self.e1UR.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)

        self.b1UR= Button(self.windUpdRes, text= "Search", width=10, command = self.calc_Updv)
        self.b1UR.grid(row=1, column=2,  pady = 10, sticky = W)

        self.b2UR= Button(self.windUpdRes, text= "Back", width=10, command= self.back_to_Main2)
        self.b2UR.grid(row=3, column=1,  pady = 10, sticky = W)

    def calc_Updv(self):
        self.update = self.svUR.get()
        self.Connect()
        
        QCR= 'Select ReservationID, TotalCost FROM RESERVATION WHERE ((ReservationID = "'+self.update+'") AND (isCancelled = "'+"0"+'"))'
        self.Curs.execute(QCR)
        
        updatev = self.Curs.fetchall()

        if len(updatev) == 0:
            messagebox.showwarning("Error","Enter Valid Res. Number")
            

        else :
            ListUR = []

            for i in updatev:
                ListUR.append(i)

            self.update = str(ListUR [0][0])
            self.currentCost = str(ListUR [0][1])
            print(self.update, self.currentCost)
            QCR2= 'Select TrainNo, DepartsFrom, ArrivesAt, Class, NoOfBags, PassengerName FROM RESERVATIONRESERVESTRAINROUTE WHERE ( ReservationID = "'+self.update+'")'
            self.Curs.execute(QCR2)
            data = self.Curs.fetchall()
            bList=[]
            
            bList.append(data)
            QCR3 = 'SELECT DepartDate FROM RESERVATIONRESERVESTRAINROUTE WHERE ( ReservationID = "'+self.update+'")'
            self.Curs.execute(QCR3)
            aList = []
            dates = self.Curs.fetchall()
            self.currentCost = float(self.currentCost)
        
            aList.append(dates)
            print(aList)
            self.windUpdRes.withdraw()
            self.updateWin = Toplevel()
            Label(self.updateWin, text="Train Number", anchor="w").grid(row=0, column=0,columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Duration", anchor="w").grid(row=0, column=2, columnspan =2, sticky="ew")
            Label(self.updateWin, text="Departure", anchor="w").grid(row=0, column=4, columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Arrival", anchor="w").grid(row=0, column=6, columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Class", anchor="w").grid(row=0, column=8, columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Price", anchor="w").grid(row=0, column=10, columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Bags", anchor="w").grid(row=0, column=12, columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Passenger Name", anchor="w").grid(row=0, column=14, columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Depart Station", anchor="w").grid(row=0, column=16, columnspan = 2, sticky="ew")
            Label(self.updateWin, text="Arrive Station", anchor="w").grid(row=0, column=18, columnspan = 2, sticky="ew")
            Label(self.updateWin, text = "Update", anchor = "w").grid(row = 0, column = 20, columnspan = 2, sticky = "ew")
            
                    
                    
                    
                        
                
            
            self.updateList = []
            
            x = 1
            self.y = IntVar()
            z = 0
            for tup in range(len(bList[0])): #not working when two reservations returned
                print(tup)
                t = ()
                print(aList[0][tup])
                print(bList[0][tup][1], bList[0][tup][2],bList[0][tup][0])
                monster= 'SELECT S.Arrival, S.Departure, TIMEDIFF(S.Arrival, S.Departure) AS Duration FROM (SELECT X.TrainNo, X.DepTime as Departure, Y.ArrivalTime as Arrival, X.StationName as DepartStation, Y.StationName as ArrStation FROM (SELECT TrainNo, DepTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+bList[0][tup][1]+'") AS X JOIN (SELECT TrainNo, ArrivalTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+bList[0][tup][2]+'") AS Y on (X.TrainNo = Y.TrainNo) WHERE (X.DepTime < Y.ArrivalTime)) as S JOIN TRAINROUTE ON (S.TrainNo = TRAINROUTE.TrainNo) WHERE S.TrainNo ="'+bList[0][tup][0]+'"'
                self.Curs.execute(monster)
                cList = []
                for item in self.Curs.fetchall():
                    cList.append(item)
                route = "SELECT FirstClassPrice, SecondClassPrice, TrainNo FROM TRAINROUTE WHERE TrainNo = '"+bList[0][tup][0]+"'"
                self.Curs.execute(route)
                dList = []
                for item in self.Curs.fetchall():
                    dList.append(item)
                sprice = dList[0][1]
                fprice = dList[0][0]
                if bList[0][tup][3] == "1st Class":
                    price = fprice;
                else:
                    price = sprice
                print(cList, dList)
                Label(self.updateWin, text=bList[0][tup][0], anchor="w").grid(row=x, column=0,columnspan = 2, sticky="ew")
                Label(self.updateWin, text=cList[0][2], anchor="w").grid(row=x, column=2, columnspan =2, sticky="ew")
                Label(self.updateWin, text=cList[0][1], anchor="w").grid(row=x, column=4, columnspan = 2, sticky="ew")
                Label(self.updateWin, text=cList[0][0], anchor="w").grid(row=x, column=6, columnspan = 2, sticky="ew")
                Label(self.updateWin, text=bList[0][tup][3], anchor="w").grid(row=x, column=8, columnspan = 2, sticky="ew")
                Label(self.updateWin, text=price, anchor="w").grid(row=x, column=10, columnspan = 2, sticky="ew")
                Label(self.updateWin, text=bList[0][tup][4], anchor="w").grid(row=x, column=12, columnspan = 2, sticky="ew")
                Label(self.updateWin, text=bList[0][tup][5], anchor="w").grid(row=x, column=14, columnspan = 2, sticky="ew")
                Label(self.updateWin, text=bList[0][tup][1], anchor="w").grid(row=x, column=16, columnspan = 2, sticky="ew")
                Label(self.updateWin, text=bList[0][tup][2], anchor="w").grid(row=x, column=18, columnspan = 2, sticky="ew")
                Radiobutton(self.updateWin, text = "Update?", variable = self.y, value = z,  anchor = "w").grid(row = x, column = 20, columnspan = 2, sticky = "ew")
                x = x + 1
                z = z + 1
                t = t +(bList[0][tup][0], cList[0][2], cList[0][1], cList[0][0], bList[0][tup][3], price, bList[0][tup][4], bList[0][tup][5], bList[0][tup][1], bList[0][tup][2],self.update,self.currentCost,aList[0][tup])
                self.updateList.append(t)
            Button(self.updateWin, text = "Update",anchor = "w", command = self.Upd_Resv2).grid(row = x + 2, column = 0, columnspan = 2, sticky = "ew")
            self.y.set(100)        
    #Add Upd Resrv dynamic parts
    def Upd_Resv2(self):
        print(self.updateList)
        print(self.y.get())
        if(self.y.get() == 100):
            messagebox.showwarning("Error", "Nothing Selected to Update")
        else:
            toUpdate = self.y.get()
            dateQuery = 'SELECT DepartDate FROM RESERVATIONRESERVESTRAINROUTE WHERE ReservationID ="'+self.update+'" AND TrainNo ="'+self.updateList[toUpdate][0]+'"'
            self.Connect()
            self.Curs.execute(dateQuery)
            d = self.Curs.fetchall()
            diff = d[0][0] - date.today()
            print(diff)
            if (diff.days < 1):
                messagebox.showwarning("Error", "Too Close to Departure Date")
            else:
                
            
                self.updateWin.withdraw()
                self.updateWin2 = Toplevel()
                self.updateWin2.title("Selected Reservation")
                Label(self.updateWin2, text="Train Number", anchor="w").grid(row=0, column=0,columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Duration", anchor="w").grid(row=0, column=2, columnspan =2, sticky="ew")
                Label(self.updateWin2, text="Departure", anchor="w").grid(row=0, column=4, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Arrival", anchor="w").grid(row=0, column=6, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Class", anchor="w").grid(row=0, column=8, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Price", anchor="w").grid(row=0, column=10, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Bags", anchor="w").grid(row=0, column=12, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Passenger Name", anchor="w").grid(row=0, column=14, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Depart Station", anchor="w").grid(row=0, column=16, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text="Arrive Station", anchor="w").grid(row=0, column=18, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][0], anchor="w").grid(row=1, column=0,columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][1], anchor="w").grid(row=1, column=2, columnspan =2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][2], anchor="w").grid(row=1, column=4, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][3], anchor="w").grid(row=1, column=6, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][4], anchor="w").grid(row=1, column=8, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][5], anchor="w").grid(row=1, column=10, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][6], anchor="w").grid(row=1, column=12, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][7], anchor="w").grid(row=1, column=14, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][8], anchor="w").grid(row=1, column=16, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text=self.updateList[toUpdate][9], anchor="w").grid(row=1, column=18, columnspan = 2, sticky="ew")
                Label(self.updateWin2, text = "New Departure Date", anchor = "w").grid(row = 2, column = 0, columnspan = 2, sticky = "ew")
                self.updateSV = StringVar()
                Entry(self.updateWin2, textvariable= self.updateSV, width = 20, state= "normal",bg="gold").grid(row = 2, column = 2, columnspan = 4, sticky = "ew")
                Label(self.updateWin2, text = "Enter Date in Format YY/MM/DD", anchor = "w").grid(row = 2, column = 8, columnspan = 4, sticky = "ew")
                Button(self.updateWin2, text = "Next", anchor = "w", command = self.Upd_Resv3).grid(row = 2, column = 14, columnspan = 2, sticky = "ew")

    def Upd_Resv3(self):
        dat = self.updateSV.get()
        toUpdate = self.y.get()
        print(dat)
        if(len(dat) == 0):
            messagebox.showwarning("Error", "Please Enter a value in Date")
        
        try:
            new = datetime.strptime(dat, "%y/%m/%d").date()
            print("Reached Try")
##            print(new)
##            #print(self.updateList, len(self.updateList[0]))
##            #print(self.updateList[0][12])
##            self.diff1 = new - date.today()
##            print(self.diff1)
        except:
            print("Reached Except")
            messagebox.showwarning("Error", "Enter Date in correct format")
        diff1 = new - date.today()
        print(diff1)
        if (diff1.days <= 0):
            messagebox.showwarning("Error", "Please select new date after current departure date")
        else:
            updateQ = 'UPDATE RESERVATIONRESERVESTRAINROUTE SET DepartDate="'+str(new)+'" WHERE TrainNo="'+self.updateList[toUpdate][0]+'" AND ReservationID = "'+self.updateList[toUpdate][10]+'"'
            self.Connect()
            self.Curs.execute(updateQ)
            self.newDate = dat
            print("reached again")

            self.updateWin2.withdraw()
            self.updateWin3 = Toplevel()
            Label(self.updateWin3, text="Train Number", anchor="w").grid(row=0, column=0,columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Duration", anchor="w").grid(row=0, column=2, columnspan =2, sticky="ew")
            Label(self.updateWin3, text="Departure", anchor="w").grid(row=0, column=4, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Arrival", anchor="w").grid(row=0, column=6, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Class", anchor="w").grid(row=0, column=8, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Price", anchor="w").grid(row=0, column=10, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Bags", anchor="w").grid(row=0, column=12, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Passenger Name", anchor="w").grid(row=0, column=14, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Depart Station", anchor="w").grid(row=0, column=16, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text="Arrive Station", anchor="w").grid(row=0, column=18, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text = "New Departure Date", anchor = "w").grid(row = 0, column = 20, columnspan = 2, sticky = "ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][0], anchor="w").grid(row=1, column=0,columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][1], anchor="w").grid(row=1, column=2, columnspan =2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][2], anchor="w").grid(row=1, column=4, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][3], anchor="w").grid(row=1, column=6, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][4], anchor="w").grid(row=1, column=8, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][5], anchor="w").grid(row=1, column=10, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][6], anchor="w").grid(row=1, column=12, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][7], anchor="w").grid(row=1, column=14, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][8], anchor="w").grid(row=1, column=16, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text=self.updateList[toUpdate][9], anchor="w").grid(row=1, column=18, columnspan = 2, sticky="ew")
            Label(self.updateWin3, text = self.newDate, anchor = "w").grid(row = 1, column = 20, columnspan = 2, sticky = "ew")
            Label(self.updateWin3, text = "Cost of Update", anchor = "w").grid(row = 2, column = 0, columnspan = 2, sticky = "ew")
            Label(self.updateWin3, text = "50", anchor = "w").grid(row = 2, column = 2, columnspan = 2, sticky = "ew")
            Label(self.updateWin3, text = "Updated Cost", anchor = "w").grid(row = 3, column = 0, columnspan = 2, sticky = "ew")
            self.currentCost = self.currentCost + 50
            Label(self.updateWin3, text = str(self.currentCost), anchor = "w").grid(row = 3, column = 2, columnspan = 2, sticky = "ew")
            resQ = 'UPDATE RESERVATION SET TotalCost ="'+str(self.currentCost)+'" WHERE ReservationID ="'+self.update+'"'
            self.Connect()
            self.Curs.execute(resQ)
            Button(self.updateWin3, text = "Back",anchor = "w", command= self.back_to_Main).grid(row = 4,column = 0, columnspan = 2, sticky = "ew")

    def back_to_Main(self):

        self.updateWin3.withdraw()
        self.windCF.deiconify()

    def back_to_Main2(self):
        self.windUpdRes.withdraw()
        self.windCF.deiconify()
        
            
            
        
            
            
    def Canc_Resv (self):

        self.windCanRe = Toplevel()


        self.lCaR = Label(self.windCanRe, text= "Cancel Reservation", font = ("Helvetica",16))
        self.lCaR.grid(row = 0, column = 1, pady = 50)

        self.l1CaR= Label(self.windCanRe, text= "Reservation ID", font = ("Helvetica", 8))
        self.l1CaR.grid(row=1,column=0, sticky= E)

        self.svCaR = StringVar()

        self.e1CaR= Entry(self.windCanRe, textvariable= self.svCaR, width = 20, state= "normal",bg="gold")
        self.e1CaR.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)

        self.b1CaR= Button(self.windCanRe, text= "Search", width=10, command = self.CRFunc)
        self.b1CaR.grid(row=1, column=2,  pady = 10, sticky = W)

        self.b2CaR= Button(self.windCanRe, text= "Back", width=10, command= self.CRtoCF)
        self.b2CaR.grid(row=3, column=1,  pady = 10, sticky = W)

    def CRtoCF(self):
        self.windCanRe.withdraw()
        self.windCF.deiconify()
        
    def cancelTree(self, frame) :
        tree3 = ttk.Treeview(frame)
        tree3.pack()
        tree3["show"] = "headings"
        tree3["columns"] = ("Train", "Departure Time","Arrival Time", "Departs From", "Arrives At","Class", "Price", "Bags", "Passenger Name")
        tree3.heading("Train", text = "Train")
        tree3.heading("Departure Time", text = "Departure Time")
        tree3.heading("Arrival Time", text = "Arrival Time")
        tree3.heading("Departs From", text = "Departs From")
        tree3.heading("Arrives At", text = "Arrives At")
        tree3.heading("Class", text = "Class")
        tree3.heading("Price", text= "Price")
        tree3.heading("Bags", text = "Bags")
        tree3.heading("Passenger Name", text = "Passenger Name")
        return tree3
    def cancelTree2(self, frame) :
        tree4 = ttk.Treeview(frame)
        tree4.pack()
        tree4["show"] = "headings"
        tree4["columns"] = ("Total Cost", "Date of Cancellation", "Refund")
        
        tree4.heading("Total Cost", text = "Total Cost")
        tree4.heading("Date of Cancellation", text = "Date of Cancellation")
        tree4.heading("Refund", text = "Refund")
        
        return tree4
        
        
        
    def CRFunc(self):
        self.Connect()
        self.resid= self.svCaR.get()
        QCR= 'Select ReservationID, TotalCost FROM RESERVATION WHERE ((ReservationID = "'+self.resid+'") AND (isCancelled = "'+"0"+'"))'
        self.Curs.execute(QCR)
        
        cancelv = self.Curs.fetchall()

        if len(cancelv) == 0:
            messagebox.showwarning("Error","Enter Valid Res. Number")
            

        else :
            ListCR = []

            for i in cancelv:
                ListCR.append(i)

            self.rid = str(ListCR [0][0])
            TotalCst= str(ListCR [0][1])
            print(self.rid, TotalCst)
            QCR2= 'Select TrainNo, DepartsFrom, ArrivesAt, Class, NoOfBags, PassengerName FROM RESERVATIONRESERVESTRAINROUTE WHERE ( ReservationID = "'+self.rid+'")'
            self.Curs.execute(QCR2)
            data = self.Curs.fetchall()
            bList=[]
            
            bList.append(data)
            QCR3 = 'SELECT DepartDate FROM RESERVATIONRESERVESTRAINROUTE WHERE ( ReservationID = "'+self.rid+'")'
            self.Curs.execute(QCR3)
            aList = []
            dates = self.Curs.fetchall()
            TotalCst = float(TotalCst)
            for item in dates:
                aList.append(item)
            #fprint(aList[0][0],aList[1][0])
            earliest = aList[0][0]
            print(aList)
            if len(aList) > 1 :
                for l in range(len(aList)):
                    
                    if aList[l][0] < earliest:
                    
                        earliest = aList[l][0]
                
            else :
                earliest = aList[0][0]
            print(earliest)
            difference = earliest - date.today()
            if(difference.days <= 1) :
                messagebox.showwarning("Cancel", "Unable To Cancel Because its too late")
                return
            elif (difference.days > 7):
                refund = 0.8* TotalCst - 50
            else:
                refund = 0.5*TotalCst - 50
            if refund < 0:
                refund = 0
            print(TotalCst, refund)
            
            
            
            self.winCancel = Toplevel()
            self.rootWin.withdraw()
            frame3 = Frame(self.winCancel)
            frame3.pack(side = TOP)
            tree3 = self.cancelTree(frame3)
            self.Connect()
            print(bList, len(bList),len(bList[0]), len(bList[0][0]))
            for tup in range(len(bList[0])): #not working when two reservations returned
                print(tup)
                print(bList[0][tup][1], bList[0][tup][2],bList[0][tup][0])
                monster= 'SELECT S.Arrival, S.Departure, TIMEDIFF(S.Arrival, S.Departure) AS Duration FROM (SELECT X.TrainNo, X.DepTime as Departure, Y.ArrivalTime as Arrival, X.StationName as DepartStation, Y.StationName as ArrStation FROM (SELECT TrainNo, DepTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+bList[0][tup][1]+'") AS X JOIN (SELECT TrainNo, ArrivalTime, StationName FROM TRAINSTOPSATSTATION  WHERE StationName = "'+bList[0][tup][2]+'") AS Y on (X.TrainNo = Y.TrainNo) WHERE (X.DepTime < Y.ArrivalTime)) as S JOIN TRAINROUTE ON (S.TrainNo = TRAINROUTE.TrainNo) WHERE S.TrainNo ="'+bList[0][tup][0]+'"'
                self.Curs.execute(monster)
                cList = []
                for item in self.Curs.fetchall():
                    cList.append(item)
                route = "SELECT FirstClassPrice, SecondClassPrice, TrainNo FROM TRAINROUTE WHERE TrainNo = '"+bList[0][tup][0]+"'"
                self.Curs.execute(route)
                dList = []
                for item in self.Curs.fetchall():
                    dList.append(item)
                sprice = dList[0][1]
                fprice = dList[0][0]
                if bList[0][tup][3] == "1st Class":
                    price = fprice;
                else:
                    price = sprice
                print(cList, dList)
                tree3.insert("", 0, text = "Line 1", values = (bList[0][tup][0], cList[0][1],  cList[0][0],bList[0][tup][1],bList[0][tup][2],bList[0][tup][3], price, bList[0][tup][4], bList[0][tup][5] ))
            frame4 = Frame(self.winCancel)
            frame4.pack(side = TOP)
            
            tree4 = self.cancelTree2(frame4)
            tree4.insert("", 0, text = "Line 1", values = (TotalCst, date.today(), refund))
                          
            cancelled = 'UPDATE RESERVATION SET IsCancelled = 1 WHERE ReservationID ="'+self.rid+'"'
            self.Curs.execute(cancelled)
        

        
    def Write_Rev (self):

        self.windGR = Toplevel()
        self.windCF.withdraw()
        

        self.lGvR = Label(self.windGR, text= "Give Review", font = ("Helvetica",16))
        self.lGvR.grid(row = 0, column = 1, pady = 50)

        self.l1GvR= Label(self.windGR, text= "Train Number", font = ("Helvetica", 8))
        self.l1GvR.grid(row=1,column=0, sticky= E)

        self.l2GvR= Label(self.windGR, text= "Rating", font = ("Helvetica", 8))
        self.l2GvR.grid(row=2,column=0, sticky= E)

        self.l3GvR= Label(self.windGR, text= "Comment", font = ("Helvetica", 8))
        self.l3GvR.grid(row=3,column=0, sticky= E)

        self.sv2GvR = StringVar()
        self.sv2GvR.set("VERY GOOD")
        self.w2GvR = OptionMenu(self.windGR, self.sv2GvR, "VERY GOOD", "GOOD", "NEUTRAL","BAD", "VERY BAD")
        self.w2GvR.grid(row=2,column=2)
        

        self.sv1GvR = StringVar()
        self.sv3GvR = StringVar()
        
        self.e1GvR= Entry(self.windGR, textvariable= self.sv1GvR, width = 20, state= "normal",bg="gold")
        self.e1GvR.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)
        
        self.e1GvR= Entry(self.windGR, textvariable= self.sv2GvR, width = 20, state= "disabled",bg="gold")
        self.e1GvR.grid(row=2,column=1, pady= 5, padx = 20, sticky=W)
        
        self.e1GvR= Entry(self.windGR, textvariable= self.sv3GvR, width = 20, state= "normal",bg="gold")
        self.e1GvR.grid(row=3,column=1, pady= 5, padx = 20, sticky=W)

        self.b1GvR= Button(self.windGR, text= "Submit", width=10, command = self.Give_Rev)
        self.b1GvR.grid(row=4, column=1,  pady = 10, sticky = W)

        self.b2GvR= Button(self.windGR, text= "Back", width=10, command = self.GvRtoCF)
        self.b2GvR.grid(row=4, column=2,  pady = 10, sticky = W)
        
    def Give_Rev(self):
        trainNo = self.sv1GvR.get()
        rating = self.sv2GvR.get()
        print(rating)
        comment = self.sv3GvR.get()
        
        self.Connect()

        Q = "SELECT TrainNo FROM TRAINROUTE WHERE TrainNo = '" + trainNo + "'"

        self.Curs.execute(Q)
        data = self.Curs.fetchall()
        if data:
            QInsert = "INSERT INTO REVIEW(Comment, Rating, Username, TrainNo) VALUES('" + comment + "', '" + rating + "', '" + self.username + "', '" + trainNo + "')"
            self.Curs.execute(QInsert)
            messagebox.showwarning("Success","Thank you for your review for " + trainNo)
        else:
            messagebox.showwarning("Inccorect Train Number","Enter Correct Train Number")

    def GvRtoCF(self):
        self.windGR.withdraw()
        self.windCF.deiconify()




#MANAGER VIEWS

    def Man_Ch_Func(self):

        self.windMCF = Toplevel()
        self.rootWin.withdraw()


        self.lMCF = Label(self.windMCF, text= "Choose Functionality", font = ("Helvetica",16))
        self.lMCF.grid(row = 0, column = 1, pady = 50)

        self.b1MCF= Button(self.windMCF, text= "View Revenue Report", width=40, bg="white", command= self.View_Rev_Rpt)
        self.b1MCF.grid(row=1, column=1,  pady = 10, sticky = W)

        self.b2MCF= Button(self.windMCF, text= "View Popular Route Report", width=40, bg="white", command= self.createPop)
        self.b2MCF.grid(row=2, column=1,  pady = 10, sticky = W)

        self.b3MCF= Button(self.windMCF, text= "Log Out", width=12, bg="gold", command= self.LogOutMGR)
        self.b3MCF.grid(row=3, column=1,  pady = 10, sticky = W)


###################################################################################
    def View_Rev_Rpt(self): 
        self.Connect()

        Queryrr =  "Select F.M as Month, TotalCost as Revenue FROM(Select ReservationID, month(DepartDate) as M FROM RESERVATIONRESERVESTRAINROUTE WHERE((month(CurDate())- month(DepartDate)<=3) AND (month(CurDate())- month(DepartDate) > 0))) AS F JOIN RESERVATION ON (F.ReservationID = RESERVATION.ReservationID) GROUP BY F.M"
        
        self.Curs.execute(Queryrr)
        L = []
        for i in self.Curs:
            L.append(i)
        if (len(L) != 0):
            self.windowRevR = Toplevel()
            #self.windMCF.withdraw() 
            
            
            framerr = Frame(self.windowRevR)
            framerr.pack()
            self.l0VRR = Label(framerr, text= "View Revenue Report")
            self.l0VRR.pack(side = TOP)
            treerr = self.getReportTree(framerr)
            treerr.pack(side = TOP)
    
            for row in L:
                if (str(row[0])== "1"):
                    monthyo = "January"
                elif(str(row[0])== "2"):
                    monthyo = "February"
                else:
                    monthyo = "March"
                treerr.insert("", 0, text = "Line 1", values = (monthyo, row[1]))
                
        else:
            messagebox.showwarning("Incorect Train Number","Enter Correct Train Number")

        
            



    def getReportTree(self, frame):
        Rtree = ttk.Treeview(frame)
        Rtree.pack()
        Rtree["show"] = "headings"
        Rtree["columns"] = ("Month", "TotalCost")
        Rtree.heading("Month", text = "Month")
        Rtree.heading("TotalCost", text = "Total Cost")

        #add back button
        #get month names
        
        return Rtree

    def LogOutMGR (self):
        self.windMCF.withdraw()
        self.rootWin.deiconify()

    #View Review

    def Find_Rev(self):

        self.windRe = Toplevel()
        
        self.lFVR = Label(self.windRe, text= "View Review", font = ("Helvetica",16))
        self.lFVR.grid(row = 0, column = 1, pady = 50)

        self.l1FVR= Label(self.windRe, text= "Train Number", font = ("Helvetica", 8))
        self.l1FVR.grid(row=1,column=0, sticky= E)

        self.svFVR = StringVar()
        
        self.e1FVR= Entry(self.windRe, textvariable= self.svFVR, width = 20, state= "normal",bg="gold")
        self.e1FVR.grid(row=1,column=1, pady= 5, padx = 20, sticky=W)

        self.b1FVR= Button(self.windRe, text= "Back", width=10, command = self.ViewRevtoCF)
        self.b1FVR.grid(row=2, column=0,  pady = 10, sticky = W)

        self.b2FVR= Button(self.windRe, text= "Next", width=10, command = self.View_Rev)
        self.b2FVR.grid(row=2, column=1,  pady = 10, sticky = W)

    def View_Rev(self):


        self.Connect()
        
        trainNo = self.svFVR.get()
        QReview = "SELECT Comment, Rating FROM REVIEW WHERE TrainNo = '" + trainNo + "'"
        self.Curs.execute(QReview)
        reviews = self.Curs.fetchall()

        QTrain = "SELECT TrainNo FROM TRAINROUTE WHERE TrainNo = '" + trainNo + "'"
        self.Curs.execute(QTrain)
        train = self.Curs.fetchall()
        
        if train:
            if reviews:
                K = []
                for review in reviews:
                    
                    K.append(review)
                if (len(K) != 0):
                    self.windRe2 = Toplevel()
                    self.windRe.withdraw()
                     
            
                    framere = Frame(self.windRe2)
                    framere.pack()
                    self.l0VRE = Label(framere, text= "View Review")
                    self.l0VRE.pack(side = TOP)
                    treere = self.getReviewTree(framere)
                    treere.pack(side = TOP)
 
    
                for row in K:
                
                    treere.insert("", 0, text = "Line 1", values = (str(row[0]), row[1]))
                
            else:
                messagebox.showwarning("No Review Found","There is no review for " + ''.join(train))
        else:
            messagebox.showwarning("No Train Found","There is no such train " + ''.join(train))
        

        self.b1VR= Button(self.windRe2, text= "Check Another", width=30, command = self.CheckAnother)
        self.b1VR.pack(side=TOP)

    def CheckAnother(self):
        self.windRe2.withdraw()
        self.windRe.deiconify()

    def ViewRevtoCF (self):
        
        self.windRe.withdraw()
        self.windCF.deiconify()
        
        

    def getReviewTree(self, frame):
        Retree = ttk.Treeview(frame)
        Retree.pack()
        Retree["show"] = "headings"
        Retree["columns"] = ("Comment", "Rating")
        Retree.heading("Comment", text = "Comment")
        Retree.heading("Rating", text = "Rating")

        return Retree

    def popTree(self,frame):
        tree = ttk.Treeview(frame)
        tree.pack()
        tree["show"] = "headings"
        tree["columns"] = ("Month", "Train", "Reservations")
        tree.heading("Month", text = "Month")
        tree.heading("Train", text = "Train")
        tree.heading("Reservations", text = "Number of Reservations")
        return tree

    def createPop(self):

        self.createPwin = Toplevel()
        print("reached here")
        popular = 'SELECT count(TrainNo),TrainNo, month(DepartDate) FROM ((SELECT ReservationID FROM RESERVATION WHERE (IsCancelled = 0)) AS S JOIN RESERVATIONRESERVESTRAINROUTE ON (S.ReservationID = RESERVATIONRESERVESTRAINROUTE.ReservationID))  WHERE(month(DepartDate) < 4 AND month(DepartDate) > 0 ) GROUP BY month(DepartDate), TrainNo'
        self.Connect()
        self.Curs.execute(popular)
        reports = self.Curs.fetchall()
        m1reservations = []
        m2reservations = []
        m3reservations = []
            
        for tup in reports:
            if (int(tup[2]) == 1):
                m1reservations.append(tup)
            elif (int(tup[2]) == 2):
                m2reservations.append(tup)
            elif (int(tup[2]) == 3) :
                m3reservations.append(tup)
        resList = []
        newList = []
        for i in m1reservations:
            
            resList.append(int(i[0]))
        resList.sort()
        
        for x in resList:
            print(x)
            for y in m1reservations:
                print(y)
                print(y[0])
                if (x == y[0] and y not in newList):
                    print("reached here")
                    newList.append(y)
        resList2 = []
        newList2 = []
        resList3 = []
        newList3 = []
        for i in m2reservations:
            
            resList2.append(int(i[0]))
        resList2.sort()
        
        for x in resList2:
            
            for y in m2reservations:
                print(y)
                print(y[0])
                if (x == y[0] and y not in newList2):
                    print("reached here")
                    newList2.append(y)
        
        for i in m3reservations:
            
            resList3.append(int(i[0]))
        resList3.sort()
            
        for x in resList3:
            print(x)
            for y in m3reservations:
                print(y)
                print(y[0])
                if (x == y[0] and y not in newList3):
                    print("reached here")
                    newList3.append(y)
        
        print(m1reservations, m2reservations, m3reservations)
        
        print(newList, newList2, newList3)
        count1 = 0
        count2 = 0
        count3 = 0
        check1 = 0 
        check2 = 0
        check3 = 0
        monthcheck = 0
        frame1 = Frame(self.createPwin)
        frame1.pack()
        tree = self.popTree(frame1)
        tree.pack()
        while(count1  < 3 and check1<len(newList)):
            if(monthcheck == 2 or monthcheck == len(newList)-1):
                tree.insert("", 0, text = "Line 1", values = ("January", newList[count1][1], newList[count1][0]))

            else:
                tree.insert("", 0, text = "Line 1", values = (" ", newList[count1][1], newList[count1][0]))
            count1 = count1 + 1
            check1 = check1 + 1
            monthcheck = monthcheck + 1 

        monthcheck = 0
        while(count2  < 3 and check2<len(newList2)):
            if(monthcheck == 2 or monthcheck == len(newList2)-1):
                tree.insert("", 0, text = "Line 1", values = ("February", newList2[count2][1], newList2[count2][0]))

            else:
                tree.insert("", 0, text = "Line 1", values = (" ", newList2[count2][1], newList2[count2][0]))
            count2 = count2 + 1
            check2 = check2 + 1
            monthcheck = monthcheck + 1
            
        monthcheck = 0
        while(count3  < 3 and check3<len(newList3)):

            if(monthcheck == 2 or monthcheck == len(newList3)-1):
                tree.insert("", 0, text = "Line 1", values = ("March", newList3[count3][1], newList3[count3][0]))

            else:
                tree.insert("", 0, text = "Line 1", values = (" ", newList3[count3][1], newList3[count3][0]))
            count3 = count3 + 1
            check3 = check3 + 1
            monthcheck = monthcheck + 1
            
        
        
        
        
        

        
        
        

        

        
        
        

        

        

       

        
        
        

        





         
        
        
        

        

        


        


Win= Tk()
app= Phasetres(Win)
Win.mainloop()


        
        

        
