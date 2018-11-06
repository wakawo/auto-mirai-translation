from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import os, pdb, re, sys, argparse, shutil


def arg_parse():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
                        prog="main.py", 
                        usage="main.py -i input_file -o --output_file", 
                        add_help = True 
                        )

    parser.add_argument("-i", "--input_path", 
                        help = "Input file name.",
                        type = str,
                        required = True)

    parser.add_argument("-o", "--output_dir",
                        help = "Output dir path",
                        type = str,
                        default = "output/")
    
    args = parser.parse_args()
    return args


def formatter(input_path, output_path):
    pattern = r"^Abstract$|^\d\..*$"
    first = True

    with open(output_path, mode='w') as f:
        pass

    with open(output_path, mode='a') as out_file:
        with open(input_path) as in_file:
            for in_line in in_file:
                if re.match(pattern, in_line):
                    if(first):
                        first = False
                        out_file.write(in_line)
                    else:    
                        out_file.write('\n'+in_line)
                else:
                    out_file.write(in_line.replace('\n', ' '))
            out_file.write('\n')


def get_translated_text(driver, origin_text):
    driver.find_element_by_id('translateSourceInput').send_keys(origin_text)
    sleep(3)
    driver.find_element_by_id('translateButtonTextTranslation').click()
    sleep(3)
    translation = driver.find_element_by_id('translate-text')
    sleep(3)
    driver.find_element_by_id('translateSourceInput').clear()
    return translation.text


def main():
    args = arg_parse() 

    try:
        new_dir_path = args.output_dir + '/' + args.input_path.rsplit('/')[-1].split('.')[0]
        os.mkdir(new_dir_path)
        origin_path = new_dir_path + '/origin.txt'
        formatted_path = new_dir_path + '/formatted.txt'
        translated_path = new_dir_path + '/translated.txt'
    except:
        print("Make dirctory error.")
        raise()

    shutil.copy(args.input_path, origin_path)
    formatter(input_path=args.input_path, output_path=formatted_path)

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

    with open(formatted_path) as f:
        all_text = f.read()
        matched_list = re.findall(pattern, all_text)
        for before in matched_list:
            after = get_translated_text(driver, before+'.')
            translated_list.append(after)
        
    with open(translated_path, mode='w') as f:
        f.write(' '.join(translated_list))

    driver.close()

if __name__=='__main__':
    main()
