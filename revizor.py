#!/usr/local/bin/python3
# coding: utf8
import pandas as pd
import re
import requests
import numpy as np
import urllib
import os
hearders = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}

def urlrequest(url,i):
    try:
       url_check = requests.get(url, timeout=(3, 5), headers=hearders)
       url_check.encoding = 'utf-8'
       url_check = url_check.text
       url_check2 = url_check[url_check.find('<title>') + 7: url_check.find('</title>')]
       #url_check=url_check2.encoding = 'utf-8'
       if str(requests.get(url,timeout=(3, 5)).status_code) == '200' and url_check2 != 'Доступ ограничен':
          with open('./uploads/log.txt', 'a') as file:
              file.write(url+'\n')
          print(url+ ' - Ресурс доступен!')
          clean_array2[i] = urllib.parse.urlsplit(url).netloc
       else:
          clean_array2[i] = str('empty')
    except:
        clean_array2[i] = str('empty')
def check_log():
    try:
       os.remove("./uploads/log.txt")
       os.remove("./uploads/named.log")
    except:
       return 0
check_log()
FILENAME = "./uploads/report.csv"
dft = pd.read_csv(FILENAME, encoding='cp1251', skiprows=16, delimiter=';', error_bad_lines=False)
df=dft
numpyMatrix = dft.values
j = np.delete(numpyMatrix, np.s_[0,1,2,3,4,6,7,8,10,11,12], axis=1)
t = len(j)
l=0
#print(t)
clean_array=np.arange(t, dtype=np.object)
while l < t:
        tm = str(j[l,1])
        if  tm != 'nan':
            p = str(j[l,1])
            clean_array[l] = re.search("(?P<url>https?://[^\s]+)", p).group("url").rstrip('/')
        else:
            p2 = str(j[l,0])
            if p2 != 'nan' and p2 != 'None':
                clean_array[l] = re.search("(?P<url>https?://[^\s]+)", p2).group("url").rstrip(',')
        l = l + 1
uniques = np.unique(clean_array)
df=uniques
n = len(df)
i=0
print('Всего ресурсов в реестре: '+ str(n))
clean_array2=np.arange(n, dtype=np.object)
while i < n:
    urlrequest(uniques[i],i)
    i = i + 1
    print('Обработано '+ str(i) + ' записей из ' + str(n))
#print(clean_array2)
clean_array = np.unique(clean_array2)
h = len(clean_array)
m=0
print('Проверка окончена!')
while m < h:
    url = str(clean_array[m])
    if url != 'empty':
        with open('./uploads/named.log', 'a') as file:
            file.write('zone "'+url+'" {type master; file "/etc/namedb/master/empty.db"; };\n')
    m = m + 1
