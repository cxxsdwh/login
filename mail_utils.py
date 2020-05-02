import numpy as np
import time
mail_n=100
mail_dt=3600
mail_ls=['' for i in range(mail_n)]
mail_key=np.zeros(mail_n,dtype=int)
mail_try=np.zeros(mail_n,dtype=int)
mail_time=np.zeros(mail_n,dtype=int)
def push_mail(addr):
    if addr in mail_ls:
        tmp_n= mail_ls.index(addr)
    else:
        tmp_n=np.argmin(mail_time)
        mail_ls[tmp_n]=addr
    key_int=np.random.randint(0,1000000)
    key_str="{:06d}".format(key_int)
    mail_key[tmp_n]=key_int
    mail_time[tmp_n]=int(time.time())
    mail_try[tmp_n]=0
    return key_str
def check_mail(addr,key):
    global mail_try
    if addr not in mail_ls:
        return False
    tmp_n= mail_ls.index(addr)
    if mail_key[tmp_n]==int(key) and mail_try[tmp_n]<=5 and (int(time.time())-mail_time[tmp_n])<mail_dt:
        return True
    else:
        if mail_try[tmp_n]<=5:
            mail_try[tmp_n]+=1
        return False
