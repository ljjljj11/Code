import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


NAVER_URL = 'https://www.naver.com/'
NAVER_MAIL_URL = 'https://mail.naver.com/'


def open_driver() -> webdriver.Chrome:
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    return driver


def manual_login(driver: webdriver.Chrome) -> bool:
    driver.get(NAVER_URL)

    try:
        login_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='account']//a[contains(text(), '로그인')]"))
        )
        login_link.click()
    except Exception:
        pass

    print('브라우저에서 직접 로그인하세요. 로그인 완료 후 콘솔에서 Enter를 누르세요.')
    try:
        input()
    except EOFError:
        pass

    try:
        driver.get(NAVER_URL)
        time.sleep(1)
        driver.get(NAVER_MAIL_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        return True
    except Exception:
        return False


def get_mail_titles(driver: webdriver.Chrome) -> list[str]:
    driver.get(NAVER_MAIL_URL)
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except Exception:
        return []

    selectors = [
        (By.CLASS_NAME, 'mail_title'),
        (By.CSS_SELECTOR, 'a.subject'),
        (By.CSS_SELECTOR, 'strong.mail_title'),
        (By.CSS_SELECTOR, 'span.mail_title'),
        (By.CSS_SELECTOR, 'div.subject a'),
    ]

    titles: list[str] = []
    for by, sel in selectors:
        try:
            elements = driver.find_elements(by, sel)
        except Exception:
            elements = []
        if elements:
            for el in elements:
                title = _clean_mail_block_text(el.text)
                if title:
                    titles.append(title)
            if titles:
                break
    return titles


def _clean_mail_block_text(raw: str) -> str:
    if not raw:
        return ''
    lines = [ln.strip() for ln in raw.splitlines() if ln and ln.strip()]
    noise_keys = {'메일제목', '메일본문미리보기열기', '새창으로메일보기'}
    for ln in lines:
        compact = ''.join(ln.split())
        if compact in noise_keys:
            continue
        return ln
    return ''


def main() -> None:
    try:
        driver = open_driver()
    except Exception as exc:
        print('웹드라이버 실행 실패:', exc)
        sys.exit(1)

    try:
        if not manual_login(driver):
            print('로그인 확인 실패')
            sys.exit(1)

        items = get_mail_titles(driver)
        print(items)
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == '__main__':
    main() 
    