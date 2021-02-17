import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import smtplib
from tkinter import messagebox
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


def exit():
    messagebox.askquestion("Çıkış", "Emin Misin ?")
    quit()
def getstock(entry_stock):
    stock = entry_stock
    PATH = "C:/Program Files (x86)/chromedriver.exe"

    driver = webdriver.Chrome(PATH)
    driver.minimize_window()
    driver.get("http://google.com")
    search = driver.find_element_by_name("q")
    search.send_keys(f"{stock} hisse")
    search.send_keys(Keys.RETURN)
    time.sleep(0.5)
    stockCode1 = driver.find_element_by_xpath(
        "//*[@id='knowledge-finance-wholepage__entity-summary']/div/g-card-section/div/g-card-section/div[1]/div[1]/div[2]")
    value1 = driver.find_element_by_xpath(
        "//*[@id='knowledge-finance-wholepage__entity-summary']/div/g-card-section/div/g-card-section/span[1]/span/span[1]")
    dayMax1 = driver.find_element_by_xpath(
        "//*[@id='knowledge-finance-wholepage__entity-summary']/div/div/g-card-section[2]/div/div/div[1]/table/tbody/tr[2]/td[2]")
    dayMin1 = driver.find_element_by_xpath(
        "//*[@id='knowledge-finance-wholepage__entity-summary']/div/div/g-card-section[2]/div/div/div[1]/table/tbody/tr[3]/td[2]")
    change_percent1 = driver.find_element_by_xpath(
        "//*[@id='knowledge-finance-wholepage__entity-summary']/div/g-card-section/div/g-card-section/span[2]/span[2]/span[1]")
    change1 = driver.find_element_by_xpath(
        "//*[@id='knowledge-finance-wholepage__entity-summary']/div/g-card-section/div/g-card-section/span[2]/span[1]")
    opening1 = driver.find_element_by_xpath(
        "//*[@id='knowledge-finance-wholepage__entity-summary']/div/div/g-card-section[2]/div/div/div[1]/table/tbody/tr[1]/td[2]")
    stockCode2 = str(stockCode1.text)
    stockCode = stockCode2[5::1]

    value = str(value1.text)
    dayMax = str(dayMax1.text)
    dayMin = str(dayMin1.text)
    change_percent = str(change_percent1.text)
    change = str(change1.text)
    opening = str(opening1.text)
    sign = change[0]
    driver.close()
    label['text'] = f"Hisse Adı: {stockCode}\n\nAçılış: {opening} ₺\nGüncel Değer: {value} ₺\nGün içi en yüksek: {dayMax} ₺\nGün içi en düşük: {dayMin} ₺\nDeğişim(%): {sign}{change_percent}\nDeğişim: {change} ₺ "

def graphWindow(entry_stock):
    graphstock = entry_stock
    graphPage = tk.Toplevel(root)
    graphPage.geometry("500x500")
    graphPage.title("Grafik")
    fig = Figure(figsize=(5, 4), dpi=100)

    PATH = "C:/Program Files (x86)/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    my_url = 'https://www.google.com/'
    driver.get(my_url)
    search = driver.find_element_by_name("q")
    search.send_keys(f"{graphstock} hisse")
    search.send_keys(Keys.RETURN)

    month = driver.find_element_by_xpath(
        "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section[1]/div/div[1]/div/div[3]/div/div/div/div")
    month.click()
    action = webdriver.ActionChains(driver)
    time.sleep(2)
    element = driver.find_element_by_xpath(
        "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section[1]/div/div[2]/div/div")

    location = element.location
    size = element.size


    action.move_to_element_with_offset(element, 651, 0).perform()
    date = driver.find_element_by_xpath(
        "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section[1]/div/div[2]/div/div/div[1]/span[4]").text
    value = driver.find_element_by_xpath(
        "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section[1]/div/div[2]/div/div/div[1]/span[1]").text

    print(value, date)

    dictionary = {}
    dictionary[value] = date
    data = []
    pace = -33
    i = 0
    while i < 8:

        action.move_by_offset(pace, 0).perform()
        date = driver.find_element_by_xpath(
            "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section[1]/div/div[2]/div/div/div[1]/span[4]").text
        value = driver.find_element_by_xpath(
            "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/g-card-section[1]/div/div[2]/div/div/div[1]/span[1]").text
        i = i + 1

        real_len = len(value) - 4

        data.insert(i, str(value[:real_len:1]))

        if value in dictionary:
            pass
        else:
            dictionary[value] = date
    print(data)
    new_dot = []
    new_data = []
    i = 0
    while i < len(data):
        if "." in data[i]:
            new_dot.insert(i, data[i].replace(".", ""))
            new_data.insert(i, float(new_dot[i].replace(",", ".")))
        else:
            new_data.insert(i, float(data[i].replace(",", ".")))
        i += 1

    print(type(new_data[0]))
    print(new_data)

    driver.quit()

    def createGraphlist(n):
        return list(range(1, n + 1))

    value_graphlist = []

    i = 0
    while i < len(new_data):
        value_graphlist.insert(i, new_data[(len(new_data) - 1) - i])
        i += 1


    fig.add_subplot(111).plot(createGraphlist(len(data)), value_graphlist)
    ganvas=FigureCanvasTkAgg(fig, master=graphPage)
    fig.suptitle(f"{entry_stock} Grafik", fontsize=16)
    ganvas.draw()
    ganvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(ganvas, graphPage)
    toolbar.update()
    ganvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_key_press(event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, ganvas, toolbar)

    ganvas.mpl_connect("key_press_event", on_key_press)





