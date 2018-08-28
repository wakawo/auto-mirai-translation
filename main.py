from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import pdb, re, sys

def main():
    args = sys.argv
    input_path = args[1]
    if(input_path is None):
        print('Require input file.')
        sys.exit()
    pattern = r'([\s\S]{,490})\.'
    translated_list = []

    driver = webdriver.Chrome()
    driver.get('https://miraitranslate.com/trial/')

    driver.find_element_by_xpath('''
        //*[@id="tab-box"]/div/div[2]/div[1]/div[1]/div[1]/span/span[1]/span/span[2]/b
        ''').click()
    focused_elem = driver.switch_to.active_element
    focused_elem.send_keys('英語')
    focused_elem.send_keys(Keys.ENTER)

    with open(input_path) as f:
        all_text = f.read()
        matched_list = re.findall(pattern, all_text)
        for before in matched_list:
            after = get_translated_text(driver, before+'.')
            translated_list.append(after)
        
    with open('translated.txt', mode='w') as f:
        f.write(' '.join(translated_list))

    driver.close()

def get_translated_text(driver, origin_text):
    driver.find_element_by_id('translateSourceInput').send_keys(origin_text)
    sleep(3)
    driver.find_element_by_id('translateButtonTextTranslation').click()
    sleep(3)
    translation = driver.find_element_by_id('translate-text')
    sleep(3)
    driver.find_element_by_id('translateSourceInput').clear()
    return translation.text

if __name__=='__main__':
    main()