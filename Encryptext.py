#Encrypt a text you type on the textbox and save it in an encrypted file.
#Decrypt that same file to a text file.

import PySimpleGUI as sg
import sys,io,os
import pyAesCrypt as ac
import start
import webbrowser as wb

class EnText:
    
    def __init__(self) ->None:

        #Define the buffer size for encyption and decryption. In this case it is 64k.
        global bufferSize
        bufferSize=64*1024

        #layout of the text encryption and decryption window.
        self.__layout=[
                [sg.Text("Plain Text:")],
                [sg.Multiline(size=(40,10),key='Dec')],
                [sg.Text("Enter password of encryption:",pad=((0,0),(20,0)))],
                [sg.Input(size=(20,1),password_char="*",key="pass",pad=((0,0),(10,20)))],
                [sg.Checkbox("Show password",key="P",enable_events=True)],
                [sg.Button("Encrypt",size=(10,1),pad=((0,20),(20,20))),sg.Button("Decrypt",size=(10,1),pad=((20,0),(20,20)))],
                [sg.Button("Back",size=(10,1),pad=((0,20),(20,20))),sg.Button("Exit",size=(10,1),pad=((20,0),(20,20)),button_color="white on red")]
        ]

        #creating an instance for this window.
        self.__window=sg.Window("TEXT ENCRYPTION & DECRYPTION",self.__layout,size=(600,650),element_justification="c")

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
            
            #If the user clicks on Encrypt button then run the WriteToFile function.
            if self.__event=="Encrypt":
                self.WriteToFile()
            
            #If the user clicks on Decrypt button then run the Dcryption function.
            if self.__event=="Decrypt":
                self.Dcryption()

    #Definition of the WriteToFile function.
    def WriteToFile(self):
        
        #Check if the text field is empty or not. If empty, notify that the text field is empty and exit the function.
        if self.__value["Dec"]=="\n":
            sg.popup("Text field is empty.",title="ERROR",text_color="red")
            return
        
        #Check the validity of the password entered. If the value is empty then notify to enter the password and return.
        if self.__value["pass"]=="":
            sg.popup("Enter the password for encryption.",title="ERROR",text_color="red")
            return
        
        #Getting the text typed by the user, encode string to bytes and provide it to the BytesIO object.
        #BytesIO object is used to perform byte operations in the memory so as to perform in-memory encryption and decryption.
        self.__data=io.BytesIO(self.__value["Dec"].encode())

        #Run a while loop to get the save directory and file name from the user.
        while True:
            self.__dir=sg.popup_get_folder("Choose the directory to save the file:")

            #Checking validity of the directory.
            if os.path.isdir(self.__dir):
                self.__fileN=sg.popup_get_text("Enter file name")
                break
            else:
                sg.popup("Choose a valid directory:",title="ERROR",text_color="red")
                return
        
        #Open a file in the user defined directory in write binary mode since the encryption is a binary stream.
        #The encrypted file has an extension of .aes.
        with open(self.__dir+"\\"+self.__fileN+".txt.aes","wb") as f:
            #Encrypt the data into a file and provide the password and buffer size to the encryption object.
            ac.encryptStream(self.__data,f,self.__value["pass"],bufferSize)
        
        #After encryption, reset the text fields of the window.
        self.__window["Dec"].update("")
        self.__window["pass"].update("")

        #Once the encryption is done, open the folder in new window where the file is being saved.
        wb.open_new(self.__dir)
    

    #Definition of the Dcryption function.
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
                
                #After decryption open a new window to the file location.
                wb.open_new(os.path.dirname(self.__dest))
                return
            
            #This exception is thrown by the ac.decryptFile object if the password is incorrect or the file is corrupted.
            except ValueError:
                sg.popup("Password incorrect or the file is corrupted.",title="ERROR",text_color="red")

#Main driver of this file.
if __name__=="__main__":
    EnText()