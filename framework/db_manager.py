'''
Created on May 28, 2017

@author: Mahmoud
'''

import sys, os
import mysql.connector
from mysql.connector import Error

def printUsage():
    print ('Usage: python db_manager.py file [OPTION] is_malicious_dataset[0|1]:\nOPTION')
    print ('- apps: save a scanning file to the DB, after uploading the apps to VT. Requires db_file_* file')
    print ('- av_results: save VT reports to DB, after downloading the reports. Requires *details file')
    print ('- date: store apps date (year and month) into the DB')

if len(sys.argv) < 4:
    printUsage()
    sys.exit()

f = sys.argv[1]
is_malicious = sys.argv[3]
av_results_table_name = 'av_results_'

if is_malicious=='-1':
    av_results_table_name = 'av_results_adam'
elif is_malicious=='0':
    av_results_table_name = 'av_results_benign'   
else:
    av_results_table_name = 'av_results_malicious'
        
if not os.path.exists(f):
    print ('file not found:'+f)
    printUsage()
    sys.exit()

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
 
#     finally:
#         conn.close()

# conn = mysql.connector.connect(host='127.0.0.1',database='obf',user='mahmoud',password='mahmoud')


################################################ Apps table
def insert_app(scan_id,sha256,analysis_link,app,dataset,minor_dataset,obfuscator,obf_strategy):
    global conn
    query = "INSERT INTO apps(scan_id,sha256,analysis_link,app,dataset,minor_dataset,obfuscator,obf_strategy) " \
    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    args = (scan_id,sha256,analysis_link,app,dataset,minor_dataset,obfuscator,obf_strategy)
    if conn.is_connected:        
        cursor = conn.cursor()
        cursor.execute(query, args)
#         if cursor.lastrowid:
#             print('app id', cursor.lastrowid)
#         else:
#             print('app id not found')
        conn.commit()
        cursor.close()    
    else:
        print ('not connected')
        connect()
        if not conn.is_connected:
            print ('not connected 2nd time ....')
            sys.exit()        
           
def store_apps(f):
    x = 1
    for l in open(f,'r'):
        if x == 1:
            if not l.startswith('scan_id,sha256,analysis_link,dataset,'):
                print ('providing wrong file for option:'+option+' or the header has been changed.')
                sys.exit()                
            x = 2
            continue        
        #l:scan_id,sha256,analysis_link,dataset,minor_dataset,apk_path,obfuscator,obf_strategy
        arr = l.strip().split(',')

        scan_id=arr[0]
        sha256=arr[1]
        analysis_link=arr[2]
        dataset=arr[3]
        minor_dataset=arr[4]
        app=arr[5]
        obfuscator=arr[6]
        obf_strategy=arr[7]
        
        insert_app(scan_id,sha256,analysis_link,app,dataset,minor_dataset,obfuscator,obf_strategy)

################################################ av_results table    
def insert_av_result(scan_id, av, result, marked_malicious):
    
        
    global conn
    query = "INSERT INTO "+av_results_table_name+"(scan_id, av, result, is_malicious, marked_malicious, correct) " \
    "VALUES(%s,%s,%s,%s,%s,%s)"
    
    correct = 1
    if is_malicious != marked_malicious:
        correct=0
    args = (scan_id, av, result, is_malicious, marked_malicious, correct)
    if conn.is_connected:        
        cursor = conn.cursor()
        cursor.execute(query, args)
#         if cursor.lastrowid:
#             print('av_result id', cursor.lastrowid)
#         else:bv "
#             print('av_result id not found')
        conn.commit()
        cursor.close()    
    else:
        print ('not connected')
        connect()
        if not conn.is_connected:
            print ('not connected 2nd time ....')
            sys.exit()        

def store_av_results(f):
    x = 1
    scan_id = ''     
    
    for l in open(f,'r'):
        malicious=1
        if x == 1:
            if not l.startswith('hash:'):
                print ('providing wrong file for option:'+option+' or the first line has been changed.')
                sys.exit()
            x = 2
                                
        #l: hash: SCAN_ID
        #l: AV_TOOL->RESULT
        
        if 'hash:' in l:
            scan_id = l.split()[1].strip()
        elif '->' in l:    
            arr = l.strip().split('->')
            av=arr[0]
            result = arr[1]
            if result == 'None':
                malicious = 0
            
            insert_av_result(scan_id, av, result, malicious)    
            
################################################ app_date table    
def insert_app_date(app, pkg, year, month, day):
    global conn
    query = "INSERT INTO app_date(app,is_malicious, pkg, dex_year, dex_month, dex_day) " \
    "VALUES(%s,%s,%s,%s,%s,%s)"
    args = (app,is_malicious,  pkg, year, month, day)
    if conn.is_connected:        
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print('app_date id', cursor.lastrowid)
        else:
            print('app_date id not found')
        conn.commit()
        cursor.close()    
    else:
        print ('not connected')
        connect()
        if not conn.is_connected:
            print ('not connected 2nd time ....')
            sys.exit()        

def store_apps_date(f):
    x = 1
    for l in open(f,'r'):
        if x == 1:
            if not l.startswith('app,app_path,package,dex_year'):
                print ('providing wrong file for option:'+option+' or the header has been changed.')
                sys.exit()                
            x = 2
            continue        
        #l:app,app_path,package,dex_year,dex_month,dex_day,cert_year,cert_month,cert_day
        arr = l.strip().split(',')
        app=arr[1]
        pkg = arr[2]
        year=arr[3]
        month=arr[4]
        day=arr[5]
        
        if year=='':
            year=0
        if month=='':
            month=0
        if day=='':
            day=0
            

        insert_app_date(app, pkg, year, month, day)

    
# stuff to run always here such as class/def
def main():        
    pass

if __name__ == "__main__":
    connect()
    
    option = sys.argv[2].lower()    
    print ('processing '+f+', option:'+option)
    
    if 'apps' == option:
        store_apps(f)
    elif 'av_results' == option:
        store_av_results(f)
    elif 'date' == option:
        store_apps_date(f)
    else:
        print('Undefined option')
        printUsage()
        sys.exit()
                    