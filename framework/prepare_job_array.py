'''
Created on Apr 30, 2017

@author: Mahmoud
'''

import os, sys
import shutil


################### Main ###################
# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
    
    dirs = {}
    dataset_dir = '/share/seal/hammadm/obf/Obfuscation/dataset'
    dirs['VikingHorde'] = os.path.join(dataset_dir,'VikingHorde')
#     dirs['FalseGuide'] = os.path.join(dataset_dir,'falseGuide')
#     dirs['Benign'] = os.path.join(dataset_dir,'pure_benign_apps')
#     dirs['Virusshare'] = os.path.join(dataset_dir,'virusshare')
#     dirs ['Matteo'] = os.path.join(dataset_dir,'matteo_malware')
#     dirs ['BrainTest'] = os.path.join(dataset_dir,'BrainTest')
    
#     dirs ['local Matteo'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/dataset/matteo_malware'
#     dirs['local test dataset'] = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/test_dataset'
    
#     '/share/seal/hammadm/obf/Obfuscation/dataset/matteo_malware'
    cleaned_apps = 0
    dc_finished = 0
    signed_apks = 0
    for dir, path in dirs.items():
        i = 1
        if os.path.isdir(path):
            apps = [a for a in os.listdir(path) if os.path.isdir(os.path.join(path,a))]
            for a in apps:
                input_path = os.path.join(path,'input.'+str(i))
                if not os.path.exists(input_path):
                    os.makedirs(input_path)
                    shutil.move(os.path.join(path,a), os.path.join(input_path,a))
                    i+=1
