from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options, executable_path=r'/usr/local/bin/chromedriver')

# store starting time
begin = time.time()

# FINRA's TRACE Bond Center
driver.get('http://finra-markets.morningstar.com/BondCenter/Results.jsp')

# click agree
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, ".button_blue.agree"))).click()

# click edit search
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'a.qs-ui-btn.blue'))).click()

# click advanced search
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'a.ms-display-switcher.hide'))).click()

# select bond ratings
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'select.range[name=moodysRating]')))
Select((driver.find_elements(By.CSS_SELECTOR,
    'select.range[name=moodysRating]'))[0]).select_by_visible_text('C')
Select((driver.find_elements(By.CSS_SELECTOR,
    'select.range[name=moodysRating]'))[1]).select_by_visible_text('Aaa')
Select((driver.find_elements(By.CSS_SELECTOR,
    'select.range[name=standardAndPoorsRating]'))[0]).select_by_visible_text('B-')
Select((driver.find_elements(By.CSS_SELECTOR,
    'select.range[name=standardAndPoorsRating]'))[1]).select_by_visible_text('BBB+')

# select Sub-Product Type
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'select[name=subProductType]')))
Select((driver.find_elements(By.CSS_SELECTOR,
    'select[name=subProductType]'))[0]).select_by_visible_text('Corporate Bond')

# select Bond Seniority
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'select[name=securityDescription]')))
Select((driver.find_elements(By.CSS_SELECTOR,
    'select[name=securityDescription]'))[0]).select_by_visible_text('Senior')

# input Trade Yield
inputElement = driver.find_element(By.XPATH, "(//input[@name='tradeYield'])[1]")
inputElement.send_keys('0.001')
inputElement = driver.find_element(By.XPATH, "(//input[@name='tradeYield'])[2]")
inputElement.send_keys('50')

###############################################

# select Trade Date(MM/DD/YYYY)
inputElement = driver.find_element(By.CSS_SELECTOR,'.qs-ui-ipt.range.date[calid="5"]')
ActionChains(driver).click(inputElement).perform()

# Create for loop to click 1 time when targeting the Previous Year Button
for d in range(1):
    previous = driver.find_element(By.CSS_SELECTOR,'.py')
    # Make click in that button
    ActionChains(driver).click(previous).perform()

webelem1 = driver.find_element(By.XPATH, "(/html/body/div[4]/div[2]/table/tbody/tr[2]/td[2]/div)")
# webelem1 = driver.find_element_by_css_selector('.dayNum[val="2020-08-03"]')
ActionChains(driver).click(webelem1).perform()

inputElement = driver.find_element(By.CSS_SELECTOR,'.qs-ui-ipt.range.date[calid="6"]')
ActionChains(driver).click(inputElement).perform()

webelem2 = driver.find_element(By.CSS_SELECTOR,'.dayNum.today')
ActionChains(driver).click(webelem2).perform()

###############################################

# click show results
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'input.button_blue[type=submit]'))).click()

# wait for results
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '.rtq-grid-row.rtq-grid-rzrow .rtq-grid-cell-ctn')))

# wait for page total
WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((
    By.CSS_SELECTOR, '.qs-pageutil-total')))

time.sleep(3)

# capture total of pages
pages = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((
    By.CSS_SELECTOR, '.qs-pageutil-total')))[0].text

# isolate the number of pages
pages = pages.split(" ")[1]
print(f'Total pages returned: {pages}')

# create dataframe from scrape
frames = []

for page in tqdm(range(1, int(pages)), position=0, leave=True, desc = "Retrieving Bond Data"):
    bonds = []

    # wait for page marker to be on expected page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, (f"a.qs-pageutil-btn[value='{str(page)}']"))))
    
    # wait for page next button to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'a.qs-pageutil-next')))
    
    # wait for table grid to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.rtq-grid-bd')))
    
    # wait for tablerows to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.rtq-grid-bd > div.rtq-grid-row')))
    
    # wait for table cell to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.rtq-grid-cell')))

    # Wait 3 seconds to ensure all rows load
    time.sleep(3)
    
    # scrape table rows
    headers = [title.text for title in driver.find_elements(By.CSS_SELECTOR,
    '.rtq-grid-row.rtq-grid-rzrow .rtq-grid-cell-ctn')[1:]]

    tablerows = driver.find_elements_by_css_selector(
        'div.rtq-grid-bd > div.rtq-grid-row')
    for tablerow in tablerows:
        try:
            tablerowdata = tablerow.find_elements(By.CSS_SELECTOR,
                'div.rtq-grid-cell')
            bond = [item.text for item in tablerowdata[1:]]
            bonds.append(bond)
        except:
            pass

    # Convert to Dataframe
    df = pd.DataFrame(bonds, columns=headers)

    frames.append(df)

    try:
        driver.find_element(By.CSS_SELECTOR,'a.qs-pageutil-next').click()
    except:
        break

bond_prices_df = pd.concat(frames)

# store end time 
end = time.time()

# total time taken 
print(f"Total runtime of the program is {end - begin} seconds")

bond_prices_df.to_csv("bond.csv")
