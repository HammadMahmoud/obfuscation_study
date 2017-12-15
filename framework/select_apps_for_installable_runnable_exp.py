'''
Created on July 21, 2017

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
    print ('Usage: python select_apps_for_installale_runnable_exp output_file_path')

if len(sys.argv) < 2:
    printUsage()
    sys.exit()

dataset_dir= '/share/seal/hammadm/obf/Obfuscation/dataset'
local_benign_dir = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/test_dataset'
benign_dataset = os.path.join(dataset_dir,'pure_benign_apps')
vs_dataset = os.path.join(dataset_dir,'virusshare')
matteo_dataset = os.path.join(dataset_dir,'matteo_malware')


output_dir = sys.argv[1]

result_path=os.path.join(output_dir, 'selected_apps_for_installable_runnable_exp.csv')     
results=open(result_path,'w+')
# log_file=open(os.path.join(output_dir, 'installable_exp.log'),'w+')

results.write('app_dir,apk_path,obfuscator,is_malicious\n')

allatori_suffixes= ['_all.apk','_reorder_member.apk','_control-flow.apk','_control_flow.apk',
                    '_string_encryption.apk','_string-encryption.apk','_cf_rm.apk','_cf_rm_sencryption.apk',
                    '_cf_rm_renaming.apk','_cf_rm_renaming.apk']

def get_app(l, key_str):
    shuffle(l)    
    for a in l:
        if key_str in a:
            return a 

def get_dc_app(l):  
    shuffle(l)  
    for a in l:
        if prog.match(a):
            return a
    return None

def get_allatori_app(l, app):
    shuffle(allatori_suffixes)
    for al in allatori_suffixes:
        if app+al in l:
            return app+al
    return None
        
def candidate_apps(l, app_dir, app):    
    l_str = str(l)
    selected_apps=[]
    selected_apps.append(os.path.join(app_dir,app+'.apk')+';'+'Original')
    #SimpleTools: we need at least one
    if '_repack.apk' not in l_str:
        selected_apps=None
        return selected_apps
    selected_apps.append(os.path.join(app_dir,app+'_repack.apk')+';'+'SimpleTootls')
    if '_resign.apk' not in l_str:
        selected_apps=None
        return selected_apps
    selected_apps.append(os.path.join(app_dir,app+'_resign.apk')+';'+'SimpleTootls')
#     if '-za-ADAM.apk' not in l_str:
#         selected_apps=None
#         return selected_apps

#     if '-za-ADAM.apk' in l_str:
#         selected_apps.append(os.path.join(app_dir,app+'-za-ADAM.apk')+';'+'SimpleTootls')
#         l.remove(app+'-za-ADAM.apk')
#         l_str=str(l)
    #ProGuard
    if '_proguard.apk' not in l_str:
        selected_apps=None
        return selected_apps
    selected_apps.append(os.path.join(app_dir,app+'_proguard.apk')+';'+'ProGuard')
    #DashO
    if '_dashO' not in l_str:
        selected_apps=None
        return selected_apps
    a = get_app(l, 'dashO')
    selected_apps.append(os.path.join(app_dir,a)+';'+'DashO')
    #ADAM
    if '-ADAM.apk' not in l_str:
        selected_apps=None
        return selected_apps
    a = get_app(l, 'ADAM')
    selected_apps.append(os.path.join(app_dir,a)+';'+'ADAM')
#     if '-ADAM.apk' in l_str:
#         a = get_app(l, 'ADAM')
#         selected_apps.append(os.path.join(app_dir,a)+';'+'ADAM')

    #DC
    dc_app = get_dc_app(l)
    if not dc_app:
        selected_apps=None
        return selected_apps
    selected_apps.append(os.path.join(app_dir,dc_app)+';'+'DroidChameleon')
    #Allatori
    at_app = get_allatori_app(l, app)
    if not at_app:
        selected_apps=None
        return None 
    selected_apps.append(os.path.join(app_dir,at_app)+';'+'Allatori')
    return selected_apps    
    

def select_apks(dataset_dir, is_malicious):
    inpts = [i for i in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, i))]
    for i in inpts:
        i_path = os.path.join(dataset_dir,i)
        apps = [a for a in os.listdir(i_path) if os.path.isdir(os.path.join(i_path, a))]
        for app in apps:
            app_dir = os.path.join(i_path, app)
            apks = [a for a in os.listdir(app_dir) if os.path.join(app_dir, a).endswith('.apk')]
            if len(apks) < 6: #we are looking for apps that are obfuscated by all obfuscators
                continue;
            selected_apps = candidate_apps(apks, app_dir, app)
            if selected_apps:
                for sa in selected_apps:
                    arr = sa.split(';')
                    results.write(app_dir+','+arr[0]+','+arr[1]+','+ str(is_malicious)+'\n')
#             else:
#                 print 'No app has been selected for '+app    
        
################### Main ###################

# stuff to run always here such as class/def
def main():        
    pass

if __name__ == "__main__":
    
    if os.path.exists(benign_dataset):
        select_apks(benign_dataset, 0)
        print ('Finished Benign Dataset! see results at '+result_path)
    if os.path.exists(vs_dataset):    
        select_apks(vs_dataset, 1)
        print ('Finished VS Dataset! see results at '+result_path)
    if os.path.exists(matteo_dataset):
        select_apks(matteo_dataset, 1)
        print ('All done! see results at '+result_path)
    if os.path.exists(local_benign_dir):
        select_apks(local_benign_dir, 1)
        print ('All done! see results at '+result_path)

results.close()
# log_file.close()