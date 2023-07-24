from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


TARGET_URL = 'https://speechnotes.co/dictate/'
XPATH_LIBRARY = {
    'record_button': '//div[@id="start_button"]'
}



def print_help():
    print(f'''This is a python selenium refresher: \n
          d.get("https://en.wikipedia.org/wiki/Main_Page") \n
          //tag[contains(@attribute, 'substring')]
          //div[contains(text(), 'Google')]"
          
          How to use: \n
          --f for find_element(By.XPATH, '//button')
          ie: --f target_xpath -> e = find_element(By.XPATH, '//target_xpath')\n
          --fs for find_elementS(By.XPATH, '//button'
          driver.find_elements(By.XPATH, '//button')
          
          \n   
          ''')


def create_driver():
    import undetected_chromedriver as uc

    # opt = Options()
    # opt.add_argument("start-maximized")
    # opt.add_argument("--disable-extensions")
    # opt.add_experimental_option("prefs", {
    #     "profile.default_content_setting_values.media_stream_mic": 1,
    #     "profile.default_content_setting_values.media_stream_camera": 1,
    #     "profile.default_content_setting_values.geolocation": 1,
    #     "profile.default_content_setting_values.notifications": 1
    # })

    chrome_options = uc.ChromeOptions()
    prefs = {"profile.default_content_setting_values.media_stream_mic" : 1}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = uc.Chrome(headless=False, use_subprocess=False,chrome_options=chrome_options)

    # driver = uc.Chrome(headless=False, use_subprocess=False, desired_capabilities=desired_cap)

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


def test_func():
    d.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": TARGET_URL    ,   # e.g https://www.google.com
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )


    # e.send_keys(Keys.ENTER)
    # d.switch_to.active_element
    # d.switch_to.active_el

# common funcs
# actions = ActionChains(d)
# actions.send_keys(Keys.ENTER).perform()
# d.switch_to.active_element
# with open('f2.txt', 'w', encoding="utf-8") as f: f.write(d.page_source)


def run():
    global d  # used to allow to assign variables in exec()
    d = create_driver()

    get_target_url(d, TARGET_URL)

    test_func()
    execution_wheel(d)

if __name__ == '__main__':
    run()

