'''
Created on July 21, 2017

@author: Mahmoud
'''
import os, sys, datetime, subprocess
from time import localtime, strftime, sleep
import re, datetime

prog = re.compile('t\d_\w')

extract_package_name = '/Users/Mahmoud/bin/extract_package_name_from_apk.sh'
adb = '/Users/Mahmoud/Tools/android-sdk-macosx/platform-tools/adb'
clearLogcatCmnd = adb+' logcat -c'

def printUsage():    
    print ('Usage: python conduct_installable_exp apks_dir output_dir')

if len(sys.argv) < 3:
    printUsage()
    sys.exit()


apks_dir = sys.argv[1]
output_dir = sys.argv[2]
logs_dir = os.path.join(output_dir,'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

d = str(datetime.datetime.now())    
results_path = os.path.join(output_dir, 'installable_apks_results_'+d+'.csv')
results=open(results_path,'w+')
# log_file=open(os.path.join(output_dir, 'installable_exp.log'),'w+')

results.write('obfuscator,app_dir,apk_path,pkg,process,success,process_output,start time,finish time,time\n')


def installApk(app_name, app_dir,apk_path, pkg):    
    apk_name=os.path.basename(apk_path)
    pkg_log=os.path.join(logs_dir, pkg+'-'+apk_name+'.install')
    os.system(clearLogcatCmnd)                
    print 'Installing '+apk_path
    t1 = datetime.datetime.now()
    process_output = subprocess.check_output([adb,'install', apk_path])
    process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
    print 'Install: '+process_output_str
    success=0
    if 'Success' in process_output:
        success=1
    
    t2 = datetime.datetime.now()
    t = t2 - t1
    sleep(1)
    if success==0:
        os.system(adb+' logcat -d >>'+pkg_log)
    results.write(get_obfuscator_name(apk_name, app_name)+','+app_dir+','+apk_path+','+ pkg+',install,'+str(success)+','+ process_output_str+','+ str(t1)+','+ str(t2)+','+str(t)+'\n')
    return success

def removeApk(appName, app_dir,apk_path, pkg):
    apk_name=os.path.basename(apk_path)
    pkg_log=os.path.join(logs_dir, pkg+'-'+apk_name+'.remove')
    os.system(clearLogcatCmnd)                
    print 'Uninstalling '+pkg
    t1 = datetime.datetime.now()
    process_output = subprocess.check_output([adb,'uninstall', pkg])
    process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
    print 'Remove:' +process_output_str
    success=0
    if 'Success' in process_output:
        success=1
    
    t2 = datetime.datetime.now()
    t = t2 - t1
    sleep(1)
    if success==0:
        os.system(adb +' logcat -d >>'+pkg_log)
    results.write(get_obfuscator_name(apk_name, appName)+','+app_dir+','+apk_path+','+ pkg+',uninstall,'+str(success)+','+ process_output_str+','+ str(t1)+','+ str(t2)+','+str(t)+'\n')

def get_obfuscator_name(apkName, appName):
    
    if apkName == (appName+'.apk'):
        return 'Original'
    elif '_repack.apk' in apkName:        
        return 'Simple Tools'
    elif '_resign.apk' in apkName:
        return 'Simple Tools'
    elif '-za-ADAM.apk' in apkName:
        return 'Simple Tools'
    #ProGuard
    elif '_proguard.apk' in apkName:
        return 'ProGuard'
    #DashO
    elif '_dashO' in apkName:
        return 'DashO'
    #ADAM
    elif '-ADAM.apk' in apkName:
        return 'ADAM'
    elif prog.match(apkName):
        return 'DroidChameleon'

    return 'Allatori'
################### Main ###################

# stuff to run always here such as class/def
def main():        
    pass

if __name__ == "__main__":
    
#     apks = [a for a in os.listdir(apks_dir) if os.path.join(apks_dir, a).endswith('.apk')]
    apps = [a for a in os.listdir(apks_dir) if os.path.isdir(os.path.join(apks_dir, a))]
    for app in apps:
        try:             
            pkg=''
            app_dir = os.path.join(apks_dir, app)
            print 'working on '+app_dir
            apk_path = os.path.join(apks_dir, app, app+'.apk')
            process_output = subprocess.check_output([extract_package_name, apk_path])
            pkg = process_output.replace('\n','')
            pkg = pkg.replace('\n','')
            if ': error' in pkg.lower():
                results.write(get_obfuscator_name(app+'.apk', app)+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_original,'+str(0)+','+ pkg+','+ str(0)+','+ str(0)+','+str(0)+'\n')
                continue
            else:
                results.write(get_obfuscator_name(app+'.apk', app)+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_original,'+str(1)+','+ ''+','+ str(0)+','+ str(0)+','+str(0)+'\n')
            success = installApk(app, app_dir, apk_path, pkg)
            sleep(1)
            removeApk(app, app_dir,apk_path, pkg)
            success = 1                        
            if success == 1:                
                apks = [a for a in os.listdir(app_dir) if os.path.join(app_dir, a).endswith('.apk')]
                for apk in apks:
                    try:
                        pkg=''
                        if apk==app+'.apk':
                            continue
                        apk_path = os.path.join(app_dir, apk)
#                         print extract_package_name+' '+apk_path
                        process_output = subprocess.check_output([extract_package_name, apk_path],stderr=subprocess.STDOUT)
#                         process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
#                         print 'process_output:'+process_output_str
                        pkg = process_output.replace('\n','')
#                         print pkg
                        if ': error' in pkg.lower():
                            results.write(get_obfuscator_name(apk, app)+','+app_dir+','+apk_path+','+ ''+',extract_pkg_obfuscated,'+str(0)+','+ pkg+','+ str(0)+','+ str(0)+','+str(0)+'\n')
                        else:
#                             print 'PKG: '+pkg
                            results.write(get_obfuscator_name(apk, app)+','+ app_dir+','+apk_path+','+ pkg+',extract_pkg_success_obfuscated,'+str(1)+','+ ''+','+ str(0)+','+ str(0)+','+str(0)+'\n')
                            print ('apk:'+apk_path+' '+pkg)
                            installApk(app, app_dir,apk_path, pkg)
                            sleep(1)
                            removeApk(app, app_dir,apk_path, pkg)                            
                            
                    except:
                        process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
                        results.write(get_obfuscator_name(apk, app)+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_obfuscated_app,'+str(0)+','+ process_output_str+','+ str(0)+','+ str(0)+','+str(0)+'\n')
#                         print ('Error APK: '+app_dir+','+apk_path+','+ pkg+',extract_pkg_obfuscated_app,'+str(0)+','+ process_output_str+','+ str(0)+','+ str(0)+','+str(0))
                        pass
        except:
            process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
            results.write(get_obfuscator_name(apk, app)+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_original_app,'+str(0)+','+ process_output_str+','+ str(0)+','+ str(0)+','+str(0)+'\n')
            pass
#             print ('Error APP: '+app_dir+','+apk_path+','+ pkg+',extract_pkg_original_app,'+str(0)+','+ process_output_str+','+ str(0)+','+ str(0)+','+str(0)+'\n')

results.close()
print ('find the output at '+results_path)
# log_file.close()