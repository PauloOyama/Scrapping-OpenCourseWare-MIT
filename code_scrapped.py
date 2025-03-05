
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement
import traceback
import time
import re
import os

# `tmp` directory will be where the downloaded files will be placed
cwd = os.getcwd()
try:
    if( not os.path.exists(cwd+'\\tmp')):
        os.mkdir(cwd+'\\tmp')
except Exception as e:
    print(e)
    
    
options = webdriver.ChromeOptions()

#This options is needed to set the downloaded directory and for downloading the files
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
# base_url = "https://ocw.mit.edu/search/?q=database&t=Computer%20Science" 
base_url = "https://ocw.mit.edu/search/?l=Graduate&t=Computer%20Science" 
# base_url = "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/download/"
# base_url = "https://ocw.mit.edu/search/?t=Computer%20Science" 

browser = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.

# When loaded the browser, then scroll to the bottom.
browser.get(base_url)
browser.implicitly_wait(5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# `Courses` will be the directory that manages the courses 
try:
    if(not os.path.exists(cwd+'\\Courses')):
        os.mkdir(cwd+'\\Courses')
except Exception as e:
    print(e)

#Counter iterate through the courses
counter = 0
# It has stopped in another execution ? 
is_recovered_session = False

# If it is a recovery session, then take the last course saved
try:
    f = open("recovery_session.txt", "r")
    counter = int(f.read())
    is_recovered_session = True
except FileNotFoundError as e:
    f = open("recovery_session.txt", "w")
    f.write(str(counter))
    f.close()

try:
    while True:
        height = browser.execute_script("return document.body.scrollHeight")
        #If its a recovery session, then scroll until the courses be avalaible in the html source
        if is_recovered_session and counter//10 > 0:
            print('Recovery Session finded....')
            print('Initiating in '+ str(counter))
            for _ in range(counter//10):
                print('------')
                print(f'HEIGHT= {browser.execute_script("return document.body.scrollHeight")}')
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #sleep and implicit_await will be needed to the html be loaded
                time.sleep(8)
            is_recovered_session = False
        
        #Take courses that will be downloaded
        clickable: WebElement
        try:
            clickable = browser.find_element(By.ID, f'search-result-{counter}-title')
        except NoSuchElementException as e:
            #It's the end of the page ? 
            height = browser.execute_script("return document.body.scrollHeight")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #sleep and implicit_await will be needed to the html be loaded
            time.sleep(8)
            new_height = browser.execute_script("return document.body.scrollHeight")
            
            #Yes, then finish the program
            if(new_height == height):
                print("Finished Scrapping...")
                exit()
                
        browser.implicitly_wait(5)
        clickable.click()

        #Is there something to be downloaded ? 
        try:
            click_download = browser.find_element(By.XPATH, '//html/body/div[1]/div[1]/div[2]/div[3]/div/div/div/div[2]/div/a')
            
        except NoSuchElementException as e:
            #No, don't have, just go to the next course
            print('Nothing to Download...')
            time.sleep(4)
            counter+=1
            #Back, to the previous page
            browser.execute_script("window.history.go(-1)")
            browser.implicitly_wait(5)
            continue
        
        #Yes, there is, click in downloaded contents

        click_download.click()
        time.sleep(2)

        #Take Bs4 page source for some validations
        html = browser.page_source
        soup = BeautifulSoup(html)

        #Is there something to be downloaded ?
        resources = soup.find_all("div", class_= "resource-list-toggle")
        if len(resources)==0:
            #No, there isn't.
            counter+=1
            browser.execute_script("window.history.go(-1)")
            browser.execute_script("window.history.go(-1)")
            continue
        
        #Yes, there is, so create the course name directory in ./Courses/
        title:str = soup.find('h1').text
        title = title.strip('/\n')
        title = title.replace(':','-')
        title = '_'.join(title.split(' '))
        print("Initiating Course " + title + ' - ' + str(counter))
        
        try:
            if(not os.path.exists(cwd+'\\Courses'+'\\'+title)):
                os.mkdir(cwd+'\\Courses'+'\\'+title)
        except Exception as e:
            print(e)
            
        #Checker the indexes of the toggles to be downloaded
        checker = soup.find_all("div", class_= "resource-list")
        indexes = []

        for i,x in enumerate(checker):
            if x.find('h4'):
                indexes.append(i)
                

        for i,x in enumerate(resources):
            
            #Reload html page source
            html = browser.page_source
            soup = BeautifulSoup(html)
            
            #Take section name
            section_name:str = x.find('h4').text
            #Use XPath to find the Selenium element to click
            if len(resources) == 1:
                click_lectures = browser.find_element(By.XPATH, f'//*[@id="main-course-section"]/div/div[2]/div/div[1]/a')
            else:
                click_lectures = browser.find_element(By.XPATH, f'//*[@id="main-course-section"]/div/div[2]/div[{indexes[i]+1}]/div[1]/a')

            is_dropped = click_lectures.get_attribute("aria-expanded")
            # print(is_dropped)
            if is_dropped == 'false':
                click_lectures.click()
            
            #There is an option to "See All" ? 
            has_see_all=False
            try:
                #Find XPath of the "See All" Button
                click_see_all = browser.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[{indexes[i]+1}]/div[2]/div[11]/div/div/a')
                # print('See All Button Finded...')
                click_see_all.click()
                browser.implicitly_wait(5)
                
                #Take the new html page source
                html = browser.page_source
                soup = BeautifulSoup(html)
                
                #Let's start downloading the files
                res = soup.find_all('a',class_='resource-thumbnail')
                for j,x in enumerate(res):
                    #Take files only, if its file type is explicit
                    if re.search('\..{1,4}$',x.attrs['href']):
                        # mp4 must be handled differently!
                        if '.mp4' in x.attrs['href']:
                            
                            # Take the name of the content, then store the link in a .txt file
                            mp4_name = soup.find_all('a',class_='resource-list-title')
                            mp4_name:str = mp4_name[j].text
                            mp4_name = mp4_name.replace(' ','_')
                            mp4_name = re.sub('[^A-Za-z0-9_.]+', '', mp4_name)
                            
                            
                            f = open("./tmp/" +mp4_name+'.txt', "w")
                            f.write(x.attrs['href'])
                            f.close()
                            time.sleep(1)
                            continue
                        
                        #If is not a Mp4 file, then just download
                        click_assignment_download_sell_all = browser.find_element(By.XPATH,f'//a[contains(@href,"{x.attrs['href']}")]')
                        click_assignment_download_sell_all.click()
                        time.sleep(1)
                    
                #Just go back to the previous page
                has_see_all=True
                browser.execute_script("window.history.go(-1)")
                time.sleep(4)
                    
            except NoSuchElementException as e:
                #Is doens't have 'See All' just pass through normally
                print('No See All encountered!')
                pass
            
            
            if not has_see_all:
                res = soup.find_all(id=re.compile("resource-list-container"))

                counter_ii = 0
                for j,x in enumerate(res[i].find_all('a', href=True)):
                    #Take files only, if its file type is explicit
                    if re.search('\..{1,4}$',x['href']):
                        # mp4 must be handled differently!
                        if '.mp4' in x['href']:
                            # Take the name of the content, then store the link in a .txt file
                            mp4_name = soup.find_all('a',class_='resource-list-title')
                            mp4_name:str = mp4_name[counter_ii].text
                            mp4_name = mp4_name.replace(' ','_')
                            mp4_name =  re.sub('[^A-Za-z0-9_.]+', '', mp4_name)
                            
                            
                            f = open("./tmp/" +mp4_name+'.txt', "w")
                            f.write(x.text)
                            f.close()
                            
                            counter_ii+=1
                            continue
                        
                        #If is not a Mp4 file, then just download
                        click_assignment_download = browser.find_element(By.XPATH,f'//a[contains(@href,"{x['href']}")]')
                        click_assignment_download.click()
                        time.sleep(1)
                
                time.sleep(4)
            
            #Moving files in ./tmp to ./Cousess
            list_of_files = os.listdir(os.getcwd() + '\\tmp')
            #Treatment of any special character in name
            section_name =  re.sub('[^A-Za-z0-9_/.]+', '', section_name)
            section_name = '_'.join(section_name.split(' '))
            
            #For each file in directory
            for file in list_of_files:
                #All files has some hash leading the content in the page
                #Then, take this hash and trim it.
                find_hash =re.findall(r'[a-z0-9]{32}_',file)
                new_name = file
                if(len(find_hash) != 0):
                    new_name = file.lstrip(find_hash[0])
                os.rename(os.getcwd() + '\\tmp'+'\\'+file,  os.getcwd() + '\\tmp'+'\\' + new_name)
                
                #Movement tmp -> Couses
                origin_path = os.getcwd() + '\\tmp'+'\\'+new_name
                try:
                    os.mkdir(os.getcwd() + '\\Courses'+'\\'+ title+'\\'+ section_name)
                except:
                    pass
                destination_path =os.getcwd() + '\\Courses'+'\\'+title+'\\'+ section_name+'\\'+new_name
                os.replace(origin_path,destination_path)
                
            #Just close the toogled section
            # click_lectures.click()
            time.sleep(1.5)
            
        #Go back to the initial page
        counter+=1
        browser.execute_script("window.history.go(-1)")
        browser.implicitly_wait(5)
        browser.execute_script("window.history.go(-1)")
        browser.implicitly_wait(5)


        if counter % 10 == 7:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(7)

#if there is an exception, save the current counter in a txt file
except Exception as e:
    print(e)
    print(traceback.format_exc())
finally:
    f = open("recovery_session.txt", "w")
    f.write(str(counter))
    f.close()