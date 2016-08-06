import Strava.Import_strava as imp_s
import Runtastic.Export_runtastic as exp_r
import Strava.Strava_retriever as st_r
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
import os

import readline, rlcompleter

readline.parse_and_bind("tab:complete")

# First step : instantiate a browser that will be used to sync strava account to runtastic account
browser = exp_r.instantiate_auto_download_browser()

# Second step : retrieve information from Strava
st_r.connect_to_strava(browser)
# browser.implicitly_wait(8)
st_r.log_onto_strava(browser)
# browser.implicitly_wait(8)
st_r.navigate_to_history(browser)
browser.implicitly_wait(8)
##TODO: make sure we retrieve a date - the implicit wait does not work 100% of the time
last_date = st_r.retrieve_last_activity(browser)
if last_date == 0:
	print """Warning, no activity could be found browsing Strava account. Something is probably wrong unless your Strava account is brand new. Continue ?"""
	##TODO: allow user to continue with y/n 
	raise Exception('no history')
# browser.implicitly_wait(8)

# Intermediate step to check results relevancy
# print last_date

# Third step : download every activity that is not yet in strava according to its date
browser.execute_script("window.open('https://www.runtastic.com', '_blank');")
browser.switch_to_window(browser.window_handles[1])
# browser.implicitly_wait(8)
##TODO: deal with the case where we're not on the page we think after logging (example "premium usership" promotion) 
exp_r.log_onto_runtastic(browser)
# browser.implicitly_wait(8)
runtastic_in_advance = exp_r.navigate_to_latest_activity(browser, last_date)
if not runtastic_in_advance:
	print "Strava last activity is more recent than what is in runtastic, stopping there !"
	exit()
	
browser.implicitly_wait(8)
exp_r.download_relevant_activities(browser, last_date)
# browser.implicitly_wait(8)

# Fourth step : import all activities on strava
imp_s.connect_to_strava_dashboard(browser)
imp_s.navigate_to_upload_panel(browser)
#dl_dir = browser.profile.default_preferences["browser.download.dir"]
dl_dir = '/home/matthieu/Downloads' ## TODO: remove ASAP, this bugfix will only work on current setup
# print dl_dir
wait = WebDriverWait(browser, 10)

full_dl_files = os.listdir(dl_dir)
dl_files = [filetcx for filetcx in full_dl_files if '.tcx' in filetcx]
for dl_file in dl_files:
	print dl_file
	upload_btns = browser.find_elements_by_css_selector("a[href*='upload']")
	upload_btn = [elem for elem in upload_btns if "file" in elem.text.lower()]
	if upload_btn:
		upload_btn[0].click()
		ui.WebDriverWait(browser, 5).until(lambda s: '.tcx' in s.find_element_by_css_selector("span[class='multi_text']").text)
		upload_btn = browser.find_elements_by_css_selector("input[type*='file']")
		upload_btn = upload_btn[0]
	else:
		raise Exception("Could not find the upload btn") 
	# print dl_file
	new_name = str(hash(dl_file)) + ".tcx"
	os.rename(dl_dir+ os.sep + dl_file, dl_dir + os.sep + new_name)
	act_notes = imp_s.retrieve_notes(dl_dir + os.sep + new_name)
	# print act_notes
	imp_s.import_activity(dl_dir, new_name, upload_btn)
	# print "starting the wait"
	ui.WebDriverWait(browser, 30).until(lambda s: s.find_element_by_css_selector("button[class='btn-primary right action-button save-and-view'][style='']").is_displayed())
	# print "finished waiting"
	# save_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "save-and-view")))
	save_btn = browser.find_elements_by_class_name("save-and-view")[1]
	comment_field = browser.find_elements_by_css_selector("textarea[name*='description']")[0]
	comment_field.send_keys(act_notes)
	save_btn.click()
	ui.WebDriverWait(browser, 10).until(lambda s: s.find_element_by_css_selector("a[data-menu*='segment']").is_displayed())
	os.remove(dl_dir + os.sep + new_name)
	imp_s.navigate_to_upload_panel(browser)

s = raw_input("Close browser ? Y/N")
if "Y" in s:
	browser.close()
else:
	pass
