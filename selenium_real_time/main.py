from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
import pyperclip
import keyboard
import pyautogui
# from selenium.webdriver import Keys
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



TARGET_URLS = {
    'dictation_url': 'https://speechnotes.co/dictate/',
    'grammar_url': 'https://www.deepl.com/write'
}

XPATH_LIBRARY = {
    'record_button': '//div[@id="start_button"]',
    'text_area': '//div[@id="output_box"]/textarea',
    'text_mirror': '//div[@id="mirror_container"]//div',
    'grammar_text_area': 'd-textarea',
}


def manage_webdriver():
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    ChromeDriverManager().install()


#  undetectable driver
# def create_driver():
#     import undetected_chromedriver as uc
#
#     manage_webdriver()
#
#     options = uc.ChromeOptions()
#     options.headless = True
#     options.add_argument('--headless=new')
#     options.add_argument("--no-default-browser-check")
#     options.add_argument('--no-sandbox')
#     options.add_argument("--start-maximized")
#     options.add_experimental_option("prefs", {
#         "profile.default_content_setting_values.media_stream_mic": 2
#     })
#
#     driver = uc.Chrome(options=options)
#
#     print('driver created')
#
#     return driver


def grant_permissions(d):
    d.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": TARGET_URLS['dictation_url'],
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )


def record_and_paste(d):

    # start recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    text = get_text(d)

    paste_text(text)

    # stop recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    # print_grammar_correction(d, text)


def print_grammar_correction(d, text):

    # open grammar page
    d.get(TARGET_URLS['grammar_url'])

    # paste text
    d.find_element(By.XPATH, '//textarea').send_keys(text)

    # wait for grammar correction
    sleep(1)

    # get corrected text
    corrected_text = d.find_element(By.XPATH, '//textarea').text

    # paste corrected text
    paste_text(corrected_text)

    # go back to dictation page
    d.get(TARGET_URLS['dictation_url'])


def get_text(d):
    tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
    wait_until_started_to_change(d, XPATH_LIBRARY['text_mirror'])
    text_chain = []

    while True:

        sleep(0.1)
        tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
        text_chain.append(tm.text)

        if tm.text == '':  # when input recording ends, it sets to ''
            # the last normally is '' -> [-2], unless only one word is said [-1]
            try:
                return text_chain[-2]
            except:
                return text_chain[-1]


def wait_until_started_to_change(d, xpath_element):
    n = 0
    while True:
        sleep(0.1)
        n += 1
        element = d.find_element(By.XPATH, xpath_element)
        if element.text != '':
            return
        elif n > 70:
            print('element not changed after ' + str(n) + ' iterations')
            return


def paste_text(text):
    # copy old clipboard to avoid the user from having the same text twice when pasting
    old_clipboard = pyperclip.paste()

    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

    pyperclip.copy(old_clipboard)


def close_driver(d):
    d.close()
    d.quit()


def open_tabs(d):
    d.execute_script("window.open('');")
    d.switch_to.window(d.window_handles[1])
    d.get(TARGET_URLS['grammar_url'])
    d.switch_to.window(d.window_handles[0])



def print_help():
    print(f'''This is a python selenium refresher: 
          d.get("https://en.wikipedia.org/wiki/Main_Page") 
          //tag[contains(@attribute, 'substring')]
          //div[contains(text(), 'Google')]"# actions = ActionChains(d)
            actions.send_keys(Keys.ENTER).perform()
            d.switch_to.active_element
            with open('f2.txt', 'w', encoding="utf-8") as f: f.write(d.page_source)
          
          How to use: 
          --f for find_element(By.XPATH, '//button')
          ie: --f target_xpath -> e = find_element(By.XPATH, '//target_xpath')
          --fs for find_elementS(By.XPATH, '//button'
          driver.find_elements(By.XPATH, '//button')
          
            
          ''')


def create_uc_driver():
    import undetected_chromedriver as uc

    driver = uc.Chrome(headless=False, use_subprocess=False)

    return driver


def create_normal_driver():
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.chrome.service import Service

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  #, options=chrome_options)
    return driver


def get_target_url(d, target_url):
    d.get(target_url)


def read_user_input():
    return input("Enter function to run, q for exit, h for help: ")


def execute_func(func):

    try:
        print("executing: " + func + "\n")
        exec(func, globals())  # globals used to allow to assign variables
    except Exception as e:
        print("\n" + str(e) + "\n")
        pass


def function_parser(func):

    if func.lower() in ("quit", "q", "exit"):
        return 'q'
    if func.lower() in ("help", "h"):
        print_help()
        return 'continue'

    # common function layout
    # if '--f' or '-f' in func.lower():
    #     try:
    #         xpath = func.split(' ')[1]
    #         func = f"d.find_element(By.XPATH, '{xpath}')"
    #
    #         print("\n xpath is: " + xpath, "\n", "function is: " + func + "\n")
    #
    #         return func
    #
    #     except Exception as e:
    #         print(e)
    #         pass

    return func


def execution_wheel(d):

    while True:

        function_to_execute = read_user_input()

        r = function_parser(function_to_execute)
        if r == 'q':  # if user input is q, exit
            break
        elif r == 'continue':
            continue

        execute_func(r)


def grant_permissions():
    d.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": TARGET_URLS['dictation_url'],   # e.g https://www.google.com
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )


def open_second_tab(d):
    d.execute_script(f'''window.open("{TARGET_URLS['grammar_url']}","_blank");''')


# works well only when there are only 2 tabs present
def switch_tabs(d):
    current_tab = d.current_window_handle

    # check all the tabs, switch to the one that differs from the current tab
    for tab in d.window_handles:
        if tab != current_tab:
            d.switch_to.window(tab)


def print_grammar_correction(text):
    switch_tabs(d)

    # clean old input text

    # send text
    # include xpath in path library Json
    d.find_element(By.XPATH, '//d-textarea[contains(@class, "lmt__source_textarea")]').send_keys(text)

    sleep(1.5)

    # copy text
    d.find_element(By.XPATH, '//d-textarea[contains(@class, "lmt__textarea lmt__target_textarea")]').click()


def run():
    global d  # used to allow to assign variables in exec()
    # d = create_uc_driver()
    d = create_normal_driver()

    get_target_url(d, TARGET_URLS['dictation_url'])
    open_second_tab(d)

    grant_permissions()  # microphone, geo location, camera

    execution_wheel(d)


if __name__ == '__main__':
    run()

