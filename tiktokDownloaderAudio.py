from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

from time import sleep

def download_audio(url: str, filename: str = "audio.mp3") -> bool:
    """download audio from TikTok. Returns True on success"""
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
    options.set_preference("dom.webdriver.enabled", False)
    options.add_argument("--headless")
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get("https://musicaldown.com/ru/tiktok-mp3")
    sleep(3)
    inputField = driver.find_element(
        By.ID, 'link_url'
    )
    inputField.send_keys(url)
    sleep(1)
    button = driver.find_elements(By.XPATH, "//button[@class='btn waves-effect waves-light orange']")
    button[0].click()
    sleep(3)
    audio_element = driver.find_elements(By.XPATH, "//source")
    if len(audio_element) == 0:
        driver.quit()
        return False
    audio = audio_element[0]
    src = audio.get_attribute('src')
    driver.quit()
    audio_data = requests.get(src)
    with open(filename, "wb") as file:
        file.write(audio_data.content)
    return True