# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 00:14:53 2018

@author: bing
"""

#import yaml
#input_file = '_data/links.yml'
#
#stream = open(input_file, "rb")
#data_lists = yaml.load(stream)
##iterate  -> section,categories
#for data_list in data_lists:
#    print(data_list['section'])#读取 section名称
#    for category in data_list['categories']:
##        print(category['category']) #输出category名称
##        print(category['links'])#输出links的list  
#        for x in category['links']:
#            print(x['name'])
#            print(x['style'])
#            print(x['url'])
#            print(x['des'])

#keys=['one', 'two', 'three'] 
#values= [1, 2, 3]
#
#gg = [list(x) for x in zip(keys,values)] 
#read yaml file
import yaml

input_file ='search_services.yml'

def read_yaml(file):
    stream = open(file, "rb")
    return yaml.load(stream)  
    
data = read_yaml(input_file)

for myDict in data:
    if 'baidu' in myDict.values():
        print(myDict['name'])
