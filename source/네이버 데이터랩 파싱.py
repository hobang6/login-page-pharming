from selenium import webdriver
import requests
import time
import win32api
import os
import ctypes
import sys


def main():
    top_list = [[] for i in range(6)]
    delay = 0.5

    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('프로그램을 관리자 권한으로 실행해 주세요!\n')
        os.system('pause')
        sys.exit(0)

    chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

    if not os.path.isfile(chrome_path):
        print('크롬 브라우저를 설치 해주세요!\n')
        os.system('pause')
        sys.exit(0)

    chrome_info = win32api.GetFileVersionInfo(chrome_path, "\\")
    ms = chrome_info['FileVersionMS']
    ls = chrome_info['FileVersionLS']
    chrome_ver = "%d.%d.%d.%d" % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
    chrome_ver = chrome_ver[:2]

    stable_chrome = '<td style="white-space:nowrap; background:#a0e75a;"'
    latest_chrome_ver = requests.get('https://en.wikipedia.org/wiki/Google_Chrome_version_history').text
    ver_index = latest_chrome_ver.find(stable_chrome) + len(stable_chrome) + 1
    latest_chrome_ver = latest_chrome_ver[ver_index:ver_index + 2]

    if int(chrome_ver) < int(latest_chrome_ver):
        print('크롬 브라우저를 최신 버전으로 업데이트해주세요!\n')
        print('현재 버전 : ' + chrome_ver + '\t최신 버전 : ' + latest_chrome_ver + '\n')
        os.system('pause')
        sys.exit(0)

    temp_path = 'C:\driver_temp'
    driver_path = temp_path + '\\' + 'chromedriver' + chrome_ver + '.exe'

    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)

    if not os.path.isfile(driver_path):
        driver_url = 'https://raw.githubusercontent.com/hobang6/chromedriver/master/' + 'chromedriver' + chrome_ver + '.exe'
        print('다운로드 서버와 연결 중...')
        if requests.get(driver_url).status_code == 200:
            print('프로그램 구동에 필요한 파일을 다운로드하는 중입니다...')
            open(driver_path, 'wb').write(requests.get(driver_url, allow_redirects=True).content)
        else:
            print('파일을 다운로드하는 중 오류가 발생했습니다!\n')
            os.system('pause')
            sys.exit(0)

    url = 'https://datalab.naver.com/shoppingInsight/sCategory.naver?cid=50000003&where=shopping'  # 네이버 데이터 랩 전자제퓸 분야

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.get(url)

    print('연령대별 인기상품 가져오는 중...')

    for i in range(6):
        time.sleep(delay)
        driver.find_element_by_xpath('//*[@id="18_device_0"]').click()
        driver.find_element_by_xpath('//*[@id="19_gender_0"]').click()
        driver.find_element_by_xpath('//*[@id="20_age_0"]').click()

        time.sleep(delay)
        driver.find_element_by_xpath('//*[@id="20_age_0"]').click()
        age_path = '//*[@id="20_age_' + str(i + 1) + '"]'
        driver.find_element_by_xpath(age_path).click()

        time.sleep(delay)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/a').click()

        for j in range(5):
            time.sleep(delay)
            path = '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[' + str(j + 1) + ']'
            top_list[i].append(driver.find_element_by_xpath(path).text)
            top_list[i][j] = top_list[i][j][2:]

    for i in range(6):
        print('\n<' + str(i + 1) + '0대>')
        for j in range(5):
            print('Top' + str(j + 1) + ': ' + top_list[i][j])

    os.system('pause')


if __name__ == '__main__':
    main()
