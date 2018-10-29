from xlrd import open_workbook
from xlutils.copy import copy
from lockfile import LockFile
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
import datetime
import parameter

browser = webdriver.Chrome()
# time.sleep(1)
# js = 'document.getElementById("doyoo_monitor").style.display="none";'
# browser.execute_script(js)
browser.set_window_size(1400,900)
wait = WebDriverWait(browser, 10)
list = [[]for i in range(parameter.MAX_PRODUCT)]
list_link = [[]for i in range(parameter.NUM_OF_COUNTRY)]

def read_excel(xls):
    rexcel = open_workbook(xls,formatting_info=True)  # 用wlrd提供的方法读取一个excel文件
    rexcel.encoding ="utf-8"
    num_sheet = len(rexcel.sheets())
    for i in range(num_sheet):
        table = rexcel.sheet_by_index(i)
        cols = rexcel.sheets()[i].ncols
        rows = rexcel.sheets()[i].nrows
        for j in range(1,rows,8):
            if table.cell_value(j,3) =="":
                break
            list_link[i].append(table.cell_value(j,3))


def write_to_excel(xls,i):
    rexcel = open_workbook(xls,formatting_info=True)  # 用wlrd提供的方法读取一个excel文件
    rexcel.encoding ="utf-8"
    num_sheet = len(rexcel.sheets())
    table1 = rexcel.sheet_by_index(i)
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    excel.encoding = "utf-8"
    cols = rexcel.sheets()[i].ncols  # 用wlrd提供的方法获得现在已有的行数nrows
    rows = rexcel.sheets()[i].nrows
    table = excel.get_sheet(i)  # 用xlwt对象的方法获得要操作的sheet
    for j in range(len(list)):
        if list[j] == []:
            continue
        table.write(j*8+2,1,list[j][0])
        table.write(j*8,cols,str(datetime.datetime.now().date()))
        for k in range(1,len(list[j])):
            table.write(j*8+k+1,cols,list[j][k])
        previous_inventory = table1.cell_value(j*8+6,cols-1)
        if previous_inventory=="":
            pass
        else:
            if len(list[j])>5:
                table.write(j*8+7,cols,int(previous_inventory)-list[j][5])

    excel.save(".\data\sales_detection.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel

def processing_web_page(url,i):
    try:
        browser.get(url)
        time.sleep(1)
        try:
            stores = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#bylineInfo")))

            product_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#productTitle")))
            stars = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#reviewSummary > div.a-row.a-spacing-small > span > a > span")))
            review_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#acrCustomerReviewText")))
        except:
            pass
        try:
            list[i].append(product_title.text)
            list[i].append(stores.text)
            list[i].append(int(re.compile('\d+').search(review_number.text).group(0)))
            list[i].append(stars.text)
        except:
            pass




        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add-to-cart-button")))
        submit.click()
        try:
            time.sleep(2)
            no_thank = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#siNoCoverage-announce")))
            no_thank.click()
        except Exception:
            pass
        money = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#hlb-subcart > div.a-row.a-spacing-micro > span > span.a-color-price.hlb-price.a-inline-block.a-text-bold")))
        list[i].insert(2,money.text)
        submit_cart = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#hlb-view-cart-announce")))
        submit_cart.click()

        time.sleep(1)
        quantity = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#a-autoid-0-announce")))
        quantity.click()
        quantity_10 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#dropdown1_9")))
        quantity_10.click()
        quantity_number =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#activeCartViewForm > div.sc-list-body.sc-java-remote-feature > div > div.sc-list-item-content > div > div.a-column.a-span2.a-text-right.sc-action-links.a-span-last > div > div > input")))
        quantity_number.clear()
        quantity_number.send_keys(999)
        time.sleep(1)
        quantity_update = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#a-autoid-1-announce")))
        quantity_update.click()
        time.sleep(1)
        number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#gutterCartViewForm > div.a-box-group.sc-buy-box-group > div.a-box.a-color-alternate-background > div > div.sc-subtotal.a-spacing-mini > p > span > span:nth-child(1)")))
        total = int(re.compile('\d+').search(number.text).group(0))

        list[i].append(total)
        time.sleep(2)
        delete = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#activeCartViewForm > div.sc-list-body.sc-java-remote-feature > div > div.sc-list-item-content > div > div.a-column.a-span8 > div > div > div.a-fixed-left-grid-col.a-col-right > div > span.a-size-small.sc-action-delete > span > input[type="submit"]')))

        delete.click()

        print(list)
    except Exception:
        pass

if __name__ =='__main__':
    read_excel('.\data\sales_detection.xls')
    for i in range(len(list_link)):
        for j in range(len(list_link[i])):
            processing_web_page(list_link[i][j],j)
        write_to_excel('.\data\sales_detection.xls',i)
        list = [[] for i in range(parameter.MAX_PRODUCT)]
    # processing_web_page('https://www.amazon.fr/Minger-Ampoules-Changement-dambiance-T%C3%A9l%C3%A9commande/dp/B01JO9S75W/ref=sr_1_8?ie=UTF8&qid=1519546528&sr=8-8&keywords=ampoule+led',0)

    # processing_web_page("https://www.amazon.co.uk/Ultrasonic-Electronic-Repellent-Insects-Roaches-Mosquitoes/dp/B072P2HWFW/ref=sr_1_fkmr1_3?s=sports&ie=UTF8&qid=1501080492&sr=8-3-fkmr1&keywords=pest+offense")
    browser.close()