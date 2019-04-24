import time, sys, random, re, base64
from selenium import webdriver
# Identify DOM elements By.ID, By.XPATH, ...
from selenium.webdriver.common.by import By
# Wait for DOM elements to appear/be visible
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Most common user agents: https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
def init_driver(defaultUseragent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'):
    # Firefox options
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from selenium.webdriver.firefox.options import Options
    binary = FirefoxBinary('/usr/bin/firefox') # Change to your needs
    options = Options()
    #options.headless = True  # Headless, activate to hide browser window from interrupting your normal work
    profile = webdriver.FirefoxProfile()
    profile.set_preference("intl.accept_languages", 'en,en_US')
    #profile.set_preference("network.proxy.type", 1)
    #profile.set_preference("network.proxy.socks", "127.0.0.1")
    #profile.set_preference("network.proxy.socks_port", 1080)
    #profile.set_preference("network.proxy.socks_version", 5)
    profile.set_preference("general.useragent.override", defaultUseragent)
    profile.update_preferences()
    driver = webdriver.Firefox(options=options, firefox_binary=binary, firefox_profile=profile)
    driver.set_window_size(1920, 1080)
    return driver

def main():
    driver = init_driver()

    driver.get('file:///home/<username>/PSMA/src/meter/01_zxcvbn/index.html')
    delay = 5 # seconds

    try:
        pass_field = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'password'))) #presence_of_element_located
    except TimeoutException:
        print("Error: Element with id='password' was not found within {} seconds.").format(delay)

    try:
        submit_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'submit'))) #presence_of_element_located
    except TimeoutException:
        print("Error: Element with id='submit' was not found within {} seconds.").format(delay)

    fog = open("./"+str(sys.argv[1].split('/')[-1])+"_guess_number_result.txt", "w")
    fog.write("{}\n".format("zxcvbn_guess_number_linkedin"))
    fos = open("./"+str(sys.argv[1].split('/')[-1])+"_score_result.txt", "w")
    fos.write("{}\n".format("zxcvbn_score_linkedin"))
    with open(str(sys.argv[1]),'rU') as inputfile:
        inputfile.readline() # skip header
        for line in inputfile:
            line = line.rstrip('\r\n')
            # Send new password to evaluate
            pass_field.send_keys(line)
            submit_button.click()
            #time.sleep(0.3) # Some Ajax meters require some processing time
            # Search for result on page
            guess_number = "-1.0"
            try:
                guess_number_field = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'guess_number'))) #presence_of_element_located
            except TimeoutException:
                print("Error: Element with id='guess_number' was not found within {} seconds.").format(delay)
            guess_number = guess_number_field.get_attribute("innerHTML")
            score = "-1.0"
            try:
                score_field = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'score'))) #presence_of_element_located
            except TimeoutException:
                print("Error: Element with id='score' was not found within {} seconds.").format(delay)
            score = score_field.get_attribute("innerHTML")
            # Print result to stdout
            print("{}\t{}\t{}".format(score, guess_number, line))
            # Write result to file
            fog.write("{}\n".format(guess_number))
            fos.write("{}\n".format(score))
            pass_field.clear() # reset
            fog.flush()
            fos.flush()

    fog.close()
    fos.close()
    driver.quit()

if __name__ == "__main__":
    main()
