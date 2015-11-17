import Import_strava as imp_s
import Export_runtastic as exp_r
import Strava_retriever as st_r
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
import os

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
browser.get("https://www.runtastic.com")
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
dl_dir = browser.profile.default_preferences["browser.download.dir"]
# print dl_dir
wait = WebDriverWait(browser, 10)

dl_files = os.listdir(dl_dir)
for dl_file in dl_files:
	upload_btn = browser.find_elements_by_class_name("files")[0]
	# print dl_file
	new_name = str(hash(dl_file)) + ".tcx"
	os.rename(dl_dir+"\\"+dl_file, dl_dir + "\\" + new_name)
	imp_s.import_activity(dl_dir, new_name, upload_btn)
	# print "starting the wait"
	ui.WebDriverWait(browser, 30).until(lambda s: s.find_element_by_css_selector("button[class='btn-primary right action-button save-and-view'][style='']").is_displayed())
	# print "finished waiting"
	# save_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "save-and-view")))
	save_btn = browser.find_elements_by_class_name("save-and-view")[1]
	save_btn.click()
	imp_s.navigate_to_upload_panel(browser)

browser.close()
