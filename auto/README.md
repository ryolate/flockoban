# Flockoban auto solver

Solves flockoban automatically using [ChromeDriver].
We support Chrome only.

[ChromeDriver]: https://chromedriver.chromium.org/home

## Set up

- Download [ChromeDriver]. Place it on your PATH.
- Run `pip install selenium`.

## How to

Run google chrome with remote debugging port.

- Mac: `open -a Google Chrome --args --remote-debugging-port=9222`
- Ubuntu: `google-chrome --remote-debugging-port=9222`

Run the program specifyping the debugging port address.

`cat 0820.ans | python auto.py localhost:9222`

## Development info

- [ChromeDriver]
- [Selenium Python API]

[Selenium Python API]: https://www.selenium.dev/selenium/docs/api/py/api.html
