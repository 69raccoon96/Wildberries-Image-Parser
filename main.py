import undetected_chromedriver
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
import time


class Options(ChromeOptions):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headless: bool = False


# Paste here yor search request
search = "вентиляторы напольные"
driver = undetected_chromedriver.Chrome(options=Options())
driver.get('https://www.wildberries.ru/catalog/0/search.aspx?search=' + '%20'.join(search.split()))
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
links = soup.find_all('a', {'class': 'product-card__link'})
script = '''let showMoreButton;
let awaitCommentInterval = setInterval(() => {
    showMoreButton = document.querySelector('div.j-show-more-slide');
    if(showMoreButton){
        clearInterval(awaitCommentInterval);
        document.querySelector('div.j-show-more-slide').click();
        let scrollBottomInterval = setInterval(() => {
            let block = document.querySelector('div.j-feedbacks-popup');
            block.scrollTop = block.scrollHeight;
            if(block.scrollTop === block.scrollHeight) {
                clearInterval(scrollBottomInterval)
            }
        },1000)
    }
}, 100)'''
for link in links:
    href = link.get('href')
    driver.get(href)
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 1300);")
    time.sleep(5)
    element = driver.find_element("class name", "user-activity__tabs-wrap")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, -100);")
    time.sleep(1)
    while True:
        current = driver.find_elements("class name", "swiper-button-next")
        if len(current) == 0:
            break
        attribute = current[2].get_attribute("class")
        if attribute == 'swiper-button-next swiper-button-disabled':
            break
        current[2].click()
        time.sleep(2)

    element = driver.find_elements("css selector", '.img-plug.j-show-more-slide')
    if len(element) == 0:
        continue
    element[0].click()
    time.sleep(2)
    driver.execute_script(script)
    time.sleep(30)

    root = driver.page_source
    soup = BeautifulSoup(root)
    prettyHTML = soup.prettify()
    catalog_number = href.split("/")[-2]
    f = open(catalog_number + ".html", "a", encoding="utf-8")
    f.write(prettyHTML)
    f.close()
