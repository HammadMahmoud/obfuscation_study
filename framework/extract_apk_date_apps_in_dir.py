'''
Created on Apr 30, 2017

@author: Mahmoud
'''

# if __name__ == '__main__':
#     handleException()

import zipfile, os, shutil, sys
import allatori_config_generator as cnfg
from time import sleep
from __builtin__ import file
import subprocess


def printUsage():
    print ('Usage: python extract_apk_date_with_input_dir dataset framework_dir result_file')

if len(sys.argv) < 4:
    printUsage()
    sys.exit()

################### Global variables ###################

dataset = sys.argv[1]
framework_dir = sys.argv[2]
results_file = sys.argv[3]

#### change the aapt in  the framework/lib/extract/extract_package_name_from_apk.sh file
# aapt = '/share/seal/joshug4/android-sdks/build-tools/21.1.0/aapt'
# aapt = '/usr/local/bin/aapt'


################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here   
    exists = os.path.exists(results_file)
    if not exists:
        results =  open(results_file,'a+')
    else:    
        results = open(results_file,'r+')    
    apps_date_extracted_list = []
    if exists:
#         extracted = open(results_file,'r')
        for l in results:
            apps_date_extracted_list.append(l.split(',')[0])
    else:        
        results.write('app,app_path,package,dex_year,dex_month,dex_day,cert_year,cert_month,cert_day\n')    
    
    print (str(len(apps_date_extracted_list))+' groups extracted')
    groups = [d for d in os.listdir(dataset) if d.endswith('.apk') ]  
    for app in groups:
        if app not in apps_date_extracted_list:        
            try:                
                app_path = os.path.join(dataset,app)                
                print ('  --------------------- '+app_path+'  --------------------- ')
                dex_year = ''
                dex_month = ''
                dex_day = ''
                cert_year = ''
                cert_month = ''
                cert_day = ''
                '''                
                package = subprocess.check_output([os.path.join(framework_dir,'lib','extract_package_name_from_apk.sh ')+app_path], shell=True)
                package=package.replace('\n','')
                
                zApk = zipfile.ZipFile(app_path)
                dex_found=False
                rsa_found=False                
                for f in zApk.filelist:  #f of the type zipfile.ZipInfo
                    #zipfile.ZipInfo.date_time is (year, month, day, hour, min, sec) tuple
                    if f.filename.endswith('.dex'):
                        dex_found=True
                        dex_year = f.date_time[0]
                        dex_month =  f.date_time[1]
                        dex_day = f.date_time[2]                    
                    if f.filename.endswith('.RSA'):
                        rsa_found=True
                        cert_year = f.date_time[0]
                        cert_month =  f.date_time[1]
                        cert_day = f.date_time[2]
                    
                    if dex_found and rsa_found:
                        results.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(app,str(app_path),package,
                                                                                     dex_year,dex_month,dex_day,
                                                                                     cert_year,cert_month,cert_day))
                        break    
                #in case the app is not signed    
                if not (dex_found and rsa_found):
                    results.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(app,str(app_path),package,
                                                                                 dex_year,dex_month,dex_day,
                                                                                 cert_year,cert_month,cert_day))
                    
                
    '''                
            except:
                print ('Error: '+app+' '+str(sys.exc_info()))
                pass   
