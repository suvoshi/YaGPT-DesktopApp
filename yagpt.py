from selenium import webdriver
from selenium.webdriver.common.by import By
import html2text
from fake_headers import Headers

IMP_WAIT = 10000


class Chat:
    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument('--window-size=1920,1080')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(IMP_WAIT)

        self.driver.get("https://yandex.ru/search/?text=Hello World")
        self.driver.find_element(
            By.CSS_SELECTOR, "div[class='VanillaReact AliceFabPromo AliceFabPromo_shown']"
        ).click()

        # checking that browser render site
        self.driver.find_elements(By.CSS_SELECTOR, 'div[class*="alice__suggest alice__suggest"]')

    def send_message(self, message):
        inp = self.driver.find_element(
            By.CSS_SELECTOR, 'div[class*="input-container__text-input"]'
        )
        inp.send_keys(message)

        self.driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Отправить запрос Алисе"]'
        ).click()

    def get_answer(self):
        self.driver.find_elements(
            By.CSS_SELECTOR, 'div[class*="alice__suggest alice__suggest"]'
        )
        chat = self.driver.find_element(By.CSS_SELECTOR, "div[class*='chat svelte-']")
        return html2text.html2text(
            chat.find_elements(By.CSS_SELECTOR, "div")[-2].get_attribute("outerHTML")
        ).rstrip("\n")

    def close(self):
        self.driver.quit()
