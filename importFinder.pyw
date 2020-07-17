#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
import webbrowser

no_error = True
missing_packages = []

class err:
	def __init__(self, e, master):
		master.title("Error")
		missing_packages_str = " and ".join(missing_packages)
		err_message_str = missing_packages_str + " not installed, please install the missing package(s)"
		err_message = ttk.Label(master, text=err_message_str, foreground="#f00").pack()

try:
	import requests
	from requests.exceptions import ConnectionError
except ImportError:
	no_error = False
	missing_packages.append("Requests")
try:
	from bs4 import BeautifulSoup
except ImportError:
	no_error = False
	missing_packages.append("BeautifulSoup 4")


class ImportFind:
	def __init__(self, master):
		master.title("Java Import Finder")
		master.grid_columnconfigure(1, weight=1)
		master.bind('<Return>', self.find_class)
		
		#Initialize labels, textfield and button
		self.class_label = ttk.Label(master, text="Class to find: ")
		self.dropdown_label = ttk.Label(master, text="API to search: ")
		self.input = ttk.Entry(master)
		self.button = ttk.Button(master, text="Find")
		self.button.bind('<Button-1>', self.find_class)
		
		#Initialize & set up import statement field
		self.res_var = StringVar(master)
		self.res_var.set("")
		self.result = ttk.Entry(master, textvariable=self.res_var, state="readonly", width=40)
		
		#Set up options menu
		self.var = StringVar(master)
		self.var.set("JavaFX 8")
		self.options = OptionMenu(master, self.var, "Java 8", "Java 7", "JavaFX 8", "JUnit", "LWJGL")
		
		#set up link
		self.web = ttk.Label(text="", foreground="blue", cursor="hand2")
		self.web.bind("<Button-1>", self.open_link)
		
		self.class_label.grid(row=1, column=0)
		self.input.grid(row=1, column=1, columnspan=2)
		self.dropdown_label.grid(row=2, column=0)
		self.options.grid(row=2, column=1)
		self.button.grid(row=3, column=1)
		self.result.grid(row=4, column=0, columnspan=5, padx=5, pady=5)
		self.web.grid(row=5, column=0, columnspan=5, padx=5, pady=5)
		
	def open_link(self, event):
		webbrowser.open_new(self.web["text"])
		
	def find_class(self, event):
		search_term = self.input.get()
		api = self.var.get()
		page = None
		success = False
		url = ""
		link_part = ""
		if api == "JavaFX 8":
			url = "https://docs.oracle.com/javase/8/javafx/api/allclasses-noframe.html"
			link_part = "https://docs.oracle.com/javase/8/javafx/api/"
		if api == "Java 8":
			url = "https://docs.oracle.com/javase/8/docs/api/allclasses-frame.html"
			link_part = "https://docs.oracle.com/javase/8/docs/api/"
		if api == "Java 7":
			url = "https://docs.oracle.com/javase/7/docs/api/allclasses-noframe.html"
			link_part = "https://docs.oracle.com/javase/7/docs/api/"
		if api == "LWJGL":
			url = "https://javadoc.lwjgl.org/allclasses-frame.html"
			link_part = "https://javadoc.lwjgl.org/"
		if api == "JUnit":
			url = "http://junit.org/junit4/javadoc/latest/allclasses-frame.html"
			link_part = "http://junit.org/junit4/javadoc/latest/"
		try:
			page = BeautifulSoup(requests.get(url).content, "lxml")
			for link in page.find_all("a"):
				if link.text.lower() == search_term.lower():
					self.res_var.set("import " + link["href"].replace("/", ".")[:-5] + ";")
					self.web["text"] = link_part + link["href"]
					success = True
			if not success:
				self.res_var.set("Class not found.")
				self.web["text"] = ""
		except ConnectionError:
			self.res_var.set("Could not connect to the internet.")

def main():
	root = Tk()
	if no_error:
		app = ImportFind(root)
	else: 
		app = err(missing_packages, root)
	root.mainloop()

if __name__ == "__main__": main()
