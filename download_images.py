from selenium import webdriver
import time
import urllib.request 
import os
import sys

keywords = sys.argv[1:] 
query_keys = [key.replace('_','+') for key in keywords]


# 紀錄下載過的圖片網址，避免重複下載  
img_url_dic = {}  #maps {image_urls: ' '}
img_url_dic_file = "used_url.txt" 
stored_url_datapath = os.path.join(os.getcwd(), img_url_dic_file)
if os.path.exists(stored_url_datapath):
    with open(img_url_dic_file, "r") as data:
        img_url_dic = {d:"" for d in data.read().splitlines()}


images_folder = os.path.join(os.getcwd(), "images")


for index in range(0, len(keywords)):
    # 存圖位置
    local_path = os.path.join(images_folder, keywords[index])
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    # 爬取頁面網址 
    url = 'https://pic.sogou.com/pics?query=' + query_keys[index] + '&w=05009900'
    # 啟動chrome瀏覽器
    chrome_path = "./chromedriver" #chromedriver.exe執行檔所存在的路徑
    driver = webdriver.Chrome(chrome_path) 

    # 最大化窗口，因為每一次爬取只能看到視窗内的圖片  
    driver.maximize_window()  
    
    # 瀏覽器打開爬取頁面
    driver.get(url) 

    # 模擬滾動視窗瀏覽更多圖片
    pos = 0  
    m = 0 # 圖片編號 
    for i in range(2):  
        pos += i*500 # 每次下滾500  
        js = "document.documentElement.scrollTop=%d" % pos  
        driver.execute_script(js)  
        time.sleep(5)    
        
        counter = 0
        while (counter < 10):
            xpath = '/html/body/div[2]/div[2]/ul/li['+str(m+1)+']/div/a[1]/img'
            try:
                valid_xpath = False
                for element in driver.find_elements_by_xpath(xpath):
                    valid_xpath = True
                    img_url = element.get_attribute('src')
                    # print('img_url', img_url)
                    if img_url in img_url_dic:
                        print(str(img_url) + 'has already been already stored')
                        m += 1

                        
                    # 保存圖片到指定路徑
                    elif img_url != None:
                        counter += 1
                        m += 1
                        img_url_dic[img_url] = ''  
                        # print(img_url)
                        ext = img_url.split('/')[-1]
                        # print(ext)
                        filename = keywords[index] + '_'+ ext +'.jpg'
                        print('storing ' + filename + ' to ' + local_path + ', ' + str(i*10+counter) + ' images saved')

                        # 保存圖片
                        urllib.request.urlretrieve(img_url, os.path.join(local_path , filename)) 
                        

                if valid_xpath == False:
                    m += 1
                
            except OSError:
                print('發生OSError!')
                print(pos)
                break

            time.sleep(3)
            
    driver.close()
    
with open("used_url.txt", "w") as file:
    for key in img_url_dic:
        file.write("%s\n" % key)
