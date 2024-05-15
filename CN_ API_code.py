from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
import os

data_final = pd.DataFrame(
    columns=['website', 'hop_number', 'ip', 'asn', 'isp', 'organisation', 'latitude', 'longitude', 'domain_name'])
destination = ['facebook.com' , 'yahoo.com' , 'instagram.com' , 'knowyourmeme.com' , 'cdn.net' , 'apple.com' , 'cloudflare.com' , 'google.com' ,'cloud.tencent.com' ]
for websites in destination:

    command = f'traceroute -6 {websites}'
    abc = os.popen(command).read()
    abc_list = abc.split('\n')
    print(abc_list)
    ip_list = []
    count = 0
    source_ip = ""
    hops_not_RTO = []
    for i in abc_list:
        ip_dum = ""
        check = 0
        for j in range(len(i)):
            if i[j - 1] == '(':
                s = i[1]
                hops_not_RTO.append(s)
                for k in range(j, j + 100):
                    if i[k] == ')':
                        check = 1
                        break
                    ip_dum = ip_dum + i[k]
                ip_list.append(ip_dum)
            if check == 1:
                check = 0
                break

        count += 1
    print(ip_list)

    asn_list = []
    org_list = []
    latitude_list = []
    longitude_list = []
    isp_list = []
    dom_list = []
    for ip in ip_list:
        url = "http://ipwho.is/{}?fields=connection.asn,connection.org,connection.isp,connection.domain,latitude,longitude".format(
            ip)
        response = urlopen(url)
        data_json = json.loads(response.read())
        asn = data_json['connection']['asn']
        org = data_json['connection']['org']
        isp = data_json['connection']['isp']
        domain_name = data_json['connection']['domain']
        latitude = data_json['latitude']
        longitude = data_json['longitude']
        if asn == None:
            asn = -1
        if org == "":
            org = "NULL"
        if isp == "":
            isp = "NULL"
        if domain_name == "":
            domain_name = "NULL"
        asn_list.append(asn)
        org_list.append(org)
        latitude_list.append(latitude)
        longitude_list.append(longitude)
        dom_list.append(domain_name)
        isp_list.append(isp)

    ans_array = np.array(asn_list)
    org_array = np.array(org_list)
    lat_array = np.array(latitude_list)
    log_array = np.array(longitude_list)
    ip_array = np.array(ip_list)
    isp_array = np.array(isp_list)
    dom_array = np.array(dom_list)
    hop_array = np.array(hops_not_RTO)
    data_df = pd.DataFrame(
        {'website': websites, 'hop_number': hop_array, 'ip': ip_array, 'asn': ans_array, 'isp': isp_array,
         'organisation': org_array, 'latitude': lat_array,
         'longitude': log_array, 'domain_name': dom_array})
    data_final = data_final._append(data_df, ignore_index=True)
print(data_final)
excel_filename = "output_data1.xlsx"

data_final.to_excel(excel_filename, index=False)

