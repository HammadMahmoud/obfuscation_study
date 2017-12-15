'''
Created on Apr 30, 2017

@author: Mahmoud
'''

import os, sys

print_header = True

def printUsage():
    print ('python obfuscated_apps_statistics.py print_details[Y|N]')

if len(sys.argv) < 2:
    printUsage()
    sys.exit()
    
print_details = sys.argv[1].lower()
############### inner class
class Stat:      
    dataset_name=''
    path = ''
    apps = 0
    all_apks = 0 #number of apks
    
    allatori_tried=0
    dc_tried=0 #droic chameleon
    proguard_tried=0
    t0=0
    t1=0
    t2=0    
    t3=0    
    t4=0    
    t5=0    
    t6=0    
    t7=0    
    t8=0    
    t9=0    
    t10=0    
    t11=0    
    t12=0    
    t13=0    
    t14=0    
    t15=0    
    t16=0    
    proguard=0

    resign=0    
    repack=0    
    zipalaign=0

    allatori_string_encryption=0
    reorder_member=0    
    renaming_all=0    
    control_flow=0
    cf_rm=0    
    cf_rm_sencryption=0    
    cf_rm_renaming=0    
    allatori_all=0
    
    dashO_tried=0
    dashO_all=0
    dashO_cf=0
    dashO_renaming=0
    dashO_str_enc_cf=0
    dashO_cf_renaming=0
    dashO_str_enc=0
    dashO_str_enc_renaming=0
    
    adam_tried=0
    adam_junk=0
    adam_ir=0
    adam_cf=0
    adam_enc=0
    
    
    def __init__(self):
        self.dataset_name=''
        
    def print_stat(self, print_header):
            self.dc_tried = max(self.dc_tried, self.t0)
            trivial = self.resign+self.repack+self.zipalaign
            allatori = self.allatori_string_encryption + self.reorder_member+ self.renaming_all+ self.control_flow+ self.cf_rm+ self.cf_rm_sencryption+ self.cf_rm_renaming+ self.allatori_all                        
            dc = self.t0+self.t1+self.t2+self.t3+self.t4+self.t5+self.t6+self.t7+self.t8+self.t9+self.t10+self.t11+self.t12+self.t13+self.t14+self.t15+self.t16
            dashO = self.dashO_all+self.dashO_cf +self.dashO_renaming +self.dashO_str_enc_cf +self.dashO_cf_renaming +self.dashO_str_enc +self.dashO_str_enc_renaming
            adam = self.adam_cf+self.adam_enc+self.adam_ir+self.adam_junk
            all_obfuscated_apps = self.proguard + trivial + allatori + dc + dashO + adam
             
            print ('------------------------------------------------ All APKs:'+str(self.all_apks))
            print (self.path)        
            print('{0} [{1} original apps, {2} obfuscated apps, {3} total apps]'.format(self.dataset_name, self.apps, all_obfuscated_apps, (self.apps + all_obfuscated_apps)))
            
            
            print ('\tTrivial Obfuscation\t[{0}]'.format(str(trivial)))
            print ('\t\tResigning\t'+str(self.resign))
            print ('\t\tRepackaging\t'+str(self.repack))
            print ('\t\tZipAlaigning\t'+str(self.zipalaign))
            
            print ('\tProGuard\t[{0}]'.format(str(self.proguard))+' tried:'+str(self.proguard_tried)+'/'+str(self.apps))

            print ('\tAllatori[{0}]'.format(allatori)+' tried:'+str(self.allatori_tried)+'/'+str(self.apps))
            print ('\t\tString Encryption\t'+str(self.allatori_string_encryption))
            print ('\t\tReorder Members\t'+str(self.reorder_member))
            print ('\t\tRenaming\t'+str(self.renaming_all))
            print ('\t\tControl flow\t'+str(self.control_flow))
            print ('\t\tControl flow & reorder members\t'+str(self.cf_rm))
            print ('\t\tControl flow, reorder member, and string encryption\t'+str(self.cf_rm_sencryption))
            print ('\t\tControl flow, reorder member, and renaming\t'+str(self.cf_rm_renaming))
            print ('\t\tAll\t'+str(self.allatori_all))
                        
            print('\tDroidChameleon[{0}]'.format(str(dc))+' tried:'+str(self.dc_tried)+'/'+str(self.apps))
            dc_comma_sep = ''
            for i in range(0,17):
                x = getattr(self, 't'+str(i))                 
                print ('\t\tT{0}\t{1}'.format(str(i),str(x)))
                dc_comma_sep = dc_comma_sep + ',' + str(x)

            print ('\tDashO[{0}]'.format(dashO)+' tried:'+str(self.dashO_tried)+'/'+str(self.apps))
            print ('\t\tString Encryption\t'+str(self.dashO_str_enc))            
            print ('\t\tRenaming\t'+str(self.dashO_renaming))
            print ('\t\tControl flow\t'+str(self.dashO_cf))
            print ('\t\tString encryption & control flow\t'+str(self.dashO_str_enc_cf))            
            print ('\t\tControl flow & renaming\t'+str(self.dashO_cf_renaming))
            print ('\t\tString encryption & renaming\t'+str(self.dashO_str_enc_renaming))
            print ('\t\tAll\t'+str(self.dashO_all))

            print ('\tADAM[{0}]'.format(adam)+' tried:'+str(self.adam_tried)+'/'+str(self.apps))
            print ('\t\tJUNK\t'+str(self.adam_junk))            
            print ('\t\tRenaming\t'+str(self.adam_ir))
            print ('\t\tControl flow\t'+str(self.adam_cf))
            print ('\t\tString Encryption\t'+str(self.adam_enc))            
            

            
            header = '{0}{1}{2}{3}{4}'.format('Dataset,Original,Obfuscated, Total apps,',
            'Trivial,Resigning,Repackaging,ZipAlaigning,ProGuard,',
            'Allatori,String Encryption,Reorder Members,Renaming,Control flow,CF_RM, CF_RM_SE,CF_RM_IR,Allatori_All,',
            'DroidChameleon,T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,',
            'DashO,String Encryption (SE),Control Flow (CF),Identifier Renaming (IR),SE_CF,CF_IR,SE_IR,All,',
            'ADAM,JUNK,IR,CF,ENC'
            )
            sep = ',' 
            v0 = str(self.dataset_name)+sep+ str(self.apps)+sep+ str(all_obfuscated_apps)+sep+ str((self.apps + all_obfuscated_apps))+sep
            v1 = str(trivial)+sep+str(self.resign)+sep+str(self.repack)+sep+str(self.zipalaign)+sep+ str(self.proguard)+sep
            v2 = str(allatori)+sep+str(self.allatori_string_encryption)+sep+str(self.reorder_member)+sep+str(self.renaming_all)+sep+str(self.control_flow)+sep+str(self.cf_rm)+sep+str(self.cf_rm_sencryption)+sep+str(self.cf_rm_renaming)+sep+str(self.allatori_all)+sep
            v3 = str(dc)+dc_comma_sep+sep
            v4=  str(dashO)+sep+str(self.dashO_str_enc)+sep+str(self.dashO_cf)+sep+ str(self.dashO_renaming)+sep+str(self.dashO_str_enc_cf)+sep+str(self.dashO_cf_renaming)+sep+str(self.dashO_str_enc_renaming)+sep+str(self.dashO_all)
            v5 = str(adam)+sep+str(self.adam_junk)+sep+str(self.adam_ir)+sep+str(self.adam_cf)+sep+str(self.adam_enc)
            
            if print_header:
                print (header)
                
            row = v0+v1+v2+v3+v4+v5
            print row
            

