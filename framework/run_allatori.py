'''
Created on Apr 20, 2017

@author: Mahmoud
'''

# if __name__ == '__main__':
#     handleException()

import zipfile, os, shutil, sys
import allatori_config_generator as cnfg
import run_proguard as proguard
from time import sleep

# dataset ='/Users/Mahmoud/Documents/PhD_projects/Obfuscation/dataset/'
# dataset ='/Volumes/Android/obfuscationStudy/pure_benign_apps/'
# dataset = '/Volumes/Android/obfuscationStudy/dataset/BrainTest/'
# dataset = '/Volumes/Android/obfuscationStudy/dataset/pure_benign_apps'



def printUsage():
    print ('Usage: python run_allatori dataset frameworkDir errorFileName')

if len(sys.argv) < 4:
    printUsage()
    sys.exit()

################### Global variables ###################

dataset = sys.argv[1]
frameworkDir = sys.argv[2]
errorFileName = sys.argv[3]

# apktool = '/usr/local/bin/apktool'
# sign_apk_with_mahmoud = '/Users/Mahmoud/bin/sign_apk_with_mahmoud.sh'

# libDir = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/framework/lib'
libDir = os.path.join(frameworkDir,'lib')

apktool = 'java -jar '+os.path.join(libDir,'apktool_2.0.1.jar')+' '
sign_apk_with_mahmoud = os.path.join(libDir,'sign_apk_with_mahmoud.sh')+' '

# androidJar = '/Users/Mahmoud/Tools/android-sdk-macosx/platforms/android-22/android.jar'
androidJar = os.path.join(libDir,'android.jar')
allatori = os.path.join(libDir,'allatori_61.jar')
dx = os.path.join(libDir,'dx.jar')

errorFile = os.path.join(frameworkDir,'logs',errorFileName+'.csv')
error = open(errorFile, 'a+')
error_file_opened=False

def print_error(msg):
#     if not error_file_opened:
#         error = open(errorFile, 'a+')
#         error_file_opened=True
    print (msg)


def handleException():
    pass

