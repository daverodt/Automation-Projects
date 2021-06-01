from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os import getcwd, listdir, environ, getenv 
from pandas import read_csv
import pyotp
import time
import sys
import keyboard
import pyautogui
from selenium.webdriver.support.ui import Select



def login(user,pw,secret,currentpath):
	#Gets driver and Action for clicks
	url = "https://freshdesk.com/a/tickets/compose-email"
	driver = webdriver.Chrome(currentpath + '\\chromedriver.exe')
	driver.maximize_window()
	driver.get(url)
	wait = WebDriverWait(driver, 100)
	actions = ActionChains(driver)
	#Defines buttons and clicks them
	google_button = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="login-container"]/div[2]/a[1]')))
	actions.click(google_button).perform()
	#Defines boxes and fills them through send keys
	user_box = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="identifierId"]')))
	user_box.send_keys(user,Keys.ENTER)

	#Enter Password
	pw_box = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input')))
	pw_box.send_keys(pw, Keys.ENTER)

	method_button = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[2]/div/div/button/div[2]')))
	time.sleep(3)
	driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[2]/div/div/button/div[2]').click()
	
	select_method_button = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[3]/div/div[2]')))
	time.sleep(3)
	driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[3]/div/div[2]').click()
	
	otp_box = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="totpPin"]')))
	
	totp = pyotp.TOTP(secret)
	otp_box.send_keys(totp.now(),Keys.ENTER)
	

	#Logs in again in Google
	google_button = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="root"]/div[2]/div/div/div/div/div/div/div/div[2]/div[1]/div[2]/button')))
	driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div/div/div/div/div/div[2]/div[1]/div[2]/button').click()
	profile_button = wait.until(EC.element_to_be_clickable((
				    By.XPATH,'//*[@id="profileIdentifier"]')))
	driver.find_element_by_xpath('//*[@id="profileIdentifier"]').click()
	return driver

def get_df():
	currentpath = getcwd()
	directories = listdir(currentpath)
	for directory in directories:
		if directory.lower().startswith('cartera'):
			filename = directory
	#Opens Cartera file
	df = read_csv(currentpath + '\\' + filename)
	if 'Done' not in df:
		df['Done'] = 'False'
	emails = df['Mail'].tolist()
	return emails,currentpath, df



