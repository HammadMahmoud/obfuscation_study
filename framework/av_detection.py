'''
Created on June 6, 2017

@author: Mahmoud
'''

from __future__ import division

class av_detection:
    av = ''
    
    '''
    T: malicious
    F: benign
    
         P    N
      ----------  
    T |  TP   FN
    F |  FP   TN
    
    '''
    
    tp = 0 #malicious detected as such
    fn = 0 #malicious detected as benign
         
    tn = 0 #benign detected as such
    fp = 0 #benign detected as malicious
    
        
    def __init__(self, av):
        self.av = av
        
    def __str__(self):
        
        sep = ','
        apps = 0.0
        accuracy = 0.0
        precision = 0.0
        recall = 0.0
        f_score = 0.0
        
        apps = self.tp + self.tn + self.fn + self.fp
#         if apps<100:
#             return ''

        if apps>0:        
            accuracy = ((self.tp + self.tn)/ apps) *100  
        if (self.tp+self.fp)>0:
            precision = (self.tp / (self.tp+self.fp)) *100 
        if (self.tp+self.fn)>0:
            recall = (self.tp / (self.tp+self.fn)) *100
        if (precision+recall)>0:
            f_score = (2 * ((precision*recall)/(precision+recall)))
        
        return str(self.av)+sep+str(apps)+sep+str(self.tp)+sep+str(self.fn)+sep+str(self.tn)+sep+str(self.fp)+\
                sep+str('%.1f'%accuracy)+sep+str('%.1f'%precision)+sep+str('%.1f'%recall)+sep+str('%.1f'%f_score)
                    
    
    def addValue(self, is_malicious, correct, cnt):
#         print(str(is_malicious)+' '+str(correct)+' '+str(cnt)) 
        if is_malicious == 1:#actual is malicious (T)
            if correct==1:
                self.tp += cnt
            else:
                self.fn += cnt    
        elif is_malicious == 0: #actual is benign (F)
            if correct==1:
                self.tn += cnt
            else:
                self.fp += cnt
                
                    
            

