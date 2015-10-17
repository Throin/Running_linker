from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# personal module should contain your own personal information such as login, password etc.
from personal import strava_login, strava_pw

# First start a webdriver

driver = webdriver.Firefox()

# Then connect to strava website

strava_url = "https://www.strava.com"
driver.get(strava_url)

# Connect to account

login_btn_candidates = driver.find_elements_by_class_name("btn-login")
btn = login_btn_candidates[0]
btn.click() #TODO : check that we are on the right button, that the element is displayed
email_fields = driver.find_elements_by_name("email")
for candidate in email_fields:
	if candidate.is_displayed() and "adresse" in candidate.get_attribute("placeholder"):
		candidate.send_keys(strava_login)

pw_fields = driver.find_elements_by_name("password")
for candidate in pw_fields:
	if "passe" in candidate.get_attribute("placeholder") and candidate.is_displayed():
		candidate.send_keys(strava_pw)
		candidate.send_keys(Keys.RETURN)

# At this point, you should be logged on Strava and ready to move on to the next section
		
# Navigate to activities history

# Retrieve history and in particular last activity