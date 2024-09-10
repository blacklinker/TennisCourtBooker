from datetime import date
import os
import sys
import time
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def book(link: str, targetTime: str, dob: str, bciti_id: str, email: str):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
    chrome_options.add_argument("--disable-extensions")  # Disable extensions for a clean test

    if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
        chrome_driver_path = os.path.join(sys._MEIPASS, 'chromedriver.exe')
    else:
        chrome_driver_path = 'chromedriver-win64/chromedriver.exe'
        
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(link)
    terrainsButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctlHautPage_ctlMenu_ctlLienEspaces')))
    print(terrainsButton)
    terrainsButton.click()
    print("Go to tennis page!")

    tennisCheckBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctlBlocRecherche_ctlRestrictions_ctlSelTypeEspace_ctlListe_ctl08_ctlLigne_ctlSelection')))
    tennisCheckBox.click()
    print("Check the tennis checkbox")
    time.sleep(1)

    today = str(date.today().day)
    nextDay = str(date.today().day + 1)
    dates = driver.find_elements(By.CLASS_NAME, 'Ludik_cal_gen_days')
    for d in dates:
        if d.text == today:
            d.click()
        if d.text == nextDay:
            d.click()
    print("Check the date!")
    time.sleep(1)

    searchButton = driver.find_element(By.ID, 'ctlBlocRecherche_ctlRechercher')
    searchButton.click()
    time.sleep(1)

    targetPlace = 'Parc Poly-Arena'

    def findTargetTime():
        timeSheetTable = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tabDonnees')))
        trs = timeSheetTable.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            print(tr.text)
            if(targetTime in tr.text and targetPlace in tr.text):
                print("The target time found!")
                return tr
        return None 

    target = None
    page = 0
    while(True):
        pages = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tabDonneesPager'))).find_elements(By.TAG_NAME, 'a')
        target = findTargetTime()
        if(target != None):
            break
        if(page >= len(pages)):
            break
        else:
            pages[page].click()
            time.sleep(1)
        page+=1

    if(target == None):
        driver.quit()
        messagebox.showinfo
        messagebox.showinfo("Error", f"The time {targetTime} not found")

    addToCart = target.find_element(By.TAG_NAME, 'td')
    addToCart.click()
    print("Added to cart!")
    time.sleep(1)

    cart = driver.find_element(By.ID, 'ctlHautPage_ctlMenu_ctlLienPanier')
    cart.click()
    print('Go to cart')
        
    BCITI_ID_Input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'colDossier'))).find_element(By.TAG_NAME, 'input')
    BCITI_ID_Input.send_keys(bciti_id)

    DOB_Input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'colNip'))).find_element(By.TAG_NAME, 'input')
    DOB_Input.send_keys(dob)
    print("Input BCITI ID and DOB")
    time.sleep(1)

    confirmButton = driver.find_element(By.ID, 'ctlMenuActionsHaut_ctlAppelPanierConfirm')
    confirmButton.click()
    time.sleep(1)
    confirmButton.click()
    print("Confirm button clicked")

    politic_inputs = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'politiques'))).find_elements(By.TAG_NAME, 'input')
    for politic_input in politic_inputs:
        politic_input.click()
    print("Politic checkboxes clicked")
    time.sleep(1)

    email_Input = driver.find_element(By.ID, 'ctlConditions_ctlCourriel')
    email_Input.send_keys(email)
    print("email input")
    time.sleep(1)

    completeButton = driver.find_element(By.ID, 'ctlMenuActionHaut_ctlCompleterGratuit')
    completeButton.click()
    print('complete button clicked!')

    sendEmailCheckbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctlFormulaireCourriel_ctlListeAdressesPersonnes_ctl00_ctlAdressePersonne_ctlSelection')))
    sendEmailCheckbox.click()
    print('Send email checkbox clicked!')
    time.sleep(1)

    sendEmail = driver.find_element(By.ID, 'ctlFormulaireCourriel_ctlEnvoyer')
    sendEmail.click()
    print('Email sent!!!!!!!')

    time.sleep(2)
    driver.quit()
    print('quit browser')