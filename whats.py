from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from os import getcwd
from os import path
from os import listdir
from random import randrange
from pandas import read_csv
from math import floor
from decimal import Decimal
import tkinter as tk
from tkinter import messagebox
import sys


def action(new_amount):
	global amount, j
	amount = new_amount
	j = 0
	ContinueApplication()

def ContinueApplication():
    MsgBox = tk.messagebox.askquestion ('Continue','Are you sure you want to continue running next %s?'%amount,icon = 'question')
    if MsgBox == 'yes':
       root.destroy()
    else:
        tk.messagebox.showinfo('Return','You will now return to the application screen')
        currentpath = getcwd()
        sys.exit()
        
def keys(input_box,i,send):
	if send == True:
		input_box.send_keys(Keys.ENTER)
	
	else:
		input_box.send_keys(Keys.CONTROL, "a")
		input_box.send_keys(Keys.BACKSPACE)
	
print('Starting...')
#getcwd()
currentpath = getcwd()
directories = listdir(currentpath)
for directory in directories:
	if directory.lower().startswith('cartera'):
		filename = directory
if path.exists(currentpath + '\\test.txt'):
	send = False
else:
	send = True

df = read_csv(currentpath + '\\' + filename)
if 'Done' not in df:
	df['Done'] = 'False'

phones = df['phone'].tolist()
mensaje1 = df['Mensaje 1/3'].tolist()
mensaje2 = df['Mensaje 2/3'].tolist()
mensaje3 = df['Mensaje 3/3'].tolist()
# Replace below path with the absolute path
# to chromedriver in your computer
driver = webdriver.Chrome(currentpath + '\\chromedriver.exe')
url = "https://wa.me/"
inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
wait = WebDriverWait(driver, 100)
amount = 5
i = 0
j = 0
for phone in phones:
	print(df.loc[i,'Done'])
	if df.loc[i,'Done'] != True:
		driver.get(url + str(floor(phone)))
		print(url + str(floor(phone)))
		elem = wait.until(EC.element_to_be_clickable((
		    By.XPATH,'//*[@id="action-button"]')))
		actions = ActionChains(driver)
		actions.click(elem).perform()
		elem2 = wait.until(EC.element_to_be_clickable((
		    By.XPATH,'//*[@id="fallback_block"]/div/div/a')))
		actions = ActionChains(driver)
		actions.click(elem2).perform()
		input_box = wait.until(EC.element_to_be_clickable((
		    By.XPATH,inp_xpath)))
		delay = float(Decimal(randrange(155, 389))/100)
		input_box.send_keys(mensaje1[i])
		sleep(delay)
		print("Send:",send)
		keys(input_box,i,send)
		delay = float(Decimal(randrange(155, 489))/100)
		input_box.send_keys(mensaje2[i])
		sleep(delay)
		keys(input_box,i,send)
		delay = float(Decimal(randrange(155, 289))/100)
		input_box.send_keys(mensaje3[i])
		sleep(delay)
		keys(input_box,i,send)
		
		delay = float(Decimal(randrange(255, 500))/100)
		print('Waiting:',delay)
		keys(input_box,i,send)
		df.loc[i,'Done'] = 'True'
		df.to_csv(currentpath + '\\' + filename)
		sleep(delay)
		i+=1
		j+=1
		
		
		if j%amount == 0:
			root= tk.Tk()
			canvas1 = tk.Canvas(root, width = 10, height = 10)
			canvas1.pack()

			button1 = tk.Button (root, text=('Continue 5'),command=lambda: action(5),bg='blue',fg='white')
			button1.pack(side=tk.LEFT)

			button2 = tk.Button (root, text=('Continue 10'),command=lambda: action(10),bg='green',fg='white')
			button2.pack(side=tk.RIGHT)
			canvas1.create_window(1,1)
			root.mainloop()
			if j != 0:
				df.to_csv(currentpath + '\\Cartera 1.3 - 4_25.csv',index=False)
				sys.exit()
	else:
		i+=1
	print("Processed:",i)