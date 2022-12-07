from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import json

# fill in the chrome driver directory
driver_location = 'C:\Program Files\Google\Chrome\Application\chromedriver_win32\chromedriver.exe'
s = Service(driver_location)
chrome_options = webdriver.ChromeOptions()
chrome_options.accept_untrusted_certs = True
chrome_options.assume_untrusted_cert_issuer = True
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--allow-http-screen-capture")
chrome_options.add_argument("--disable-impl-side-painting")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-seccomp-filter-sandbox")
# headless mode, comment it to check the browser behaviour
chrome_options.add_argument("--headless")


class city_u_model():
    def __init__(self):
        self.browser = webdriver.Chrome(
            service=s, chrome_options=chrome_options)

    def scroll_to_bottom(self):
        temp_height = 0
        while True:
            self.browser.execute_script("window.scrollBy(0, 2000)")
            time.sleep(1.5)
            check_height = self.browser.execute_script(
                "return document.documentElement.scrollTop || \
                    window.pageYOffset || document.body.scrollTop;")
            if check_height == temp_height:
                break
            temp_height = check_height

    def locate_xpath(self, xpath):
        try:
            WebDriverWait(self.browser, 20, 0.5).until(EC.visibility_of_element_located(
                (By.XPATH, xpath)))
            return True
        except:
            return False

    def get_name_by_staff(self, staff):
        name = staff.find_element(By.CLASS_NAME, 'name').find_element(
            By.CLASS_NAME, 'en').text
        idx = name.index(' ')
        name = name[idx+1:]
        return name

    def get_email_by_staff(self, staff):
        email = staff.find_elements(By.CLASS_NAME, 'email')
        if not email:
            return ""
        return email[0].text

    def get_jobtitle_by_staff(self):
        jobtitle = self.browser.find_elements(By.CLASS_NAME, 'jobtitle')
        if not jobtitle:
            return []
        return [x.text for x in jobtitle]

    def get_image_by_staff(self, staff):
        img = staff.find_elements(
            By.CLASS_NAME, 'scholar-thumbnail')
        if not img:
            return ""
        else:
            img = img[0].find_elements(By.TAG_NAME, 'img')
            if not img:
                return ""
            else:
                return img[0].get_attribute('src')

    def get_edu_by_staff(self):
        edu = self.browser.find_elements(By.CLASS_NAME, 'qualifications')
        if not edu:
            return []
        else:
            edu = edu[0].find_elements(By.TAG_NAME, 'p')
            return [x.text for x in edu]

    def get_research_interest_by_staff(self):
        rs = self.browser.find_elements(By.XPATH,
                                        "//h2[contains(text(),'Research Interests/Areas')]")

        if not rs:
            return []

        else:

            rs = self.browser.find_elements(By.XPATH,
                                            "//h2[contains(text(),'Research Interests/Areas')]\
                             /following-sibling::div/ul")
            if rs:
                rs = rs[0].find_elements(By.TAG_NAME, 'li')
            else:
                rs = self.browser.find_elements(By.XPATH,
                                                "//h2[contains(text(),'Research Interests/Areas')]\
                             /following-sibling::div")[0].find_elements(By.TAG_NAME, 'p')
            return [x.text for x in rs]

    def save(self, d):
        folder = "data"
        folder_exist = os.path.exists(folder)
        filename = d["name"].replace(' ', '_') + ".json"
        dir = "/" + folder + "/" + filename
        if not folder_exist:
            os.makedirs(folder)
            print("New folder for CityU_Faculty made")
        else:
            # Reduce printing messages for saving time
            print("Saving data into " + dir)
        jsonOrderedFile = json.dumps(d, indent=4)
        with open(os.getcwd() + dir, 'w') as jsonfile:
            jsonfile.write('[\n')
            jsonfile.write(jsonOrderedFile)
            jsonfile.write('\n]')

    def run(self):
        for i in range(0, 100):
            url = "https://www.cityu.edu.hk/directories/people/academic?keyword=&page=" + \
                str(i)
            self.browser.get(url)
            staff_lst = self.browser.find_elements(By.CLASS_NAME, 'views-row')
            for staff in staff_lst:
                d = {}
                profile = staff.find_element(
                    By.CLASS_NAME, 'view-profile').find_element(By.TAG_NAME, 'a')
                name = self.get_name_by_staff(staff)
                email = self.get_email_by_staff(staff)
                img = self.get_image_by_staff(staff)
                profile.click()
                self.browser.switch_to.window(self.browser.window_handles[1])
                position = self.get_jobtitle_by_staff()
                edu = self.get_edu_by_staff()
                research_interest = self.get_research_interest_by_staff()
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                d["name"] = name
                d["email"] = email
                d["education"] = edu
                d["position"] = position
                d["research interest"] = research_interest
                d["image"] = img
                self.save(d)
            time.sleep(1)
        self.browser.quit()


if __name__ == "__main__":
    model = city_u_model()
    model.run()
