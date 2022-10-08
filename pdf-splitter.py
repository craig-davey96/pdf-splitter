import os.path , subprocess

from PyPDF2 import PdfReader , PdfWriter

import tkinter
import tkinter.messagebox
from tkinter.filedialog import askopenfilename , askdirectory

import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):

    WIDTH = 800
    HEIGHT = 310

    fileName = ''
    location = ''
    numberOfPages = 0

    pdf = ''

    def __init__(self):
        super().__init__()

        self.title("PDF Splitter")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}y")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


        ## Create Buttons

        self.fileSelectButton = customtkinter.CTkButton(master=self, text="SELECT PDF" , height=50 , width=260 , command=self.getPdf)
        self.fileSelectButton.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky='nswe')

        self.saveLocationButton = customtkinter.CTkButton(master=self, text="SELECT SAVE LOCATION" , height=50 , width=260 , command=self.getDirectory , state="disabled")
        self.saveLocationButton.grid(row=0, column=2, columnspan=2, pady=10, padx=20, sticky='nswe')

        self.splitButton = customtkinter.CTkButton(master=self, text="SPLIT PDF", height=50 , width=765 , command=self.splitPdf , state="disabled")
        self.splitButton.grid(row=4, column=0, columnspan=4, pady=10, padx=20, sticky='nswe')

        ## Details Frame

        self.detailsFrame = customtkinter.CTkFrame(master=self , width=560 , height=200)
        self.detailsFrame.grid(row=2,column=0, columnspan=4, pady=10, padx=20, sticky='nswe')

        ## Details

        self.selectedPdfLabel = customtkinter.CTkLabel(master=self.detailsFrame , text="SELECTED PDF:" , justify="left" , width=200)
        self.selectedPdfLabel.grid(row=0 , column=0 , pady=10 , padx=10 , sticky="w")
        self.selectedPdfLabel2 = customtkinter.CTkLabel(master=self.detailsFrame , text="", justify="right" , width=400)
        self.selectedPdfLabel2.grid(row=0 , column=1 , pady=10 , padx=20 , sticky="we")

        self.selectedLocationLabel = customtkinter.CTkLabel(master=self.detailsFrame , text="SELECTED LOCATION:", justify="left" , width=200)
        self.selectedLocationLabel.grid(row=1 , column=0 , pady=10 , padx=10 , sticky="w")
        self.selectedLocationLabel2 = customtkinter.CTkLabel(master=self.detailsFrame , text="", justify="right" , width=400)
        self.selectedLocationLabel2.grid(row=1 , column=1 , pady=10 , padx=20 , sticky="we")

        self.numberOfPagesLabel = customtkinter.CTkLabel(master=self.detailsFrame , text="NUMBER OF PAGES: ", justify="left" , width=200)
        self.numberOfPagesLabel.grid(row=2 , column=0 , pady=10 , padx=10 , sticky="w")
        self.numberOfPagesLabel2 = customtkinter.CTkLabel(master=self.detailsFrame , text="", justify="right")
        self.numberOfPagesLabel2.grid(row=2 , column=1 , pady=10 , padx=20 , sticky="we")

    def getPdf(self):
        App.fileName = askopenfilename(filetypes=[("Pdf file", '*.pdf')])

        if App.fileName:
            App.pdf = PdfReader(App.fileName)
            App.numberOfPages = App.pdf.numPages

            self.numberOfPagesLabel2.configure(text=f"{App.numberOfPages}")
            self.selectedPdfLabel2.configure(text=f"{os.path.basename(App.fileName)}")

            self.saveLocationButton.configure(state="normal")

    def getDirectory(self):
        App.location = askdirectory()
        self.selectedLocationLabel2.configure(text=f"{App.location}")
        self.splitButton.configure(state="normal")

    def splitPdf(self):
        self.splitButton.configure(text="Splitting ...")
        number = 0;
        for page in range(App.numberOfPages):
            number = number + 1
            output = PdfWriter()
            output.addPage(App.pdf.pages[page])
            outputFileName = os.path.join(App.location , f"{os.path.basename(App.fileName).replace('.pdf' , '')}-{page}.pdf")
            with open(outputFileName , "wb") as outputStream:
                output.write(outputStream)
        if number == App.numberOfPages:
            subprocess.run(['explorer' , os.path.realpath(App.location)])
            self.splitButton.configure(text="SPLIT PDF")
            tkinter.messagebox.showinfo('Success' , 'Your pdf has been successfully split')
            self.reset()

    def reset(self):
        App.numberOfPages = ''
        App.pdf = ''
        App.prefix = ''
        App.fileName = ''

        self.splitButton.configure(state="disabled")
        self.saveLocationButton.configure(state="disabled")

        self.numberOfPagesLabel2.configure(text="")
        self.selectedPdfLabel2.configure(text="")
        self.selectedLocationLabel2.configure(text="")

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.resizable(False , False)
    app.mainloop()
