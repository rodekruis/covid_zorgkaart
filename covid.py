# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:01:26 2020

@author: ATeklesadik
"""
""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import math
########################## check current active typhoons in PAR and send email alert 


    #%% per city 
GDC_code = pd.read_csv('/P01_rk_branch_locations/data/DAC_gemmente.csv',sep=';')
DAC='Gelderland-Midden'
list_gemments=GDC_code[GDC_code['naam']==DAC]['statnam'].values

#%% per city 
url='https://www.zorgkaartnederland.nl/overzicht/plaatsen'
res_s = requests.get(url)
soup = BeautifulSoup(res_s.content,'html.parser')
output1=[]
for items in soup.find_all('li', class_="list-group-item"):
    item=items.find('a',href=True)
    link_item='https://www.zorgkaartnederland.nl'+item['href']
    #output['{}'.format(item['title'])]=link_item
    try:
        found = re.search('\((.+?)\)', items.text.split(' ')[-1]).group(1)
        city = items.text.split(' ')[-2]
    except AttributeError:
        found = '' # apply your error handling
        city='NA'
    print(city,found)
    pages_no = math.ceil(int(found)/20) if math.ceil(int(found)/20) < 9000 else 1000
    if city in list_gemments:     
        for elm in range(1,pages_no+1):            
            url_s=link_item +'/pagina{}'.format(elm)
            res_s = requests.get(url_s)
            soup_s = BeautifulSoup(res_s.content,'html.parser')
            for items2 in soup_s.find_all('li', class_="media"):
                list1=[]
                list1.append(city)
                item2=items2.find('a',href=True)
                item3=items2.find('span',class_="context").get_text().replace("\n", "").replace("    ", "") 
                list1.append(item3)                                       
                link_item2='https://www.zorgkaartnederland.nl'+item2['href']
                #res_s2 = requests.get(link_item2)
                #soup_s2 = BeautifulSoup(res_s2.content,'html.parser')
                #location=soup_s.find_all('span', class_="context") 
                #list1.extend([k for k in [name.get_text().replace("\n", "").replace(" ", "") for name in soup_s2.find_all('span', class_="address_content")]])
                #Address=[name.get_text().replace("\n", "").replace(" ", "") for name in soup_s2.find_all('span', class_="address_content")]
                #try:
                 #   tele_no=soup_s2.find('span', itemprop="telephone").text
                #except:
                   # tele_no='NA'
                #organization_name=soup_s2.find('div', class_="organization_title_holder").find('span', itemprop="name").text
                
                #list1.append(organization_name)
                #list1.append(tele_no)
                for items_1 in items2.find_all('div', class_="location"):
                    lat_lon=items_1['data-location']
                    pra_name=items_1['data-title']
                    pra_con=items_1.get_text().replace("\n", "").replace("    ", "")
                    list1.append(pra_name)
                    list1.append(pra_con)
                    list1.append(lat_lon)
            if (len(list1) >1):
                output1.append(list1)
#%% save the file   
fname=open("/P01_rk_branch_locations/data/DAC_Gelderland-Midden.txt",'w')
fname.write('"place";"services";"name";"location";"lat-lon"'+'\n')
for items in output1:
    if (len(items) >2):
        fname.write(';'.join([str(elem) for elem in items])+'\n') 
fname.close()
  
#%% for service provide
# make sure the list of service providers has the name of all the services we need data for 
service_list=["Verpleeghuis en verzorgingshuis",
"Woonvoorziening voor lichamelijk gehandicapten",
"Woonvoorziening voor verstandelijk gehandicapten",
"Woonvoorziening voor visueel gehandicapten",
"Instelling voor auditief gehandicapten",
"Instelling voor lichamelijk gehandicapten",
"Instelling voor verstandelijk gehandicapten",
"Instelling voor visueel gehandicapten",
"Hospice",
"GGD",
"Huisartsenpost",
"Huisartsenpraktijk",
"Zorghotel",
"Geriatrische revalidatiezorg",
"ziekenhuis"]

url='https://www.zorgkaartnederland.nl/overzicht/organisatietypes'
list1=[]
time_counter=0
res_s = requests.get(url)
soup = BeautifulSoup(res_s.content,'html.parser')
for items1 in soup.find_all('section', class_="content_section"):
    for items2 in items1.find_all('ul', class_="list-group col-lg-6"):
        for items3 in items2.find_all('li', class_="list-group-item"):
            item=items3.find('a',href=True)
            service_type=item.text
            if service_type in service_list:             
                link_item='https://www.zorgkaartnederland.nl'+item['href']
                found = re.search('\((.+?)\)', items3.text.split(' ')[-1]).group(1)
                pages_no = math.ceil(int(found)/20) if math.ceil(int(found)/20) < 9000 else 1000
                for elm in range(1,pages_no+1):
                    if time_counter >1000: # to avoid the get.request error
                        time.sleep(1)
                        time_counter=0
                    url_s=link_item +'/pagina{}'.format(elm)
                    res_s = requests.get(url_s)
                    soup_s = BeautifulSoup(res_s.content,'html.parser')
                    for items4 in soup_s.find_all('li', class_="media"):
                        lat_lon=items4['data-location']
                        items5=items4.find('div',class_="media-body")
                        service_naam=items5.find('h4',class_="media-heading title orange").get_text().replace("\n", "")
                        item6=items5.find('a',href=True)
                        Locatie=items5.find('span',class_="context").get_text()
                        #print(service_type,service_naam,Locatie,lat_lon)
                        service_info=service_type+";"+service_naam+";"+Locatie+";"+lat_lon
                        list1.append(service_info)
                        #item3=items2.find('span',class_="context").get_text().replace("\n", "").replace("    ", "") 
                        #list1.append(item3)                                       
#%%  for service provide
                        
fname=open("/RK capacity/P01_rk_branch_locations/data/GDC_content2.txt",'w')
fname.write('"service_type";"service_naam";"Locatie";"lat-lon"'+'\n')
for items in list1:
        fname.write(items+'\n') 
fname.close()                      



#%% for telephone number
'''
url='https://www.zorgkaartnederland.nl/zorginstelling'
output1=[]
for elm in range(1,2529):
    url_s=url +'/pagina{}'.format(elm)
    res_s = requests.get(url_s)
    soup_s = BeautifulSoup(res_s.content,'html.parser')
    for items in soup_s.find_all('li', class_="media"):
        list1=[]
        item2=items.find('a',href=True)
        lat_lon=items['data-location']
        link_item2='https://www.zorgkaartnederland.nl'+item2['href']
        res_s2 = requests.get(link_item2)
        soup_s2 = BeautifulSoup(res_s2.content,'html.parser')
        list1.extend([k for k in [name.get_text().replace("\n", "").replace(" ", "") for name in soup_s2.find_all('span', class_="address_content")]])
        #Address=[name.get_text().replace("\n", "").replace(" ", "") for name in soup_s2.find_all('span', class_="address_content")]
        try:
            tele_no=soup_s2.find('span', itemprop="telephone").text
        except:
            tele_no='NA'
        list1.append(tele_no)
        organiz=soup_s2.find('div', class_="organization_title_holder").find('span', itemprop="name").text
        list1.append(organiz)
        list1.append(lat_lon)
        output1.append(list1)


 
    #item=items.find('div', class_="left_media_holder icon_holder")

'''
