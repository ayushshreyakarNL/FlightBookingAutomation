from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import NoSuchElementException

def book_flight(origin, destination, departure_date, return_trip, return_date, adults, child, infant, classType, filter, specialFare):


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Navigate to the travel website
    driver.get("https://www.yatra.com/?_ga=2.251687050.2094761562.1713764136-2038293306.1713251411")

    try:
        print("Waiting for page to load...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "booking_engine_modues")))
        print("Page loaded successfully.")

        # Find and fill out the origin field
        origin_input = driver.find_element(By.NAME, "flight_origin")
        origin_input.clear()
        origin_input.send_keys(origin)
        time.sleep(2)  # Adding a sleep to ensure the autocomplete options load
        origin_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{origin}')]")))
        origin_option.click()

        # Find and fill out the destination field
        destination_input = driver.find_element(By.NAME, "flight_destination")
        destination_input.clear()
        destination_input.send_keys(destination)

        # Wait until overlay disappears
        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "autocomplete-results")))

        # Click on the destination option
        destination_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{destination}')]")))

        # Scroll to the top of the page
        driver.execute_script("window.scrollTo(0, 0);")

        # Scroll to the destination option
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });", destination_option)

        # Click on the destination option
        ActionChains(driver).move_to_element(destination_option).click().perform()

        # Click on the departure date input field and select the date
        departure_date_input = driver.find_element(By.NAME, "flight_origin_date")
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });",
                              departure_date_input)

        # Click on the departure date input field
        departure_date_input.click()
        time.sleep(1)  # Wait for the datepicker to appear
        departure_date_element = driver.find_element(By.XPATH, f"//td[@data-date='{departure_date}']")
        departure_date_element.click()

        if return_trip == 'yes':
            departure_date_input = driver.find_element(By.NAME, "flight_destination_date")
            departure_date_input.click()
            time.sleep(1)  # Wait for the datepicker to appear
            departure_date_element = driver.find_element(By.XPATH, f"//td[@data-date='{return_date}']")
            departure_date_element.click()

        pax_info = driver.find_element(By.XPATH, "//div[@id='BE_flight_paxInfoBox']")
        pax_info.click()
        time.sleep(2)
        while adults > 1:
            buttonClick = driver.find_element(By.XPATH, "(//span[@class='ddSpinnerPlus'])[1]")
            buttonClick.click()
            time.sleep(2)
            adults = adults - 1
        time.sleep(2)

        while child > 0:
            childButtonClick = driver.find_element(By.XPATH, "(//span[@class='ddSpinnerPlus'])[2]")
            childButtonClick.click()
            time.sleep(2)
            child = child - 1
        time.sleep(2)

        while infant > 0:
            infantButtonClick = driver.find_element(By.XPATH, "(//span[@class='ddSpinnerPlus'])[3]")
            infantButtonClick.click()
            time.sleep(2)
            infant = infant - 1
        time.sleep(2)

        if classType == "Premium Economy":
            ClassClick = driver.find_element(By.XPATH, "(//span[@class='ddlabel'])[2]")
            ClassClick.click()

        if classType == "Business":
                ClassClick = driver.find_element(By.XPATH, "(//span[@class='ddlabel'])[3]")
                ClassClick.click()

        if filter == "Non Stop":
            check = driver.find_element(By.XPATH, "(//div[@class='filter-list'])")
            check.click()

        if specialFare == "Student Fare":
            check = driver.find_element(By.XPATH, "(//div[@id='specialFareContainer'])")
            check.click()
        if specialFare == "Armed Forces":
            check = driver.find_element(By.XPATH, "(//div[@id='armedforcesContainer'])")
            check.click()
        if specialFare == "Senior Citizen":
            check = driver.find_element(By.XPATH, "(//div[@id='seniorcitizenContainer'])")
            check.click()

        # Click on the search button using JavaScript
        search_button = driver.find_element(By.ID, "BE_flight_flsearch_btn")
        driver.execute_script("arguments[0].click();", search_button)

        print("Waiting for search results...")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "search-page")))
        print("Search results loaded successfully.")

        if return_trip == 'yes':

            # Wait for flight details element to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='wr-hr-center wr-width grid flex ']")))

            first_flight = driver.find_element(By.XPATH, "//div[@class='wr-hr-center wr-width grid flex ']")
            first_flight_details = first_flight.text.split('\n')

            # Check if there are flight details available
            if first_flight_details:
                print("Selected Flight Details:")
                for detail in first_flight_details:
                    print(detail)
            else:
                print("No flight details available.")

            WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='wr-hr-center wr-width grid flex ']")))

            book_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@autom='booknow']")))
            # Scroll to the book button
            driver.execute_script("arguments[0].scrollIntoView(true);", book_button)
            # Click the book button using JavaScript
            driver.execute_script("arguments[0].click();", book_button)

            # Wait for the book_button_now to be present
            book_button_now = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@class='fs-14 secondary-button button cursor-pointer bold ']")))
            # Scroll to the book_button_now
            driver.execute_script("arguments[0].scrollIntoView(true);", book_button_now)
            # Remove any overlay or element that might intercept the click
            driver.execute_script("arguments[0].style.visibility='hidden';", book_button_now)
            # Click the book_button_now using JavaScript
            driver.execute_script("arguments[0].click();", book_button_now)
            # Wait for the page with passenger input fields to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "container-fluid pad-sm-bottom")))

        else:
            # Wait for flight details element to be present
            WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='schedule v-aligm-t pr']")))

            # Add further steps to select the desired flight and complete the booking process
            # This will depend on the specific website you're automating
            # Selecting the first flight from the search results
            first_flight = driver.find_element(By.XPATH, "//div[@class='schedule v-aligm-t pr']")
            first_flight_details = first_flight.text.split('\n')

            # Check if there are flight details available
            if first_flight_details:
                print("Selected Flight Details:")
                for detail in first_flight_details:
                    print(detail)
            else:
                print("No flight details available.")

            # Check if "View Fares" button is present
            view_fares_button_present = len(driver.find_elements(By.XPATH, "//button[@autom='morefares']")) > 0

            if view_fares_button_present:
                # Click on "View Fares" button
                view_fares_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@autom='morefares']")))
                view_fares_button.click()

                # Wait for the book button to appear after clicking "View Fares"
                book_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@autom='booknow']")))

                # Scroll to "Book" button
                driver.execute_script("arguments[0].scrollIntoView(true);", book_button)

                # Click on "Book" button using JavaScript
                driver.execute_script("arguments[0].click();", book_button)

                # Wait for the page with passenger input fields to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "container-fluid.pad-sm-bottom")))

            else:
                # Click on "Book Now" button
                book_now_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@autom='select']")))

                # Scroll to "Book" button
                driver.execute_script("arguments[0].scrollIntoView(true);", book_now_button)

                # Click on "Book" button using JavaScript
                driver.execute_script("arguments[0].click();", book_now_button)

                # Wait for the next page to load
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "container-fluid")))

    finally:
        # Close the browser window
        driver.quit()
        print("Browser closed.")


# Example usage
book_flight("BOM", "BLR", "20/05/2024", "yes", "25/05/2024", 3, 2, 1, "Economy", "Non Stop", "N/A")