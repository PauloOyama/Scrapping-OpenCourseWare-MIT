
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import re
import os


cwd = os.getcwd()
try:
    if( not os.path.exists(cwd+'\\tmp')):
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
# base_url = "https://ocw.mit.edu/courses/18-s191-introduction-to-computational-thinking-fall-2022/download/" 
base_url = "https://ocw.mit.edu/search/?q=database&t=Computer%20Science" 
# base_url = "https://ocw.mit.edu/search/?t=Computer%20Science" 

browser = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.

browser.get(base_url)
browser.implicitly_wait(5)


try:
    if(not os.path.exists(cwd+'\\Courses')):
        os.mkdir(cwd+'\\Courses')
except Exception as e:
    print(e)


counter = 0
while True:

    clickable = browser.find_element(By.ID, f'search-result-{counter}-title')
    clickable.click()
    browser.implicitly_wait(5)

    try:
        click_download = browser.find_element(By.XPATH, '//html/body/div[1]/div[1]/div[2]/div[3]/div/div/div/div[2]/div/a')
    except NoSuchElementException as e:
        print('Nothing to Download...')
        counter+=1
        browser.execute_script("window.history.go(-1)")
        browser.implicitly_wait(5)
        continue

    click_download.click()
    browser.implicitly_wait(5)



    html = browser.page_source
    soup = BeautifulSoup(html)


    resources = soup.find_all("div", class_= "resource-list-toggle")
    # print(resources)
    if len(resources)==0:
        counter+=1
        browser.execute_script("window.history.go(-1)")
        browser.execute_script("window.history.go(-1)")
        pass

    title:str = soup.find('h1').text
    title = title.strip('/\n')
    title = title.replace(':','-')
    title = '_'.join(title.split(' '))

    try:
        if(not os.path.exists(cwd+'\\Courses'+'\\'+title)):
            os.mkdir(cwd+'\\Courses'+'\\'+title)
    except Exception as e:
        print(e)
        
        
    checker = soup.find_all("div", class_= "resource-list")
    indexes = []

    for i,x in enumerate(checker):
        if x.find('h4'):
            indexes.append(i)
            

    for i,x in enumerate(resources):
        
        html = browser.page_source
        soup = BeautifulSoup(html)
        
        section_name:str = x.find('h4').text
    
        # print(indexes[i]+1)
        # print(f'//*[@id="main-course-section"]/div/div[2]/div[{indexes[i]+1}]/div[1]/a')
    
        if len(resources) == 1:
            click_lectures = browser.find_element(By.XPATH, f'//*[@id="main-course-section"]/div/div[2]/div/div[1]/a')
        else:
            # print(f'//*[@id="main-course-section"]/div/div[2]/div[{indexes[i]+1}]/div[1]/a')
            click_lectures = browser.find_element(By.XPATH, f'//*[@id="main-course-section"]/div/div[2]/div[{indexes[i]+1}]/div[1]/a')

        click_lectures.click()
        time.sleep(1.5)
        
        has_see_all=False
        try:
            click_see_all = browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[{indexes[i]+1}]/div[2]/div[11]/div/div/a')
            click_see_all.click()
            browser.implicitly_wait(5)
            
            
            html = browser.page_source
            soup = BeautifulSoup(html)
            res = soup.find_all('a',class_='resource-thumbnail')
            # print(len(res))
            for x in res:
                if re.search('\..{1,4}$',x.attrs['href']):
                    if '.mp4' in x.attrs['href']:
                        continue
                    click_assignment_download_sell_all = browser.find_element(By.XPATH,f'//a[contains(@href,"{x.attrs['href']}")]')
                    click_assignment_download_sell_all.click()
                time.sleep(0.5)
                
                
            has_see_all=True
            browser.execute_script("window.history.go(-1)")
            browser.implicitly_wait(5)
                
        except NoSuchElementException as e:
            print('No See All encountered!')
            pass
        
        
        if not has_see_all:
            res = soup.find_all(id=re.compile("resource-list-container"))

            for x in res[i].find_all('a', href=True):
                if re.search('\..{1,4}$',x['href']):
                    if '.mp4' in x['href']:
                        continue
                    # print(x)
                    # print(x['href'])
                    # leactures_pdf.append(x['href'])
                    click_assignment_download = browser.find_element(By.XPATH,f'//a[contains(@href,"{x['href']}")]')
                    # print(f'//a[contains(@href,"{x['href']}")]')
                    click_assignment_download.click()
                    time.sleep(0.5)
            
        list_of_files = os.listdir(os.getcwd() + '\\tmp')
        section_name = section_name.replace(':','-')
        section_name = '_'.join(section_name.split(' '))
        
        for file in list_of_files:
            origin_path = os.getcwd() + '\\tmp'+'\\'+file
            try:
                os.mkdir(os.getcwd() + '\\Courses'+'\\'+ title+'\\'+ section_name)
            except:
                pass
            destination_path =os.getcwd() + '\\Courses'+'\\'+title+'\\'+ section_name+'\\'+file
            os.replace(origin_path,destination_path)
            
        
        click_lectures.click()
        time.sleep(1.5)
        
    counter+=1
    browser.execute_script("window.history.go(-1)")
    browser.execute_script("window.history.go(-1)")
    browser.implicitly_wait(5)


    if counter % 10 == 9:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(7)
