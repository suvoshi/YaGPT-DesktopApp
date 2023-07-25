from selenium import webdriver
from selenium.webdriver.common.by import By
import html2text
from fake_headers import Headers
import time
import json
from random import choice

IMP_WAIT = 120


def get_promt():
    with open("./promts.json", "r") as file:
        promts = json.load(file)["main"]

    return choice(promts)


class Chat:
    def __init__(self):
        options = webdriver.FirefoxOptions()
        firefoxprofile = webdriver.FirefoxProfile()
        firefoxprofile.set_preference("media.volume_scale", "0.0")
        options.add_argument("--headless")
        options.profile = firefoxprofile

        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(IMP_WAIT)

        self.driver.get("https://yandex.ru/search/?text={}".format(get_promt()))

        time.sleep(2)

        # find element and wait till render
        button = self.driver.find_element(
            By.CSS_SELECTOR,
            "div[class='VanillaReact AliceFabPromo AliceFabPromo_shown']",
        )

        time.sleep(1)

        button.click()

        # checking that browser render site
        self.driver.find_elements(
            By.CSS_SELECTOR, 'div[class*="alice__suggest alice__suggest"]'
        )

    def send_message(self, message):
        inp = self.driver.find_element(
            By.CSS_SELECTOR, 'div[class*="input-container__text-input"]'
        )
        inp.send_keys(message)

        time.sleep(1)

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
