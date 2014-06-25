# -*- coding: utf-8 -*-

import json
import urllib2
import sys 
import re


if len(sys.argv) != 2:
    print '$: <url>'
    sys.exit(0)

request = urllib2.Request(sys.argv[1])

try:
    jsonSource = urllib2.urlopen(request)
except (ValueError, urllib2.URLError) as e:
    print e
    sys.exit(0)
    
info = []
road = ""
#jsonSource = urllib.urlopen(sys.argv[1])
regexp = re.compile(r"{\"鄉鎮市區\":\"(?P<region>[^\"]+)\",[^,]+,\"土地區段[^\:]+:\"(?P<location>[^\"]+)\","
                    r"([^,]+,)+\"交易年月\":(?P<date>[0-9]+),([^,]+,)+\"總價元\":(?P<price>[0-9]+)")
    
for line in jsonSource.readlines():
   index = 0
   result = regexp.match(line)
   if result:
      location = result.group('location')
      
      if location.find('路')!=-1 and location.find('巷')!=-1:
         index = location.find('路')
         road = location[0:index+3]
      elif location.find('街')!=-1 and location.find('巷')!=-1:
         index = location.find('街')
         road = location[0:index+3]
      else:
        if location.find('路')!=-1:
            index = location.find('路')
            road = location[0:index+3]  
        elif location.find('街')!=-1:
            index = location.find('街')
            road = location[0:index+3]  
        elif location.find('巷')!=-1:
            index = location.find('巷')
            road = location[0:index+3]  
        else:
            continue
      
      date = result.group('date')
      price = int(result.group('price'))
      match = False
      
      for i in range(len(info)):
         if info[i]['road']==road:
            match = True
            if date not in info[i]['date']:
               info[i]['date'].append(date)
            if price < info[i]['lowPrice']:
               info[i]['lowPrice'] = price
            if price > info[i]['highPrice']:
               info[i]['highPrice'] = price
      
      if match == False:
         newInfo = {'road': road, 'date': [date], 'lowPrice': price, 'highPrice': price }
         info.append(newInfo)

maxCount = 0
for j in info:
    lenOfTime = len(j['date'])
    if lenOfTime>maxCount:
        maxCount = lenOfTime

for j in info:
    lenOfTime = len(j['date'])
    if lenOfTime == maxCount:
        print j['road'] + ', ' + '最高成交價: ' + str(j['highPrice']) + ', ' + '最低成交價: ' + str(j['lowPrice'])

jsonSource.close()


