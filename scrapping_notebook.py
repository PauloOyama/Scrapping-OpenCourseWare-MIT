
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import re
import os


def find_exams(soup:BeautifulSoup):

    try:
        click_lectures = browser.find_element(By.XPATH, '//*[@id="main-course-section"]/div/div[2]/div[2]/div[1]/a')
        click_lectures = browser.find_element(By.XPATH, '//*[@id="main-course-section"]/div/div[2]/div[2]/div[1]/a')
        click_lectures = browser.find_element(By.XPATH, '//*[@id="main-course-section"]/div/div[2]/div[3]/div[1]/a')
        
        click_lectures.click()
    except NoSuchElementException as e:
        print('No Exams Section Find...')
        return False
        
    time.sleep(2)
    ls = soup.find(id='resource-list-container-exams')

    for x in ls.find_all('a', href=True):
        if re.search('\..{1,4}$',x['href']):
            # print(x)
            # print(x['href'])
            # leactures_pdf.append(x['href'])
            click_assignment_download = browser.find_element(By.XPATH,f'//a[contains(@href,"{x['href']}")]')
            click_assignment_download.click()
            time.sleep(2)
            

    list_of_files = os.listdir(os.getcwd() + '\\tmp')
    for file in list_of_files:
        origin_path = os.getcwd() + '\\tmp'+'\\'+file
        try:
            os.mkdir(os.getcwd() + '\\Courses'+'\\'+ title+'\\'+'Exams')
        except:
            pass
        destination_path =os.getcwd() + '\\Courses'+'\\'+title+'\\'+'Exams'+'\\'+file
        os.replace(origin_path,destination_path)
        
    click_lectures.click()
    return True


def find_assignments(soup:BeautifulSoup):
    try:
        click_lectures = browser.find_element(By.XPATH, '//*[@id="main-course-section"]/div/div[2]/div[1]/div[1]/a')
        click_lectures.click()
    except NoSuchElementException as e:
        print('No Assignments Section Find...')
        return False
        

    ls = soup.find(id='resource-list-container-assignments')

    for x in ls.find_all('a', href=True):
        if re.search('\..{1,4}$',x['href']):
            # print(x)
            # print(x['href'])
            # leactures_pdf.append(x['href'])
            click_assignment_download = browser.find_element(By.XPATH,f'//a[contains(@href,"{x['href']}")]')
            click_assignment_download.click()
            time.sleep(2)
            

    list_of_files = os.listdir(os.getcwd() + '\\tmp')
    for file in list_of_files:
        origin_path = os.getcwd() + '\\tmp'+'\\'+file
        try:
            os.mkdir(os.getcwd() + '\\Courses'+'\\'+ title+'\\'+'Assignments')
        except:
            pass
        destination_path =os.getcwd() + '\\Courses'+'\\'+title+'\\'+'Assignments'+'\\'+file
        os.replace(origin_path,destination_path)
        
    click_lectures.click()
    return True


def find_lectures(soup:BeautifulSoup):

    try:
        click_lectures = browser.find_element(By.XPATH, '//html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[2]/div[1]/a')
        click_lectures.click()
    except NoSuchElementException as e:
        print('No Lectures Section Find...')
        return False
        

    ls = soup.find(id='resource-list-container-lecture-notes')
    # ls.find_all('a', class_='resource-thumbnail')

    for x in ls.find_all('a', href=True):
        if re.search('\..{4}$',x['href']):
            # print(x['href'])
            # leactures_pdf.append(x['href'])
            click_leacture_download = browser.find_element(By.XPATH,f'//a[contains(@href,"{x['href']}")]')
            click_leacture_download.click()
            time.sleep(2)
            

    list_of_files = os.listdir(os.getcwd() + '\\tmp')
    for file in list_of_files:
        origin_path = os.getcwd() + '\\tmp'+'\\'+file
        try:
            os.mkdir(os.getcwd() + '\\Courses'+'\\'+ title+'\\'+'Lectures')
        except:
            pass
        destination_path =os.getcwd() + '\\Courses'+'\\'+title+'\\'+'Lectures'+'\\'+file
        os.replace(origin_path,destination_path)

    click_lectures.click()
    return True

def find_reading(soup=BeautifulSoup):

    try:
        click_readings = browser.find_element(By.XPATH, '//html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[3]/div[1]/a')
        click_readings.click()
    except NoSuchElementException as e:
        print('No Reading Section Find...')
        return False

    ls = soup.find(id='resource-list-container-readings')

    readings_pdf = []
    for x in ls.find_all('a', href=True):
        if re.search('\..{1,4}$',x['href']):
            print(x['href'])
            
            click_readings_download = browser.find_element(By.XPATH,f'//a[contains(@href,"{x['href']}")]')
            click_readings_download.click()
            time.sleep(2)

    list_of_files = os.listdir(os.getcwd() + '\\tmp')
    for file in list_of_files:
        origin_path = os.getcwd() + '\\tmp'+'\\'+file
        try:
            os.mkdir(os.getcwd() + '\\Courses'+'\\'+ title+'\\'+'Readings')
        except:
            pass
        destination_path =os.getcwd() + '\\Courses'+'\\'+title+'\\'+'Readings'+'\\'+file
        os.replace(origin_path,destination_path)

    click_readings_download.click()
    return True

cwd = os.getcwd()
try:
    os.mkdir(cwd+'\\tmp')
except Exception as e:
    print(e)
    
    
options = webdriver.ChromeOptions()

options.add_experimental_option("prefs", {
    'download.prompt_for_download':False,
    'plugins.always_open_pdf_externally':True,
    "download.default_directory": cwd+'\\tmp',
    "safebrowsing_for_trusted_sources_enabled": False,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


# base_url = "https://ocw.mit.edu/" 
base_url = "https://ocw.mit.edu/search/?t=Computer%20Science" 
# base_url = "https://ocw.mit.edu/courses/18-s191-introduction-to-computational-thinking-fall-2022/download/" 

browser = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.

# browser.options.add_experimental_option("prefs", profile)
browser.get(base_url)

browser.implicitly_wait(7)


try:
    os.mkdir(cwd+'\\Courses')
except Exception as e:
    print(e)
    
    
counter = 0

while True:
    clickable = browser.find_element(By.ID, f'search-result-{counter}-title')
    clickable.click()
    browser.implicitly_wait(7)

    try:
        click_download = browser.find_element(By.XPATH, '//html/body/div[1]/div[1]/div[2]/div[3]/div/div/div/div[2]/div/a')
    except NoSuchElementException as e:
        print('Nothing to Download...')
        browser.execute_script("window.history.go(-1)")
        counter+=1
        continue
        
    click_download.click()
    browser.implicitly_wait(7)
    
    html = browser.page_source
    soup = BeautifulSoup(html)
    
    
    title:str = soup.find('h1').text
    title = title.strip('/\n')
    title = title.replace(':','-')
    title = '_'.join(title.split(' '))

    try:
        os.mkdir(cwd+'\\Courses'+'\\'+title)
    except Exception as e:
        print(e)
    
    find_assignments(soup=soup)
    time.sleep(2)
    find_exams(soup=soup)
    time.sleep(2)
    find_lectures(soup=soup)
    time.sleep(2)
    find_reading(soup=soup)
    time.sleep(2)
    browser.execute_script("window.history.go(-1)")
    browser.execute_script("window.history.go(-1)")
    
    counter+=1
    
    scroll_height = 70
    browser.execute_script(f'window.scrollTo(0, {700+counter*scroll_height})')