from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Hosttest(TestCase):    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        dropdown=driver.find_element(By.CSS_SELECTOR,"a.nav-icon#userDropdown")
        dropdown.click()
        time.sleep(2)
        signin=driver.find_element(By.CSS_SELECTOR,"a.dropdown-item[href='/register/user_login/']")
        signin.click()
        time.sleep(2)
        email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
        email.send_keys("ananthugopalan2001@gmail.com")
        password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
        password.send_keys("Ammu@123")
        time.sleep(2)
        submit=driver.find_element(By.CSS_SELECTOR,"button#login")
        submit.click()
        time.sleep(2)
        add_product=driver.find_element(By.CSS_SELECTOR,"a[href='/seller_addProducts/'].list-group-item.list-group-item-action")
        add_product.click()
        time.sleep(2)
        product_name=driver.find_element(By.CSS_SELECTOR,"input[type='text'][name='product_name']")
        product_name.send_keys("Cauliflower")
        time.sleep(2)
        description = driver.find_element(By.CSS_SELECTOR,"textarea.form-control#id_description[name='description'][rows='4'][maxlength='200'][required]")
        description.send_keys("Cauliflower is one of the most important vegetable crops of India. It is rich in minerals such as potassium, sodium, iron, phosphorus, calcium, magnesium etc")
        time.sleep(2)
        stock = driver.find_element(By.CSS_SELECTOR,"input[type='number'][name='stock']")
        stock.send_keys("10")
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        category = driver.find_element(By.CSS_SELECTOR,"select.form-control#id_category[name='category'][required]")
        category.click()
        time.sleep(2)
        crop = driver.find_element(By.CSS_SELECTOR,"option[value='crops']")
        crop.click()
        time.sleep(2)
        subcategory = driver.find_element(By.CSS_SELECTOR,"select.form-control#id_subcategory[name='subcategory'][required]")
        subcategory.click()
        time.sleep(2)
        vegetable = driver.find_element(By.CSS_SELECTOR,"option[value='vegetables']")
        vegetable.click()
        time.sleep(2)
        price = driver.find_element(By.CSS_SELECTOR,"input[type='text'][name='price']")
        price.send_keys("250")
        time.sleep(2)
        btn = driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
        btn.click()
        time.sleep(2)
