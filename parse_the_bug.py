import requests 
import json
import re
from urlextract import URLExtract
extractor = URLExtract()
'''
tbl structure mssql
program_id
program_name
program_domains
'''

inscope_domains = []
oos_domains = []

def build_oos_bug_crowd():
    bug_crowd_url = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/bugcrowd_data.json"
    try:
       response = requests.get(bug_crowd_url,timeout=3,verify=False)
       if response:
          data = json.loads(response.text)
          for info in data:
              for key,value in info.items():
                  if "targets" in key:
                      values_in_scope = value['in_scope']
                   
                      for items in values_in_scope:
                          urls = extractor.find_urls(items['target'])
                          if urls:
                             inscope_domains.append(urls)
                             
                      values_out_of_scope = value['out_of_scope']
                   
                      for oos_items in values_out_of_scope:
                          urls = extractor.find_urls(oos_items['target'])
                          if urls:
                             oos_domains.append(urls)
                             
    except Exception as BugExcept:
       print(BugExcept)
       pass
 
 
print("Parsing BugCrowd Bounty Data For Target Scopes")   
print("*"*50)   
build_oos_bug_crowd()
inscope_list = [item for sublist in inscope_domains for item in sublist]
out_of_scope_list = [item for sublist in oos_domains for item in sublist]
print("*"*50)
print("discovered : {} In Scope Urls for Testing".format(len(inscope_list)))
print("discovered : {} Out of Scope Urls for Testing".format(len(out_of_scope_list)))