def obfuscate_app_allatori_proguard(app):

    #create a working-dir
    appDir=os.path.join(dataset,app)
    apkFile = os.path.join(appDir, (app+'.apk'))
    #create a working-dir
    workingDir =os.path.join(appDir,'working-dir')
    
    if os.path.exists(os.path.join(appDir,app+'_all.apk')) or os.path.exists(os.path.join(dataset,app,'allatori_finished')):
        if not os.path.exists(os.path.join(dataset,app,'allatori_finished')):
            open(os.path.join(dataset,app,'allatori_finished'),'a').close()
        print ('already obfuscated: '+apkFile)
        return 
    if not os.path.exists(workingDir):
        os.makedirs(name=workingDir)
    #run apktool
    apktool_output = os.path.join(workingDir, 'apktool-output')
    if not os.path.exists(apktool_output):
        apktoolCmd = '{0} d {1} -output {2}'.format(apktool, apkFile, apktool_output)
        os.system(apktoolCmd)
    movedManifest=False
    if os.path.exists(apktool_output):
        unarchivedPath = os.path.join(workingDir,app)
        #unarchive the apk file
        if not zipfile.is_zipfile(apkFile):
            print_error('invalid-apk,'+app+','+apkFile+','+str(sys.exc_info())+'\n')
            return
        if not os.path.exists(unarchivedPath):
            zApk = zipfile.ZipFile(apkFile)        
            zApk.extractall(unarchivedPath)
        if (os.path.exists(unarchivedPath)):
            print('Unarchived '+apkFile)    
    
            #trivial techniques            
            ########################### #resigning the apk
            try:
                resignedApkFile = os.path.join(appDir, (app+'_resign.apk'))
                if not os.path.exists(resignedApkFile):
                    shutil.copyfile(apkFile, resignedApkFile)
                    signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, resignedApkFile)
                    print (signApkCmd)
                    os.system(signApkCmd)
                    signApkCmd=''
            except:
                print_error('resign,'+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
            
            ########################### repackaging the app. Apktool d -> apktool b
            try:
                repackagedApkFile = os.path.join(appDir, (app+'_repack.apk'))
                if not os.path.exists(repackagedApkFile):
                    repackagingCmd = '{0} build -o {1} {2}'.format(apktool, repackagedApkFile, apktool_output)
                    print (repackagingCmd)
                    os.system(repackagingCmd)
                    if not os.path.exists(repackagedApkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file                        
                        shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                        movedManifest=True
                        print ('Build again: '+repackagingCmd)
                        os.system(repackagingCmd)
                    if os.path.exists(repackagedApkFile):
                        signRepackagedApp = '{0} {1}'.format(sign_apk_with_mahmoud, repackagedApkFile)
                        print(signRepackagedApp)
                        os.system(signRepackagedApp)
                    else:
                        print ('file not found to sign: '+repackagedApkFile)   
            except:
                print_error('repack,'+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()

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
            
            
            #run Allatori obfuscator
                
            ########################### string-encryption obfuscation
            try:               
                prefix='string-encryption'                
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_string_excryption_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx2048m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to .classes
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
            
            ########################### control flow obfuscation
            try:
                prefix='control-flow'
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_control_flow_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx512m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to .classes
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))        
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
            
            ########################### Reorder Members obfuscation
            try:
                prefix='reorder_member'
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_reorder_member_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx512m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    #DX: converts .jar to .classes
                    obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                    if os.path.exists(obfJarFile):
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))        
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()   
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
            
            ########################### Renaming obfuscation
            try:
                prefix='renaming_all'
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_renaming_all_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx512m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to .classes
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))        
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
            
            ########################### Control Flow + Reorder Member obfuscation
            try:
                prefix='cf_rm'
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_cf_rm_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx512m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to .classes
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))        
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
            
            ########################### Control Flow + Reorder Member + renaming obfuscation
            try:
                prefix='cf_rm_renaming'
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_cf_rm_renaming_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx512m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    #DX: converts .jar to .classes
                    if os.path.exists(obfJarFile):
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))        
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
            
            ########################### Control Flow + Reorder Member + String Encryption obfuscation
            try:
                prefix='cf_rm_sencryption'
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_cf_rm_sencryption_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx512m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to .classes
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))        
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()                   

            ########################### All: Control Flow + Reorder Member + renaming + String Encryption  obfuscation
            try:
                prefix='all' #CF_ENC_IR_MR
                if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
                    obfJarFile = str(os.path.join(workingDir,prefix+'-obf-classes.jar'))
                    configFile = os.path.join(workingDir,prefix+'-config.xml')
                    logFile = os.path.join(workingDir,prefix+'-log.xml')
                    cnfg.create_all_config(jarFile, obfJarFile, androidJar, logFile, configFile)
                    allatoriCmd = 'java -Xms128m -Xmx512m -jar {0} {1}'.format(allatori, configFile)
                    print (allatoriCmd)
                    os.system(allatoriCmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to .classes
                        obfDexFile = os.path.join(workingDir,prefix+'-classes.dex')
                        DxCmd = 'java -jar {0} --dex --output {1} {2}'.format(dx, obfDexFile, obfJarFile)
                        print (DxCmd)
                        os.system(DxCmd)
                        #remove old classes.dex and add the new obfuscated one
                        os.remove(dexFile)    
                        shutil.copyfile(obfDexFile, dexFile)
                        #sign the new apk file
                        shutil.copyfile(os.path.join(apktool_output,'apktool.yml'), os.path.join(unarchivedPath,'apktool.yml'))        
                        obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk')
                        buildCmd = '{0} b {1} -output {2}'.format(apktool, unarchivedPath, obf_apkFile)
                        print (buildCmd)
                        os.system(buildCmd)

                        if not os.path.exists(obf_apkFile) and not movedManifest:
                        #try build an apk file after moving the AndroidManifest file
                            movedManifest = True
                            shutil.copyfile(os.path.join(apktool_output,'AndroidManifest.xml'), os.path.join(unarchivedPath,'AndroidManifest.xml'))
                            print ('Build again: '+buildCmd)
                            os.system(buildCmd)
                        
                        if os.path.exists(obf_apkFile):
                            signApkCmd = '{0} {1}'.format(sign_apk_with_mahmoud, obf_apkFile)
                            print (signApkCmd)
                            os.system(signApkCmd)
                        else:
                            print(obf_apkFile+' file is not found.')   
                    else:
                        print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                        handleException()
            except:
                print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
                handleException()   
#             ########################### ProGuard obfuscation
#             try:                
#                 prefix = 'proguard'
#                 if not os.path.exists(os.path.join(appDir,app+'_'+prefix+'.apk')):
#                     print 'obfuscate using proguard'                                    
#                     proguard.proguard_obfuscate_app(app)
#             except:    
#                 print_error(prefix+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
#                 handleException()   
        else:
            print_error('py-zipfile-unzip'+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
            print ('Error: Unable to unzip '+apkFile)    
        
        #aapt remove -f ./original-test.apk ./classes.dex
        #aapt add -f ./original-test.apk ./classes.dex
    else:
        print_error('apktool-decode'+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
        print ('Error: Unable to run apktool on '+apkFile)
        
    open(os.path.join(dataset,app,'allatori_finished'),'a').close()    
    print('Finished '+apkFile)    
    

################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
#    print 'started ...'
    proguard.check_androguard_config(os.path.join(libDir,'proguard-android.pro'))
    print ('Welcome to Allattori obfuscator ...')        
#     obfuscate_app_allatori_proguard('test')
    
    i=0
    print ('Obfuscate apps in '+dataset)
    apps = [d for d in os.listdir(dataset) if os.path.isdir(os.path.join(dataset, d))]
    for app in apps:
        print ('Obfuscate '+app+' --------------------- ')
        try:
            obfuscate_app_allatori_proguard(app)
        except:
            print ('Error: '+app)
            pass    
        i+=1
    print (str(i)+' apps obfuscated')   


