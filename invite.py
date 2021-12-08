import time
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#Documenting my things

def get_invitees() -> pd.DataFrame:
    invitees = pd.read_csv(r'data\invitados.csv')
    invitees.set_index('Invitado', inplace=True)
    invitees['nombre'].str.split(" ")

    return invitees


def goto_web():
    driver = webdriver.Chrome(r'utils\chromedriver.exe')
    wait = WebDriverWait(driver, 40)

    return driver, wait


def send_message(invitee, driver, wait):
    url = f"https://web.whatsapp.com/send?phone={invitee['Phone']}&text={invitee['message']}"
    driver.get(url)
    attach_image(driver, invitee['file'])


def attach_image(driver, file):
    elem = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 'span[data-icon="clip"]')))
    # click to add
    driver.find_element_by_css_selector('span[data-icon="clip"]').click()
    # add file to send by file path
    attach = driver.find_element_by_css_selector('input[type="file"]')
    # attach.click()
    attach.send_keys(file)

    send = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')))
    send.click()




if __name__ == '__main__':
    invitees = get_invitees()
    wait: WebDriverWait
    driver, wait = goto_web()
    for ind in invitees.index:
        something = invitees.loc[ind]
        send_message(invitees.loc[ind], driver, wait)
        snooze = randint(300, 600) / 100
        time.sleep(snooze)
