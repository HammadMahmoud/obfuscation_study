'''
Created on July 26, 2017

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
    print ('Usage: python conduct_installable_runable_exp apks_dir installable_runnable_results_dir')

if len(sys.argv) < 3:
    printUsage()
    sys.exit()


apks_dir = sys.argv[1]
output_dir = sys.argv[2]
logs_dir = os.path.join(output_dir,'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)


d = str(datetime.datetime.now())    
# results_path = os.path.join(output_dir, 'installable_runnable_apks_results_'+d+'.csv')
# results=open(results_path,'a+')
# results.write('obfuscator,app_dir,apk_path,pkg,process,success,process_output,start time,finish time,time\n')
results=None

def handleException():
    raise;

def installApk(obfuscator, app_dir,apk_path, pkg, app_log_dir):    
    apk_name=os.path.basename(apk_path)
    pkg_log=os.path.join(app_log_dir, pkg+'-'+apk_name+'.install')
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
    results.write(obfuscator+','+app_dir+','+apk_path+','+ pkg+',install,'+str(success)+','+ process_output_str+','+ str(t1)+','+ str(t2)+','+str(t)+'\n')
    return success

def removeApk(obfuscator, app_dir,apk_path, pkg, app_log_dir):
    apk_name=os.path.basename(apk_path)
    pkg_log=os.path.join(app_log_dir, pkg+'-'+apk_name+'.remove')
    os.system(clearLogcatCmnd)                
    print 'Uninstalling '+pkg
    t1 = datetime.datetime.now()
    process_output = subprocess.check_output([adb,'shell','am','force-stop', pkg])
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
    results.write(obfuscator+','+app_dir+','+apk_path+','+ pkg+',uninstall,'+str(success)+','+ process_output_str+','+ str(t1)+','+ str(t2)+','+str(t)+'\n')

def run_monkey(obfuscator, seed_id, app_dir,apk_path, pkg, app_log_dir):
    process_output_str=''
    t1 = datetime.datetime.now()
    try:
        apk_name=os.path.basename(apk_path)
        pkg_log=os.path.join(app_log_dir, pkg+'-'+apk_name+'.'+obfuscator+'.monkey')
        app_monkey_log = open(os.path.join(app_log_dir,pkg+'.monkey.output'),'a+')
        os.system(clearLogcatCmnd)                
        print 'exercising '+pkg+' using Monkey' 
        t1 = datetime.datetime.now()
        process_output = subprocess.check_output([adb,'shell','monkey','-p', pkg,'--ignore-crashes','--ignore-security-exceptions','--pct-appswitch','50','-s',str(seed_id),'-v','-v','-v','1000'])
        #example: 'adb shell monkey -p com.ysler.wps.base --ignore-crashes --ignore-security-exceptions --pct-appswitch 50 -s 1600 -v -v -v 500'
        process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
        app_monkey_log.write('-----------------------------------------\n')
        app_monkey_log.write(obfuscator+','+str(seed_id)+','+app_dir+','+apk_path+','+pkg+'\n')
        app_monkey_log.write(process_output+'\n')    
        app_monkey_log.write('-----------------------------------------\n')
        t2 = datetime.datetime.now()
        t = t2 - t1
        sleep(1)
        os.system(adb +' logcat -d >>'+pkg_log)
        results.write(obfuscator+','+app_dir+','+apk_path+','+ pkg+',monkey,1,'+'' +','+ str(t1)+','+ str(t2)+','+str(t)+'\n')
    except:
        t2 = datetime.datetime.now()
        t = t2 - t1
        results.write(obfuscator+','+app_dir+','+apk_path+','+ pkg+',monkey,0,'+ ''+','+ str(t1)+','+ str(t2)+','+str(t)+'\n')
        handleException()
        
def exercise_app(obfuscator, seed_id, app_dir,apk_path, pkg, app_log_dir):
    #install original app
    installApk(obfuscator, app_dir, apk_path, pkg, app_log_dir)
    sleep(1)
    #exercise_app
    run_monkey(obfuscator, seed_id, app_dir, apk_path, pkg, app_log_dir)
    sleep(1)
    #remove app
    removeApk(obfuscator, app_dir, apk_path, pkg, app_log_dir)
    sleep(1)
    
def get_obfuscator_name(apkName, appName):
    apkName = os.path.basename(apkName)
    appName = os.path.basename(appName)
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


def conduct_exp():
#     original_obfuscated_map = {}
#     original_apps = []

    apps = [a for a in os.listdir(apks_dir) if os.path.isdir(os.path.join(apks_dir, a))]
    seed_id = 2000
    for app in apps:
        try:      
            seed_id += 10       
            pkg=''
            app_dir = os.path.join(apks_dir, app)
            app_log_dir=os.path.join(logs_dir,os.path.basename(app_dir))
            if os.path.exists(app_log_dir):
                continue
            else:
                os.makedirs(app_log_dir)
            print 'working on '+app_dir
            apk_path = os.path.join(apks_dir, app, app+'.apk')
            process_output = subprocess.check_output([extract_package_name, apk_path])
            pkg = process_output.replace('\n','')
            pkg = pkg.replace('\n','')
            obfuscator = get_obfuscator_name(app+'.apk', app)
            if ': error' in pkg.lower():
                results.write(get_obfuscator_name(app+'.apk', app)+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_original,'+str(0)+','+ pkg+','+ str(0)+','+ str(0)+','+str(0)+'\n')
                continue
            else:
                results.write(get_obfuscator_name(app+'.apk', app)+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_original,'+str(1)+','+ ''+','+ str(0)+','+ str(0)+','+str(0)+'\n')

            exercise_app(obfuscator, seed_id, app_dir, apk_path, pkg, app_log_dir)    

            apks = [a for a in os.listdir(app_dir) if os.path.join(app_dir, a).endswith('.apk')]
            for apk in apks:
                try:
                    pkg=''
                    if apk==app+'.apk':
                        continue
                    apk_path = os.path.join(app_dir, apk)
                    process_output = subprocess.check_output([extract_package_name, apk_path],stderr=subprocess.STDOUT)
                    pkg = process_output.replace('\n','')
                    obfuscator = get_obfuscator_name(apk, app)
                    if ': error' in pkg.lower():
                        results.write(get_obfuscator_name(apk, app)+','+app_dir+','+apk_path+','+ ''+',extract_pkg_obfuscated,'+str(0)+','+ pkg+','+ str(0)+','+ str(0)+','+str(0)+'\n')
                    else:
                        results.write(get_obfuscator_name(apk, app)+','+ app_dir+','+apk_path+','+ pkg+',extract_pkg_success_obfuscated,'+str(1)+','+ ''+','+ str(0)+','+ str(0)+','+str(0)+'\n')
                        print ('apk:'+apk_path+' '+pkg)                        
                        exercise_app(obfuscator, seed_id, app_dir, apk_path, pkg, app_log_dir)                                
                except:
                    process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
                    results.write(obfuscator+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_obfuscated_app,'+\
                                  str(0)+','+ process_output_str+','+ str(0)+','+ str(0)+','+str(0)+'\n')
                    pass
        except:
            process_output_str = str(process_output.split('\n')[0::]).replace(',',';')
            results.write(obfuscator+','+app_dir+','+apk_path+','+ pkg+',extract_pkg_original_app,'+\
                          str(0)+','+ process_output_str+','+ str(0)+','+ str(0)+','+str(0)+'\n')
            pass
        
        
    results.close()
     

######################################################
class app_behavior:
    
    def __init__(self, p_app, p_pkg, p_obfuscator):
        self.app = p_app
        self.pkg = p_pkg
        self.obfuscator = p_obfuscator
        self.crashes = list() #list of crashes in the same order they happened
        self.running_components = list() #list of running components
        
    def same_comps(self, original_comps): # same components
        orig_comps_set=set(original_comps)
        return str(orig_comps_set==set(self.running_components))
    def same_comps_seq(self, original_comps): #strict behavior
        return str(self.running_components == original_comps)
    def same_crashes(self, original_crashes):
        orig_crashes_set=set(original_crashes)
        return str(orig_crashes_set==set(self.crashes))
    def same_crashes_seq(self, original_crashes):
        return str(self.crashes==original_crashes)
        
        
    def __str__(self):
        running_comps_str = str(self.running_components).replace(',',';')
        crashes_str = str(self.crashes).replace(',',';')
        return self.app+','+self.pkg+','+self.obfuscator+','+str(len(self.running_components))+','+str(len(self.crashes))+','+running_comps_str+','+crashes_str       
######################################################
obfuscator_idx = {'Original':0,
                  'Jarsigner':1,
                  'Apktool':2,
                  'ProGuard':3,
                  'Allatori':4,
                  'DashO':5,
                  'DroidChameleon':6,
                  'ADAM':7}
def add_behavior(app, obfuscator, app_behaviors, behavior):
    if obfuscator in obfuscator_idx:
        idx = obfuscator_idx[obfuscator]
        app_behaviors[idx] = behavior

def print_app_behavior(app_behaviors, measure_behavior_results_file):
    original_app_behavior = app_behaviors[0]
    original_comps=original_app_behavior.running_components
    original_crashes=original_app_behavior.crashes
    
    one_row = original_app_behavior.app+','+original_app_behavior.pkg
    if len(original_comps)==0:
        return            
    for i in range(0, len(app_behaviors)):
        app_behavior = app_behaviors[i]
        if app_behavior:
            running_comps_str = str(app_behavior.running_components).replace(',',';').replace('\n',' ')
            unique_crashes_set = set(app_behavior.crashes)
            crashes_str = str(unique_crashes_set).replace(',',';').replace('\n', ' ')
            app_behavior_str = ','+app_behavior.obfuscator+','+\
                        running_comps_str+','+str(len(app_behavior.running_components))+','+\
                        app_behavior.same_comps(original_comps)+','+app_behavior.same_comps_seq(original_comps)+','+\
                        crashes_str+','+str(len(app_behavior.crashes))+','+str(len(unique_crashes_set))+','+\
                        app_behavior.same_crashes(original_crashes)+','+app_behavior.same_crashes_seq(original_crashes)
            one_row = one_row+app_behavior_str
        else:
            one_row = one_row + ',,,,,,,,,,'    
    one_row=one_row.replace('\n','**').strip()
#     print one_row
    measure_behavior_results_file.write(one_row+'\n')    

def measure_behavior(measure_behavior_results_file):
    
    app_behaviors = [None, None, None, None, None, None, None, None]
    empty=',,,,,,,,,,'
    h1 = 'app,pkg,,Original'+empty+'Jarsigner'+empty+'Apktool'+empty+'ProGuard'+empty+'Allatori'+empty+'DashO'+empty+'DroidChameleon'+empty+'ADAM'+empty
#     print h1
    hdr = 'app,pkg'
    for i in range(0, len(app_behaviors)):
        hdr = hdr +','+'obfuscator,started components,started components #,same comps. as original,same comps seq. as original,'\
                    'unique crashes,crashes #,unique crashes #,same crashes as original, same crashes seq as original'
#     print hdr  
    measure_behavior_results_file.write(h1+'\n')
    measure_behavior_results_file.write(hdr+'\n')

    apps = [i for i in os.listdir(logs_dir) if os.path.isdir(os.path.join(logs_dir, i))]
    
    for app in apps:
#         if app != 'imlog3':
#             continue 
        app_log_dir = os.path.join(logs_dir, app)
        logs = os.listdir(app_log_dir)
        for log in logs:
            pkg = log.split('-')[0]
            ext = obfuscator = log.split('.')[-1]
            obfuscator = log.split('.')[-2] 
#             print app,pkg,ext,obfuscator
#             print os.path.join(app_log_dir, log)
            f = open(os.path.join(app_log_dir, log), 'r')
            behavior = app_behavior(app, pkg, obfuscator)
            behavior.running_components=list()
            behavior.crashes=list()
            exception_next_line=False
            
            if 'output' in ext: 
                print log
                continue
            elif 'monkey' in ext:
                for l in f:
                    if 'EvalCompTime' in l and pkg in l and '#running#' in l:
                        #example of a line: 
                        #07-26 16:28:10.519 10669 10669 I EvalCompTime: 1. activity package #air.jp.co.studio.arcana.RegWoosh# class #air.jp.co.studio.arcana.RegWoosh.AppEntry# is #running#
                        running_comp = (l.split('class ')[1]).strip().split('#')[1].strip().replace('\n','')
#                         print running_comp
                        behavior.running_components.append(running_comp)
                    elif 'AndroidRuntime' in l and 'Process' in l and pkg in l:
                        #example of a line 
                        #crash occurred: AndroidRuntime: Process: kr.infocept.catholic.mass, PID: 12697
                        exception_next_line=True
                    elif exception_next_line:
                        #example of a line
                        #07-26 16:38:17.267 14030 14030 E AndroidRuntime: java.lang.NoClassDefFoundError: Failed resolution of: Lcom/EncryptString;
                        crash = l.split('AndroidRuntime: ')[1].strip().replace('\n','')   
                        behavior.crashes.append(crash)
#                         print crash
                        exception_next_line=False
            add_behavior(app, obfuscator, app_behaviors, behavior)                
        print_app_behavior(app_behaviors, measure_behavior_results_file)
        app_behaviors = [None, None, None, None, None, None, None, None]
######################################################


        
################### Main ###################
# stuff to run always here such as class/def

def main():
    pass

if __name__ == "__main__":
#     conduct_exp()
    
    measure_behavior_results_path=os.path.join(output_dir,'running_apps_behaviors.csv')
    measure_behavior_results_file = open(measure_behavior_results_path, 'w+')    
    measure_behavior(measure_behavior_results_file)
    print ('find output at '+measure_behavior_results_path)
#     print ('find the output at '+results_path)
    
    
