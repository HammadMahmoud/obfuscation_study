'''
Created on May 8, 2017

@author: Mahmoud
'''

# if __name__ == '__main__':
#     handleException()

import zipfile, os, shutil, sys

def printUsage():    
    print ('Usage: python run_dashO dataset obfuscation-study-dir errorFileName')

if len(sys.argv) < 4:
    printUsage()
    sys.exit()


dataset = sys.argv[1]
obfuscation_study_dir = sys.argv[2] 
frameworkDir = os.path.join(obfuscation_study_dir, 'framework')
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
dashO = os.path.join(obfuscation_study_dir,'obfuscation_tools','DashO','DashO_8.1','dashocmd')
errorFile = os.path.join(frameworkDir,'logs',errorFileName+'.csv')
error = open(errorFile, 'a+')

def print_error(msg):
    error.write(msg)
    

def handleException():
    pass

def getPrefix(i):
    tool = 'dashO'
    x = tool+ {
            0: '-str-enc-renaming',
            1: '-cf',
            2: '-str-enc',
            3: '-renaming',
            4: '-cf-renaming',
            5: '-str-enc-cf',
            6: '-all',
            }.get(i)
    return x        
    
    
def dashO_obfuscate_app(app):
    print 'DashO obfuscator '+app
    appDir=os.path.join(dataset,app)
    apkFile = os.path.join(appDir, (app+'.apk'))
    if not os.path.exists(apkFile):
        print ('Error: file not found'+apkFile)
        return
    
    workingDir =os.path.join(appDir,'working-dir')
    print ('workingDir:'+workingDir)    

    
    obf_apkFile = os.path.join(appDir,app+'_dashO-all.apk')
    if os.path.exists(obf_apkFile) or os.path.exists(os.path.join(dataset,app,'dashO_finished')):
        print ('DashO: app is already obfuscated '+obf_apkFile)
        if not os.path.exists(os.path.join(dataset,app,'dashO_finished')):
            open(os.path.join(dataset,app,'dashO_finished'),'a').close()
        return

    workingDir =os.path.join(appDir,'working-dir')
    apktool_output = os.path.join(workingDir, 'apktool-output')
    if os.path.exists(workingDir):
        print ('working-dir found '+apkFile)
    else:             
        os.makedirs(workingDir)
    #run apktool if not exists from previous run or from running dashO obfuscator        
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
            
            
            ########################### DashO obfuscation: 
            #DashO is a commercial Java and Android app obfuscator
            if os.path.exists(os.path.join(dataset,app,'dashO_finished')):
                print ('Found dashO_finished file, already obfuscated using DashO '+apkFile)
                return
            movedManifest=False
            for i in range(0,7):
                try:
                    prefix=getPrefix(i)
                    obf_apkFile = os.path.join(appDir,app+'_'+prefix+'.apk') 
                    if os.path.exists(obf_apkFile):
                        continue
                    obfJarFile = str(os.path.join(workingDir,prefix+'.jar'))                
                    if not os.path.exists(obfJarFile):
                        configFile = os.path.join(workingDir,prefix+'-config.dox')
                        shutil.copyfile(os.path.join(libDir,prefix+'-config.dox'), configFile)
                        dashOcmd = '{0} {1}'.format(dashO, configFile)
                        print (dashOcmd)
                        os.system(dashOcmd)
                    if os.path.exists(obfJarFile):
                        #DX: converts .jar to .classes
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
                        if os.path.exists(obf_apkFile):
                            print (obf_apkFile+' is already obfuscated.')
                            continue                        
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
            open(os.path.join(dataset,app,'dashO_finished'),'a').close()

            
        else:
            print_error('py-zipfile-unzip'+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
            print ('Error: Unable to unzip '+apkFile)    
        
        #aapt remove -f ./original-test.apk ./classes.dex
        #aapt add -f ./original-test.apk ./classes.dex
    else:
        print_error('apktool-decode'+','+app+','+apkFile+','+str(sys.exc_info())+'\n')
        print ('Error: Unable to run apktool on '+apkFile)

    open(os.path.join(dataset,app,'dashO_finished'),'a').close()    
    print('DashO finished '+apkFile)    
    

def check_dashO_config(file):
    f = open(file, 'r')
    for l in f:
        if '<property name="sdk.dir"' in l:
            jar = (l.replace('\n','').split('value="')[1]).replace('"/>','').strip()
            print ('check if '+jar+' exists.')
            if not (os.path.exists(jar)):
                print ('directory '+jar+' is not exists. Update '+file+' accordingly.')
                sys.exit()
                return False
        if 'pathelement' in l and '.jar' in l:   
            jar = (l.replace('\n','').split('location="')[1]).replace('"/>','').strip()
            print ('check if '+jar+' exists.')
            if not (os.path.exists(jar)):
                print ('File '+jar+' is not exists. Update '+file+' accordingly.')
                sys.exit()
                return False            
            break   
    print ('The config file looks good!')    
    return True



################### Main ###################

# stuff to run always here such as class/def
def main():        
    pass

if __name__ == "__main__":
    
    for i in range(0,7):
        check_dashO_config(os.path.join(libDir,getPrefix(i)+'-config.dox'))

#     dashO_obfuscate_app('test')

    #when no-array job is available    
    originalApksDir = dataset
    inputs = [d for d in os.listdir(dataset) if os.path.isdir(os.path.join(dataset, d))]
    for input in inputs:
        dataset = os.path.join(originalApksDir,input)
        print (dataset) 
        print ('Obfuscate apps in '+dataset)
        apps = [d for d in os.listdir(dataset) if os.path.isdir(os.path.join(dataset, d))]
        for app in apps:
            try:
                print ('Obfuscate '+app+' --------------------- ')
                dashO_obfuscate_app(app)
            except:
                print ('Error: '+app)
                pass    

#code for array-job on hpc    
#     i=0
#     print ('Obfuscate apps in '+apksDir)
#     apps = [d for d in os.listdir(apksDir) if os.path.isdir(os.path.join(apksDir, d))]
#     for app in apps:
#         try:
#             print ('Obfuscate '+app+' --------------------- ')
#             dashO_obfuscate_app(app)
#         except:
#             print ('Error: '+app)
#             pass    
#         i+=1
#     print (str(i)+' apps obfuscated')   
#           
#     print (str(i)+' apps obfuscated using DashO')   

