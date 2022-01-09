from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os
import shutil
import csv
import random
import logging

download_dir = "C:\\Users\\User\\Desktop\\vellode\\"
def get_firefox_driver():
    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", download_dir)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
    fp.set_preference("pdfjs.disabled", True)
    driver = webdriver.Firefox(firefox_profile=fp)
    return driver

def get_cibil_website():
    browser = get_firefox_driver()
    browser.get("https://consumer.cibil.com")
    browser.find_element_by_name('username').send_keys('')
    browser.find_element_by_name('psd').send_keys('')
    login = browser.find_element_by_name('submit').click()
    return browser

def generate_cibil(fullName, savingAccount , dobDay, dobMonth, dobYear, gender, incomeTaxId, voterId, universalId, phoneNumber1, currrentAddress, currrentAddressPincode, driver):
    driver.get("https://consumer.cibil.com/tile.do?name=orderForm.creditReportingPlusScore")
    time.sleep(5)
    try:
        inquiry_amount = driver.find_element_by_name('inquiryAmount').send_keys('50000')
        time.sleep(2)
        purpose_select = Select(driver.find_element_by_name('purpose'))
        time.sleep(2)
        purpose_select.select_by_visible_text('Kisan Credit Card')
        personal_loan_score = driver.find_element_by_id('includePLScore1').click()
        fullname = driver.find_element_by_name('fullName').send_keys(fullName)
        dob_day = driver.find_element_by_name('dobDay').send_keys(dobDay)
        dob_month = driver.find_element_by_name('dobMonth').send_keys(dobMonth)
        dob_year = driver.find_element_by_name('dobYear').send_keys(dobYear)
        gender_select = Select(driver.find_element_by_name('gender'))
        gender_select.select_by_visible_text(gender)
        time.sleep(2)
        income_tax_id = driver.find_element_by_name('incomeTaxId').send_keys(incomeTaxId)
        if voterId:
            voterId = driver.find_element_by_name('voterId').send_keys(voterId)
        universaL_id = driver.find_element_by_name('universalId').send_keys(universalId)
        if phoneNumber1:
            phone_number_1 = driver.find_element_by_name('phoneNumber1').send_keys(phoneNumber1)
            phone_number_1_select = Select(driver.find_element_by_name('phoneType1'))
            phone_number_1_select.select_by_visible_text('Mobile Phone')
        time.sleep(2)
        currrent_address = driver.find_element_by_name('currrentAddress').send_keys(currrentAddress)
        current_address_state_select = Select(driver.find_element_by_name('currrentAddressState'))
        current_address_state_select.select_by_visible_text('Tamil Nadu')
        currrent_address_pincode = driver.find_element_by_name('currrentAddressPincode').send_keys(currrentAddressPincode)
        time.sleep(2)
        currrent_address_category = Select(driver.find_element_by_name('currrentAddressCategory'))
        currrent_address_category.select_by_visible_text('Residence Address')
        currrent_residence_code_select = Select(driver.find_element_by_name('currrentResidenceCode'))
        currrent_residence_code_select.select_by_visible_text('Owned')
        current_address_same_as_permanent_address = driver.find_element_by_id('currentAddressSameAsPermanentAddress1').click()
        account1 = driver.find_element_by_name('account1').send_keys(savingAccount)
        #driver.save_screenshot(fullName+'.png')
        submit = driver.find_element_by_name('submit').click()
        time.sleep(2)
        #driver.get("https://consumer.cibil.com/ReportPdfResponseServlet")

        filename = max([download_dir + "/" + f for f in os.listdir(download_dir)],key=os.path.getctime)
        shutil.move(filename,os.path.join(download_dir,savingAccount +' '+fullName+'.pdf'))
        print("Cibil for {} has been saved".format(savingAccount))
    except:
        logging.basicConfig(filename='cibil_not_generated.log',format='%(asctime)s %(message)s', level=logginf.DEBUG)
        logging.debug('cibil not generated for {} Account Number {} PAN: {}'.format(fullName, savingAccount, incomeTaxId))



if __name__ == "__main__":
    print("Cibil generation program")
    with open('vellode_1347.csv','r') as file:
        driver = get_cibil_website()
        reader = csv.DictReader(file)
        for row in reader:
            userdetails = dict(row)
            fullName = userdetails['fullName']
            savingAccount = userdetails['savingAccount']
            print(userdetails)
            dobDay = userdetails['dob'].split('-')[0]
            dobMonth = userdetails['dob'].split('-')[1]
            dobYear = userdetails['dob'].split('-')[2]
            gender = userdetails['gender']
            incomeTaxId = userdetails['incomeTaxId'] or ''
            universalId = userdetails['universalId'] or ' '
            voterId = userdetails['voterId'] or None
            phoneNumber1 = userdetails['phoneNumber1'] or None
            currrentAddress = userdetails['address_1']+' '+userdetails['address_2']+' '+userdetails['address_3']+ ' ' + userdetails['address_4']+ ' '+ userdetails['state']
            currrentAddressPincode = userdetails['currrentAddressPincode']

            if userdetails['cibil_generated'] == 'No':
                generate_cibil(fullName, savingAccount , dobDay, dobMonth, dobYear, gender, incomeTaxId, voterId, universalId, phoneNumber1, currrentAddress, currrentAddressPincode, driver)
                time.sleep(2)
                print(userdetails['dob'])
                print(userdetails['incomeTaxId'])
        driver.quit()
                
                
            
