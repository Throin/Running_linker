from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time # Probably not usefull, check wether is the case or not
import sys 

my_password = "fedhop"

passed_args = sys.argv
for s in sys.argv:
    print s

driver = webdriver.Firefox()
driver.get("https://www.runtastic.com")

# Simple check on the website we've landed on
assert "Runtastic" in driver.title or "runtastic" in driver.title
print driver.title
#time.sleep(1)

# Detect "connect" button
connect_btn_candidates = driver.find_elements_by_class_name("bttn")
for candidate in connect_btn_candidates:
    if "connect" in candidate.text and candidate.is_displayed():
        candidate.click()
        break

########## Go through first page and connect to account ########## 
# Detect fields to fill : email input field and password input field
input_fields = driver.find_elements_by_class_name("js-input")
mail_field_found = False
pw_field_found = False
for elem in input_fields:
    parent = elem.find_element_by_xpath("..")
    parent_class = parent.get_attribute("class")
    if "email" in parent_class and "login" in parent_class:
        mail_input_field = elem
        mail_field_found = True
    elif "password" in parent_class and "login" in parent_class:
        pw_input_field = elem
        pw_field_found = True
    else:
        print ""

# Fill fields and connect to session
if mail_field_found and pw_field_found:
    mail_input_field.send_keys("throin@hotmail.com")
    pw_input_field.send_keys(my_password)
    pw_input_field.send_keys(Keys.RETURN)

########## ########## ########## ########## ########## ##########

##########  Go through second page to activities history ##########
# time.sleep(1)
driver.implicitly_wait(8) # TODO: try explicit wait, using Expected conditions cf http://selenium-python.readthedocs.org/en/latest/waits.html
actvities_candidate = driver.find_elements_by_class_name("usernav-activities")
try:
    actvities_candidate[0].click()
except:
    print "Could not click :'( "
        


########## This is the code graveyard, in order to come back from the dead when the time shall be right ########## 

##for elem in elems_list:
##    if 'icon-login' in elem.get_attribute("class") and elem.is_displayed():
##        elem.click()
###        time.sleep(0.5)
##        elems_list_modified = driver.find_elements_by_xpath("//*[@id]")
##        login_entered = False
##        for new_elem in elems_list_modified:
####            if new_elem.get_attribute("placeholder") and 'Email' in new_elem.get_attribute("placeholder"):
##            if new_elem.get_attribute("id") == "ember836": # Problem : id changes from one connection to the other
##                new_elem.send_keys("throin@hotmail.com")
##                login_entered = True
####            if new_elem.get_attribute("placeholder") and 'Mot de passe' in new_elem.get_attribute("placeholder"):
##            if new_elem.get_attribute("id") == "ember838":
##                new_elem.send_keys("fedhop")
##                if login_entered:
##                    new_elem.send_keys(Keys.RETURN)
##                    break
##        break
##            if new_elem.get_attribute("type") and 'submit' in new_elem.get_attribute("submit"):
##                press_enter_button = elem
##        press_enter_button.click()

# Log-in
# login_field = driver.find_element_by_name("login")
# print login_field
########## ########## ########## ########## ########## ########## ########## ########## ########## ########## 
