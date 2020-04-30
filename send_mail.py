import argparse
import smtplib
from email.mime.text import MIMEText
from email.header import Header

ap = argparse.ArgumentParser()
ap.add_argument("-k", "--key",required=True)
ap.add_argument("-t", "--to",required=True)
args = vars(ap.parse_args())
key=args['key']
to=args['to']

pw='Cxx@990104'
port=465
server_name='smtp.exmail.qq.com'
me='master@econometrica.cn'
you = to
text="验证码:"+str(key)
msg = MIMEText(text, 'plain')
msg['From'] = Header('"Chen" <'+me+'>')
msg['To'] = Header(you)
msg['Subject'] = Header("验证码:"+str(key),'utf-8')#subjec
server = smtplib.SMTP_SSL()
server.connect(server_name,port)
server.login(me, pw)
server.sendmail(me, you, msg.as_string())
server.quit()
