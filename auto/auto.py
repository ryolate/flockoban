import sys
import time
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

DIV = "html_embed_widget_69675"


def push_key(driver: webdriver.Chrome, c: str):
    webdriver.ActionChains(driver).send_keys(c * 200).perform()
    time.sleep(0.1)


MAPPING = {
    '→': 'd',
    '↓': 's',
    '←': 'a',
    '↑': 'w',
}


def solve(moves: str):
    keys = "".join(map(lambda x: MAPPING[x], moves)) + 's'

    opt = webdriver.ChromeOptions()
    opt.debugger_address = "localhost:9222"
    driver = webdriver.Chrome(options=opt)

    if not driver.title.startswith("Flockoban"):
        print("Open flockoban page and try again.", file=sys.stderr)
        exit(1)

    d: WebElement = driver.find_element_by_id(DIV)
    print(f"id: {d.id}, {d.get_attribute('class')}")

    webdriver.ActionChains(driver).move_to_element(d).perform()
    time.sleep(0.1)
    d.click()

    # reset
    push_key(driver, "r")
    time.sleep(2)

    for c in keys:
        push_key(driver, c)

    driver.quit()


def main():
    solve(input())


if __name__ == "__main__":
    main()
