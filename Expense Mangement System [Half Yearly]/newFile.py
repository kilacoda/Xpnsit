import tkinter as tk

class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		frames = (StartPage, PageOne, PageTwo)

		#all frames need to be initialized before the UI's are built
		self.frames = {}
		for F in frames:
			frame = F(self)
			frame.grid(row=0, column=0, sticky="nsew")
			self.frames[F] = frame
		for F in self.frames.values():
			F.build_UI()

		self.frames[StartPage].tkraise()

class StartPage(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.grid()

	def build_UI(self):
		#can't be part of init since it relys on other classes already started (.tkraise)
		l1 = tk.Label(self, text="Start Page")
		l1.pack()

		page_one = tk.Button(
			self,
			text="Go to first page",
			command = self.parent.frames[PageOne].tkraise)
		page_one.pack()

		page_two = tk.Button(
			self,
			text="go to second page",
			command = self.parent.frames[PageTwo].tkraise)
		page_two.pack()

class PageOne(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.grid()

	def build_UI(self):
		l1 = tk.Label(self, text="First Page")
		l1.pack()

		back_button = tk.Button(
			self,
			text="Go Back",
			command = self.parent.frames[StartPage].tkraise)
		back_button.pack()

		self.push_counter = tk.Button(
			self,
			text = 'You need to click me',
			command = self.push_me)
		self.push_counter.pack()
		self.push_count = 0

	def push_me(self):
		self.push_count += 1
		self.push_counter['text'] = "you pushed me %d times"%self.push_count

class PageTwo(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.grid()

	def build_UI(self):
		l1 = tk.Label(self, text="Second Page")
		l1.pack()

		back_button = tk.Button(
			self,
			text="Go Back",
			command = self.parent.frames[StartPage].tkraise)
		back_button.pack()

		self.push_counter = tk.Button(
			self,
			text = 'You need to click me',
			command = self.push_me)
		self.push_counter.pack()
		self.push_count = 0

	def push_me(self):
		self.push_count += 1
		self.push_counter['text'] = "you pushed me %d times"%self.push_count

app = App()

app.mainloop()
