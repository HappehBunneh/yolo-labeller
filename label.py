import os
import tkinter as tk
from PIL import Image, ImageTk

def createTextFile():
	pass

def createTextFileAll():
	data = app.picsData
	for k,v in data.items():
		fileName = k.replace('.jpg', '.txt')
		with open(fileName, 'w') as file:
			for car in v:
				img_width = 640
				img_height = 480
				toWrite = '0 {0} {1} {2} {3}\n'.format(car.x/img_width, car.y/img_height, 
car.width/img_width, car.height/img_height)
				file.write(toWrite)
	print('Done!')

class Car():
	def __init__(self, start, end, canvas):
		self.start = start
		self.end = end
		self.x = (start[0] + end[0]) / 2
		self.y = (start[1] + end[1]) / 2
		self.width = abs(start[0] - end[0])
		self.height = abs(start[1] - end[1])
		self.canvas = canvas

	def __hash__(self):
		return hash(self.canvas)

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.cursorLocation = []
		self.picPath = os.path.join(os.getcwd(), 'pic')
		self.pics = [os.path.join(self.picPath, file) for file in os.listdir(self.picPath) if '.jpg' in file]
		self.picsData = dict((i,[]) for i in self.pics)
		self.create_widgets()

	def create_widgets(self):
		self.canvas = tk.Canvas(self, width=640, height=480, cursor='crosshair')
		self.canvas.grid(row=0, column=0)
		self.canvas.bind('<ButtonPress-1>', self.onClick)
		self.canvas.bind('<B1-Motion>', self.onDrag)
		self.canvas.bind('<ButtonRelease-1>', self.onRelease)

		self.classFrame = tk.LabelFrame(self, text='Cars')
		self.classFrame.grid(row=0, column=1, sticky='wens')
		self.deleteFrame = tk.LabelFrame(self, text='Delete')
		self.deleteFrame.grid(row=0, column=2, sticky='wens')
		self.deleteButton = tk.Button(self, text='Delete', command=self.deleteData)
		self.deleteButton.grid(row=1, column=2)
		self.labelButton = tk.Button(self, text='Label(*)', command=createTextFileAll)
		self.labelButton.grid(row=1, column=1)

		self.pos = 0
		self.navFrame = tk.Canvas(self)
		self.navFrame.grid(row=1, column=0)
		self.back = tk.Button(self.navFrame, text='<', command=lambda: self.updatePicture(-1))
		self.forward = tk.Button(self.navFrame, text='>', command=lambda: self.updatePicture(1))
		self.posLabel = tk.Label(self.navFrame, text=str(self.pos))
		self.back.grid(row=0, column=0)
		self.posLabel.grid(row=0, column=1)
		self.forward.grid(row=0, column=2)
		self.updatePicture()

	def updatePicture(self, posDif=0):
		self.delete = []
		for widget in self.classFrame.winfo_children():
			widget.destroy()
		for widget in self.deleteFrame.winfo_children():
			widget.destroy()
		self.pos += posDif
		if self.pos == -1:
			self.pos = len(self.pics) - 1
		if self.pos == len(self.pics):
			self.pos = 0
		self.posLabel['text'] = self.pics[self.pos].strip('\\')
		self.im = Image.open(self.pics[self.pos])
		self.tk_im = ImageTk.PhotoImage(self.im)
		self.canvas.create_image(0, 0, anchor='nw', image=self.tk_im)
		self.updateData()

	def updateData(self):
		for i in range(len(self.picsData[self.pics[self.pos]])):
			car = self.picsData[self.pics[self.pos]][i]
			self.rect = self.canvas.create_rectangle(car.start[0], car.start[1], car.end[0], car.end[1], outline='green2')
			self.picsData[self.pics[self.pos]][i].canvas = self.rect
			self.createLabel(car, self.classFrame)

	def createLabel(self, carObject, frame=None):
		self.label = tk.Label(frame, text='Car')
		self.label.bind('<Enter>', lambda event, id = self.rect: self.highlight(id))
		self.label.bind('<Leave>', lambda event, id = self.rect: self.unhighlight(id))
		if frame != self.deleteFrame:
			self.label.bind('<1>', lambda event, id = self.rect, car=carObject, label=self.label: self.putOnChop(id, car, label))
		else:
			self.label.bind('<1>', lambda event, id = self.rect, car=carObject, label=self.label: 
self.unChop(id, car, label))
		self.label.pack()

	def putOnChop(self, id, car, label):
		self.rect = id
		self.createLabel(car, self.deleteFrame)
		self.delete.append(car)
		label.destroy()
		self.unhighlight(self.rect)
		print(self.delete)

	def unChop(self, id, car, label):
		self.rect = id
		self.delete = [i for i in self.delete if i != car]
		self.createLabel(car, self.classFrame)
		label.destroy()
		self.unhighlight(self.rect)
		print(self.delete)

	def deleteData(self):
		print(self.delete, 'to delete')
		print(self.picsData[self.pics[self.pos]])
		self.picsData[self.pics[self.pos]] = [i for i in self.picsData[self.pics[self.pos]] if i not in self.delete]
		print(self.picsData[self.pics[self.pos]])
		self.updatePicture()

	def highlight(self, id):
		self.canvas.itemconfig(id, width='3')

	def unhighlight(self, id):
		self.canvas.itemconfig(id, width='1')

	def onClick(self, event):
		self.cursorLocation = []

	def onDrag(self, event):
		x, y = event.x, event.y
		self.cursorLocation.append([x,y])

	def onRelease(self, event):
		first = self.cursorLocation[0]
		last = self.cursorLocation[-1]
		self.rect = self.canvas.create_rectangle(first[0], first[1], last[0], last[1], outline='green2')
		car = Car(first, last, self.rect)
		self.picsData[self.pics[self.pos]].append(car)
		self.createLabel(car, self.classFrame)

root = tk.Tk()
app = Application(master=root)
app.mainloop()

