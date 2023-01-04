import sys

logfile = "ldvlogs.log"
try:
    from loguru import logger
except Exception as e:
    print(e)
    print("You are missing loguru, please run pip3 install -r requirements.txt")
    with open(logfile, "a+") as f:
        f.write("You are missing loguru, please run pip3 install -r requirements.txt")
    exit()


logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<level>{level}</level>| <level>{message}</level>",
)
logger.add(
    logfile,
    rotation="200 MB",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
)
logger.debug("Running manual check...")

try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    # from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    import time
except Exception as e:
    logger.critical(
        "Missing package: " + str(e) + ", have you installed the requirements?"
    )
    exit(0)

try:
    from config import email,password
except Exception as e:
    logger.critical("Couldn't load configuration, have you filled up the ./config.py ?")
    raise e

@logger.catch
def main():
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get("https://www.leonard-de-vinci.net/")
    time.sleep(2)

    logger.debug("Headless Firefox Initialized")
    # driver.quit()
    logger.debug(f"Trying to login with {email}")
    driver.find_element(By.NAME, "login").send_keys(email)
    driver.find_element(By.ID, "btn_next").click()
    time.sleep(2)
    logger.debug("Inputing password...")
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    time.sleep(2)
    logger.success("Logged in!")
    driver.get("https://www.leonard-de-vinci.net/student/presences/")
    time.sleep(2)

    body_presences = driver.find_element(By.ID, "body_presences")
    if body_presences:
        classes_row = body_presences.find_elements(By.TAG_NAME, "tr")
        for class_row in classes_row:
            if class_row.get_attribute("class") == "warning":
                logger.debug("Found class with warning tag, clicking on it")
                class_row.find_elements(By.TAG_NAME, "td")[3].click()
                time.sleep(2)
                try:
                    logger.debug("Trying to click on set-pres btn")
                    presence_btn = driver.find_element(By.ID, "set-presence")
                    if presence_btn:
                        presence_btn.click()
                        logger.success("Clicked on button!")
                        exit()
                except Exception as e:
                    logger.success("No presence button found: presence already set!")
                    exit()
        logger.success("No courses require presence at the moment!")
    else:
        logger.success("No classes today!")
    exit()



if __name__ == "__main__":
    main()
