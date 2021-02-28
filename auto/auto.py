import sys
import time
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

DIV = "html_embed_widget_69675"


MAPPING = {
    '→': 'd',
    '↓': 's',
    '←': 'a',
    '↑': 'w',
}


class Client:
    def __init__(self):
        opt = webdriver.ChromeOptions()
        opt.debugger_address = "localhost:9222"
        self.driver = webdriver.Chrome(options=opt)

        if not self.driver.title.startswith("Flockoban"):
            print("Open flockoban page and try again.", file=sys.stderr)
            exit(1)

        self.game: WebElement = self.driver.find_element_by_id(DIV)

        webdriver.ActionChains(self.driver).move_to_element(
            self.game).perform()
        time.sleep(0.1)
        self.game.click()

    def push_key(self, c: str):
        webdriver.ActionChains(self.driver).send_keys(c * 200).perform()
        time.sleep(0.1)

    def solve(self, moves: str):
        keys = "".join(map(lambda x: MAPPING[x], moves)) + 's'

        # reset
        self.push_key("r")
        time.sleep(2)

        for c in keys:
            self.push_key(c)

    def close(self):
        self.driver.quit()


def main():
    cl = Client()

    cl.solve(input())
    cl.close()


if __name__ == "__main__":
    main()
