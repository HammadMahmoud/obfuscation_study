'''
Created on May 27, 2017

@author: Mahmoud
'''

import postfile, json, datetime, os, time, sys, re

ONLY_ADAM=True

if ONLY_ADAM:
    print 'This program will only upload apks obfuscated by ADAM obfuscator'
    
def printUsage():
    print ('python upload_apks_vt.py obfuscation_study_dir file_suffix')

if len(sys.argv) < 3:
    printUsage()
    sys.exit()


key = 'ADD_YOUR_VIRUS_TOTAL_KEY_HERE' 

frameworkDir = sys.argv[1]  
file_suffix =   sys.argv[2]

scan_ids_path = os.path.join(frameworkDir, 'vt_results','scan_ids_'+file_suffix+'.txt')

already_scanned_apps = set()
if os.path.exists(scan_ids_path):
    for l in open(scan_ids_path,'r'):
        already_scanned_apps.add(l.split(':')[0].strip())

scan_ids_path = open(scan_ids_path,'a+')    
jsons_file = open(os.path.join(frameworkDir, 'vt_results','jsons_'+file_suffix+'.txt'),'a+')
error_file = open(os.path.join(frameworkDir, 'vt_results','error_'+file_suffix+'.txt'),'a+')
db_file = open(os.path.join(frameworkDir, 'vt_results','db_file_'+file_suffix+'.csv'),'a+')
db_file.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format('scan_id','sha256','analysis_link','dataset','minor_dataset','apk_path','obfuscator','obf_strategy'))



print (str(len(already_scanned_apps))+' apps already uploaded to VT.')
    
##### methods
def send_apk_to_vt(apkFilePath):
    """
    send an apk file to the VirusTotal service to be placed on the analysis queue and write the JSON results on a file,
    note that each JSON object contains scan_id attribute which will be used later to pull the analysis result
    PARAMS:
        apkPath: full path to the apk
    """

#     return '{"scan_id": "scn_id-1495910015", "sha1": "sha1_11", "resource": "d690e4c35df8b12b2853665ad58e7b024bfdaa1dc300e7486ca7a1cdd74b762e", "response_code": 1, "sha256": "d690e4c35df8b12b2853665ad58e7b024bfdaa1dc300e7486ca7a1cdd74b762e", "permalink": "https://www.virustotal.com/file/d690e4c35df8b12b2853665ad58e7b024bfdaa1dc300e7486ca7a1cdd74b762e/analysis/1495910015/", "md5": "6d03ce83166a96ced3fc6b9667737f2e", "verbose_msg": "Scan request successfully queued, come back later for the report"}'
    
    host = "www.virustotal.com"
    selector = "https://www.virustotal.com/vtapi/v2/file/scan"
    fields = [("apikey", key)]
    file_to_send = open(apkFilePath, "rb").read()
    files = [("file", apkFilePath, file_to_send)]
    jsondata = postfile.post_multipart(host, selector, fields, files)
    return jsondata

def get_obf_strategy_dc(obfuscator, obf_strategy):
    
    return {'t0':'manifest',
            't1':'cr_junk', #control reorder and insert junk code such as nop operation
            't2':'cf',
            't3':'ir',
            't4':'enc',
            't5':'ref',
            't6':'manifest_cr_junk',
            't7':'manifest_cf',
            't8':'manifest_ir',
            't9':'manifest_enc',
            't10':'manifest_ref',
            't11':'manifest_cf_ir',
            't12':'manifest_cf_enc',
            't13':'manifest_cf_ref',
            't14':'manifest_enc_ref',
            't15':'manifest_cf_ir_enc_ref',
            't16':'manifest_cr_junk_cf_ir_enc_ref'
            }.get(obf_strategy)
            

def store_vt_result(apk_path, minor_dataset, dataset, obfuscator, obf_strategy):
    try:
        scan_id='-----'
        jsondata = send_apk_to_vt(apk_path)
        jsons_file.write(jsondata+'\n')
        response = json.loads(jsondata)
        scan_id = str(response["scan_id"])
        sha256 = str(response["sha256"])
        analysis_link = str(response["permalink"])
        if scan_id != None and len(scan_id) > 1:
            scan_ids_path.write("{0}:{1}\n".format(apk_path,scan_id))
            if 'DroidChameleon' == obfuscator:
                obf_strategy = get_obf_strategy_dc(obfuscator, obf_strategy)
            db_file.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(scan_id,sha256,analysis_link,dataset,minor_dataset,apk_path,  obfuscator, obf_strategy))            
    except Exception, e:           
        error_file.write("Exception in App:"+apk_path+'\n'+str(e)+'\n')   

################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
    
    dirs = {}
    dataset_dir = '/share/seal/hammadm/obf/Obfuscation/dataset'
    dirs['Benign'] = os.path.join(dataset_dir,'pure_benign_apps')
    dirs['Virusshare'] = os.path.join(dataset_dir,'virusshare')
    dirs ['Italy_study'] = os.path.join(dataset_dir,'matteo_malware')
    dirs ['BrainTest'] = os.path.join(dataset_dir,'BrainTest')
    dirs ['FalseGuide'] = os.path.join(dataset_dir,'falseGuide')
    dirs ['VikingHorde'] = os.path.join(dataset_dir,'VikingHorde')
    
