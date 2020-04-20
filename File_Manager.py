# Author: Andrea Mele
# E-mail: andme44@gmial.com
# Websites: 
# http://www.github.com/AndreaMele
# http://www.artstation.com/AndreaMee
# Project: File Manager

import shutil
import sys
import os
import time
import subprocess
from datetime import datetime
import sqlite3
from contextlib import closing
from sqlite3 import Error
# Global
database = r"FileList.sqlite"
conn = sqlite3.connect(database)
c = conn.cursor()

# Class Filemanager
class Filemanager:
    """ My Filemanager Class! """

    def lisDir(self):
        """Listing Direcotires and allowing other options"""
        q1 = int(input("""
        1) from current directory
        2) Specify a directory
        """))
        listNum = 1
        try:
            if q1 == 2:
                redirectPath = input("Enter a fullpath directory ex: ")
                os.chdir(redirectPath)
                print(os.getcwd())
                fl = os.scandir(redirectPath)
            elif q1 == 1:
                fl = os.scandir(cDir)
        except FileNotFoundError:
            print("File/Location not found")
            fm.lisDir()
        finally:
            print("""  _____FOLDERS_____   """)
            folders = [dirs for dirs in os.listdir(".") if not os.path.isfile(dirs)]
            for dirs in folders:
                print(str(listNum) + ") " + str(dirs))
                listNum += 1
            print("""  _____FILES_____   """)
            files = [f for f in os.listdir(".") if os.path.isfile(f)]
            for f in files:
                print(str(listNum) + ") " + str(f))
                listNum += 1
            fullDirList = ["BUFFER"] + folders + files  # offsetting my list so 1 = 1
            while True:
                try:
                    q2 = int(input("""
                    list:
                    (1) Sort View
                    (2) Copy/Move
                    (3) Delete
                    (4) Export to Database
                    (9) Main Menu
                    (0) Quit
                    """))
                    if q2 == 1:  # Sort View
                        sort = int(input("""
                        Sort View:
                        (1) A-Z, 0-9
                        (2) Z-A, 9-0
                        (3) Default View
                        """))
                        listNum = 1
                        if sort == 1: # Sort A-Z
                            folders.sort(reverse=False)
                            files.sort(reverse=False)
                        if sort == 2: # Sort Z-A
                            folders.sort(key=str.lower, reverse=True)
                            files.sort(key=str.lower, reverse=True)
                        if sort == 3: # Sort Z-A
                            folders.sort()
                            files.sort()
                        print("""  _____FOLDERS_____   """)
                        for dirs in folders:
                            print(str(listNum) + ") " + str(dirs))
                            listNum += 1
                        print("""  _____FILES_____   """)
                        for f in files:
                            print(str(listNum) + ") " + str(f))
                            listNum += 1
                        fullDirList = ["BUFFER"] + folders + files
                        break
                    elif q2 == 2:  # Copy/Move
                        sel = int(input("Enter the number of the file to copy/rename :"))
                        print("Selected : ", fullDirList[sel])
                        fm.copy(option=2, src=(fullDirList[sel]))
                        break
                    elif q2 == 3:  # Delete
                        sel = int(input("Enter the number of the file to delete :"))
                        print("Selected : ", fullDirList[sel])
                        fm.delFile(option=2, listSelect=(fullDirList[sel]))
                        break
                    elif q2 == 4:  # Export to Database
                        fm.makeTable()
                        break
                    elif q2 == 9:  # Main Menu
                        main()
                        break
                    elif q2 == 0:  # Quit
                        print("Exiting")
                        sys.exit()
                        break
                except ValueError:
                    print(":> Make a valid Selection")


    def delFile(self, option=1, listSelect=""):
        """Delete files"""
        if option == 1:  # Default, folder to delete
            path = input("Enter the path of file for deletion: ")
            try:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        print("Directory Found : ", path)
                        shutil.rmtree(path, ignore_errors=False,
                                      onerror="error;:")
                        print(path, "Folder has been deleted")
                    if os.path.isfile(path):
                        print("File Found : ", path)
                        os.remove(path)
                        print(path, "File has been deleted")
            except FileNotFoundError:
                print("File Does not exist")
        if option == 2 and listSelect != 0:  # File to delte
            try:
                if os.path.exists(listSelect):
                    if os.path.isdir(listSelect):
                        print("Directory Found : ", listSelect)
                        shutil.rmtree(
                            listSelect, ignore_errors=False, onerror="error;:")
                        print(listSelect, "Folder has been deleted")
                    if os.path.isfile(listSelect):
                        print("File Found : ", listSelect)
                        os.remove(listSelect)
                        print(listSelect, "File has been deleted")
            except FileNotFoundError:
                print("File Does not exist")


    def copy(self, option=1, src="", dst=""):
        """ Copy/Moving file """
        try:
            if option == 0:
                pass
            if option == 1:  # Default Option
                src = input("Enter the path of the file/folder to copy: ").replace(os.sep, '/')
                if os.path.isdir(src):
                    dst = input("Enter the path to copy to: ").replace(os.sep, '/').rstrip('\\/')
                    from distutils.dir_util import copy_tree
                    copy_tree(src, dst)
                if os.path.isfile(src):
                    dst = input("Enter the path to copy/rename to: ").replace(os.sep, '/') # converting the operating seperators to forwardslashes! (for windows)
                    from pathlib import Path
                    fn = Path(src).name # grabbing just the filename form the srouce fullpath file.
                    fixfn = dst.rstrip('\\/') + "/" + fn # Stringing together a new fullpath for destination
                    shutil.copy(src, fixfn)
                    print("Newly Copied/Renamed too : ",fixfn)
            if option == 2:  # When called from the list menu
                dst = input("Enter the path to copy/rename to: ").replace(os.sep, '/') # converting the operating seperators to forwardslashes! (for windows)
                from pathlib import Path 
                fn = Path(src).name # grabbing just the filename form the srouce fullpath file.
                fixfn = dst.rstrip('\\/') + "/" + fn # Stringing together a new fullpath for destination
                shutil.copy(src, fixfn)
                print("Newly Copied/Renamed too : ",fixfn)
        except:
            print("Improper formatting, ensure that directory n.")


    def newTxt(self):
        """ Creating a text file """
        fname = input('Enter a filename : ')
        if os.path.isfile(fname):
            print("overwritting the existing file")
        else:
            print("Creating the new file")
        with open(fname, "w") as outfile: 
            outfile.write(input("Enter text : "))
        readIt = int(input("""Read file just created?
            (1) Yes
            (2) No
        """))
        if readIt == 1:
            fm.readfile(option=2, path=fname)
        if readIt == 2:
            pass


    def readfile(self, option=1, path=""):
        """ Reading a file """
        if option==1:
            try:
                path = input("Enter the file path to read: ")
                print("")
                file = open(path, "r")
                print(file.read())
                input("\n Press Enter when done ...")
                file.close()
            except FileNotFoundError:
                print("File NotFound")
        if option==2:
            try:
                print("")
                file = open(path, "r")
                print(file.read())
                input("\n Press Enter when done ...")
                file.close()
            except FileNotFoundError:
                print("File NotFound")


    def editTxt(self):
        """ Edit/Append to a text file """
        fname = input('Enter a full path to txt file : ')
        text = input("Enter the text to add: ")
        try:
            with open(fname, "w") as outfile: 
                outfile.write("\n" + input("Enter text : "))
            readIt = int(input("""Read file just created?
                (1) Yes
                (2) No
            """))
            if readIt == 1:
                fm.readfile(option=2, path=fname)
            if readIt == 2:
                pass
        except FileNotFoundError :
            print("File Not Found")


    def mDir(self):
        """ Make new directories """
        newDir = input(r"""
        Enter the directory name with path to make
        ex: C:\Folder\Newdir1
        or
        ex: C:\Folder\Newdir1\Newdir2
        Where Newdir1 or Newdir2 is new directories:
        """)
        os.makedirs(newDir)
        print("Directory Created")


    def tellMeMore(self, fileNm=""):
        """ Get some information about a file """
        try:
            os.path.isfile(fileNm)
            fileSize = os.path.getsize(fileNm)
            filemodTime = datetime.fromtimestamp(os.stat(fileNm).st_mtime)
            print(f"""
            File Location : {fileNm}
            Size          : {fileSize} Bytes
            Modified      : {filemodTime}
            """)
        except FileNotFoundError:
            print("File Not Found!")
    
    def makeTable(self):
        tble_dict = {}
        table_name = "MyFileList"
        counter = 0
        q1 = int(input("""Exporting will overwrite your previous database, continue?
                        (1) Yes
                        (2) No
                        """))
        if q1 == 1:
                fdel = f'''DELETE FROM {table_name}'''
                c.execute(fdel)
                conn.commit()
                print("Table rows cleared.")
                try:
                    f1 = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            ID integer PRIMARY KEY,
                            Drive text NOT NULL,
                            Location text,
                            Filename text
                        );'''
                    c.execute(f1)
                    conn.commit()
                    print(f"....successfully added {table_name} to database")
                    fm.tableInsert(table_name)
                except Exception as e:
                    print("ERROR, enter correct a valid entry")
                    # Roll back any change if something goes wrong
                    conn.rollback()
        elif q1 == 2:
            pass

    def tableInsert(self, table_name=""):
        try:
            counter = 1
            fl = os.scandir(cDir)
            folders = [dirs for dirs in os.listdir(".") if not os.path.isfile(dirs)]
            files = [f for f in os.listdir(".") if os.path.isfile(f)]
            fullDirList = folders + files  # offsetting my list so 1 = 1
            for x in fullDirList:
                f2 = f'''INSERT OR REPLACE INTO {table_name} VALUES({counter}, '{cDir[:2]}', '{cDir[2:]}\', '{x}');'''
                # print(f2) #turn this on for table feedback
                c.execute(f2)
                counter+=1
                conn.commit()
            print(f"{counter} entries inserted")
            print(f"Database file saved to: {database}")
            print(cDir)
        except FileNotFoundError:
            print("File/Location not found")
 
# Display Menu
def displayMenu():
    print("""
    _.:: MENU ::._
    (1) List Files
    (2) New [Text File]
    (3) Read [Text File]
    (4) Edit [Text File]
    (5) Delete
    (6) Copy/Move
    (7) Make New Folder
    (8) File Info
    (9) Export to Database
    (0) QUIT
    """)

# Selet Menu
def selectMenu():
    try:
        selection = int(input("\n Please type a letter (EX: 3 ) "))
        if selection == 1:  # List Files
            fm.lisDir()
        elif selection == 2:  # New [Text File]
            fm.newTxt()
        elif selection == 3:  # Read [Text File]
            fm.readfile()
        elif selection == 4:  # Edit [Text File]
            fm.editTxt()
        elif selection == 5:  # Delete
            fm.delFile()
        elif selection == 6:  # Copy/Move
            fm.copy()
        elif selection == 7:  # Make a new directory
            fm.mDir()
        elif selection == 8:  # File info
            fileNm = input("Enter the path of the file: ").replace(os.sep, '/')
            fm.tellMeMore(fileNm)
        elif selection == 9:  # Export to Database
            fm.makeTable()
        elif selection == 0:  # QUIT
            print("Exiting")
            sys.exit()
    except ValueError:
        print("::::>> Make a valid Selection")
    except KeyboardInterrupt:
        print("Bye")
        sys.exit()

# Run first..
def main():
    while True:
        displayMenu()
        selectMenu()


if __name__ == "__main__":
    fm = Filemanager()
    cDir = os.getcwd()
    main()
