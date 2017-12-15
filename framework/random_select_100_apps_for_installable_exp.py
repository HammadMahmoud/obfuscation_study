'''
Created on July 24, 2017

@author: Mahmoud
'''
import os, sys, datetime, subprocess
from time import localtime, strftime, sleep
from random import shuffle
import re

prog = re.compile('t\d_\w')

extract_package_name = '/Users/Mahmoud/bin/extract_package_name_from_apk.sh'
adb = '/Users/Mahmoud/Tools/android-sdk-macosx/platform-tools/adb'
clearLogcatCmnd = 'adb logcat -c'

def printUsage():    
    print ('Usage: python random_select_100_apps_for_installable_exp selected_app_file installable_exp_dir')

if len(sys.argv) < 3:
    printUsage()
    sys.exit()



excluded = open('/Users/Mahmoud/Documents/PhD_projects/Obfuscation/installable_exp/selected_apps/excluded_apps.txt','r')
excluded_apps = set()
for l in excluded:
    app = l.split(',')[0].strip()
    excluded_apps.add(app)

print str(len(excluded_apps))+' apps excluded'
 

selected_apps=open(sys.argv[1],'r')
installable_apps_path = os.path.join(sys.argv[2], 'selected_apps','installable_apps.csv')
original_apps = open(os.path.join(sys.argv[2], 'selected_apps','original_apps.csv'),'w+')
installed_apps=open(installable_apps_path,'w+')


mal_italy = []
mal = []
benign_s = []

benign_original_obfuscated_map = {}
italy_original_obfuscated_map = {}
mal_original_obfuscated_map = {}

def add_key_val(map, k, item_in_val_list):
    if k in map:
        lst = map[k]
        lst.append(item_in_val_list)
    else:        
        map[k] = [item_in_val_list]
    
def write_original_apps():
    for l in selected_apps:
        if 'app_dir,apk_path' in l:
            continue
        arr = l.split(',')
        app_dir = arr[0].strip()
        if app_dir not in excluded_apps:
            if ',Original,' in l:            
                original_apps.write(l)            
            if '/pure_benign_apps/' in l:
                add_key_val(benign_original_obfuscated_map,app_dir,l)
            elif '/matteo_malware/' in l:
                add_key_val(italy_original_obfuscated_map,app_dir,l)    
            else:
                add_key_val(mal_original_obfuscated_map,app_dir,l)
################### Main ###################

# stuff to run always here such as class/def
def main():        
    pass

if __name__ == "__main__":
    
    write_original_apps()
    output_dir = '/Volumes/Android/obfuscationStudy/installable_exp/apps/'
    output_dir = os.path.join(sys.argv[2],'apps')
    benign_apps_lst = benign_original_obfuscated_map.keys()
    shuffle(benign_apps_lst)
    print ('benign_apps_lst size is '+str(len(benign_apps_lst)))
    italy_apps_lst = italy_original_obfuscated_map.keys()
    shuffle(italy_apps_lst)

    mal_apps_lst = mal_original_obfuscated_map.keys()
    shuffle(mal_apps_lst)
    
    cnt = 0;
    for original_app in benign_apps_lst:        
        appName = original_app.split('/')[-1]
        inputNo = original_app.split('/')[-2]
        if not os.path.exists(os.path.join(output_dir,appName)):
            os.makedirs(os.path.join(output_dir,appName))
            (open(os.path.join(output_dir,appName,inputNo+'.benign'),'w+')).close()
        for l in benign_original_obfuscated_map[original_app]:
            installed_apps.write(appName+','+l)
        cnt+=1
#         if cnt==50:
#             break;

    cnt = 0;
    for original_app in italy_apps_lst:
        appName = original_app.split('/')[-1]
        inputNo = original_app.split('/')[-2]
        if not os.path.exists(os.path.join(output_dir,appName)):
            os.makedirs(os.path.join(output_dir,appName))
            (open(os.path.join(output_dir,appName,inputNo+'.it.malicious'),'w+')).close()
        for l in italy_original_obfuscated_map[original_app]:            
            installed_apps.write(appName+','+l)
        cnt+=1
#         if cnt==25:
#             break;

    cnt = 0;
    for original_app in mal_apps_lst:
        appName = original_app.split('/')[-1]
        inputNo = original_app.split('/')[-2]
        if not os.path.exists(os.path.join(output_dir,appName)):
            os.makedirs(os.path.join(output_dir,appName))
            (open(os.path.join(output_dir,appName,inputNo+'.malicious'),'w+')).close()
        for l in mal_original_obfuscated_map[original_app]:            
            installed_apps.write(appName+','+l)
        cnt+=1
#         if cnt==25:
#             break;
    
    installed_apps.close()
    selected_apps.close()
    
    print ('All done! You can find the apps in '+installable_apps_path)
# log_file.close()