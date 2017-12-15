'''
Created on July 20, 2017

@author: Mahmoud
'''

import sys, os
# if __name__ == '__main__':
#     handleException()

# dataset ='/Users/Mahmoud/Documents/PhD_projects/Obfuscation/dataset/'
# dataset ='/Volumes/Android/obfuscationStudy/pure_benign_apps/'
# dataset = '/Volumes/Android/obfuscationStudy/dataset/BrainTest/'
# dataset = '/Volumes/Android/obfuscationStudy/dataset/pure_benign_apps'



def printUsage():
    print ('Usage: python run_adam dataset ADAM_project_path')

if len(sys.argv) < 3:
    printUsage()
    sys.exit()

################### Global variables ###################

dataset = sys.argv[1]
ADAM = sys.argv[2]


def handleException():
    pass

def obfuscate_app_adam(app):
    appDir=os.path.join(dataset,app)
    apkFile = os.path.join(appDir, (app+'.apk'))
    
    if os.path.exists(os.path.join(dataset,app,'adam_finished')):            
        return
    try:
        workingDir =os.path.join(appDir,'working-dir')
        if not os.path.exists(workingDir):
            os.makedirs(workingDir)

        adam_cmd = os.path.join(ADAM, 'generateapk.sh')+' '+apkFile
        os.system(adam_cmd) 
        open(os.path.join(dataset,app,'adam_finished'),'a').close()
    except:
        handleException()
    finally:
        if not os.path.exists(os.path.join(dataset,app,'adam_finished')):
            open(os.path.join(dataset,app,'adam_finished'),'a').close()


################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
#    print 'started ...'
    print ('Welcome to ADAM obfuscator ...')        
#     obfuscate_app_allatori_proguard('test')
    
    i=0
    print ('Obfuscate apps in '+dataset)
    apps = [d for d in os.listdir(dataset) if os.path.isdir(os.path.join(dataset, d))]
    for app in apps:
        print ('Obfuscate '+app+' --------------------- ')
        try:
            obfuscate_app_adam(app)
        except:
            print ('Error: '+app)
            pass    
        i+=1
    print (str(i)+' apps obfuscated')   


