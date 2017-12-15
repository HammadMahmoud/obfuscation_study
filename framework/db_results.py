'''
Created on June 5, 2017

@author: Mahmoud
'''

import sys, os
import mysql.connector
from mysql.connector import Error
from av_detection import av_detection  

# all_avs=False
avs_list = []
results_dir = '/Users/Mahmoud/Documents/PhD_projects/Obfuscation/study_results'

def printUsage():
    print ('Usage: python db_results.py [OPTION]\nOPTION ')
    print ('- per_av: detection rate per AV tool')
    print ('- per_av_dataset: detection rate per AV tool and dataset (benign or malicious)')

# if len(sys.argv) < 2:
#     printUsage()
#     sys.exit()
# option = sys.argv[1].lower()
        

global conn
def connect():
    global conn
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='obf',
                                       user='mahmoud',
                                       password='mahmoud')
        if conn.is_connected():
            print('Connected to MySQL database')            
    except Error as e:
        print(e)        
 


################################################ detection rate per AV
def detection_rate(qry_text, result_path, per_what,count_what):
    global conn
    results = open(result_path,'w+')
    
    query = qry_text
    args = ()
    av_detection_results = {}
    if conn.is_connected:        
        cursor = conn.cursor(buffered=True)
        cursor.execute(query, args)
        sep = ','
        results.write(per_what+sep+count_what+',TP,FN,TN,FP,Accuracy (%),Precision (%),Recall (%),F_score (%)\n')
        for (per_what, is_malicious, correct, cnt) in cursor:
#             group_by=per_what.encode('ascii','ignore')
#             if not all_avs:
#                 pos = (group_by.rfind('-'))       
#                 av_product = group_by[:pos]
#                 if av_product not in avs_list:                    
#                     continue
            if per_what not in av_detection_results:
                av_detect = av_detection(per_what)
                av_detection_results[per_what] = av_detect
                av_detect.addValue(is_malicious, correct, cnt)
            else:
                av_detect = av_detection_results[per_what]
                av_detect.addValue(is_malicious, correct, cnt)
                
        cursor.close()    
        for av,av_detect in av_detection_results.iteritems():
            str_av_result = str(av_detect)
            if str_av_result:
                results.write(str_av_result +'\n')
#             print (av_detect)
    else:
        print ('not connected')
        connect()
        if not conn.is_connected:
            print ('not connected 2nd time ....')
            sys.exit()        
           
    results.close()    
    print ('finished. Check '+result_path)    

def get_avs():
    avs_qry = "SELECT av FROM av_products"        
    args = ()
    if conn.is_connected:        
        cursor = conn.cursor()
        cursor.execute(avs_qry, args)
        for (a) in cursor:
            avs_list.append(str(a[0]))
    
# stuff to run always here such as class/def
def main():        
    pass

if __name__ == "__main__":
    connect()
    
    options = []

#fixed for the selected AVs
#     options.append('AV_Obf_Strategy')
#     options.append('AV_Obfuscator')

    

#     options.append('AV_Original_Apps_Year')
#     options.append('AV_Obfuscated_Apps_Year')
#     options.append('AV_All_Apps_Year')    
    
#     options.append('Original_Apps_Year')
#     options.append('Obfuscated_Apps_Year')    

#     options.append('All_Apps_Year')

#runs for all AVs

#     options.append('AV')
#     options.append('AV_Obfuscated_Apps')
#     options.append('AV_Original_Apps')

#     options.append('Obfuscator')

#     options.append('Obf_Strategy')

#     options.append('AV-Obfuscator-Strategy')


#     options.append('Year_Month')
        
