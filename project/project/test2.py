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
        email.send_keys("aswinjosereji@gmail.com")
        password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
        password.send_keys("Aswin@123")
        time.sleep(2)
        submit=driver.find_element(By.CSS_SELECTOR,"button#login")
        submit.click()
        time.sleep(2)
        all_products = driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/customer_allProducts/']")
        all_products.click()
        time.sleep(2)
        product_view = driver.find_element(By.CSS_SELECTOR,"a.btn.btn-outline-warning[href='/customer_ProductView/1/']")
        product_view.click()
        time.sleep(2)
        add_cart = driver.find_element(By.CSS_SELECTOR,"button.btn[style='background-color:#FE9A2E; color: white;']")
        add_cart.click()
        time.sleep(2)
        cart = driver.find_element(By.CSS_SELECTOR,"a.nav-icon[href='/cart/']")
        cart.click()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(3)
if __name__ == '__main__':
    import unittest
    unittest.main()
