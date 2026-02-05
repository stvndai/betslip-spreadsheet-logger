import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("App")
        self.geometry("640x420")
        
        # instance variables
        self.filePath = ctk.StringVar(value="No file selected")
        
        # file
        
        self.fileLabel = ctk.CTkLabel(self, text="File")
        self.fileLabel.grid(row=0, column=0, padx=20, pady=5)
        
        self.fileValue = ctk.CTkLabel(self, textvariable=self.filePath)
        self.fileValue.grid(row=0, column=1, padx=20, pady=5)
        
        # gamee label
        self.gameLabel = ctk.CTkLabel(self, text="file ")
        self.gameLabel.grid(row=1, column=0,padx=20, pady=5)

        # odds label
        self.oddsLabel = ctk.CTkLabel(self, text="Odds")
        self.oddsLabel.grid(row = 2, column=0, padx=20, pady=5)        
        # wager label
        
        self.wagerLabel = ctk.CTkLabel(self, text="Wager")
        self.wagerLabel.grid(row = 3, column=0, padx=20, pady=5) 
        
        # payout label
        self.payoutLabel = ctk.CTkLabel(self, text="Payout")
        self.payoutLabel.grid(row = 4, column=0, padx=20, pady=5) 
        
        # select file button
        
        self.selectFileButton = ctk.CTkButton(self,
                                              text ="select file to write",
                                              command=self.openFile)
        self.selectFileButton.grid(row=5, column=1, columnspan=2, padx=20, pady=5)
        
        # write button
        self.exportButton = ctk.CTkButton(self, text="write to file")
        self.exportButton.grid(row = 6, column=1, columnspan=2)
        
    def buttonCallback(self):
        print("button pressed")
        
    def openFile(self):
        filePath = filedialog.askopenfilename(
            title = "select spreadsheet",
            filetypes=[
                ("Spreadsheet files", "*.xlsx *.xls *.csv *.ods"),
                ("All files", "*.*")
            ]
        )
        if filePath:
            self.filePath.set(filePath)
    
if __name__ == "__main__":
    app = App()

    app.mainloop()
    
    