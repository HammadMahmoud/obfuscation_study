import os, sys
from datetime import datetime
# import datetime 
# import glob

# sys.path.append('/usr/local/bin/')

def printUsage():
    print('Usage: python runDroidChameleon dataset obfuscation_study_dir')


if len(sys.argv)<3:
    printUsage()
    sys.exit()
    
dataset = sys.argv[1]
obfuscation_study_dir = sys.argv[2]
#outputDir = 'obfuscatedMalgenome'
outputDir = 'reflection_malgenome'
droidc_script = os.path.join(obfuscation_study_dir,'obfuscation_tools','DroidChameleon','android-av','droidc')


libDir = os.path.join(obfuscation_study_dir,'framework','lib')
apktool = 'java -jar '+os.path.join(libDir,'apktool_2.0.1.jar')+' '


groups = os.listdir(dataset)

#Obfuscation study: when the number increases, the complexity increases

#one transformation
t0='-transformAndroidManifest '                 #MAN
t1='-reverseorder -insertnops -remDebugInfo '   #JUNK
t2='-insertFunctionIndirection '                #CF
t3='-renameclasses '                            #CR
t4='-encArrays -encString '                     #ENC
t5='-reflection '                               #REF

#combination of obfuscation
t6 = t0+t1  #MAN_JUNK
t7 = t0+t2  #CF_MAN
t8 = t0+t3  #MAN_CR
t9 = t0+t4  #MAN_ENC
t10 = t0+t5  #MAN_REF
t11= t0+t2+t3 #MAN_CF_CR
t12= t0+t2+t4 #CF_ENC_MAN considered as CF_ENC in the paper
t13= t0+t2+t5 #MAN_CF_REF
t14= t0+t4+t5 #MAN_ENC_REF
t15 = t0 + t2+ t3 + t4 + t5 #MAN_CF_CR_ENC_REF
t16 = t0 + t1 + t2+ t3 + t4 + t5 #MAN_JUNK_CF_CR_ENC_REF

#prefix='ref_'

trans = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16]
# trans = [t_ref]

c=0;

fileName = ('run_droidchameleon_'+str(datetime.now())+'.z').replace(' ','-') 
log_file = open(os.path.join(obfuscation_study_dir,'framework','logs',fileName),'w')
log_file.write("script started at: "+str(datetime.now())+"\n")
log_file.write('start time:'+str(datetime.now()))
# c = c + i;
for app in groups:
    apk = os.path.join(dataset,app,(app+'.apk'))
    t1 = datetime.now()
    if os.path.exists(apk):
        print ('----------------------------------------------------------\n')
        print(apk)
        if os.path.exists(os.path.join(dataset,app,('t16_'+app+'.apk'))) or os.path.exists(os.path.join(dataset,app,'dc_finished')):
            print ('App '+apk+' is already obfuscated using DroidChameleon')
            continue
        else:
            for i in range(0,len(trans)):
                print ('---------------------------T'+str(i)+'-------------------------------')
                prefix = 't'+str(i)+'_'
                out_app = os.path.join(dataset,app,prefix+app+'.apk')
                appLog = os.path.join(obfuscation_study_dir,'framework','logs','droidchameleon',app+'.log')
                if not os.path.exists(out_app):
                    cmd = 'python {0} {1} {2} {3}'.format(droidc_script, trans[i], apk, out_app)
                    print cmd
                    try:
                        os.system(cmd)
                    except:
                        log_file.write("Exception:  "+cmd+"\n")
                        pass
                    finally:
                        os.system("rm -rf " + os.path.join(dataset,app,app))
            open(os.path.join(dataset,app,'dc_finished'),'a').close()       
            t2 = datetime.now()
            t = t2 - t1
            print ('It took '+str(t.seconds)+' seconds to obfuscate '+apk+' using DC') 
log_file.write('finished: '+str(datetime.datetime.now()))
log_file.close()

