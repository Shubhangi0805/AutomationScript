from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

username = "username"
password = "password"

default_options = ["--disable-extensions", "--disable-user-media-security=true",
                   "--allow-file-access-from-files", "--use-fake-device-for-media-stream",
                   "--use-fake-ui-for-media-stream", "--disable-popup-blocking",
                   "--disable-infobars", "--enable-usermedia-screen-capturing",
                   "--disable-dev-shm-usage", "--no-sandbox",
                   "--auto-select-desktop-capture-source=Screen 1",
                   "--disable-blink-features=AutomationControlled",
                   "--ignore-certificate-errors", "--ignore-ssl-errors"]

headless_options = ["--headless", "--use-system-clipboard", "--window-size=1920x1080"]

def browser_options(chrome_type):
    webdriver_options = webdriver.ChromeOptions()
    notification_opt = {"profile.default_content_setting_values.notifications": 1}
    webdriver_options.add_experimental_option("prefs", notification_opt)
    if chrome_type == "headless":
        var = default_options + headless_options
    else:
        var = default_options
    for d_o in var:
        webdriver_options.add_argument(d_o)
    return webdriver_options

def get_webdriver_instance(browser=None):
    base_url = "https://accounts.teachmint.com/"
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    driver = Chrome(service=ChromeService(ChromeDriverManager().install()), options=browser_options(browser))
    driver.maximize_window()
    driver.get(base_url)
    return driver

def enter_phone_number_otp(driver, creds):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))).send_keys(creds[0])
        time.sleep(1)
        print("Entered user phone number {}".format(creds[0]))
        driver.find_element(By.ID, "send-otp-btn-id").click()
        WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
        WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
        time.sleep(1)
        _input_otp_field = "//input[@data-group-idx='{}']"
        for i, otp in enumerate(creds[1]):
            otp_field = _input_otp_field.format(str(i))
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, otp_field))).send_keys(otp)
            print("Entered OTP {}".format(creds[1]))
        time.sleep(1)
        driver.find_element(By.ID, "submit-otp-btn-id").click()
        time.sleep(2)

        # Handle the "Skip password creation" step if the element exists
        try:
            skip_password_creation = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@onclick='onSkipPassCreationClick()']"))
            )
            skip_password_creation.click()
            WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
            WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
            time.sleep(1)
            print("Successfully skipped password creation")
        except:
            print("Skip password creation element not found, continuing without skipping")
    except Exception as e:
        print(f"Error in enter_phone_number_otp: {e}")
        driver.quit()

def login(admin_credentials=["0000020232", "120992", "@Automation-2"], account_name="@Automation-2"):
    try:
        driver = get_webdriver_instance()
        WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
        WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
        time.sleep(1)
        enter_phone_number_otp(driver, admin_credentials)
        user_name = "//div[@class='profile-user-name']/..//div[text()='" + account_name + "']"
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, user_name)))
        driver.find_element(By.XPATH, user_name).click()
        dashboard_xpath = "//a[text()='Dashboard']"
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, dashboard_xpath)))
        time.sleep(20)
        driver.refresh()
        time.sleep(20)
        return driver
    except Exception as e:
        print(f"Error in login: {e}")
        driver.quit()


def navigate_to_generate_certificate(driver):
    try:
        # Store the current window handle
        main_window_handle = driver.current_window_handle
    
        # Find Quick Actions element
        quick_actions_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]"
        quick_actions_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, quick_actions_xpath)))

        # Click on Quick Actions
        quick_actions_element.click()

        print("Successfully clicked on Quick Actions.")

        # Find "Generate Certificate" option within Quick Actions menu
        generate_certificate_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[11]/a/span"
        generate_certificate_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, generate_certificate_xpath)))

        # Click on "Generate Certificate" option
        generate_certificate_element.click()

        print("Successfully clicked on Generate Certificate in Quick Actions.")
        time.sleep(2)

        # After clicking on Generate Certificate, click on 'School leaving certificate'
        school_leaving_certificate_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/div[4]/div[2]/div[3]/div[1]/div"
        school_leaving_certificate_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, school_leaving_certificate_xpath)))

        # Click on 'School leaving certificate'
        school_leaving_certificate_element.click()

        print("Successfully clicked on School leaving certificate.")
        time.sleep(2)

        # After clicking on "School leaving certificate", click on "Generate" button
        generate_button_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/div[1]/div/div[3]/div[2]/div[2]/button[2]"
        generate_button_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, generate_button_xpath)))

        # Click on "Generate" button
        generate_button_element.click()

        print("Successfully clicked on Generate button.")
        time.sleep(2)

        # After clicking on Generate button, search and select the student
        search_student_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div/div/input"
        search_student_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, search_student_xpath)))
        search_by_name = "Sam"
        

        # Click to select the student
        search_student_element.click()

        print("Successfully selected the student.")
        time.sleep(2)

        # Now, click on Generate
        generate_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div[3]/div[1]/div/table/tbody/tr/td[4]/button/div"
        generate_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, generate_xpath)))

        # Click on Generate
        generate_element.click()

         # After clicking on Generate button, update remarks
        update_remarks_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[2]"
        update_remarks_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, update_remarks_xpath)))

        # Click on the update remarks element
        update_remarks_element.click()

        print("Successfully clicked on Update Remarks.")
        time.sleep(2)

        
        # Find and click on the Generate button
        generate_button_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/footer/div/button"
        generate_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, generate_button_xpath)))

        generate_button.click()

        print("Successfully clicked on Generate button.")
        time.sleep(2)
        
        # Find and click on the Download button
        download_button_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div[1]/div/div[3]/button[2]/div"
        download_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, download_button_xpath)))

        download_button.click()

        print("Successfully clicked on Download button.")
        time.sleep(2)
        # Loop through all open tabs and close the one with the desired URL
        for handle in driver.window_handles:
           driver.switch_to.window(handle)
           if driver.current_url == "https://teachmint.storage.googleapis.com/":  # Replace with the actual URL
              driver.close()
              break
        # Switch back to the main window
        driver.switch_to.window(main_window_handle)
        print("Successfully switched back to the main window.")
        time.sleep(2)

        # Find and click on Certificates and Downloads button
        certificates_and_downloads_button_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div[1]/div[1]/span[1]/p/a"
        certificates_and_downloads_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, certificates_and_downloads_button_xpath)))

        certificates_and_downloads_button.click()

        print("Successfully clicked on Certificates and Downloads button.")
        time.sleep(2)

        # Find and click on View All button
        view_all_button_xpath = "/html/body/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/div[5]/span"
        view_all_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, view_all_button_xpath)))

        view_all_button.click()

        print("Successfully clicked on View All button.")
        time.sleep(2)
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout waiting for element: {e}")
    except Exception as e:
        print(f"Error updating remarks: {e}")
        raise

def main():
    try:
        driver = login()
        navigate_to_generate_certificate(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Start")
    main()
    print("End")