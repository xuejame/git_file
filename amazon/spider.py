import re

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from xlrd import open_workbook
from xlutils.copy import copy
import xuejame_test
from multiprocessing import Pool
import datetime
from lockfile import LockFile

#SERVICE_ARGS = ['--load-images=false','--disk-cache=true']
#browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser = webdriver.Chrome()
browser.set_window_size(1400,900)
wait = WebDriverWait(browser, 5)
list_product = []

def read_file():
    f = open('.\data\parameter1.txt')
    line = f.readline().strip('\n')
    i =-1
    list = []
    while line:
        if(line.find("https:") != -1):
            i = i+1
            list.append([])
            list[i].append(line)
        else:
            list[i].append(line)
        line = f.readline().strip('\n')
    return list

def search(url , key_word , shop):
    try:
        browser.get(url)
        input =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#twotabsearchtextbox")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#nav-search > form > div.nav-right > div > input")))

        input.send_keys(key_word)
        submit.click()
        try:
            if shop =='Bestuni':
                try:
                    Any_click = WebDriverWait(browser, 2).until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#leftNavContainer > ul:nth-child(2) > div > li:nth-child(1) > span > a > h4")))
                except TimeoutException:
                    Any_click = WebDriverWait(browser, 2).until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#leftNavContainer > ul:nth-child(3) > div > li:nth-child(1) > span > a > h4")))
            else:
                Any_click = WebDriverWait(browser, 2).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#leftNavContainer > ul:nth-child(3) > li:nth-child(1) > span > a > span")))
            Any_click.click()
        except TimeoutException:
            pass

        time.sleep(2)   #等待2秒，不然运行太快
        try:
            total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pagn > span.pagnDisabled")))
            if(total.text == ""):
                total = 20
            else:
                total = int(total.text)
                if total>20:
                    total = 20
        except TimeoutException:
            total = 5

        if total > 0:
            print(key_word)
            click_one(shop,1)
        return total
    except TimeoutException:
        search(url , key_word , shop)

def find_exist(word,list):
    for i in range(len(list)):
        if word in list[i]:
            return i
    return -1


def click_one(shop,number):
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#s-results-list-atf")))
        html = browser.page_source
        doc = pq(html)
        items = doc("#atfResults #s-results-list-atf .s-item-container").items()
        for item in items:
            # print(item.find('h2').attr("data-attribute"))
            # print(item.find('.a-link-normal').attr('href'))
            # print(item.find('.a-row .a-size-small').eq(1).text())
            # print(item.find('.a-offscreen').text())
            if (item.find('.a-row .a-size-small').eq(1).text() == shop):
                temp_i = find_exist(item.find('h2').attr("data-attribute"),list_product)#是否存在某个元素
                temp_j = item.find('h2 span').text().find('[')  #是否是广告
                if temp_i != -1:#如果已存在该元素
                    if temp_j !=-1:#如果是sponsored
                        list_product[temp_i][2] = number
                    else:
                        list_product[temp_i][1] = number
                else:
                    if temp_j !=-1:#如果是sponsored
                        list_product.append([item.find('h2').attr("data-attribute"),'无',number])
                    else:
                        list_product.append([item.find('h2').attr("data-attribute"), number, '无'])
    except Exception:
        click_one(shop, number)



def write_to_excel(xls,sheet,key_word):

    rexcel = open_workbook(xls)  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[sheet].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(sheet)  # 用xlwt对象的方法获得要操作的sheet
    list = list_product
    row = rows
    if (len(list)==0):
        table.write(row, 1, key_word)
    for i in range(len(list)):
        table.write(i+row, 0, list[i][0])  # xlwt对象的写方法，参数分别是行、列、值
        table.write(i + row, 1, key_word)
        table.write(i+row, 2, list[i][1])
        table.write(i+row, 3, list[i][2])
    excel.save(xls)  # xlwt对象的保存方法，这时便覆盖掉了原来的excel

def search_order():
    pass

def processing_web_page(url):
    browser.get(url)
    list = []
    stores = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#bylineInfo")))
    product_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#productTitle")))
    stars = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#acrPopover > span.a-declarative > a > i.a-icon.a-icon-star.a-star-5 > span")))
    review_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#acrCustomerReviewText")))
    question_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#askATFLink > span")))
    money = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#priceblock_ourprice")))
    small_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#productDetails_detailBullets_sections1 > tbody > tr:nth-child(7) > td > span > span:nth-child(3)")))
    big_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#productDetails_detailBullets_sections1 > tbody > tr:nth-child(7) > td > span > span:nth-child(1)")))
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#add-to-cart-button")))
    submit.click()
    time.sleep(2)
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
    number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#activeCartViewForm > div.sc-list-body.sc-java-remote-feature > div > div.sc-list-item-content > div > div.a-column.a-span2.a-text-right.sc-action-links.a-span-last > div > div > input")))

    list.append(stores.text)
    list.append(product_title.text)
    list.append(stars.text)
    list.append(review_number.text)
    list.append(money.text)
    list.append(small_title.text)
    list.append(big_title.text)
    list.append(number.text)
    print(list)




def next_page(shop,page_number):
    try:
        time.sleep(1)
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#pagnNextString")))
        submit.click()
#        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#pagn > span.pagnCur"),str(page_number)))
        print(page_number)
        click_one(shop, page_number)
    except Exception:
        next_page(shop,page_number)

def get_product():
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#s-results-list-atf")))
    html = browser.page_source
    doc = pq(html)
    items = doc("#s-results-list-atf").items()
    for item in items:
        product = {
            'image': item.find('.img').attr('src'),
            'shop' : item.find('a-size-small a-color-secondary').text(),
        }

def main(i,j,xls,list_parameter):

    # total = int(re.compile('(\d+)').search(total).group(1))

    # for i in range(2,total+1):
    #     next_page(i)


            total = search(list_parameter[i][0], list_parameter[i][j], list_parameter[i][1])
            for k in range(2,total+1):
                next_page(list_parameter[i][1],k)
            write_to_excel(xls,i,list_parameter[i][j])
            list_product[:] = []




if __name__ == '__main__':
    print(datetime.datetime.now().time())
    xls = xuejame_test.xuejame_time()
    list_parameter = read_file()
    # p = Pool()
    for i in range(len(list_parameter)):
        for j in range(2,len(list_parameter[i])):
            main(i,j,xls,list_parameter)
            # p.apply_async(main,args=(i,j,xls,list_parameter))
    # p.close()
    # p.join()
    print(datetime.datetime.now().time())
    browser.close()
