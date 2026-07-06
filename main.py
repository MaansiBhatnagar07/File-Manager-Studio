from pathlib import Path 
import os 

def createfile():
    try: 
        name = input("Please tell your file name:-  ")
        path = Path(name)
        if not path.exists():
            with open(path, "w") as fs:
                data = input("what you want to write:-  ")
                fs.write(data)
            print("file created successfully")
        else:
            print("Error file name already exists")
    except Exception as err:
        print(f"an error occured as {err}")



def readfile():
    try:
        name = input("Please tell your file name:- ")
        path = Path(name)
        if path.exists():
            with open(path, "r") as fs :
                content = fs.read()
                print(f"your file name is \n {content}")
        else:
            print("Error no such file exists")
    except Exception as err:
        print(f"an error occured as {err}")


def updatefile():
    try:
        name = input("Plesee tell me your file namr")
        path = Path(name)

        if path.exists():
            print("OPERATIONS")
            print("1. Renaming the file")
            print("2. Appending the clone")
            print("3. Overwriting the file ")

            choice = int(input("enter your option:- "))
            
            if choice ==1:
                newname = input("tell me your new name:= ")
                new_path = Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("reanmed successfully")
                else:
                    print("file already exists")

            elif choice == 2:
                with open(path, "a") as fs:
                    data = input("what do you want to append:- ")
                    fs.write("  \n" +data)
                print("successfully append")

            elif choice == 3:
                with open (path, "w") as fs:
                    data = input("what do you want to overwritr:- ")
                    fs.write("  \n" +data)
                print("successfully overwrite")
     except Exception as err:
        print(f"an error occured as {err}")


def deletefile():
    try:
        name = input("Please tell your file name:- ")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("file deleted successfully")
        else:
            print("Error no such file exists ")
     except Exception as err:
        print(f"an error occured as {err}")

                    
                    

print("press 1 for creating a file")
print("press 2 for reading a file")
print("press 3 for updating a file")
print("press 4 for deleting a file")

a= int(input("\ntell me your response:-  "))

if a ==1:
    createfile()
if a ==2:
    readfile()
if a ==3:
    updatefile()
if a ==4:
    deletefile()

