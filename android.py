from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

app = Flask(__name__)

# Function to scrape Instagram followers count
def parse_data(s):
    data = {}
    s = s.split("-")[0]
    s = s.split(" ")
    data['Followers'] = s[0]
    return data

def scrape_data(username):
    URL = f"https://www.instagram.com/{username}/"
    r = requests.get(URL)
    s = BeautifulSoup(r.text, "html.parser")
    meta = s.find("meta", property="og:description")
    return parse_data(meta.attrs['content'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        
        # Initialize Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--display=:1") # localhost:1 -> display ID = 1
        driver = webdriver.Chrome(options=options)
        driver.get("https://instaavm.com/instagram-ucretsiz-takipci/")
        driver.maximize_window()

        # Fill out the form on the external site
        driver.find_element_by_xpath("/html/body/section[2]/div/div/div[2]/div/div[2]/form/div[1]/div/input").send_keys("Rastgele Kisi")
        driver.find_element_by_xpath("/html/body/section[2]/div/div/div[2]/div/div[2]/form/div[2]/div/input").send_keys("Bos Meslek")
        driver.find_element_by_xpath("/html/body/section[2]/div/div/div[2]/div/div[2]/form/div[3]/div/input").send_keys("Mukemmel bir site takipci kasmak icin, sizde deneyin")
        driver.find_element_by_xpath("/html/body/section[2]/div/div/div[2]/div/div[2]/form/div[3]/button").click()

        driver.find_element_by_xpath("/html/body/section[2]/div/div/div[1]/div/div[2]/form/div[1]/div[1]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/section[2]/div/div/div[1]/div/div[2]/form/div[2]/div/input").send_keys(45)
        driver.find_element_by_xpath("/html/body/section[2]/div/div/div[1]/div/div[2]/form/div[3]/button").click()

        # Wait for some time while scraping follower data
        a=140
        print("Basladi")
        while (a >= 0):
            print(a)
            time.sleep(1)
            a -= 1
        print("Bitdi")
        data = scrape_data(username)
        
        driver.close()
        
        return render_template('result.html', data=data)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
