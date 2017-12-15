'''
Created on July 5, 2017

@author: Mahmoud
'''

import sys, os, operator

results_dir = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/study_results'

def print_dic(dic, key):
    try:
        return dic[key]
    except:
        return ''
    
def printUsage():
    print ('Usage: python process_db_results.py FILE_PATH')

if len(sys.argv) < 2:
    printUsage()
    sys.exit()

result_file_path = sys.argv[1]    
result_file = open(result_file_path,'r')

dims = ['Original','ALIGN','DR','MAN','REPACK','CF','CR','ENC','IR','JUNK','MR','REF','CF_ENC','CF_IR','CF_MAN','CF_MR','CR_MAN','ENC_IR','ENC_MAN','JUNK_MAN','MAN_REF','CF_CR_MAN','CF_ENC_IR','CF_ENC_MR','CF_IR_MR','CF_REF_MAN','ENC_REF_MAN','CF_ENC_IR_MR','CF_CR_ENC_MAN_REF','CF_CR_ENC_JUNK_MAN_REF']
# dims = ['Original','APKTOOL','ALLATORI','DROIDCHAMELEON','PROGUARD','DASHO','ADAM']
# dims = ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']


class av_strategies:
    av = ''
    strategy_performance = {}
    strategy_fscore = {}
    
    def __init__(self, av_name):
        self.av=av_name
        self.strategy_performance = {}
        self.strategy_fscore = {}
        
    def add_strategy(self, strategy, values):
        self.strategy_performance[strategy] = values
        self.strategy_fscore[strategy] = (values[values.rfind(',')+1::]).replace(',','')
        
        
    
       
    def __str__(self):
#         sorted_strategies = sorted(self.strategy_performance, key=operator.itemgetter(0))
#         return self.av+','+str(sorted_strategies).replace('[','').replace(']','').replace('\'','').replace(' ','')
#         return self.av+','+str(self.strategy_performance).replace('\'','').replace('{','').replace('}','').replace(':',',').replace(' ','')

        sep = ','
        ret_str = '' # self.av
        for dim in dims:
            #statistics line
            strategy_perf = ',,,,,,,,,,,'
            if dim in self.strategy_performance:
                strategy_perf = self.strategy_performance[dim]
            ret_str = ret_str+sep+strategy_perf.replace(self.av+',','')

        #return self.av+ret_str
        return self.av+ret_str
        
    def __repr__(self):
        return self.__str__()

    def av_strategies_fscore(self):
        sep = ','
        ret_fscore_str = ''
        for dim in dims:
            #only the fscore
            strategy_perf = ''
            if dim in self.strategy_fscore:
                strategy_perf = self.strategy_fscore[dim]
            ret_fscore_str = ret_fscore_str+sep+strategy_perf

        return self.av+ret_fscore_str


def av_obfuscation_strategy():
    anti_malwares = {}
           
    for l in result_file:
        values =  l.strip().split(',')
        per_what = values[0]
        pos = per_what.rfind('-')
        dim1 = per_what[0:pos].strip() #anti-malware        
        dim2 = per_what[pos+1::].strip() #obfuscation strategy
        if len(dim2)==0:
            dim2='Original'
        new_line = dim1+','+dim2+','+str(values[1::]).replace('[','').replace(']','').replace('\'','').replace(' ','')
        my_av_strategies = None    
        if dim1 not in anti_malwares:
            my_av_strategies = av_strategies(dim1) 
            anti_malwares[dim1] = my_av_strategies
        else:
            my_av_strategies = anti_malwares[dim1]
        
        my_av_strategies.add_strategy(dim2, new_line)    
            
    new_result_file_path = result_file_path.replace('.csv','_dimensions.csv')
    fscore_result_file_path = result_file_path.replace('.csv','_dimensions_fscore.csv')
    new_results = open(new_result_file_path,'w+')
    fscore_results = open(fscore_result_file_path,'w+')
    
    header='Anti-malware'
    fscore_header = 'Anti-malware'
    for dim in dims:
        header = header+','+dim+',Apps,TP,FN,TN,FP,Accuracy (%),Precision (%),Recall (%),'+dim
        fscore_header = fscore_header + ','+dim
    
    new_results.write(header+'\n')
    fscore_results.write(fscore_header+'\n')
    for dim1, av_line in anti_malwares.iteritems() :
        new_results.write(str(av_line)+'\n')        
#         print(av_line.av_strategies_fscore())
        fscore_results.write(av_line.av_strategies_fscore()+'\n')
    
        
#         print ('dim1='+dim1+fscore)
        
#         fscore_results.write(str(av)+'\n')
#         print str(av)
    new_results.close()    
    print 'See the output on '+    new_result_file_path
    print 'For F-score only, see the output on '+    fscore_result_file_path
        
    

def av_obfuscator():
    original = {}
    apktool = {}
    allatori = {}
    dc = {}
    pg = {}
    dasho = {}
    
    anti_malwares = set()
           
    for l in result_file:
        values =  l.strip().split(',')
        per_what = values[0]
        pos = per_what.rfind('-')
    #     print dims+'  '+ str(pos)
        dim1 = per_what[0:pos]
        dim2 = per_what[pos+1::]
        if len(dim2)==0:
            dim2='Original'
        anti_malwares.add(dim1)
        new_line = dim1+','+dim2+','+str(values[1::]).replace('[','').replace(']','').replace('\'','').replace(' ','')
        if 'ORIGINAL' in dim2.upper():
            original[dim1] = new_line 
        elif 'APKTOOL' in dim2.upper() :
            apktool[dim1] = new_line
        elif 'ALLATORI' in dim2.upper():
            allatori[dim1] = new_line
        elif 'DROIDCHAMELEON' in dim2.upper():
            dc[dim1] = new_line
        elif 'PROGUARD' in dim2.upper():
            pg[dim1] = new_line
        elif 'DASHO' in dim2.upper():
            dasho[dim1] = new_line
    
    sep = ','
    new_result_file_path = result_file_path.replace('.csv','_dimensions.csv')
    new_results = open(new_result_file_path,'w+')
#     h = 'AV,Obfuscator,Apps,TP,FN,TN,FP,Accuracy (%),Precision (%),Recall (%),F_score (%),'
    h = 'Anti-malware,Obfuscator,Apps,TP,FN,TN,FP,Accuracy (%),Precision (%),Recall (%),'
    header = h+'Original,'+h+'Apktool,'+h+'Allatori,'+h+'DroidChameleon,'+h+'ProGuard,'+h+'DashO'+'\n'
    new_results.write(header)
    for av in anti_malwares:
        new_results.write(print_dic(original,av)+sep+print_dic(apktool,av)+sep+print_dic(allatori,av)+sep+print_dic(dc,av)+sep+print_dic(pg,av)+sep+print_dic(dasho,av)+'\n')
    new_results.close()    
    print 'See the output on '+    new_result_file_path
    

#/Users/Mahmoud/Documents/PhD_projects/Obfuscation/study_results/detection_per_av_obfuscator.csv
# av_obfuscator()

#
av_obfuscation_strategy()
        
    
