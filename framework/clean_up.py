'''
Created on Apr 30, 2017

@author: Mahmoud
'''

import os, sys
import shutil

print 'Usage:'
print 'python clean_up.py frameworkDir check_allatori doSign add_dc_finished check_dashO check_proguard check_apktool check_adam'

frameworkDir = sys.argv[1]
check_allatori=False
doSign = False
add_dc_finished = False
check_dasho = False
check_proguard = False
check_apktool=False
check_adam=False

if sys.argv[2].lower()=='y':
    check_allatori=True
if sys.argv[3].lower()=='y':
    doSign=True
if sys.argv[4].lower() == 'y':
    add_dc_finished=True
if sys.argv[5].lower() == 'y':
    check_dasho=True
if sys.argv[6].lower() == 'y':
    check_proguard=True    
if sys.argv[7].lower() == 'y':
    check_apktool=True    
if sys.argv[8].lower() == 'y':
    check_adam=True    

libDir = os.path.join(frameworkDir,'lib')

apktool = 'java -jar '+os.path.join(libDir,'apktool_2.0.1.jar')+' '
sign_apk_with_mahmoud = os.path.join(libDir,'sign_apk_with_mahmoud.sh')+' '
cleaned_apps=0
################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
    
    dirs = {}
    dataset_dir = '/share/seal/hammadm/obf/Obfuscation/dataset'
    dirs['Benign'] = os.path.join(dataset_dir,'pure_benign_apps')
#     dirs['Virusshare'] = os.path.join(dataset_dir,'virusshare')
    dirs ['BrainTest'] = os.path.join(dataset_dir,'BrainTest')
    dirs ['FalseGuide'] = os.path.join(dataset_dir,'falseGuide')
    dirs ['VikingHorde'] = os.path.join(dataset_dir,'VikingHorde')
    
#     dirs ['local Matteo'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/dataset/matteo_malware'
    dirs['local test dataset'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/test_dataset'
    
#     '/share/seal/hammadm/obf/Obfuscation/dataset/matteo_malware'
    cleaned_apps = 0
    dc_finished = 0
    signed_apks = 0
    dasho_finished_removed = 0
    allatori_finished_removed = 0
    proguard_finished_removed = 0
    apktool_output_removed = 0
    adam_finished_removed=0
    for dir, path in dirs.items():
        if os.path.isdir(path):
            inputs = [a for a in os.listdir(path) if os.path.isdir(os.path.join(path,a))]
            
            for input in inputs:
                apps = [a for a in os.listdir(os.path.join(path,input)) if os.path.isdir(os.path.join(path,input))]
#                 apps = [a for a in os.listdir(path) if os.path.isdir(os.path.join(path,a))]
                for a in apps:     
                    if a.startswith('.'):
                        continue
                    #Allatori clean-up
                    if check_allatori:
                        obf_apkFile = os.path.join(path,input,a,a+'_all.apk')
                        if not os.path.exists(obf_apkFile):                        
                            if os.path.exists(os.path.join(path,input,a,'allatori_finished')):
                                os.remove(os.path.join(path,input,a,'allatori_finished'))
                                allatori_finished_removed+=1
                    if add_dc_finished:        
                        #add tried_dc file if t0_apk file is generated
                        if os.path.exists(os.path.join(path,input,a,'t15_'+a+'.apk')) and not os.path.exists(os.path.join(path,a,'dc_finished')):
                            open(os.path.join(path,input,a,'dc_finished'),'a').close()
                            dc_finished+=1
    
                    if doSign:
                        #sign apks            
                        for apk in os.listdir(os.path.join(path,input,a)):
                            if apk.endswith('.apk') and apk.replace('.apk','') != a:
                                signCmd = signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, os.path.join(path,input,a,apk))
    #                             print (signCmd)
                                os.system(signCmd)
                                signed_apks+=1
    
                    if check_dasho:        
                        obf_apkFile = os.path.join(path,input,a,a+'_dashO-all.apk')
                        if not os.path.exists(obf_apkFile):
                            if os.path.exists(os.path.join(path,input,a,'dashO_finished')):
                                os.remove(os.path.join(path,input,a,'dashO_finished'))
                                dasho_finished_removed+=1

                    if check_proguard:
                        obf_apkFile = os.path.join(path,input,a,a+'_proguard.apk')
                        if not os.path.exists(obf_apkFile):
                            if os.path.exists(os.path.join(path,input,a,'proguard_finished')):
                                os.remove(os.path.join(path,input,a,'proguard_finished'))
                                proguard_finished_removed+=1
                    #check apktool
                    if check_apktool:
                        if not os.path.exists(os.path.join(path,input,a,'working-dir','apktool-output','apktool.yml')):
                            if os.path.exists(os.path.join(path,input,a,'working-dir','apktool-output')):
                                shutil.rmtree(os.path.join(path,input,a,'working-dir','apktool-output'))
                                apktool_output_removed+=1
                    if check_adam:
                        if os.path.exists(os.path.join(path,input,a,'adam_finished')):
                            os.remove(os.path.join(path,input,a,'adam_finished'))
                            adam_finished_removed+=1
                                                        
            print ('Signed APKs '+str(signed_apks))
            print ('removed allatori_finished '+str(allatori_finished_removed))
            print ('removed dashO_finished '+str(dasho_finished_removed))
            print ('removed proguard_finished '+str(proguard_finished_removed))
            print ('removed apktool-output '+str(apktool_output_removed))
            print ('added dc_finished '+str(dc_finished))
            
            
            
                        
