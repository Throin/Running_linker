from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from CustDate import CustDate

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
driver.implicitly_wait(8)
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
assert "Tableau" in driver.title

		
# Navigate to activities history
# This history can be reached from the dashboard through drop down menu "Entrainement" and link "Mes activites"
dd_menus = driver.find_elements_by_class_name("drop-down-menu")
for menu in dd_menus:
	if menu.get_attribute("class") == "drop-down-menu enabled" and menu.text == u'Entra\xeenement':
		hover = ActionChains(driver).move_to_element(menu)
		hover.perform()
		
		activity_candidates = driver.find_elements_by_partial_link_text("Mes acti")
		# TODO: check that we don't have multiple such elements
		activity_candidates[0].click()
		break

# Retrieve history and in particular last activity
driver.implicitly_wait(8)

## TODO: check we only have one element and this element is indeed the "Date" column
top_date_col = driver.find_elements_by_class_name("active")
top_date_col = top_date_col[0]

assert top_date_col.text == u'Date'

## TODO: reput the column in descending order : if top_date_col.get_attribute("xx") == u'DESC' then get child and click it
date_loc_x = top_date_col.location["x"]

data_candidates = driver.find_elements_by_class_name("view-col")
dates  = []
for elem in data_candidates:
	if elem.location["x"] == date_loc_x:
		dates.append(elem.text)

## TODO: Extract dates in readable format and return last date
print dates
cust_dates = []
for indiv_date in dates:
	# First separate the day from the date, then the different element from the date. To robustify this, we would need to check the format is indeed what we assume here - probably higher in the code, while parsing the "Date" column head
	processed_raw = indiv_date.split()
	processed_figures = processed_raw[1].split("/")
	cust_dates.append(CustDate(day = processed_figures[0], month = processed_figures[1], year = processed_figures[2]))

