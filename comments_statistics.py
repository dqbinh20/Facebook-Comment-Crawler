from selenium import webdriver
from selenium.webdriver.common.by import By
import openpyxl
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import requests
import os

wb_comment = openpyxl.Workbook()
cookies_object_list = []

def loadCookiesFile(filename):
    try:
        wb_cookie = openpyxl.load_workbook(filename)
        ws = wb_cookie.active
        for row in ws.iter_rows():
            cookies_object_list.append({"name": row[0].value, "value": row[1].value})
    except FileNotFoundError:
        print("Error: File 'cookies.xlsx' not found.")
    return cookies_object_list



def crawlAndSave(cookies_object_list):
    ##
    sheet_default = wb_comment.active
    sheet_default.cell(row=1, column=1).value = "Tên"
    sheet_default.cell(row=1, column=2).value = "Số lượng"
    row_sheet_default_index = 2
    
    ##
    driver = webdriver.Firefox()
    driver.get("http://www.facebook.com/")
    groupName = {}

    for cookies_object in cookies_object_list:
        cookies = []
        user_id = ""
        try:
            for item in cookies_object["value"].split("; "):
                name, value = item.split("=")
                if name == "c_user":
                    user_id = value
                cookies.append({"name": name, "value": value})
        except:
            continue

        # add cookie to browser
        for cookie in cookies:
            driver.add_cookie(cookie)
        

        # check cookie isvalid
        try:
            driver.get(f"http://www.facebook.com/{user_id}/allactivity?activity_history=false&category_key=COMMENTSCLUSTER&manage_mode=false&should_load_landing_page=false")        
            comment_history_tag = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[4]")))
            comments_tag = comment_history_tag.find_elements(By.XPATH,"div/div[2]/div[1]/div/a")
            numberCmt_pre = len(comments_tag)
            # 
        except TimeoutException:
            print("cookie error")
            continue

        # check date time
        from datetime import datetime
        try :
            dataComment = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[4]/div[1]/div/div/div/div/div/h2/span/span")
            dmy = dataComment.text.split(" ")
            if (int(datetime.now().strftime("%d"))!=int(dmy[0]) or int(datetime.now().strftime("%m"))!=int(dmy[2].replace(",","")) or int(datetime.now().strftime("%Y"))!=int(dmy[3])):
                print(cookies_object["name"], " Hôm nay chưa comment")
                sheet_default.cell(row=row_sheet_default_index, column=1).value = cookies_object["name"]
                sheet_default.cell(row=row_sheet_default_index, column=2).value = 0
                row_sheet_default_index += 1
                continue
        except:
            continue


        while True:
            time.sleep(2)
            comment_history_tag = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[4]")
            comments_tag = comment_history_tag.find_elements(By.XPATH,"div/div[2]/div[1]/div/a")
            if (len(comments_tag) == numberCmt_pre):
                # khoong conf cmt
                break
            numberCmt_pre = len(comments_tag)

        comments = {}
        link_list = []
        contents = []
        for i in comments_tag:
            contents.append(i.text.split("\n")[1])
            link_list.append(i.get_attribute("href").split("/"))
                
        for i in range(len(contents)):
            location = link_list[i][3]

            if link_list[i][3] == "groups":
                if link_list[i][4] not in groupName:
                    responseGroupUrl = requests.get(f"https://www.facebook.com/groups/{link_list[i][4]}")
                    groupName[link_list[i][4]] = responseGroupUrl.text.split('<title>')[1].split("</title>")[0]
                    print(groupName[link_list[i][4]])
                location = groupName[link_list[i][4]]                    

            if location not in comments:
                comments[location] = {}
            if contents[i] not in comments[location]:
                comments[location][contents[i]] = 0
            comments[location][contents[i]] += 1

        sheet_default.cell(row=row_sheet_default_index, column=1).value = cookies_object["name"]
        sheet_default.cell(row=row_sheet_default_index, column=2).value = len(contents)
        row_sheet_default_index += 1

        ws = wb_comment.create_sheet(cookies_object["name"])
        ws.cell(row=1, column=1).value = "Nơi comment"
        ws.cell(row=1, column=2).value = "Nội dung"
        ws.cell(row=1, column=3).value = "Số lượng"
        row_index = 2
        for location, content_dict in comments.items():
            ws.cell(row=row_index, column=1).value = location
            for content, count in content_dict.items():
                ws.cell(row=row_index, column=2).value = content
                ws.cell(row=row_index, column=3).value = count
                row_index += 1  # Move to the next row for the next comment
    
    wb_comment.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),"comments.xlsx"))
    print("Comments saved to comments.xlsx")
    driver.close()

loadCookiesFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.xlsx'))
crawlAndSave(cookies_object_list)
