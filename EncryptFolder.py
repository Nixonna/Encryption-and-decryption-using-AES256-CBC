#Select a folder and encrypt the files in that folder. (exclusive of sub-directory).
#Decrypt these files and decide whether to keep the original files or not.
#For decryption, directly click the decrypt button.

import PySimpleGUI as sg
import sys,os
import start
import pyAesCrypt as ac
import webbrowser as wb

class EnFolder:
    def __init__(self) -> None:

        #Define the buffer size for encyption and decryption. In this case it is 64k.
        global bufferSize
        bufferSize=64*1024

        #layout of the folder encryption and decryption window.
        self.__layout=[
            [sg.Text("Choose a folder to encrypt all the files in it.")],
            [sg.Input(readonly=True,key="fdir")],
            [sg.FolderBrowse(key="Infolder",enable_events=True)],
            [sg.Text("Enter password of encryption:",pad=((0,0),(20,0)))],
            [sg.Input(size=(20,1),password_char="*",key="pass",pad=((0,0),(10,20)))],
            [sg.Checkbox("Show password",key="P",enable_events=True)],
            [sg.Radio("Keep original files","D1",default=True,key="R"),sg.Radio("Delete original files","D1",key="R2")],
            [sg.Button("Encrypt",size=(10,1),pad=((0,20),(20,20))),sg.Button("Decrypt",size=(10,1),pad=((20,0),(20,20)))],
            [sg.Button("Back",size=(10,1),pad=((0,20),(20,20))),sg.Button("Exit",size=(10,1),pad=((20,0),(20,20)),button_color="white on red")]
        ]

        #creating an instance for this window.
        self.__window=sg.Window("FOLDER ENCRYPTION & DECRYPTION",self.__layout,size=(600,500),element_justification="c")

        #Infinite loop to run this window.
        while True:
            
            #Capture the events and widget values from the window.
            self.__event,self.__value=self.__window.read()
            
            #If the user tries to click the exit or the window close button then the program stops the execution.
            if self.__event in (None,"Exit",sg.WIN_CLOSED):
                sys.exit()
            
            # Back button takes the user to the main window.
            if self.__event=="Back":
                self.__window.hide()
                start.Start()
            
            #Show the password on the input field if the user chooses to or else hide the password.
            if self.__event=="P":
                if self.__value["P"]:
                    self.__window["pass"].update(password_char='')
                else:
                    self.__window["pass"].update(password_char='*')
            
            #Definiton of folder browser event to update the selected directory on the input widget.
            if self.__event=="Infolder":
                self.__window["fdir"].update(self.__value["Infolder"])
            
            #If the user clicks on Encrypt button then run the Encryption function.
            if self.__event=="Encrypt":
                self.Encryption()
            
            #If the user clicks on Decrypt button then run the Dcryption function.
            if self.__event=="Decrypt":
                self.Dcryption()
    
    #Definition of the Encryption function.
    def Encryption(self):
        #Check the validity of the password and the path of the folder selected.
        #If any of them is invalid then popup an error and exit the function.
        if self.__value["pass"]=="":
            sg.popup("Enter the password for encryption.",title="ERROR",text_color="red")
            return
        if self.__value["Infolder"]=="":
            sg.popup("Choose a folder to encrypt!!",title="ERROR",text_color="red")
            return
        
        #Get the path of the folder selected.
        self.__InDir=self.__value["Infolder"]

        #Get a list of all the files and folders in that directory.
        #This encryption only works for the files in that directory and doesn't encrypt sub-directories.
        self.__Infiles=os.listdir(self.__InDir)
        
        #Iterate through the list of files and folders and encrypt only the files in the directory.
        for files in self.__Infiles:
            #Checking if the selected entity is a folder or file.
            path=os.path.join(self.__InDir,files)

            #If it is a file then encrypt or else skip that entity.
            if not os.path.isdir(path):

                #calling the encryption object and pass the respected parameters.
                ac.encryptFile(path,path+".aes",self.__value["pass"],bufferSize)
                
                #If the user chooses to delete the original final then remove that file from the directory.
                if self.__value["R2"]:
                    os.remove(path)
        
        #After encryption, reset the text fields of the window.
        self.__window["fdir"].update("")
        self.__window["pass"].update("")

        #Once the files are encrypted then open that directory in new window.
        wb.open_new(self.__InDir)
    
    #Defintion of the Dcryption function.
    def Dcryption(self):

        #Get the folder to decrypt the files in it.
        self.__folder=sg.popup_get_folder("Choose the folder to decrypt:")
        
        #Check the validity of the folder selected.
        #If the path is invalid then display an error popup and exit the function.
        if self.__folder in (None,""):
            return
        if not os.path.exists(self.__folder):
            sg.popup("Incorrect location","Select correct location.",title="ERROR",text_color="red")
            return
        
        #Get the user to enter the password for the decryption of the files.
        # (Warning) decrypt the folder only if the password for all the files are the same or else the program will throw error. 
        while True:
            self.__pass=sg.PopupGetText("Enter the password!")
            if self.__pass in (None,""):
                return
            try:
                #Once we get the password, we list the files and folders in that directory.
                self.__files=os.listdir(self.__folder)
                
                #Iterate through the list of files and folders and encrypt only the files in the directory.
                for files in self.__files:

                    #Checking if the selected entity is a folder or file.
                    path=os.path.join(self.__folder,files)

                    #If it is a file then encrypt or else skip that entity.
                    if not os.path.isdir(path):

                        #Separate the file path and extension of the file.
                        dir,ext=os.path.splitext(path)

                        #Check if the file's extension is .aes. If not then skip that file.
                        if ext==".aes":

                            #Call the decryptFile object and pass the required parameters.
                            ac.decryptFile(path,dir,self.__pass,bufferSize)
                        
                        #If the user chooses to delete the original final then remove that file from the directory.
                        if self.__value["R2"]:
                            os.remove(path)
                
                #Once the files are encrypted then open that directory in new window.
                wb.open_new(self.__folder)
                return
            
            #This exception is thrown by the ac.decryptFile object if the password is incorrect or the file is corrupted.
            except ValueError:
                sg.popup("Password incorrect or the files have different password",title="ERROR",text_color="red")

#Main driver code
if __name__=="__main__":
    EnFolder()