def mailWindow():

    mailPage= tk.Toplevel(root)
    mailPage.geometry('250x200')
    mailPage.title("Mail Gönder")
    receiver_mail = tk.Entry(mailPage)
    receiver_mail.place(relx=0.1 , rely=0.1, relwidth=0.75, relheight=0.1)
    send_mail = Button(mailPage,text="Mail Gönder",command=lambda:sendMail(receiver_mail.get()) )
    send_mail.place(relx=0.1,rely=0.3)

    def sendMail(receiver_mail):
        sender = "hissebotu41@gmail.com"
        password = "cwxuagvgihqfbzam"
        subject = "Hisse Bildirimi"
        body = label['text'] + "\nBu mail 'serkan Yazılım' tarafından bilgilendirme amacıyla gönderilmiştir. Tüm veriler ve bilgiler, yalnızca kişisel bilgilendirme amacıyla olduğu gibi sağlanmıştır ve alım satım amaçlı veya yatırım, vergi, yasal, muhasebe veya  diğer konularda tavsiye niteliğinde değildir."
        msg = f'Subject: {subject}\n\n{body}'

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver_mail, msg.encode('utf-8'))
            messagebox.showinfo("Mail Bilgisi", f"Bilgiler {receiver_mail} adresine gönderilmiştir")



root = tk.Tk()
root.title("Hissetör V.2")
canvas = tk.Canvas(root, width=440, height=330, bg='#80c1ff')
canvas.pack()
background_image= tk.PhotoImage(file='test4.png')
background_label = tk.Label(root,image=background_image)
background_label.place(relwidth=1, relheight=1)

entry_stock = tk.Entry(root,font=('calibre',10, 'bold'))
entry_stock.place(relx=0.1 , rely=0.1, relwidth=0.45, relheight=0.08)

value_Button = tk.Button(root, text="Hisse Bildisi",bg='grey',command= lambda: getstock(entry_stock.get()))
value_Button.place(relx=0.6,rely=0.1, relwidth=0.2, relheight=0.07)
mail = tk.Button(root, text="Mail Gönder !",bg="grey",command=mailWindow)
mail.place(relx=0.6,rely=0.4, relwidth=0.2, relheight=0.07)
exit = tk.Button(root, text="Çıkış !", bg ='red',command=exit)
exit.place(relx=0.6,rely=0.65, relwidth=0.2, relheight=0.07)
graphic= tk.Button(root, text="Grafik",bg="grey",command= lambda: graphWindow(entry_stock.get()))
graphic.place(relx=0.6, rely=0.25, relwidth=0.2,relheight=0.07)


label = tk.Label(root,font=('calibre',11, 'bold'))
label.place(relwidth=0.45, relheight=0.6,relx=0.1,rely=0.2)

label2 = tk.Label(root,font=('calibre',8, 'bold'),text="Serkan Yazılım© 2020 ")
label2.place(relwidth=0.26, relheight=0.06,relx=0.72,rely=0.94)
root.mainloop()