import time, sys, random, re, base64
from selenium import webdriver
# Chrome: https://github.com/SergeyPirogov/webdriver_manager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# Identify DOM elements By.ID, By.XPATH, ...
from selenium.webdriver.common.by import By
# Wait for DOM elements to appear/be visible
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Most common user agents: https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
def init_driver(defaultUseragent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'):
    # Chrome options
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless') # Headless, activate to hide browser window from interrupting your normal work
    options.add_argument('--accept-lang=en_US')
    #options.add_argument('--proxy-server=socks5://127.0.0.1:1080')
    options.add_argument('--user-agent=' + defaultUseragent)
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    return driver

def main():
    driver = init_driver()

    driver.get('file:///home/<username>/PSMA/src/meter/01_zxcvbn/index.html')
    delay = 5 # seconds

    try:
        pass_field = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'password'))) #presence_of_element_located
    except TimeoutException:
        print(f"Error: Element with id='password' was not found within {delay} seconds.")

    try:
        submit_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'submit'))) #presence_of_element_located
    except TimeoutException:
        print(f"Error: Element with id='submit' was not found within {delay} seconds.")

    fog = open("./"+str(sys.argv[1].split('/')[-1])+"_guess_number_result.txt", "w", encoding="utf-8")
    fog.write("zxcvbn_guess_number_"+str(sys.argv[1].split('/')[-1])+"\n")
    fos = open("./"+str(sys.argv[1].split('/')[-1])+"_score_result.txt", "w", encoding="utf-8")
    fos.write("zxcvbn_score_"+str(sys.argv[1].split('/')[-1])+"\n")
    with open(str(sys.argv[1]), "r", encoding="utf-8") as inputfile:
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
                print(f"Error: Element with id='guess_number' was not found within {delay} seconds.")
            guess_number = guess_number_field.get_attribute("innerHTML")
            score = "-1.0"
            try:
                score_field = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'score'))) #presence_of_element_located
            except TimeoutException:
                print(f"Error: Element with id='score' was not found within {delay} seconds.")
            score = score_field.get_attribute("innerHTML")
            # Print result to stdout
            print(f"{score}\t{guess_number}\t{line}")
            # Write result to file
            fog.write(f"{guess_number}\n")
            fos.write(f"{score}\n")
            pass_field.clear() # reset
            fog.flush()
            fos.flush()

    fog.close()
    fos.close()
    driver.quit()

if __name__ == "__main__":
    main()
