# -*- coding: utf-8 -*-
"""

Start a new Chrome window 

"""

from selenium import webdriver

if __name__ == "__main__":        
    chrome_options = webdriver.ChromeOptions()
    # set your proxy
    chrome_options.add_argument('--proxy-server=socks5://localhost:12333') 
    # set user-data-dir so that the login information can be record
    chrome_options.add_argument(r"user-data-dir=C:\Users\username\AppData\Local\Google\Chrome\User_Data_Spider") 
    # set whether loadimage  
    #chrome_options.add_argument('blink-settings=imagesEnabled=false') 
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
    chrome_options.add_experimental_option("useAutomationExtension", False);   
    
    #  open a new chrome window
    driver = webdriver.Chrome(chrome_options=chrome_options,port=10810)
    
    # record executor_url and session_id to reuse it
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    
    with open("SessionInfo.txt", 'w') as f:
        f.writelines(executor_url+"\n")
        f.writelines(session_id)
        f.close()

 
    driver.get("http://www.google.com/")
    
    print(session_id)
    print(executor_url)    
