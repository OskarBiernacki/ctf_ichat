import ichat.models
import ichat.utils
import random
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import system

from ichat import app
import time

class Administrator:
    def __init__(self):
        self.username = 'admin'
        self.password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=10))
        self.id = ichat.utils.create_user(self.username, self.password, is_admin=True, is_bot=False)
        self.is_running = False
        self.driver = None
        self.userWithLastReadedMessage = {}
        print('Admin created in database')
        print(f'Admin username: {self.username}')
        print(f'Admin password: {self.password}')
    
    def run(self):
        self.is_running = True
        print('Admin thread starting...')
        Thread(target=self.update_loop).start()
        
    def update_loop(self):
        while self.is_running:
            with app.app_context():
                try:
                    self.update()
                    time.sleep(1)
                except Exception as ex:
                    print(ex)

    def update(self):
        if self.driver is None:
            #service = ChromeService(executable_path="/usr/bin/chromedriver")
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            options.add_argument('--disable-gpu')
            options.timeouts = {"implicit": 10000, "pageLoad": 10000, "script": 10000}

            self.driver = webdriver.Chrome(options=options)
            print('Driver created')
            self.safe_web_load("http://127.0.0.1:5000/login")

            time.sleep(2)

        # Handle JavaScript alert if present
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Alert accepted")
        except NoAlertPresentException:
            pass

        if "login" in self.driver.current_url:
            print("Login page detected. Logging in...")
            self.login()

        self.visit_unreaded_chat()
        # print(f'current_admin_url:{self.driver.current_url}'+' '*10, flush=True, end="\r")

    def visit_unreaded_chat(self):
        messages = ichat.models.Message.query.filter_by(receiver_id=self.id).all()
        for message in messages:
            if message.sender_id not in self.userWithLastReadedMessage or message.send_time > self.userWithLastReadedMessage[message.sender_id]:
                self.userWithLastReadedMessage[message.sender_id] = message.send_time

                url_to_load = f"http://127.0.0.1:5000/chat/{message.sender_id}"
                self.safe_web_load(url_to_load)

                break
    
    def safe_web_load(self, url): # handling with infite js loops
        load_thread = Thread(target=self.driver.get, args=(url,))
        load_thread.start()
        load_thread.join(timeout=4)
                
        if load_thread.is_alive():
            print(f"Timeout on loading {url} - killing webdriver")
            ichat.utils.send_message(self.id, self.id, f"Timeout on loading {url} - killing webdriver")
            time.sleep(5)
            self.driver = None       

    def login(self):
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.click()

        self.safe_web_load(f'http://127.0.0.1:5000/chat/{self.id}')

        time.sleep(2)