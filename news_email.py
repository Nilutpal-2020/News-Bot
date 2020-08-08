import requests
import bs4
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import secrets  # CREATE A secrets.py file and add your credentials there
import schedule
import time
import datetime
# import getpass


def main():
    res = requests.get("https://www.theatlantic.com/world/")
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    news_dict = {}
    for news in soup.select('.c-tease__link'):
        news_dict[news.getText()] = news['href']

    headlines = ''
    n = 1
    for key, val in news_dict.items():
        headlines += f"{n}. {key} |  {val} \n"
        n += 1

    # Save the headlines into a file:
    today = datetime.datetime.now()
    date = today.strftime("%d %A %Y %X")

    with open("HEADLINES.docx", mode='a', encoding='utf-8') as f:
        f.write(f"\nTHE ATLANTIC HEADLINES ({date})\n\n{headlines}")

    # Send Email
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()
    smtp_object.starttls()

    # email = input('Enter your email: ')
    # password = getpass.getpass("Enter your password: ")
    email = ''  # secrets.email  # Enter your email here
    password = ''  # secrets.password  # Enter your app password here
    # App password can be generated here 'myaccount.google.com/security'
    smtp_object.login(email, password)

    from_address = email
    to_address = ''  # ENTER YOUR DESTINED EMAIL HERE
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "THE ATLANTIC HEADLINES"
    msg['From'] = from_address
    msg['To'] = to_address

    text = headlines

    part = MIMEText(text, 'plain')
    msg.attach(part)

    smtp_object.sendmail(from_address, to_address, msg.as_string())
    smtp_object.quit()
    print("Email sent successfully to : " + to_address)


# schedule.every().day.at("11:00").do(main)
schedule.every(1).minutes.do(main)

while True:
    schedule.run_pending()
    localtime = time.localtime()
    result = time.strftime("%I: %M: %S %p", localtime)
    print(result)
    time.sleep(60)  # sleep for 60 seconds
    # time.sleep(86400) # sleep for 1 day

if __name__ == '__main__':
    main()
