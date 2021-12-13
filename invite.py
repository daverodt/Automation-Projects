import time
from random import randint

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_invitees() -> pd.DataFrame:
    # Gets DataFrame from csv that includes name, phone number, message
    invitees = pd.read_csv(r'data\invitados.csv')
    invitees.set_index('Invitado', inplace=True)

    return invitees


def goto_web():
    # Opens chrome geckodriver which should be located in utils folder
    driver = webdriver.Chrome(r'utils\chromedriver.exe')

    # Defines a wait time of 40 seconds to get whatsapp working in the web
    wait = WebDriverWait(driver, 40)

    return driver, wait


def send_message(invitee, driver, wait):
    # Sets the url that contains the person's phone number and the message
    url = f"https://web.whatsapp.com/send?phone={invitee['Phone']}&text={invitee['message']}"
    driver.get(url)
    if invitee['file'] != "":
        attach_image(driver, invitee['file'])
    # Waits for the click button to be available
    send = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')))
    # Sends the image with the message
    send.click()


def attach_image(driver, file):
    # Sets element for image icon
    elem = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 'span[data-icon="clip"]')))
    # Click to add image in the icon
    elem.click()
    # add file to send by file path
    attach = driver.find_element_by_css_selector('input[type="file"]')
    # Attaches the image by using the file url
    attach.send_keys(file)


if __name__ == '__main__':
    invitees = get_invitees()
    driver, wait = goto_web()
    #Loops for all invitees
    for ind in invitees.index:
        something = invitees.loc[ind]
        send_message(invitees.loc[ind], driver, wait)
        #Random snooze to make it more human and less censorship prone for whatsapp
        snooze = randint(300, 600) / 100
        time.sleep(snooze)
