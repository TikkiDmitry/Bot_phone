from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from simon.chat.pages import ChatPage
from simon.chats.pages import PanePage
from simon.pages import BasePage
from simon.accounts.pages import LoginPage

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
print("Scan QR Code, And then Enter")
input()
print("Logged In")

# 1. Get all opened chats
#       opened chats are the one chats or conversations
#       you already have in your whatsapp.
#       IT WONT work if you are looking for a contact
#       you have never started a conversation.
pane_page = PanePage(driver)
chat_page = ChatPage(driver)

# a = pane_page.opened_chats()
# time.sleep(100)
# print(a)
#
# for oc in a:
#     print(oc.name)  # contact name (as appears on your whatsapp)


# get all chats
opened_chats = driver.find_elements(By.CLASS_NAME, '_8nE1Y')
# time.sleep(10)
# phone = driver.find_elements(By.XPATH, '//*[@id="app"]/div/span[4]/div/ul/div/div/li[1]')
# a = chat_page.driver.find_elements(By.CLASS_NAME, 'a4ywakfo qt60bha0')
# b = pane_page.driver.find_elements(By.CLASS_NAME, 'a4ywakfo qt60bha0')

# c = driver.find_elements(By.CSS_SELECTOR, '#pane-side > div:nth-child(1)')
# time.sleep(10)
# d = driver.find_elements(By.CLASS_NAME, 'k8VZe')
# e = driver.find_elements(By.XPATH, '//*[@id="pane-side"]/div[1]')

# print(c)
# k = 0
# for i in c:
#     print(i.text)
#     k+=1
# print(k)
#
# # print(phone)
# # for i in phone:
# #     print(i.text)
#
# for i in e:
#     print(i.text)
# print(e)
#
# for i in d:
#     print(i.text)
# print(d)
d = []
print(len(opened_chats))
k = 0
for i in opened_chats:
    print(i.text)
    a = i.text
    d.append(a)
    k += 1
    # b = driver.find_element(By.CSS_SELECTOR, '#app > div > div > div._2Ts6i._1xFRo > span > div > span > div > div > section > div.gsqs0kct.oauresqk.efgp0a3n.tio0brup.g0rxnol2.tvf2evcx.oq44ahr5.lb5m6g5c.brac1wpa.lkjmyc96.b8cdf3jl.bcymb0na.myel2vfb.e8k79tju > div.p357zi0d.ktfrpxia.nu7pwgvd.fhf7t426.f8m0rgwh.gndfcl4n > div')
    # print(b)
print(d)
print(k)

# print(len(c))
# print(len(e))
# print(len(d))

# print(a)
# print(b)


def test_can_detect_if_chat_is_completely_new():
    # can detect if current chat is fresh (new) chat initiated by contact/client
    assertFalse(chat_page.is_chat_new())

driver.quit()

# _10kwi _1BX24 dd20w
