import os
from time import sleep
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select

QR_CODE_EXPIRES_IN = 30
QR_CODE_QUERY = (By.XPATH, "//div[@data-testid='qrcode']")
CHAT_QUERY = (By.CLASS_NAME, '_8nE1Y')

class WhatsappScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=/chrome_data")
        self.driver = webdriver.Chrome()
        self.logged_in = False
    
    def save_qrcode(self, qrcode_img: bytes):
        path = Path("images") / "qrcode.png"
        with open(path, "wb") as f:
            f.write(qrcode_img)
    
    def find_qr_code(self, wait=1):
        try:
            qr_code = WebDriverWait(self.driver, wait).until(lambda d: d.find_element(*QR_CODE_QUERY))
        except TimeoutException:
            qr_code = None
        return qr_code
    
    def get_qr_code_image_as_png(self):
        qrcode_element = self.find_qr_code()
        qrcode = qrcode_element.screenshot_as_png
        return qrcode
    
    def get_qr_code_image_as_base64(self):
        qrcode_element = self.find_qr_code()
        qrcode_b64 = qrcode_element.screenshot_as_base64
        return qrcode_b64
    
    def find_chats(self):
        chats = self.driver.find_elements(*CHAT_QUERY)
        return chats
    
    def update_auth_status(self):
        qrcode = self.find_qr_code()
        while qrcode:
            qrcode_image = self.get_qr_code_image_as_png()
            self.save_qrcode(qrcode_image)
            sleep(1)
            qrcode = self.find_qr_code()
        if os.path.exists("images/qrcode.png"):
            os.remove("images/qrcode.png")
    
    def init(self):
        self.driver.get("https://web.whatsapp.com")

    def loop(self):
        while self.started:
            self.update_auth_status()
            if not self.logged_in:
                self.wait_until_logged_in()
                chats = self.driver.find_elements(CHAT_QUERY)
                print([c.text for c in chats])
    
    def start(self):
        self.init()
        self.started = True
        self.loop()
        
    def __exit__(self):
        self.driver.quit()
        
        
if __name__=="__main__":
    scrapper = WhatsappScraper()
    scrapper.start()