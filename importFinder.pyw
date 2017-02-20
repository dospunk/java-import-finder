from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup

class ImportFind:
	def __init__(self, master):
		master.title("Java Import Finder")
		master.grid_columnconfigure(1, weight=1)
		
		#self.title = ttk.Label(master, text="Import Statement Finder for Java")
		self.class_label = ttk.Label(master, text="Class to find: ")
		self.dropdown_label = ttk.Label(master, text="API to search: ")
		self.input = ttk.Entry(master)
		self.button = ttk.Button(master, text="Find", command=self.find_class)
		
		self.res_var = StringVar(master)
		self.res_var.set("")
		self.result = ttk.Entry(master, textvariable=self.res_var, state="readonly", width=40)
		
		self.var = StringVar(master)
		self.var.set("JavaFX 8")
		self.options = OptionMenu(master, self.var, "Java 8", "JavaFX 8")
		
		#self.title.grid(row=0,column=0,columnspan=5)
		self.class_label.grid(row=1, column=0)
		self.input.grid(row=1, column=1, columnspan=2)
		self.dropdown_label.grid(row=2, column=0)
		self.options.grid(row=2, column=1)
		self.button.grid(row=3, column=1)
		self.result.grid(row=4, column=0, columnspan=5, padx=5, pady=5)
		
	def find_class(self):
		search_term = self.input.get()
		api = self.var.get()
		#print(search_term)
		#print(api)
		page = None
		success = False
		url = ""
		if api == "JavaFX 8":
			url = "https://docs.oracle.com/javase/8/javafx/api/allclasses-noframe.html"
		if api == "Java 8":
			url = "https://docs.oracle.com/javase/8/docs/api/allclasses-frame.html"
		page = BeautifulSoup(requests.get(url).content, "lxml")
		for link in page.find_all("a"):
			if link.text == search_term:
				self.res_var.set("import " + link["href"].replace("/", ".")[:-5] + ";")
				success = True
		if not success:
			self.res_var.set("Class not found.")

def main():
	root = Tk()
	app = ImportFind(root)
	root.mainloop()

if __name__ == "__main__": main()