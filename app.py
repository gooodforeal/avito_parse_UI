from tkinter import *
from tkinter import messagebox

import openpyxl
import os
import random

from openpyxl.workbook.workbook import Workbook
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# app
app = Tk()

# func
def btn():
    search = search_inp.get()
    place = city_inp.get()
    reps = pages_inp.get()

    if search and place and reps:
        messagebox.showinfo('Working', 'Program is working, dont close!')

        reps = int(reps)

        options = webdriver.ChromeOptions()

        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "chromedriver.exe")

        driver = webdriver.Chrome(
            executable_path=path,
            options=options
            )

        url = "https://www.avito.ru/"


        try:
            print("[+] Searching...")

            driver.get(url=url)

            search_input = driver.find_element_by_class_name("input-input-Zpzc1")
            # search_input = driver.find_element_by_xpath('//*[@id="downshift-2095-input"]')
            search_input.clear()
            search_input.send_keys(search)

            #region_btn = driver.find_element_by_class_name("main-text-g_qrO")
            region_btn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[5]/div[1]/span/span/div/div')
            region_btn.click()

            region_input = driver.find_element_by_class_name("suggest-input-rORJM")
            # region_input = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div/div[6]/div/div/span/div/div[1]/div[2]/div/input')
            region_input.clear()
            region_input.send_keys(place)

            show_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div/div[6]/div/div/span/div/div[3]/div[2]/div/button').click()

            page = 1

            search = search.replace(" ", "+")
            cur_url = driver.current_url
            ur1, ur2 = cur_url.split("?")

            print("[+] Collecting urls...")

            hrefs = []

            rep = 0

            while page <= reps:
                work_url = f"{ur1}?p={page}&q={search}"
                driver.get(url=work_url)

                cards = driver.find_elements_by_class_name("iva-item-content-UnQQ4")

                if len(cards):
                    for card in cards:
                            href = card.find_element_by_class_name("iva-item-body-R_Q9c").find_element_by_class_name("iva-item-titleStep-_CxvN").find_element_by_tag_name("a").get_attribute("href")
                            hrefs.append(href)
                    print(f"[+] {page} collected...")
                    page += 1
                else:
                    break

            print("[+] Saving...")

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Название", "Цена", "Имя продавца", "Дата публикации", "Ссылка"])

            count = 0

            for href in hrefs:
                driver.get(url=href)

                try:
                    title = driver.find_element_by_class_name("title-info-title-text").text.strip()
                    link = href
                except:
                    title = " "
                    link = " "
                try:
                    seller = driver.find_element_by_class_name("seller-info-name").find_element_by_tag_name("a").text.strip()
                except:
                    seller = " "
                try:
                    price = driver.find_element_by_xpath('//*[@id="price-value"]/span/span[1]').get_attribute("content") + " ₽"
                except:
                    price = " "
                try:
                    date = driver.find_element_by_class_name("title-info-metadata-item-redesign").text.strip()
                except:
                    date = " "

                ws.append([title, price, seller, date, link])

                count += 1
                print(f"[+] {count} broadcast done...")

            ws.column_dimensions["A"].width = 60
            ws.column_dimensions["C"].width = 15
            ws.column_dimensions["D"].width = 20
            ws.column_dimensions["E"].width = 150

            wb.save(f"res{random.randint(1, 1000)}.xlsx")

        except Exception as e:
            print(e)
        finally:
            print("[+] finishing...")
            driver.close()
            driver.quit()
    else:
        messagebox.showerror('Eror', 'Wrong enter!')


# settings
app['bg'] = '#121624'  # Background
app.title('Avito Parse by Pikassoo') # Title
app.geometry("300x225") # Resolution
app.resizable(width=False, height=False) # Resizebleness

# canvas = Canvas(app, width=500, height=300) # To add widgets
# canvas.pack() # Accept canvas

# frame = Frame(app, bg="#121624") # Working area inside window
# frame.place(relwidth=1, relheight=1) # frame sizing

#Widgets
title = Label(app, text='AVITO PARSER', font='Comfortaa 20', bg='#121624', fg='white') # Title text
title1 = Label(app, text='Запрос:', font=200, bg='#121624', fg='grey') # Title text
search_inp = Entry(app, bg='#166272')
title2 = Label(app, text='Город:', font=200, bg='#121624', fg='grey') # Title text
city_inp = Entry(app, bg='#166272')
title3 = Label(app, text='Сколько страниц:', font=200, bg='#121624', fg='grey') # Title text
pages_inp = Entry(app, bg='#166272')
btn = Button(app, text='Start', bg="#3C4555", command=btn, width=20, fg="white", font='10') # Button

# Pack
title.pack() # Accept title
title1.pack() # Accept title
search_inp.pack()
title2.pack() # Accept title
city_inp.pack()
title3.pack() # Accept title
pages_inp.pack()
btn.place(x = 55, y=180) # Accept button


app.mainloop() # App run
