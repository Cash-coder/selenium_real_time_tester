from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


def click(d, xpath):
    wait = WebDriverWait(d, 6)

    # target = wait.until(
    # EC.presence_of_element_located((By.XPATH, xpath)))
    # EC.element_to_be_clickable((By.XPATH, xpath)))
    try:
        # this avoids error: element click intercepted ... Other element would receive the click:
        # select highest level xpath: div inside a header, select header
        target = wait.until(EC.visibility_of_element_located((By.XPATH , xpath)))
        target.click()

        # ADVICE: sometimes you can avoid interception error
        # by sending key RETURN instead of clicking d.xpath.send_keys(Keys.RETURN)

        # Action chains has little accuracy, lots of mistakes clicking in the wrong plage
        # actions = ActionChains(d)
        # actions.move_to_element(target).click().perform()
        # print('clicked')

        sleep(0.5)

        try:
            d.switch_to.active_element
        except Exception as e:
            # print(e)
            print("can't switch to active element")
    except Exception as e:
        print(f"---Can't click this xpath: {xpath}")
        print(e)
