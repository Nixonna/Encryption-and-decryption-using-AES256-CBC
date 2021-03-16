import PySimpleGUI as sg
import sys
import Encryptext
import EncryptFile
import EncryptFolder

class Start:
    def __init__(self)->None:

        #Tooltip text for the buttons present in the main window.
        self.__tooltip1="Encrypt a text you type on the textbox and save it in an encrypted file.\nDecrypt that same file to a text file."
        self.__tooltip2="Encrypt a file and save it in your prefered directory. \nDecrypt the same files and decide whether to keep the original files or not."
        self.__tooltip3="Select a folder and encrypt the files in that folder. (exclusive of sub-directory) \nDecrypt these files and decide whether to keep the original files or not."
        
        #Layout of the main window.
        self.__layout=[
                
                [sg.Text("ENCRYPT AND DECRYPT:",pad=((0,0),(40,20)),text_color="black")],
                [sg.Button("Text*",size=(10,1),pad=((0,0),(20,20)),tooltip=self.__tooltip1)],
                [sg.Button("Files*",size=(10,1),pad=((0,0),(20,20)),tooltip=self.__tooltip2)],
                [sg.Button("Folders*",size=(10,1),pad=((0,0),(20,20)),tooltip=self.__tooltip3)],
                [sg.Button("Exit",size=(10,1),pad=((0,0),(20,20)),button_color="white on red")],
                [sg.Text("* hover over the button to know more.",pad=((250,0),(100,0)),text_color="black")]
                    ]
        
        #Creating instance for main window.
        self.__window=sg.Window("MAIN",self.__layout,size=(500,500),element_justification="c")

        #Infinite loop to run the main window.
        while True:

            #capture the events from the main window.
            self.__event,_=self.__window.read()

            #If the user tries to click the exit or the window close button then the program stops the execution.
            if self.__event in (None,"Exit",sg.WIN_CLOSED):
                sys.exit()
            
            #Action taken for various buttons in main window.
            if self.__event=="Text*":
                self.__window.hide()
                Encryptext.EnText()
            
            if self.__event=="Files*":
                self.__window.hide()
                EncryptFile.EnFile()
            
            if self.__event=="Folders*":
                self.__window.hide()
                EncryptFolder.EnFolder()

#Main driver of this file.
if __name__=="__main__":
    Start()
