import smtplib

s = smtplib.SMTP("smtp.gmail.com", 587) # SMTP 서버 설정
s.ehlo()

s.starttls()
s.ehlo()
s.login("mightyrh@gmail.com","i'msofast")