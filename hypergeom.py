#std lib imports
import os
import math
#gui imports
from Tkinter import *
import tkFont, tkMessageBox
from PIL import Image, ImageTk
#custom module imports 
from experiment import Experiment 

class Window(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		if getattr(sys, 'frozen', False):
			current_dir = os.path.dirname(sys.executable)
		else:
			current_dir = os.path.dirname(os.path.realpath(__file__))
		imgs_dir = os.path.join(current_dir, 'imgs')
		backArrowImage = Image.open(os.path.join(imgs_dir, 'back.png'))#"imgs\\back.png")
		forwardArrowImage = Image.open(os.path.join(imgs_dir, 'forward.png'))#"imgs\\forward.png")
		self.backArrowPhoto = ImageTk.PhotoImage(backArrowImage)
		self.forwardArrowPhoto = ImageTk.PhotoImage(forwardArrowImage)
		self.initUI()

	def initUI(self):
		self.parent.title('Hypergeometric Distribution Simulator')

		labelfont = tkFont.nametofont('TkDefaultFont')
		labelfont.config(size=12)

		#frame for data entry (grid manager)
		self.fields = Frame(self)
		self.fields.pack(side=LEFT, fill=Y)

		#labels for data entry
		self.sampleLabel = Label(self.fields, text='Sample Size:')
		self.sampleLabel.grid(row=0, column=0, sticky=W, padx=5, pady=5)

		self.populationLabel = Label(self.fields, text='Population Size:')
		self.populationLabel.grid(row=1, column=0, sticky=W, padx=5, pady=5)

		self.numSuccessesLabel = Label(self.fields, text='Number of Successes:')
		self.numSuccessesLabel.grid(row=2, column=0, sticky=W, padx=5, pady=5)

		self.numTrialsLabel = Label(self.fields, text='Number of Trials:')
		self.numTrialsLabel.grid(row=3, column=0, sticky=W, padx=5, pady=5)

		#input boxes and submit button for data entry
		self.sampleEntry = Entry(self.fields)
		self.sampleEntry.grid(row=0, column=1, padx=5, pady=5)

		self.populationEntry = Entry(self.fields)
		self.populationEntry.grid(row=1, column=1, padx=5, pady=5)

		self.numSuccessesEntry = Entry(self.fields)
		self.numSuccessesEntry.grid(row=2, column=1, padx=5, pady=5)

		self.numTrialsEntry = Entry(self.fields)
		self.numTrialsEntry.grid(row=3, column=1, padx=5, pady=5)

		self.runTrialsButton = Button(self.fields, text='Run Experiment', command=self.runExperiment)
		self.runTrialsButton.grid(row=4, column=1, sticky=E, padx=5, pady=5)

		#canvas
		self.canvas = Canvas(self, background='white')
		self.canvas.pack(side=RIGHT, fill=BOTH, expand=1)

		#main window centering
		self.pack(fill=BOTH, expand=1)
		self.centerWindow()

	def centerWindow(self):
		width = 700
		height = 400
		x = (self.parent.winfo_screenwidth() - width) / 2
		y = (self.parent.winfo_screenheight() - height) / 2
		self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

	def runExperiment(self):
		try:
			e = Experiment(int(self.sampleEntry.get()), int(self.populationEntry.get()),
				int(self.numSuccessesEntry.get()))
			e.perform(int(self.numTrialsEntry.get()))
			self.drawResult(e.results, 0)
		except AssertionError as error:
			tkMessageBox.showerror('Data Entry Error', error.args[0])
		except ValueError as error:
			tkMessageBox.showerror('Data Entry Error', 'Please make sure each field is filled out'
			+ ' and only contains numbers') 

	def drawResult(self, results, index):
		#clear canvas 
		self.canvas.delete(ALL)
		try:
			self.forwardButton.destroy()
			self.backButton.destroy()
			self.titleLabel.destroy()
			self.successesLabel.destroy()
			self.failuresLabel.destroy()
		except AttributeError: 
			pass

		#place labels
		self.titleLabel = Label(self.canvas, text='Trial ' + str(index + 1))
		self.titleLabel.place(relx=0.5, rely=0.1, anchor=CENTER)

		self.successesLabel = Label(self.canvas, text=str(results[index][0]) + ' Successes')
		self.successesLabel.place(relx=0.275, rely=.75, anchor=CENTER)

		self.failuresLabel = Label(self.canvas, text=str(results[index][1]) + ' Failures')
		self.failuresLabel.place(relx=0.725, rely=.75, anchor=CENTER)

		#create dictionaries containing selected widths and heights based on percentage
		canvas_height = self.canvas.winfo_height()
		canvas_width = self.canvas.winfo_width()
		widths = {percentage : int(math.floor(percentage / 100.0 * canvas_width)) for percentage in 
			[10, 45, 55, 90]}
		heights = {percentage : int(math.floor(percentage / 100.0 * canvas_height)) for percentage in 
			[25, 70]}
		
		#use percentages to draw results
		num_marbles = sum(results[index])
		jar_width = math.floor(widths[45] - widths[10])
		jar_height = math.floor(heights[70] - heights[25])

		num_marbles_per_row = find_nearest_larger_perfect_square(num_marbles) 
		marble_diameter = 1.0 * jar_width / num_marbles_per_row		

		for i in range(results[index][0]):
			x_offset = marble_diameter * (i % num_marbles_per_row) 
			x0 = (widths[10] + x_offset)
			y0 = heights[70] - math.floor(i / num_marbles_per_row) * marble_diameter
			self.canvas.create_oval(x0, y0, x0 + marble_diameter, y0 - marble_diameter, outline='black',
				fill='green', width=2.0)
		for i in range(results[index][1]):
			x_offset = marble_diameter * (i % num_marbles_per_row)
			x0 = widths[55] + x_offset
			y0 = heights[70] - math.floor(i / num_marbles_per_row) * marble_diameter
			self.canvas.create_oval(x0, y0, x0 + marble_diameter, y0 - marble_diameter, outline='black',
				fill='red', width=2.0)

		self.canvas.create_rectangle(widths[10], heights[25], widths[45], heights[70],
			outline='black', fill=None, width=3.0)	
		self.canvas.create_rectangle(widths[55], heights[25], widths[90], heights[70],
			outline='black', fill=None, width=3.0)	

		#set up two buttons (left/right) to shuffle between results
		if int(self.numTrialsEntry.get()) > 1:
			if index == 0:
				self.forwardButton = Button(self.canvas, image=self.forwardArrowPhoto, command=self.callback(results, index + 1))
				self.forwardButton.place(relx=0.9, rely=0.9, anchor=CENTER)
			elif index == len(results) - 1:
				self.backButton = Button(self.canvas, image=self.backArrowPhoto, command=self.callback(results, index - 1))
				self.backButton.place(relx=0.1, rely=0.9, anchor=CENTER)
			else:
				self.forwardButton = Button(self.canvas, image=self.forwardArrowPhoto, command=self.callback(results, index + 1))
				self.backButton = Button(self.canvas, image=self.backArrowPhoto, command=self.callback(results, index - 1))
				self.forwardButton.place(relx=0.9, rely=0.9, anchor=CENTER)
				self.backButton.place(relx=0.1, rely=0.9, anchor=CENTER)

	def callback(self, results, index):
		def temp(): 
			self.drawResult(results, index)
		return temp

def find_nearest_larger_perfect_square(n):
	return int(math.ceil(math.sqrt(n)))

def main():
	root = Tk()
	app = Window(root)
	root.mainloop()

if __name__ == '__main__':
	main()