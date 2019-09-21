import os
import numpy as np

pics = [os.path.join(os.getcwd(), 'pic', file) for file in os.listdir(os.path.join(os.getcwd(), 'pic')) if 
'.txt' not in file]
print(len(pics))
percentage = 10.0
numberOfFiles = int((percentage/100)*len(pics))

lol = np.random.choice(pics, numberOfFiles, replace=False)
with open('train.txt', 'w') as file:
	for i in pics:
		if i not in lol:
			file.write(i + '\n')
with open('test.txt', 'w') as file:
	for i in lol:
		file.write(i + '\n')
