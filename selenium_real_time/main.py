from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


TARGET_URL = 'https://www.deepl.com/write#en/this%20is%20a%20test%20text'
XPATH_LIBRARY = {
    'accept_cookies_banner': '//*[@data-testid="cookie-banner-strict-accept-selected"]',
    'input_area': '(//p[@_d-id])[1]',
    'output_area': '(//p[@_d-id])[2]',
}


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


def create_driver():
    import undetected_chromedriver as uc

    driver = uc.Chrome(headless=False, use_subprocess=False)

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
            "origin": TARGET_URL    ,   # e.g https://www.google.com
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )






def run():
    global d  # used to allow to assign variables in exec()
    d = create_driver()

    get_target_url(d, TARGET_URL)

    #grant_permissions()  # microphone, geo location, camera

    execution_wheel(d)

if __name__ == '__main__':
    run()

