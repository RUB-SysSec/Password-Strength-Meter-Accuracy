import time, sys, random, re, base64
from selenium import webdriver
# Firefox: https://github.com/SergeyPirogov/webdriver_manager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# Identify DOM elements By.ID, By.XPATH, ...
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Clearing the pass_field on Twitch does not work with clear()
# Wait for DOM elements to appear/be visible
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Most common user agents: https://www.whatismybrowser.com/guides/the-latest-user-agent/firefox
def init_driver(defaultUseragent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0'):
    # Firefox options
    options = webdriver.FirefoxOptions()
    #options.add_argument('-headless') # Headless, activate to hide browser window from interrupting your normal work
    options.set_preference('intl.accept_languages', 'en,en_US')
    #options.set_preference('network.proxy.type', 1)
    #options.set_preference('network.proxy.socks', '127.0.0.1')
    #options.set_preference('network.proxy.socks_port', 1080)
    #options.set_preference('network.proxy.socks_remote_dns', True)
    options.set_preference('general.useragent.override', defaultUseragent)
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    driver.set_window_size(1920, 1080)
    return driver

def main():
    driver = init_driver()

    driver.get('https://www.twitch.tv/signup')
    delay = 5 # seconds

    try:
        pass_field = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'password-input'))) #presence_of_element_located
    except TimeoutException:
        print(f"Error: Element with id='password-input' was not found within {delay} seconds.")

    fob = open("./"+str(sys.argv[1].split('/')[-1])+"_bar_result.txt", "w", encoding="utf-8")
    fob.write("twitch_bar_"+str(sys.argv[1].split('/')[-1])+"\n")
    fos = open("./"+str(sys.argv[1].split('/')[-1])+"_strength_result.txt", "w", encoding="utf-8")
    fos.write("twitch_strength_"+str(sys.argv[1].split('/')[-1])+"\n")
    fot = open("./"+str(sys.argv[1].split('/')[-1])+"_text_result.txt", "w", encoding="utf-8")
    fot.write("twitch_text_"+str(sys.argv[1].split('/')[-1])+"\n")
    with open(str(sys.argv[1]), "r", encoding="utf-8") as inputfile:
        inputfile.readline() # skip header
        for line in inputfile:
            line = line.rstrip('\r\n')
            # Send new password to evaluate
            pass_field.send_keys(line)
            time.sleep(2.0) # Some Ajax meters require some processing time
            # Search for result on page
            bar = "-1.0"
            try:
                bar_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'tw-progress-bar'))) #presence_of_element_located
                bar = bar_field.get_attribute("aria-valuenow")
            except TimeoutException:
                print(f"Error: Element with class='tw-progress-bar' was not found within 1 second.")
            strength = "-1.0"
            try:
                strength_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "password-indicator password-indicator")]/div[2]/p'))) #presence_of_element_located
                strength = strength_field.get_attribute("innerHTML")
            except TimeoutException:
                print(f"Error: Element strength_field was not found within 1 second.")
            text = "-1.0"
            try:
                text_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "form-group-auth__animated-text")]/div/div/p'))) #presence_of_element_located
                text = text_field.get_attribute("innerHTML")
            except TimeoutException:
                print(f"Error: Element text_field was not found within 1 second.")
            # Print result to stdout
            print(f"{bar}\t{strength}\t{text}\t{line}")
            # Write result to file
            fob.write(f"{bar}\n")
            fos.write(f"{strength}\n")
            fot.write(f"{text}\n")
            #pass_field.clear() # reset
            pass_field.send_keys(Keys.CONTROL + "a")
            pass_field.send_keys(Keys.DELETE)
            fob.flush()
            fos.flush()
            fot.flush()
    fob.close()
    fos.close()
    fot.close()
    driver.quit()

if __name__ == "__main__":
    main()
