import requests, sys
from bs4 import BeautifulSoup
from gooey import Gooey
from argparse import *
import time
# from IPython.display import clear_output
import smtplib

flg = True
try:

    def send_mail(url, email):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('pricemon007@gmail.com', 'Abcd@123')

        subject = 'Price Fell Down'
        body = 'Check Amazon link ' + url

        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail(
            'pricemon007@gmail.com',
            email,
            msg
        )
        print('email has been sent')
        flg = False
        server.quit()


    @Gooey
    def main():

        parser = ArgumentParser()
        parser.add_argument('-URL', '--URL', help='Paste URL here!', type=str, required=True)
        parser.add_argument('-y', '--target', help='Enter your required price', type=str, required=True)
        parser.add_argument('-t', '--email', help='Enter your email Id', type=str, required=True)
        args = parser.parse_args()
        arguments = vars(args)
        records = []
        records.append(arguments)
        for i in records:
            if i['URL']:
                url = i['URL']
            if i['target']:
                target = i['target']
            if i['email']:
                email = i['email']
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        if soup.find(id='priceblock_dealprice'):
            discount = soup.find(id='priceblock_dealprice').get_text()
            discount = discount[1:]
            discount = discount.strip()
            discount = discount.replace(',', '')
            discount = float(discount)
            print("dis", discount)
            if discount < float(target):
                send_mail(url, email)
                flg = False
            else:
                print('Nope')
                flg = True

        else:
            price = soup.find(id='priceblock_ourprice').get_text()
            price = price[1:]
            price = price.strip()
            price = price.replace(',', '')
            price = float(price)
            print("pri", price)

            if price < float(target):
                send_mail(url, email)
                flg = False
            else:
                flg = True
        return flg


    if __name__ == '__main__':
        while flg:
            flg = main()
            time.sleep(5)
except:
    print("Some error has occured!!")