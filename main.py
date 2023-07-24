

def test_driver():
    import undetected_chromedriver as uc
    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get('https://nowsecure.nl')
    driver.save_screenshot('nowsecure.png')


def read_user_input():
    return input("Enter function to run: ")


def execute_func(func):
    print("Executing function: " + func)
    # exec(func)


def run():
    func_to_execute = read_user_input()
    execute_func(func_to_execute)


if __name__ == '__main__':
    run()

