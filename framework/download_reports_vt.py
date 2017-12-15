'''
Created on May 27, 2017

@author: Mahmoud
'''

import json, datetime, os, time, sys, re, urllib, urllib2

def printUsage():
    print ('python download_reports_vt.py results_dir scan_ids_file_path')

if len(sys.argv) < 3:
    printUsage()
    sys.exit()

regex = re.compile(r"(AndroidOS_|TrojanSpyAndroidOS\.|Android-Malicious\.|TrojanAndroid\.|AndroidOS\.|Trojan-Spy\.|Trojan\.|Android\.|Andr\.|\.\w\.|\-\w)|\(\w\)|\.\w\n", re.IGNORECASE)

myApiKey = 'ADD_YOUR_KEY_HERE'
maxRequestPerMinute = 600

frameworkDir = sys.argv[1]
scan_ids_path=sys.argv[2]
scan_ids_path = os.path.join(frameworkDir,'vt_results',scan_ids_path)
scan_ids_path=scan_ids_path.replace('.txt','')
 
print scan_ids_path

requests_counter = 1
# dict = {}
details_path = scan_ids_path+'_download_details.txt'

already_downloaded_reports = set()
if os.path.exists(scan_ids_path+'_download_details.txt'):
    for l in open(details_path,'r'):
        if 'hash: ' in l:
            already_downloaded_reports.add(l.split(':')[1].strip())

print (str(len(already_downloaded_reports))+' reports downloaded')        

scan_ids_file = open(scan_ids_path+'.txt')
#generated files
details = open(details_path,'a+')
jsons = open(scan_ids_path+'_download_jsons.txt','a+')
errors=open(scan_ids_path+'_download_errors.txt','a+')

t1 = datetime.datetime.now()
url = 'https://www.virustotal.com/vtapi/v2/file/report'
appHash = l.strip() 
for l in scan_ids_file:
    if ':' in l:
        appHash = l.split(':')[1].strip() 
    
    if appHash not in already_downloaded_reports:
        try:
            parameters = {'resource': appHash, 'apikey': myApiKey}
            #parameters = {"resource": batchRequest, "apikey": myApiKey}
            data = urllib.urlencode(parameters)
            req = urllib2.Request(url, data)
            result = urllib2.urlopen(req)
            jsondata = result.read()
            jsons.write(jsondata+'\n')
            response_dict = json.loads(jsondata)
            antiviruses =  response_dict.get('scans', {})
            response_code = str(response_dict['response_code'])
            if response_code=='0':
                continue
            details.write('hash: '+appHash+'\n')
            family=''
            for antivirus in antiviruses:               
                family = str(response_dict.get('scans', {}).get(antivirus, {}).get("result"))
                details.write(antivirus+'->'+family+'\n')
                family = family.replace(':','').replace('/','.')
#                familyB = family
#                family = regex.sub(' ', family).strip()
#                family = family.lower()      
#                if family.lower() not in ('none', 'unclassifiedmalware') and len(family)>1:
#                   if dict.has_key(family):
#                      dict[family] = dict[family] + 1
#                   else:
#                      dict[family] = 1
#             if len(dict)>0:
#                sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))            
#                resultFile.write(str(sorted_dict[len(sorted_dict)-1][0])+':'+appHash+'\n')
#print sorted_dict
#                dict.clear()
#             else:
#                resultFile.write("NoFamily:{0}".format(appHash)+'\n');
            details.write('--------------------------------------------------\n');
        except Exception, e:
            e = sys.exc_info()
            errors.write("Exception: "+appHash+'\n'+str(e)+'\n'+jsondata)
            pass
        
        t = (datetime.datetime.now() - t1).seconds
        if (requests_counter==maxRequestPerMinute and t<60 ):    
            time.sleep(60 - t + 5)
            requests_counter=0
            t1=datetime.datetime.now()
        if t>=60: #in case the numbe of requests per minute is high, i.e., it took more than one minute to reach the limit per minute
            t=0    
            requests_counter=0
            t1=datetime.datetime.now()
        requests_counter += 1
    
details.close()      
errors.close()
jsons.close()
