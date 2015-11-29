from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import codecs

from personal import strava_pw, strava_login

def import_activity(folder_name, file_name, button):
	path = folder_name + "\\" + file_name
	if button.is_displayed():
		button.send_keys(path)
	return 
	
def import_activities(folder_names, file_names, button):
	assert len(folder_names) == len(file_names)
	counter = 0
	for folder_name in folder_names:
		import_activity(folder_name, file_names[counter], button)
		counter += 1
		
	return
	
def connect_to_strava_dashboard(browser):
	browser.get("https://www.strava.com/login")
	# browser.find_elements_by_partial_link_text("connecter")[0].click() # Useful only if we connect to strava main page rather than login page
	adress_form = browser.find_elements_by_id("email")
	if adress_form:
		adress_form = adress_form[0]
		assert adress_form.is_displayed()
		adress_form.send_keys(strava_login)
		
	pw_form = browser.find_elements_by_id("password")
	if pw_form:
		pw_form = pw_form[0]
		assert pw_form.is_displayed()
		pw_form.send_keys(strava_pw + Keys.RETURN)
	
	return "Tableau de bord" in browser.title

def navigate_to_upload_panel(browser):
	expandable_menu = browser.find_elements_by_class_name("new-upload-button")
	if expandable_menu:
		hover = ActionChains(browser).move_to_element(expandable_menu[0])
		hover.perform()
		
		upload_menu = browser.find_elements_by_class_name("upload-activity")
		if upload_menu:
			upload_menu[0].click()
			browser.implicitly_wait(4)
			upload_from_file = browser.find_elements_by_partial_link_text("Fichier")
			if upload_from_file:
				upload_from_file[0].click()
			
	return		
	
## TODO: handle case where neither <Notes> nor <Track> tags are found. Currently, throw exception at the end of file
def retrieve_notes(filename):
	with codecs.open(filename, 'r', encoding='utf-8') as fHandle:
		found = False
		while (not found):
			line = fHandle.next()
			found = '<Notes>' in line or '<Track>' in line
		
		if '<Notes>' in line:
			#Strip the tags
			value_no_left_tag = line.split('<Notes>')[1]
			value_no_tag = value_no_left_tag.split('</Notes>')[0]
			return value_no_tag
			
		elif '<Track>' in line:
			return str()
		
		else:
			return str()
	
if __name__ == "__main__":
	browser = webdriver.Firefox()
	connect_to_strava_dashboard(browser)
	navigate_to_upload_panel(browser)
	
	
else:
	# print "imported"
	pass