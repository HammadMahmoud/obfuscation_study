'''
Created on Apr 20, 2017

@author: Mahmoud
'''

# if __name__ == '__main__':
#     handleException()

import zipfile, os, shutil, sys
# import allatori_config_generator as cnfg
from time import sleep

def printUsage():
    print ('Usage: python run_proguard dataset frameworkDir errorFileName')

if len(sys.argv) < 4:
    printUsage()
    sys.exit()


dataset = sys.argv[1]
frameworkDir = sys.argv[2]
errorFileName = sys.argv[3]
# create_working_dir='n'
# if len(sys.argv) == 5:
#     create_working_dir = (sys.argv[4]).lower().strip() #if Y, create a working-dir, N: if there is no working-dir, then do not obfuscate


libDir = os.path.join(frameworkDir,'lib')
apktool = 'java -jar '+os.path.join(libDir,'apktool_2.0.1.jar')+' '
sign_apk_with_mahmoud = os.path.join(libDir,'sign_apk_with_mahmoud.sh')+' '
androidJar = os.path.join(libDir,'android.jar')
allatori = os.path.join(libDir,'allatori_61.jar')
dx = os.path.join(libDir,'dx.jar')
proguard = os.path.join(libDir,'proguard.jar')
errorFile = os.path.join(frameworkDir,'logs',errorFileName+'.csv')

error_file_opened = False

def print_error(msg):
#     if not error_file_opened:
#         error = open(errorFile, 'a+')
#         error_file_opened=True
    print (msg)

def handleException():
    pass

def proguard_obfuscate_app(app):
    print 'Proguard obfuscator '+app    
    appDir=os.path.join(dataset,app)
    apkFile = os.path.join(appDir, (app+'.apk'))
    prefix='proguard'
    obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
    if os.path.exists(obf_apkFile) or os.path.exists(os.path.join(dataset,app,'proguard_finished')):
        print ('app is already obfuscated '+obf_apkFile)
        if not os.path.exists(os.path.join(dataset,app,'proguard_finished')):
            open(os.path.join(dataset,app,'proguard_finished'),'a').close()
        return
    #create a working-dir
    try:
        workingDir =os.path.join(appDir,'working-dir')
        apktool_output = os.path.join(workingDir, 'apktool-output')
        if os.path.exists(workingDir):
            print ('working-dir found '+apkFile)
        else:
            os.makedirs(workingDir)
            #run apktool if not exists from previous run or from running Allattori obfuscator        
        if not os.path.exists(apktool_output):
            apktoolCmd = '{0} d {1} -output {2}'.format(apktool, apkFile, apktool_output)
            os.system(apktoolCmd)
        
        if os.path.exists(apktool_output):
            unarchivedPath = os.path.join(workingDir,app)
            #unarchive the apk file
            if not zipfile.is_zipfile(apkFile):
                print_error('invalid-apk,'+app+','+apkFile+','+str(sys.exc_info())+'\n')
                return
            if not os.path.exists(unarchivedPath):
                zApk = zipfile.ZipFile(apkFile)   
                zApk.extractall(unarchivedPath)
            if os.path.exists(unarchivedPath):
                print('Unarchived '+apkFile)                
                try:
                    #Dex2Jar: convert the file.dex to a file.jar
                    jarFile = str(os.path.join(workingDir,'output_dex2jar.jar'))
                    dexFile = str(os.path.join(unarchivedPath,'classes.dex'))
                    if not os.path.exists(jarFile):                
                        if not os.path.exists(dexFile):
                            print_error('missingDexFile,'+app+','+apkFile+','+str(sys.exc_info())+'\n')
                            return   
                        Dex2JarCmd = libDir+'/dex2jar/d2j-dex2jar.sh -o '+ jarFile+' '+dexFile
                        os.system(Dex2JarCmd)
                        print (Dex2JarCmd)
                except:
                    print_error('Dex2Jar,'+app+','+apkFile+','+str(sys.exc_info())+'\n')
                    handleException()   
                
                
                ########################### pro-guard obfuscation: 
                #ProGuard is a free Java class file shrinker, optimizer, obfuscator, and preverifier
                try:                
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))                
                    if not os.path.exists(obfJarFile):
                        configFile = os.path.join(workingDir,prefix+'-android.pro')
                        shutil.copyfile(os.path.join(libDir,prefix+'-android.pro'), configFile)
    #                 logFile = os.path.join(workingDir,prefix+'-log.xml')
    #                 cnfg.create_string_excryption_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                        proguardCmd = 'java -Xms128m -Xmx2048m -jar {0} @{1}'.format(proguard, configFile)
                        print (proguardCmd)
                        os.system(proguardCmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to classes.dex
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        if not os.path.exists(obfDexFile):
                            DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                            print (DxCmd)
                            os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        if os.path.exists(dexFile):
                            os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        if os.path.exists(obf_apkFile):
                            print (obf_apkFile+' is already obfuscated.')
                            return
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)
                        if not os.path.exists(obf_apkFile):
                            #try build an apk file after moving the AndroidManifest file                        
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)                    
                        else:
                            print ('file not found to sign: '+obf_apkFile)                        
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')                    
                        handleException()
                except:
                    print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                    handleException()   
                
            else:
                print_error('py-zipfile-unzip'+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                print ('Error: Unable to unzip '+apkFile)    
            
            #aapt remove -f ./original-test.apk ./classes.dex
            #aapt add -f ./original-test.apk ./classes.dex
        else:
            print_error('apktool-decode'+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
            print ('Error: Unable to run apktool on '+apkFile)
            
        open(os.path.join(dataset,app,'proguard_finished'),'a').close()    
        print('Proguard finished '+apkFile)    
    except:
        pass
    finally:
        if not os.path.exists(os.path.join(dataset,app,'proguard_finished')):
            open(os.path.join(dataset,app,'proguard_finished'),'a').close()
################################################################################################################
def check_androguard_config(file):
    f = open(file, 'r')
    print ('check if '+file+' exists.')
    for l in f:
        if l.startswith('-libraryjars'):
            print ('check this line '+l)
            jar = (l.replace('\n','').split()[1]).strip()
            if not (os.path.exists(jar) and jar.endswith('.jar')):
                print ('JAR file '+jar+' is not exists. Update '+file+' accordingly.')
                sys.exit()
                return False
            break   
    return True



################### Main ###################

# stuff to run always here such as class/def
def main():        
    pass

if __name__ == "__main__":
    check_androguard_config(os.path.join(libDir,'proguard-android.pro'))
#     proguard_obfuscate_app('test')
        
    i=0
    print ('Obfuscate apps in '+dataset)
    apps = [d for d in os.listdir(dataset) if os.path.isdir(os.path.join(dataset, d))]
    for app in apps:
        print ('Obfuscate '+app+' --------------------- ')
        try:
            proguard_obfuscate_app(app)
        except:
            print ('Error: '+app)
            pass    
        i+=1
    print (str(i)+' apps obfuscated using ProGuard')   