################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
    
    dirs = {}
    dataset_dir = '/share/seal/hammadm/obf/Obfuscation/dataset'
    dirs['Benign'] = os.path.join(dataset_dir,'pure_benign_apps')
    dirs['Virusshare'] = os.path.join(dataset_dir,'virusshare')
    dirs ['study'] = os.path.join(dataset_dir,'matteo_malware')
    dirs ['BrainTest'] = os.path.join(dataset_dir,'BrainTest')
    dirs ['FalseGuide'] = os.path.join(dataset_dir,'falseGuide')
    dirs ['VikingHorde'] = os.path.join(dataset_dir,'VikingHorde')
    
#     dirs ['local Matteo'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/dataset/matteo_malware'
#     dirs['local test dataset'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/test_dataset'
    dirs['local dataset'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/dataset'
    
    
#     '/share/seal/hammadm/obf/Obfuscation/dataset/matteo_malware'
    
    if print_details == 'n':
        benign_stat = Stat()
        benign_stat.dataset_name = 'Benign'
        
        malicious_stat = Stat()
        malicious_stat.dataset_name = 'Malicious'
     
            
    
    for dir, path in dirs.items():
        if os.path.isdir(path):
            
            if print_details == 'y':
                stat = Stat()
                stat.dataset_name = dir
                stat.path = path
            else:
                if dir in ('Benign'):
                    stat = benign_stat                    
                    stat.path = path
                else:
                    stat = malicious_stat                    
                    stat.path = stat.path+':'+path
                        
                        
            inputs = [a for a in os.listdir(path) if os.path.isdir(os.path.join(path,a))]
            
            for input in inputs:                
                apps = [a for a in os.listdir(os.path.join(path,input)) if os.path.isdir(os.path.join(path,input,a))]
#                 print (input+'-->'+str(apps))
                stat.apps += len(apps)
                for a in apps:
                    if os.path.exists(os.path.join(path,input,a,'allatori_finished')) or os.path.exists(os.path.join(path,input,a,a+'_string-encryption.apk')):
                        stat.allatori_tried+=1
                    if os.path.exists(os.path.join(path,input,a,'dc_finished')) or os.path.exists(os.path.join(path,input,a,'t0_'+a+'.apk')):
                        stat.dc_tried+=1
                    if os.path.exists(os.path.join(path,input,a,'proguard_finished')) or os.path.exists(os.path.join(path,input,a,a+'_proguard.apk')):
                        stat.proguard_tried+=1
                    if os.path.exists(os.path.join(path,input,a,'dashO_finished')) or os.path.exists(os.path.join(path,input,a,a+'_dashO-str-enc.apk')):
                        stat.dashO_tried+=1
                    if os.path.exists(os.path.join(path,input,a,'adam_finished')):
                        stat.adam_tried+=1
                            
                    for i in range(0,17):
                        apk = 't'+str(i)+'_'+a+'.apk'
                        if os.path.exists(os.path.join(path,input,a,apk)):
                            x = getattr(stat, 't'+str(i))
                            setattr(stat, 't'+str(i), x+1)
                    
                    if os.path.isdir(os.path.join(path,input,a)):                    
                        for apk in os.listdir(os.path.join(path,input,a)):
                            if apk.endswith('.apk'):
                                stat.all_apks+=1
                                if '_proguard.apk' in apk:                                 
                                    stat.proguard += 1            
                                elif (a+'_resign.apk') in apk:
                                    stat.resign+=1    
                                elif (a+'_repack.apk') in apk:
                                    stat.repack+=1    
                                elif (a+'-za-ADAM.apk') in apk:
                                    stat.zipalaign+=1    
                                ## Allatori      
                                elif (a+'_all.apk') in apk:
                                    stat.allatori_all+=1    
                                elif (a+'_reorder_member.apk') in apk:
                                    stat.reorder_member+=1    
                                elif (a+'_renaming_all.apk') in apk:
                                    stat.renaming_all+=1    
                                elif (a+'_control-flow.apk') in apk or (a+'_control_flow.apk') in apk:
                                    stat.control_flow+=1    
                                elif (a+'_string_encryption.apk') in apk or (a+'_string-encryption.apk') in apk:
                                    stat.allatori_string_encryption+=1    
                                elif a+'_cf_rm.apk' in apk:
                                    stat.cf_rm+=1    
                                elif (a+'_cf_rm_sencryption.apk') in apk:
                                    stat.cf_rm_sencryption+=1    
                                elif (a+'_cf_rm_renaming.apk') in apk:
                                    stat.cf_rm_renaming+=1    
                                elif (a+'_cf_rm_renaming.apk') in apk:
                                    stat.cf_rm_renaming+=1    
                                ## DashO                                    
                                elif (a+'_dashO-all.apk') in apk:
                                    stat.dashO_all +=1    
                                elif (a+'_dashO-cf-renaming.apk') in apk:
                                    stat.dashO_cf_renaming +=1    
                                elif (a+'_dashO-cf.apk') in apk:
                                    stat.dashO_cf +=1    
                                elif (a+'_dashO-renaming.apk') in apk:
                                    stat.dashO_renaming +=1    
                                elif (a+'_dashO-str-enc-cf.apk') in apk:
                                    stat.dashO_str_enc_cf +=1    
                                elif (a+'_dashO-str-enc-renaming.apk') in apk:
                                    stat.dashO_str_enc_renaming +=1    
                                elif (a+'_dashO-str-enc.apk') in apk:
                                    stat.dashO_str_enc +=1
                                ## ADAM                                    
                                elif (a+'-of1-JUNK-ADAM.apk') in apk:
                                    stat.adam_junk+=1    
                                elif (a+'-of2-IR-ADAM.apk') in apk:
                                    stat.adam_ir+=1    
                                elif (a+'-of3-CF-ADAM.apk') in apk:
                                    stat.adam_cf+=1    
                                elif (a+'-of4-ENC-ADAM.apk') in apk:
                                    stat.adam_enc+=1    
#                                 else:
#                                     print 'else:'+apk        
            if print_details == 'y':                        
                stat.print_stat(print_header)
                print_header=False
         
    if print_details == 'n':
        benign_stat.print_stat(print_header)            
        print_header=False
        malicious_stat.print_stat(print_header)
            
     
#     groups = [d for d in os.listdir(apksDir) if d.endswith('.apk') ]  
#     for app in groups:
