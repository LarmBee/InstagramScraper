# Instagram Scraper in Python using Selenium
# Scraper logs into Instagram and Inputs the username in the search box
# Data collected is Name ,Followers ,Following ,Posts_URL


import selenium
import time
import urllib.request
import os
import wget
import requests

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Launch Chrome and navigate to the Instagram Page

driver = webdriver.Chrome("C:/chromedriver_win32/chromedriver.exe")
driver.get("https://www.instagram.com")

username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

# clear the input boxes
username.clear()
password.clear()

# input username and password
username.send_keys("")  # Your username i.e ("Peter")
password.send_keys("")  # Your password goes here

# login button auto click
log_in = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()
# not now auto click (Save login info )
not_now = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
# not now auto click (Turn on notifications)
not_now2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Not Now')]"))).click()

# navigate to the search box input
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))

search_box.clear()

# The user name we are searching
keyword = "nike"
search_box.send_keys(keyword)
search_box.send_keys(Keys.ENTER)

# select first result from search box
first_result = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, '-qQT3')))
first_result.click()

# get username
name = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/h2')))

print("Username: " + name.text)

# get number of posts
posts = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'g47SY')))
print("Posts: " + posts.text)

# number of followers
followers = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span")))
print("Number of Followers: " + followers.text)

# number of following
following = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span")))
print("Number of Following: " + following.text)

time.sleep(2)
# scroll for more images
driver.execute_script("window.scrollTo(0,4000)")
time.sleep(1)
driver.execute_script("window.scrollTo(0,4000)")

# posts url

posts = []
links = driver.find_elements_by_tag_name('a')
for link in links:
    post = link.get_attribute('href')
    if '/p/' in post:
        posts.append(post)


download_url = []
for post in posts:
    headers = {'User-Agent': 'Mozilla'}
    r = requests.get('{}?__a=1'.format(post), headers=headers)
    data = r.json()['graphql']['shortcode_media']
    shortcode = data['shortcode']
    is_video = data['is_video']
    if is_video:
        download_url.append('This is a video file')
    else:
        download_url.append('This is an image file')

# joins the two lists together side by side
links = [''.join(x) for x in zip(posts, download_url)]

# prints links and whether the post is a video file or an image file
print(links)
