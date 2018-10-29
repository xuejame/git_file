from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.PhantomJS()
wait = WebDriverWait(browser, 5)
browser.get('http://www.baidu.com')
html = browser.page_source
if(html.find("深圳大学城")!=-1):
    browser.get("http://10.0.10.66/srun_portal_pc.php?ac_id=13&")
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#bt_connect")))
    submit_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#uname")))
    submit_password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pass")))

    submit_name.send_keys('33317S051060')
    submit_password.send_keys('13713776676')
    submit.click()
    print('登录成功')
else:
    print('无需登录')
browser.close()