#     if not all_avs:
#         get_avs()
    
    
    for option in options:    
    
        count_what = 'Apps'
        if option == 'AV' or option=='all':
            per_what_file = os.path.join(results_dir,'detection_per_av.csv')
            qry = """
                select av as per_what, is_malicious, correct, count(*) cnt
                from av_results_malicious_selected_avs 
                group by av, is_malicious, correct
                Union All
                select av, is_malicious, correct, count(*) cnt
                from av_results_benign_selected_avs 
                group by av, is_malicious, correct
                """       
            detection_rate(qry,per_what_file, option,count_what)         
    
        if option == 'AV_Obfuscated_Apps' or option=='all':
            per_what_file = os.path.join(results_dir,'detection_per_av_on_obfuscated_apps.csv')
            qry = """
                select av as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and obfuscator != '' and
                a.scan_id is not null and a.dataset = 'benign'
                group by av,is_malicious, correct
                UNION ALL
                select av as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and obfuscator != '' and
                a.scan_id is not null and a.dataset != 'benign'
                group by av,is_malicious, correct;
                """       
            detection_rate(qry,per_what_file, option,count_what)         
    
        if option == 'AV_Original_Apps' or option=='all':
            per_what_file = os.path.join(results_dir,'detection_per_av_on_original_apps.csv')
            qry = """
                select av as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and obfuscator = '' and
                a.scan_id is not null and a.dataset = 'benign'
                group by av,is_malicious, correct
                UNION ALL
                select av as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and obfuscator = '' and
                a.scan_id is not null and a.dataset != 'benign'
                group by av,is_malicious, correct;
                """       
            detection_rate(qry,per_what_file, option,count_what)         
    
        if option == 'AV_Obfuscator' or option=='all':
            per_what_file = os.path.join(results_dir,'detection_per_av_obfuscator.csv')
            qry = """
                select CONCAT(av,'-',obfuscator) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and 
                a.scan_id is not null and a.dataset = 'benign'
                group by av,obfuscator, is_malicious, correct
                UNION ALL
                select CONCAT(av,'-',obfuscator) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and 
                a.scan_id is not null and a.dataset != 'benign'
                group by av,obfuscator, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
    
        if option == 'AV_Obf_Strategy' or option=='all':
            per_what_file = os.path.join(results_dir,'detection_per_av_obf_strategy.csv')
            qry = """
                select CONCAT(av,'-',upper(obf_strategy)) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id 
                a.scan_id is not null and a.dataset = 'benign'
                group by av,obf_strategy, is_malicious, correct
                UNION ALL
                select CONCAT(av,'-',upper(obf_strategy)) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id  and
                a.scan_id is not null and a.dataset != 'benign'
                group by av,obf_strategy, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'AV_Original_Apps_Year' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_per_av_year_original_apps.csv')
            qry = """
                select CONCAT(av,'-',app_year) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and obfuscator = '' and
                a.scan_id is not null and a.dataset = 'benign'
                group by av,app_year, is_malicious, correct
                UNION ALL
                select CONCAT(av,'-',app_year) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and obfuscator = '' and 
                a.scan_id is not null and a.dataset != 'benign'
                group by av,app_year, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'AV_Obfuscated_Apps_Year' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_per_av_year_obfuscated_apps.csv')
            qry = """
                select CONCAT(av,'-',app_year) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and obfuscator != '' and
                a.scan_id is not null and a.dataset = 'benign'
                group by av,app_year, is_malicious, correct
                UNION ALL
                select CONCAT(av,'-',app_year) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and obfuscator != '' and 
                a.scan_id is not null and a.dataset != 'benign'
                group by av,app_year, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         

        if option == 'Original_Apps_Year' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_original_apps_per_year.csv')
            qry = """
                select app_year as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and obfuscator = '' and
                a.scan_id is not null and a.dataset = 'benign' and app_year <> 0
                group by app_year, is_malicious, correct
                UNION ALL
                select app_year as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and obfuscator = '' and
                a.scan_id is not null and a.dataset != 'benign'  and app_year <> 0
                group by app_year, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'Obfuscated_Apps_Year' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_obfuscated_apps_per_year.csv')
            qry = """
                select app_year as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and obfuscator != '' and 
                a.scan_id is not null and a.dataset = 'benign' and app_year <> 0
                group by app_year, is_malicious, correct
                UNION ALL
                select app_year as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and obfuscator != '' and 
                a.scan_id is not null and a.dataset != 'benign'  and app_year <> 0
                group by app_year, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'All_Apps_Year' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_all_apps_per_year.csv')
            qry = """
                select app_year as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and 
                a.scan_id is not null and a.dataset = 'benign' and app_year <> 0
                group by app_year, is_malicious, correct
                UNION ALL
                select app_year as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and 
                a.scan_id is not null and a.dataset != 'benign'  and app_year <> 0
                group by app_year, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'AV_All_Apps_Year' or option=='all':
            per_what_file = os.path.join(results_dir,'detection_per_av_all_apps_year.csv')
            qry = """
                select CONCAT(av,'-',upper(app_year)) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and 
                a.scan_id is not null and a.dataset = 'benign'
                group by av,app_year, is_malicious, correct
                UNION ALL
                select CONCAT(av,'-',upper(app_year)) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and 
                a.scan_id is not null and a.dataset != 'benign'
                group by av,app_year, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'AV-Obfuscator-Strategy' or option=='all':
            per_what_file = os.path.join(results_dir,'detection_per_av_obfuscator_strategy.csv')
            qry = """
                select CONCAT(av,'-',upper(obfuscator),'-',upper(obf_strategy)) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset = 'benign'
                group by av,obfuscator,obf_strategy, is_malicious, correct
                UNION ALL
                select CONCAT(av,'-',upper(obfuscator),'-',upper(obf_strategy)) as per_what, is_malicious, correct, count(distinct r.scan_id) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset != 'benign'
                group by av,obfuscator,obf_strategy, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'Obf_Strategy' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_per_obf_strategy.csv')
            qry = """
                select upper(obf_strategy) as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset = 'benign'
                group by obf_strategy, is_malicious, correct
                UNION ALL
                select upper(obf_strategy) as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset != 'benign'
                group by obf_strategy, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'Obfuscator' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_per_obfuscator.csv')
            qry = """
                select upper(obfuscator) as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset = 'benign'
                group by obfuscator, is_malicious, correct
                UNION ALL
                select upper(obfuscator) as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset != 'benign'
                group by obfuscator, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)         
        if option == 'Year_Month' or option=='all':
            count_what = 'AV_Results'
            per_what_file = os.path.join(results_dir,'detection_per_year_month.csv')
            qry = """
                select CONCAT(app_month,'/',app_year) as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_benign_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset = 'benign' and app_year <> 0
                group by app_year, app_month, is_malicious, correct
                UNION ALL
                select CONCAT(app_month,'/',app_year) as per_what, is_malicious, correct, count(*) cnt
                from apps a, av_results_malicious_selected_avs r
                where a.scan_id = r.scan_id and
                a.scan_id is not null and a.dataset != 'benign' and app_year <> 0
                group by app_year, app_month, is_malicious, correct;
            """    
            detection_rate(qry,per_what_file, option,count_what)
            

        
    
