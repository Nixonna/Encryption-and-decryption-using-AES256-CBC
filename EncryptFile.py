#Encrypt a file and save it in your prefered directory.
#Decrypt the same files and decide whether to keep the original files or not.

import PySimpleGUI as sg
import sys,os
import pyAesCrypt as ac
import start
import webbrowser as wb

class EnFile:

    def __init__(self) ->None:
        
        #Define the buffer size for encyption and decryption. In this case it is 64k.
        global bufferSize
        bufferSize=64*1024

        #layout of the file encryption and decryption window.
        self.__layout=[

            [sg.Text("Choose a file to encrypt:")],
            [sg.Input(readonly=True,key="fdir")],
            [sg.FileBrowse(key="file",enable_events=True)],
            [sg.Text("Choose the destination of encrypted file:")],
            [sg.Radio("Same directory","D1",default=True,key="R",enable_events=True),sg.Radio("Choose directory","D1",key="R2",enable_events=True)],
            [sg.Text("Choose the destination",visible=False,key="des")],
            [sg.Input(readonly=True,key="Ddir",visible=False)],
            [sg.FolderBrowse(key="folder",disabled=True,enable_events=True)],
            [sg.Text("Enter password of encryption:",pad=((0,0),(20,0)))],
            [sg.Input(size=(20,1),password_char="*",key="pass",pad=((0,0),(10,20)))],
            [sg.Checkbox("Show password",key="P",enable_events=True)],
            [sg.Radio("Keep original file","D2",default=True,key="K"),sg.Radio("Delete original file","D2",key="K2")],
            [sg.Button("Encrypt",size=(10,1),pad=((0,20),(20,20))),sg.Button("Decrypt",size=(10,1),pad=((20,0),(20,20)))],
            [sg.Button("Back",size=(10,1),pad=((0,20),(20,20))),sg.Button("Exit",size=(10,1),pad=((20,0),(20,20)),button_color="white on red")]
        ]

        #creating an instance for this window.
        self.__window=sg.Window("FILE ENCRYPTION & DECRYPTION",self.__layout,size=(600,650),element_justification="c")

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
            
            #Definiton of file browser event to update the selected file on the input widget.
            if self.__event=="file":
                self.__window["fdir"].update(self.__value["file"])
            
            #Definiton of folder browser event to update the selected directory on the input widget.
            if self.__event=="folder":
                self.__window["Ddir"].update(self.__value["folder"])
            
            #If the user clicks on Encrypt button then run the Encryption function.
            if self.__event=="Encrypt":
                self.Encryption()
            
            #If the user clicks on Decrypt button then run the Dcryption function.
            if self.__event=="Decrypt":
                self.Dcryption()
            
            #If the user wants to save the file to new directory the enable the widgets to get the new directory.
            if self.__event=="R2":
                if self.__value["R2"]:
                    self.__window["des"].update(visible=True)
                    self.__window["Ddir"].update(visible=True)
                    self.__window["folder"].update(disabled=False)
            
            #If the user chooses to keep the files in the same directory then disable the the widgets to get the new directory. 
            if self.__event=="R":
                if self.__value["R"]:
                    self.__window["des"].update(visible=False)
                    self.__window["Ddir"].update(visible=False)
                    self.__window["folder"].update(disabled=True)

    #Defintion of Encryption function.
    def Encryption(self):
        
        #Check the validity of password and the path of the file choosen.
        #If any one is invalid then throw a popup and exit the function.
        if self.__value["pass"]=="":
            sg.popup("Enter the password for encryption.",title="ERROR",text_color="red")
            return
        if self.__value["file"]=="":
            sg.popup("Choose a file to encrypt!!",title="ERROR",text_color="red")
            return
        
        #Get the path of the file choosen.
        self.__InDir=self.__value["file"]

        #If the user chooses to save the encrypted file in the same directory, get the seperate the path of the directory and file name.
        if self.__value["R"]:
            self.__ODir=os.path.dirname(self.__InDir)
            self.__OFName=os.path.basename(self.__InDir)
        
        #If the user chooses to save the encrypted file in different directory, get the path of the directory and file name.
        #The encrypted file naame will be same as the input file name. Only the extention will differ.
        else:
            self.__ODir=self.__value["folder"]
            self.__OFName=os.path.basename(self.__InDir)
        
        #Encrypt the file and save it to the prefered destination.
        #We provide the password and buffer size to the encryptFile object.
        ac.encryptFile(self.__InDir,self.__ODir+"\\"+self.__OFName+".aes",self.__value["pass"],bufferSize)

        #If the user chooses to delete the original final then remove that file from the directory.
        if self.__value["K2"]:
            os.remove(self.__ODir+"\\"+self.__OFName)

        #After encryption, reset the text fields of the window.
        self.__window["fdir"].update("")
        self.__window["Ddir"].update("")
        self.__window["pass"].update("")

        #Open the directory of the encrypted file in new window.
        wb.open_new(self.__ODir)
    
    #Defintion of Dcryption function.
    def Dcryption(self):

        #A popup window to choose a .aes file to decrypt.
        self.__file=sg.popup_get_file("Choose the file to decrypt:",file_types=(("AES FILES","*.aes"),))
        
        #If the user closes the popup or doesn't choose anything then exit the Dcryption function.
        if self.__file== None or self.__file=="":
            return
        
        #Check the validity of the file directory. 
        if not os.path.exists(self.__file):
            sg.popup("Incorrect file location","Select correct file location.",title="ERROR",text_color="red")
            return
        
        #Split the file path and the file extention.
        self.__dest,_=os.path.splitext(self.__file)
        
        #To decrypt, we require the correct password from the user.
        while True:
            self.__pass=sg.PopupGetText("Enter the password!")
            if self.__pass in (None,""):
                return
            try:
                #Once we get the password from the user, we decrypt the file. 
                ac.decryptFile(self.__file,self.__dest,self.__pass,bufferSize)

                #If the user chooses to delete the original final then remove that file from the directory.
                if self.__value["K2"]:
                    os.remove(self.__file)

                #After decryption open a new window to the file location.
                wb.open_new(os.path.dirname(self.__dest))
                return
            
            #This exception is thrown by the ac.decryptFile object if the password is incorrect or the file is corrupted.
            except ValueError:
                sg.popup("Password incorrect!!",title="ERROR",text_color="red")


#Main driver of this file.
if __name__=="__main__":
    EnFile()