from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint


#driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome()
driver.get('https://account.mail.ru/login/')
driver.implicitly_wait(5)
driver.maximize_window()

elem = driver.find_element(By.NAME, 'username')
elem.send_keys('study.ai_172', Keys.ENTER)
elem = driver.find_element(By.NAME, 'password')
elem.send_keys('NextPassword172#', Keys.ENTER)
driver.implicitly_wait(3)

urls = set()

while True:
    actions = ActionChains(driver)
    letters = driver.find_elements(By.XPATH, "//div[@class='dataset__items']/a")
    if letters[-1].get_attribute('href') in urls:
        break
    driver.implicitly_wait(2)
    for link in letters:
        url = link.get_attribute('href')
        urls.add(url)
    actions.move_to_element(letters[-1])
    actions.perform()

#pprint(urls)
urls -= {None}
client = MongoClient('localhost', 27017)
db = client['mail_ru']
#pprint(urls)
for i in urls:
    l_dict = {}
    driver.get(i)
    print(i)
    driver.implicitly_wait(2)
    l_dict['from'] = driver.find_element(By.XPATH, "//span[@class='letter-contact']").get_attribute('title')
    l_dict['title'] = driver.find_element(By.XPATH, '//h2[@class="thread-subject"]').text
    #print(l_dict[l_title])
    l_dict['date'] = driver.find_element(By.CLASS_NAME,'letter__date').text
    l_dict['text'] = driver.find_element(By.XPATH,"//div[@class='letter__body']").text
    try:
        db.mail_db.insert_one(l_dict)
    except DuplicateKeyError:
        pass


#pprint(l_dict)
print(db.mail_db.count_documents({}))