import argparse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-k", "--key",required=True)
ap.add_argument("-t", "--to",required=True)
args = vars(ap.parse_args())

with open(sys.path[0]+"/no_git.txt",'r') as cg:
    myls=cg.read().split('\n')
key=args['key']
to=args['to']

pw=myls[3]
port=int(myls[0])
server_name=myls[1]
me=myls[2]
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
