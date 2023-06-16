import os 
import smtplib
import imghdr
from email.message import EmailMessage

import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

email_address = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASS')

msg = EmailMessage()

yf.pdr_override()
start = dt.datetime(2023,1,1)
now = dt.datetime.now()

stock = "Enter the symbol of stock of your choice"
target_price = 123 # Enter the target price according to the stock

msg["Subject"] = "Alert on" + stock
msg["From"] = email_address
msg["To"] = "youremailaddress@gmail.com" # enter your email address on which you want alert

alerted = False

while 1:
    df = pdr.get_data_yahoo(stock, start, now)
    current_close = df["Adj Close"][-1] #current price of the stock
    
    # print(current_close)
    
    condition = current_close>target_price
    
    if(condition and alerted == False):
        alerted = True
        message = stock + " Has activated the alert price of " + str(target_price) + "\n Current Price: "+str(current_close)
        
        # print(message)
        
        msg.set_content(message)
        
        files=[r"Enter the path of excel file"]
        
        for file in files:
            with open(file,"rb") as f:
                file_data = f.read()
                file_name="Enter the name of file. "
                
                msg.add_attachment(file_data, maintype="application",subtype='ocetet-stream',filename=file_name)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
            
            # print("Completed")
        
    else:
        print("No New Alerts!")
    
    time.sleep(60)