#     dirs ['local Matteo'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/dataset/matteo_malware'
    dirs['local test dataset'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/test_dataset'
#     dirs['Benign'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/test_dataset/one_app_dataset'
    
    for minor_dataset, path in dirs.items():
        if os.path.isdir(path):
            obfuscator=''
            obf_strategy=''
            dataset = 'malicious'
            is_malicious = 1
            if minor_dataset in ('Benign'):
                dataset = 'benign'
                is_malicious = 0
                
            inputs = [a for a in os.listdir(path) if os.path.isdir(os.path.join(path,a))]

            for input in inputs:
                apps = [a for a in os.listdir(os.path.join(path,input)) if os.path.isdir(os.path.join(path,input))]
                
                for a in apps:
                    if not ONLY_ADAM:
                        #DroidChameleon
                        for i in range(0,17):
                            apk = 't'+str(i)+'_'+a+'.apk'
                            if os.path.exists(os.path.join(path,input,a,apk)):
                                
                                if os.path.join(path,input,a,apk) not in already_scanned_apps:
                                    obfuscator='DroidChameleon'
                                    obf_strategy = 't'+str(i)
                                    store_vt_result(os.path.join(path,input,a,apk), minor_dataset, dataset, obfuscator, obf_strategy)                            
                            
                    obfuscator='---'
                    if os.path.isdir(os.path.join(path,input,a)):                    
                        for apk in os.listdir(os.path.join(path,input,a)):
                            if not ONLY_ADAM and re.match('t\d*_'+a+'.apk',apk): #DroidChameleon app
                                continue                            
                            if ONLY_ADAM and '-ADAM.apk' not in apk:
                                continue 
                            if apk.endswith('.apk'): 
                                if os.path.join(path,input,a,apk) in already_scanned_apps:
                                    continue

                                if a+'.apk' == apk: #the original app
                                    if dataset == 'benign':
                                        db_file.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format('0','0','0',dataset,minor_dataset,os.path.join(path,input,a,apk),  '', ''))
                                        continue
                                    else:    
                                        obfuscator=''
                                        obf_strategy = ''
                                ##ADAM
                                elif '-ADAM.apk' in apk:                                 
                                    obfuscator='ADAM'
                                    if '-za-ADAM.apk' in apk:
                                        obfuscator='trivial'
                                        obf_strategy = 'ALIGN'
                                    else: #apk=appName-ofN-STRATEGY-ADAM.apk 
                                        obf_strategy = apk.split('-')[-2]
                                                                        
                                ##ProGuard
                                elif '_proguard.apk' in apk:                                 
                                    obfuscator='ProGuard'
                                    obf_strategy = 'ir'                                    
                                ## trivial                
                                elif (a+'_resign.apk') in apk:
                                    obfuscator='trivial'
                                    obf_strategy = 'resigning'                                    
                                elif (a+'_repack.apk') in apk:
                                    obfuscator='trivial'
                                    obf_strategy = 'repackaging'                                    
                                ## Allatori
                                elif (a+'_all.apk') in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'enc_ir_mr'
                                elif (a+'_reorder_member.apk') in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'mr'                                    
                                elif (a+'_renaming_all.apk') in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'ir'                                    
                                elif (a+'_control-flow.apk') in apk or (a+'_control_flow.apk') in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'cf'                                    
                                elif (a+'_string_encryption.apk') in apk or (a+'_string-encryption.apk') in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'enc'                                    
                                elif a+'_cf_rm.apk' in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'cf_mr'                                    
                                elif (a+'_cf_rm_sencryption.apk') in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'cf_enc_mr'
                                elif (a+'_cf_rm_renaming.apk') in apk:
                                    obfuscator='Allatori'
                                    obf_strategy = 'cf_ir_mr'
                                ## DashO                                    
                                elif (a+'_dashO-all.apk') in apk:
                                    obfuscator='dashO'
                                    obf_strategy = 'cf_enc_ir'                                    
                                elif (a+'_dashO-cf-renaming.apk') in apk:
                                    obfuscator='dashO'
                                    obf_strategy = 'cf_ir'                                    
                                elif (a+'_dashO-cf.apk') in apk:
                                    obfuscator='dashO'
                                    obf_strategy = 'cf'
                                elif (a+'_dashO-renaming.apk') in apk:
                                    obfuscator='dashO'
                                    obf_strategy = 'ir'                                    
                                elif (a+'_dashO-str-enc-cf.apk') in apk:
                                    obfuscator='dashO'
                                    obf_strategy = 'cf_enc'                                    
                                elif (a+'_dashO-str-enc-renaming.apk') in apk:
                                    obfuscator='dashO'
                                    obf_strategy = 'enc_ir'                                    
                                elif (a+'_dashO-str-enc.apk') in apk:
                                    obfuscator='dashO'
                                    obf_strategy = 'enc'
                                store_vt_result(os.path.join(path,input,a,apk), minor_dataset, dataset, obfuscator, obf_strategy)
