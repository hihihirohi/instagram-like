# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import time

import urllib.parse
import urllib.request

browser = webdriver.Chrome()

#ログインすページ
loginURL = "https://www.instagram.com/" 
#タグのURL
tagSearchURL = "https://www.instagram.com/explore/tags/{}/?hl=ja"

#調べたいタグ
tagName = "好きなタグ" 

#ログイン時の使用Path
loginPath = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'
usernamePath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input'
passwordPath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input'

#ログイン後のダイアログ表示を閉じる
pushPath = '/html/body/div[3]/div/div/div[3]/button[2]'

#投稿してある写真の場所
mediaPath = 'div.eLAPa' 

#イイネボタン
likeXpath = '/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span'

#次へボタン
nextPagerSelector = 'a.coreSpriteRightPaginationArrow'

#USER情報
username = "電話番号またはユーザー名"
password = "パスワード" 

#list
mediaList = []

#counter

likedCounter = 0

if __name__ == '__main__':

    #ログイン時の処理
    #使用するURLの取得
    browser.get(loginURL)
    time.sleep(3)

    #ログインフォ-ムに遷移
    browser.find_element_by_xpath(loginPath).click()
    time.sleep(3)

    #ログインフォームにあるユーザー情報の入力
    usernameField = browser.find_element_by_xpath(usernamePath)
    usernameField.send_keys(username)
    passwordField = browser.find_element_by_xpath(passwordPath)
    passwordField.send_keys(password)

    passwordField.send_keys(Keys.RETURN)

    #
    time.sleep(3)
    browser.find_element_by_xpath(pushPath).click()

    encodedTag = urllib.parse.quote(tagName) #普通にURLに日本語は入れられないので、エンコードする
    encodedURL = tagSearchURL.format(encodedTag)
    print("encodedURL:{}".format(encodedURL))
    browser.get(encodedURL)

    #Finished tag search. now at https://www.instagram.com/explore/tags/%E8%AA%AD%E5%A3%B2%E3%83%A9%E3%83%B3%E3%83%89/?hl=ja
    time.sleep(3)
    browser.implicitly_wait(10)

    #写真を取得してクリックする
    mediaList = browser.find_elements_by_css_selector(mediaPath)
    mediaCounter = len(mediaList)

    print("Found {} media".format(mediaCounter))

    for media in mediaList:
        media.click()

        # 次へボタンが表示されるまで
        while True:
            try:
                time.sleep(3)
                browser.find_element_by_xpath(likeXpath).click()
                browser.implicitly_wait(10)
                likedCounter += 1
                print("liked {} of {}".format(likedCounter,mediaCounter))
                browser.find_element_by_css_selector(nextPagerSelector).click()
            except:
                #もう次へボタンが存在しない場合、エラーをはくのでそこで終了
                break 
        #for文自体も終了させる
        break 

    print("You liked {} media".format(likedCounter))