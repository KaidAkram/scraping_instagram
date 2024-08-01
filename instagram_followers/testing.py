
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


username =input("Enter your username: ")
passwor = input("Enter your password: ")
account = input("Enter the name of the account: ")
#the path of the chromedriver you just downloaded.
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


#log in to instagaram

def login_instagram(username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    
    #enter username
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(username)
    
    #enter password
    
    password_input= driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
   
    #log in 
    login_button = driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[3]/button")
    login_button.click()
    time.sleep(3)
    
    #wait until the main page is loaded 
    plus_tard = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(), 'Plus tard')]")))
    plus_tard.click() 
    time.sleep(20)
    



def open_followers(username):
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(3)
    
    #click on the followers link
    followers_link = driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
    followers_link.click()
    
    
    #wait for tbe followers page to load
    WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2] ")))
    




def scrape_followers():
    followers_list = driver.find_elements(By.XPATH, "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
    number_followers = driver.find_element(By.XPATH, "//*[@id='mount_0_0_PB']/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a/span/span/span").text
    number_followers = int(number_followers.replace(",", ""))
    action_chain = ActionChains(driver)
    followers = set()
    
    while len(followers) < number_followers:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_list)
        time.sleep(2)
        
        follower_elements = driver.find_elements(By.XPATH, "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div")
        
        for follower in follower_elements:
            followers.add(follower.get_attribute('title'))
            
        if len(followers) >= number_followers:
            break
        
    return followers



    


def main():
   
    login_instagram(username, passwor)
    open_followers(account)
    followers = scrape_followers()
    print(followers)
    
    


if __name__ == "__main__":
    main()