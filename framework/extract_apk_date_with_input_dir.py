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
    print ('Usage: python extract_apk_date dataset frameworkDir result_file')

if len(sys.argv) < 4:
    printUsage()
    sys.exit()

################### Global variables ###################

dataset = sys.argv[1]
frameworkDir = sys.argv[2]
fname = sys.argv[3].replace('.csv','')
results_file = os.path.join(frameworkDir,'apk_dates',fname+'.csv') 

#### change the aapt in  the framework/lib/extract/extract_package_name_from_apk.sh file
# aapt = '/share/seal/joshug4/android-sdks/build-tools/21.1.0/aapt'
# aapt = '/usr/local/bin/aapt'


################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    add_header = True
    apps_date_extracted_list = set()
    if os.path.exists(results_file):
        add_header=False
        for l in open(results_file,'r'):
            apps_date_extracted_list.add(l.split(',')[0])
           
    results = open(results_file,'a+')
    if add_header:
        results.write('app,app_path,package,dex_year,dex_month,dex_day,cert_year,cert_month,cert_day\n')    
    
    print (str(len(apps_date_extracted_list))+' apps extracted')
    inputs = [a for a in os.listdir(dataset) if os.path.isdir(os.path.join(dataset,a))]
      
    for input in inputs:
        apps = [a for a in os.listdir(os.path.join(dataset,input)) if os.path.isdir(os.path.join(dataset,input))]
        for a in apps:
            if a.startswith('.'):
                continue
            apk = os.path.join(dataset,input, a,a+'.apk')
            if a+'.apk' not in apps_date_extracted_list:        
                try:                                                    
                    print ('  --------------------- '+apk+'  --------------------- ')
                    dex_year = ''
                    dex_month = ''
                    dex_day = ''
                    cert_year = ''
                    cert_month = ''
                    cert_day = ''
                    
                    package = subprocess.check_output([os.path.join(frameworkDir,'framework','lib','extract_package_name_from_apk.sh ')+apk], shell=True)
                    package=package.replace('\n','')
                    print package
                 
                    zApk = zipfile.ZipFile(apk)
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
                            results.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(a+'.apk',apk,package,
                                                                                         dex_year,dex_month,dex_day,
                                                                                         cert_year,cert_month,cert_day))
                            break    
                    #in case the app is not signed    
                    if not (dex_found and rsa_found):
                        results.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(a+'.apk',apk,package,
                                                                                     dex_year,dex_month,dex_day,
                                                                                     cert_year,cert_month,cert_day))
                     
                 
                except:
                    print ('Error: '+apk+' '+str(sys.exc_info()))
                    pass   
