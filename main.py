from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
import csv
import time

def isAlertAvail(browser):
    try:
        wait = WebDriverWait(browser, timeout=10).until(EC.alert_is_present())
        return True
    except TimeoutException:
        return False

if(__name__ == '__main__'):
    #Input user
    print('Mulai pada data ke: ', end="")
    start = int(input())
    print('Selesai pada data ke: ', end="") #Included
    end = int(input())
    print('Timeout (Default 10): ', end="") #Kalau koneksi lagi lag, naikin aja yak
    timeout = int(input())
    print('Nama file text: ', end="")
    filename = input()
    print('Nama file csv: ', end="")
    csvname = input()
    #Setup txt
    f = open(filename, 'r')
    text = f.read()
    template = []
    for t in text.split('\n'):
        template.append(t) 
    #Setup csv
    res = []
    file = open(csvname, 'r+')
    reader = csv.reader(file)
    header = next(reader, None)
    column_nama = header.index('Nama')
    column_no_telp = header.index('No. Telp')
    #Cutting useless column and row
    for i, line in enumerate(reader):
        if(i >= start and i <= end):
            tupel = line[column_nama], line[column_no_telp]
            res.append(tupel)
    print(res)
    #Start opening browser
    browser = webdriver.Chrome('chromedriver')
    browser.get('https://web.whatsapp.com/')

    for r in res:
        try:
            #Access API
            num = r[1][1:]
            browser.get('https://web.whatsapp.com/send?phone=62' + num + '&text&source&data&app_absent')
            #Check if theres alert
            isAvail = isAlertAvail(browser)
            if(isAvail):
                browser.switch_to.alert.accept()
            #Wait render website
            wait = WebDriverWait(driver=browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'side')))
            inputField = browser.find_elements_by_class_name('_3FRCZ')[1]
            #Start typing
            sent = template[0]
            splitted = text.split('\n')
            for counter, s in enumerate(splitted):
                if('{nama}' in s):
                    s = s.replace('{nama}', r[0])
                inputField.send_keys(s)
                inputField.send_keys(Keys.SHIFT,'\n')
            send_button = browser.find_element_by_class_name('_1U1xa')
            send_button.send_keys(Keys.ENTER)
            #Send status
            print('Done sending to ' + r[0] + ' - ' + r[1])
            success = open('success.txt', 'a+')
            success.write(r[0] + ' - ' + r[1] + '\n')
            success.close()
        except IndexError as e:
            #Send status
            print('Failed to send text to ' + r[0] +  ' - ' + r[1])
            failure = open('failure.txt', 'a+')
            failure.write(r[0] + ' - ' + r[1] + '\n')
            failure.close()