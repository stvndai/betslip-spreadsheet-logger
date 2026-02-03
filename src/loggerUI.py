import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageGrab
import os
import logger

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("App")
        self.geometry("400x400")
        self.img = None

        
        self.filePath = ctk.StringVar(value="No file selected")
        
        # file
        self.fileLabel = ctk.CTkLabel(self, text="File")
        self.fileLabel.grid(row=0, column=0, padx=20, pady=5)
        
        self.fileValue = ctk.CTkLabel(self, textvariable=self.filePath)
        self.fileValue.grid(row=0, column=1, padx=20, pady=5)
        
        # game label
        self.gameValue = ctk.StringVar(value="no game detected")

        self.gameLabel = ctk.CTkLabel(self, text="file ")
        self.gameLabel.grid(row=1, column=0, padx=20, pady=5)

        self.gameEntry = ctk.CTkEntry(self, textvariable=self.gameValue)
        self.gameEntry.grid(row=1, column=1, padx=20, pady=5)

        # odds label
        self.oddsValue = ctk.StringVar(value="no odds detected")
        
        self.oddsLabel = ctk.CTkLabel(self, text="Odds")
        self.oddsLabel.grid(row=2, column=0, padx=20, pady=5)

        self.oddsEntry = ctk.CTkEntry(self, textvariable=self.oddsValue)
        self.oddsEntry.grid(row=2, column=1, padx=20, pady=5)
        
        # wager label   
        self.wagerValue = ctk.StringVar(value="no wager detected")


        self.wagerLabel = ctk.CTkLabel(self, text="Wager")
        self.wagerLabel.grid(row=3, column=0, padx=20, pady=5)

        self.wagerEntry = ctk.CTkEntry(self, textvariable=self.wagerValue)
        self.wagerEntry.grid(row=3, column=1, padx=20, pady=5)
        
        # payout label
        self.payoutValue = ctk.StringVar(value="no payout detected")

        self.payoutLabel = ctk.CTkLabel(self, text="Payout")
        self.payoutLabel.grid(row=4, column=0, padx=20, pady=5)
        
        self.payoutEntry = ctk.CTkEntry(self, textvariable=self.payoutValue)
        self.payoutEntry.grid(row=4, column=1, padx=20, pady=5)
        # select file button
        self.selectFileButton = ctk.CTkButton(
            self,
            text="select file to write",
            command=self.openFile
        )
        self.selectFileButton.grid(row=5, column=1, columnspan=2, padx=20, pady=5)
        
        # write button
        self.exportButton = ctk.CTkButton(self, text="write to file")
        self.exportButton.grid(row=6, column=1, columnspan=2)

        # image frame (PASTE TARGET)
        self.imgFrame = ctk.CTkFrame(self, width=200, height=200)
        self.imgFrame.grid(row=7, column=0, columnspan=2, pady=20)
        self.imgFrame.grid_propagate(False)

        self.pasteLabel = ctk.CTkLabel(
            self.imgFrame,
            text="Paste image here\n(Ctrl+V)"
        )
        self.pasteLabel.pack(expand=True)

        # bind paste
        self.bind("<Control-v>", self.onPaste)
        

    def onPaste(self, event=None):    
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            self.img = img
            results = logger.runDetection(img)
            self.displayImage(img)
        
            for item in results:
                print(item)
            
    def displayImage(self, img):
        img.thumbnail((180, 180))
        self.tk_img = ctk.CTkImage(light_image=img, size=(img.width, img.height))

        self.pasteLabel.configure(image=self.tk_img, text="")

        
    def buttonCallback(self):
        print("button pressed")
        
    def openFile(self):
        filePath = filedialog.askopenfilename(
            title="select spreadsheet",
            filetypes=[
                ("Spreadsheet files", "*.xlsx *.xls *.csv *.ods"),
                ("All files", "*.*")
            ]
        )
        if filePath:
            self.filePath.set(filePath)