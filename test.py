import datetime
from re import L
from time import sleep
from turtle import color
from pymongo import MongoClient,errors
import warnings  # to avoid the update() depreactionWarning (mongoDB)
warnings.filterwarnings("ignore",category=DeprecationWarning)


#connection to database 
client = MongoClient("mongodb://127.0.0.1:27017")

db = client["database"] #database

#collections
patdb = db["patient"] 
bloodb = db["blood"]
docdb = db["Doctors"]

#print(db.list_collection_names())


#contains the color code for termainal 
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




#class handling a Exception 
class custom(Exception):
    pass

##functions 

def doctors():
    """ the doctor gets access to the patient document and the blood document
    """

    print("Hey!! Doc nice to see you !!")
    print(colors.OKBLUE+"What you want to do today ? "+colors.ENDC)
    sleep(0.8)
    print("""
    1.view patients name and their personal data 
    2.get patients data of a particular blood group
    3.add a new Doctor 
    4.view the Doctor's Data 
    """)
    a = int(input())
    try:
        if a == 1:
            pname = input("Enter the name of the patient:").lower().strip()

            value = patdb.find({"name":pname}) # retrieving the data from the database by the [name]
            if value:
                print(" \n name :{0}\n age: {1} \nblood group : {2}\n address : {3}\n".format(value[0]["name"], value[0]["age"], value[0]["bloodGRP"], value[0]["address"]))

            else:
                print(colors.WARNING+"The patient doesn't exitst !!"+colors.ENDC)

        elif a == 2 :
            bloodGroup = input("Enter the blood group: ").upper()
            print(bloodGroup)
            query = bloodb.find({"bloodgrp":bloodGroup})
            query=list(query)
            if query:
                print("The blood group {0} exits in blood bank cout: {1} ".format(query[0]["bloodgrp"],query[0]["count"]))
            else:
                print("The blood group doesn't exists in the bank!!!")

        elif a == 3:
            dname = str(input("Enter the name :"))
            role = str(input("Enter the role:"))
            docdb.insert({"name":dname,"splt":role})
            print(colors.OKGREEN+"Data added"+colors.ENDC)
        
        elif a == 4: 
            data = list(docdb.find({}))
            for i in range(len(data)):
                print("name:{0} Role:{1}".format(data[i]["name"],data[i]["splt"]))
        else : 
            raise ValueError
    except ValueError :
        print("Check the option you have entered!!!!")

    

def patient():
    print("""Welcome!! Blood bank welcomes you heartly!! """)
    print("""please select below options to proceed further:
    1:Add new patient data 
    2.View your data 
    3.Update the data """)
    option = int(input())
    year = datetime.date.today().year
    today =str(datetime.date.today())



    if option == 1 :
        try:
            name = str(input("Please Enter your name: ")).lower()
            age = int(input("please Enter your age :"))
            birth_year = int (input("Please Enter year: "))
            add = str(input("Enter the present address:"))
            bloodgrp = input("Enter your blood group:").upper()
            
            
            if (year-birth_year)>=18 and year-birth_year == age :
                try: 
                    insert = {
                        "name":name,
                        "age":age,
                        "birth_year":birth_year,
                        "address":add,
                        "bloodGRP":bloodgrp,
                        "date":today        
                                }
                    patdb.insert_one(insert)
                    if patdb:
                        print(colors.OKGREEN+"YOURE DATA IS ADDED SUCCESSFULLY!!!"+colors.ENDC)
                        update() # calls thee function to upodate the user data into the blood document 
                    else:
                        raise custom
                except errors.DuplicateKeyError:
                    print(colors.WARNING+"The user is already present inside the database !!!!!"+colors.ENDC)
            else: 
                print(colors.BOLD+"You are too young to give blood !!!!"+colors.ENDC)
        except custom:
            print(colors.FAIL+"ERROR WITH ADDING DATA OR DATABASE ERROR !!!!"+colors.ENDC)

        except KeyboardInterrupt:
            print(colors.FAIL+"Terminating......"+colors.ENDC)
            
    elif option == 2:
        check_db = str(input("please enter the name of the patient: ")).lower()
        data_check =list( patdb.find({"name":check_db}))

        if data_check:
            print("name :{0}\n age: {1} \nblood group : {2}\n address : {3}\n".format(data_check[0]["name"], data_check[0]["age"], data_check[0]["bloodGRP"], data_check[0]["address"]))
        else:
            print("No details found regarding this user !!!")

    elif option == 3:
        print("Please enter the updated values::: ")
        name = str(input("Enter who's do u want to change:")).lower()
        update_name = str(input("Enter name : ")).lower()
        age = int(input("please Enter your age :"))
        birth_year = int (input("Please Enter year: "))
        add = str(input("Enter the present address:"))
        bloodgrp = input("Enter your blood group:").upper()

        updated = patdb.replace_one({"name":name},{"name":update_name,"age":age,"birth_year":birth_year,"address":add,"bloodGRP":bloodgrp,"date":today})
        if updated : 
            print("The user has been found and the changes have been made !!")
        else :
            print("User not found !!!")
        
    else :
        raise ValueError

def bloodBank():
    print("Welcome to blood bank !!!")
    blood = str(input("Enter the blood group:")).upper()
    bloodlist = ["A+","A-","AB+","AB-","B+","B-","O+","O-"]

    if blood in bloodlist:
        query_blood = list(bloodb.find({"bloodgrp":blood}))
        print("the amount of the blood available is {} packs".format(query_blood[0]["count"]))
    else:
        print(colors.FAIL+"Please re-enter the blood group!!! "+colors.ENDC)
    
def update():
    pdb = list(patdb.find())
    count_bloodGRP = []

    for i in range(len(pdb)):
        count_bloodGRP.append(pdb[i]["bloodGRP"])

    for i in range(len(count_bloodGRP)):
        bloodb.update({"bloodgrp":count_bloodGRP[i]},{"$inc":{"count":1}})
            

        

##welcoming 
##driver code

print(colors.HEADER+"Welcome".center(20,'*')+colors.ENDC)

print("Enter your access to the database:")
print("""
1.Doctor
2.patient
3.require blood """)
try :    
    option = int(input())

    if option == 1 : 
        doctors()
    elif option == 2:
        patient()
    elif option == 3:
        bloodBank()
    else:
        raise ValueError

except KeyboardInterrupt :
    print(colors.FAIL+"Terminating......"+colors.ENDC)