def sendmails(emails, driver,df):
	wait = WebDriverWait(driver, 100)
	subject = 'Paga hoy y recibe tu renovación inmediata!!'
	description = 'Cobranza D4'
	#Gets Current Path and filename
	iteration = 0
	for email in emails:
		print(df.loc[iteration,'Done'])
		if df.loc[iteration,'Done'] == True:
			print('Ignored', email)
			iteration += 1
			continue
		if iteration == 1 or iteration == 6:
			time.sleep(50)
			driver.get('https://freshdesk.com/a/tickets/compose-email')
		else:
			driver.get('https://freshdesk.com/a/tickets/compose-email')
		#email = 'dave.rodt@gmail.com'
		
		#Fill DropDown
		for attempt in range(3):
			try:
				dropDown = wait.until(EC.element_to_be_clickable((
								    By.XPATH,'//*[@id="ember147"]')))
				dropDown.click()
				dropDown.send_keys(Keys.DOWN)
				dropDown.send_keys(Keys.ENTER)
				boxes = driver.find_elements_by_xpath('.//span[@class = "ember-power-select-selected-item"]')[0]
				#print(boxes.text)
				#print('dropDown:',dropDown.location)
				if 'Crédito' in boxes.text:
					break
				elif attempt == 2:
					failed == True
					continue
			except:
				print('Failed DropDown Attempt:',attempt)
				continue


		#Fill Email
		for attempt in range(4):
			try:
				email_box = driver.find_element_by_xpath('//*[@id="ember160"]')
				print('email_box:',email_box.location)
				pyautogui.click(x=350, y=(email_box.location['y']*.9489+137.7))
				time.sleep(attempt + 1)
				keyboard.write(email)
				time.sleep(attempt + 1)
				keyboard.press_and_release('enter')
				boxes = driver.find_elements_by_xpath('.//span[@class = "ember-power-select-selected-item"]')[1]
				if email in boxes.text:
					break
				elif attempt == 3:
					failed == True
			except:
				print('Failed Email Attempt:',attempt)
				continue

		#Fill Subject
		subject_box = driver.find_element_by_xpath('//*[@id="subject_ember165"]')
		subject_box.send_keys(subject)

		#Fill Description
		for attempt in range(3):
			try:
				 
				description_box = driver.find_element_by_xpath('//*[@id="ember169"]/div/div/div/div[1]')
				print('description_box:',description_box.location)
				#Gets description box location and adds some coordinates
				pyautogui.click(350, description_box.location['y']*.9489+137.7+(attempt*10))
				#Writes a letter for the program to recognize something was written
				keyboard.write('a')
				#Selects all to delete what's already been written
				keyboard.press_and_release('ctrl+a')
				time.sleep(attempt + 0.1)
				keyboard.write('a')
				keyboard.press_and_release('ctrl+a')
				time.sleep(attempt + 0.1)
				#Writes the command for Description Template
				keyboard.write('/c')
				time.sleep(attempt + 1.5)
				keyboard.press_and_release('enter')
				keyboard.write(description)
				time.sleep(attempt + 1.5)
				keyboard.press_and_release('enter')				
				boxes = WebDriverWait(driver, 6).until(EC.element_to_be_clickable((
								    By.XPATH,'//*[@id="ember169"]/div/div/div/div[1]/div[1]')))
				print(boxes.text)
				if 'hola' in boxes.text.lower():
					break
				elif attempt == 2:
					failed == True
					continue
				else:
					driver.execute_script("window.scrollTo(0, 0)")
					time.sleep()

			except:
				print('Failed Description Attempt:',attempt)
				continue

		#Fill Type
		number = 0
		for attempt in range(3):
			try:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(attempt + 1)
				Type_combobox = driver.find_element_by_xpath('//*[@id="ember199"]')
				#print('Type_combobox:',Type_combobox.location)
				print('Type_combobox:',Type_combobox.location)
				pyautogui.click(350, Type_combobox.location['y']*.9489-150 + number)
				time.sleep(attempt + 0.1)
				keyboard.write('Crédito - Pagos')
				time.sleep(attempt + 1)
				keyboard.press_and_release('enter')
				
				#print('check:',check.location)
				boxes = driver.find_elements_by_xpath('.//span[@class = "ember-power-select-selected-item"]')
				print(len(boxes))
				if len(boxes)==4:
					print('Named it in Tag')
					pyautogui.click(500, Type_combobox.location['y']*.9489-75)
					print(number)
					keyboard.press_and_release('backspace')
					number = -75

				if 'Crédito - Pagos' in boxes[4].text:
					break
					
				elif attempt == 2:
					failed == True
					continue


			except:
				print('Failed Type Attempt:',attempt)
				continue
		#Check		
		check = driver.find_element_by_xpath('//*[@id="ember212"]/label')
		check.click()

		#Submit
		submit = driver.find_element_by_xpath('//*[@id="ember214"]')

		print(submit.text)
		submit.click()
		df.loc[iteration,'Done'] = 'True'
		iteration+=1
		print(iteration)
		df.to_csv(currentpath + '\\Cartera  - 26 de abril.csv',index=False)
		






if __name__ == "__main__":
	user = getenv('MAIL_USER')
	pw = getenv('MAIL_PASSWORD')
	secret = getenv('MAIL_SECRET')
	emails, currentpath, df = get_df()
	driver = login(user,pw,secret,currentpath)
	print('url:,',driver.command_executor._url)      
	print('sessionid:',driver.session_id)            
	

	sendmails(emails,driver, df)
	while(True):
		pass





