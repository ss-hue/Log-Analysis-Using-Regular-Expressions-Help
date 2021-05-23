#!/usr/bin/env python3

import re
import os
import sys
import operator
import csv

#dictionary that contains all the ERROR messages logged and how many times
#each error was found.

error = {}


#Dictionary that contains all the entries related to each user. INFO and ERROR logs.

per_user = {}

#Variable that contains the input file from command line

file = sys.argv[1]

#variable that store the username found on each line of the log system




with open(file) as f:
    
    for line in f.readlines():

        line = line.strip()

        match = re.search(r" ?\((.*)\)$", line)

        if match is not None:

            username = match.group(1)

        if username not in per_user:
        
            per_user[username] = {}

            per_user[username]['INFO'] = 0

            per_user[username]['ERROR'] = 0
        
            
        if 'ERROR' in line:
    
            if username in per_user:
                
                per_user[username]['ERROR'] += 1
            
            else:

                per_user[username]['ERROR'] = 1

            err_type = re.search(r"ticky: ERROR ([\w ]*) ", line).group(1)

            if err_type in error:

                error[err_type] += 1

            else:
                error[err_type] = 1
            
            
        
        elif 'INFO' in line:
                    
            if username in per_user:
                
                per_user[username]['INFO'] += 1
            
            else:

                per_user[username]['INFO'] = 1

        

error_list_sorted = sorted(error.items(), key= operator.itemgetter(1), reverse=True)


user_stats_sorted = [[key,per_user[key]["INFO"],per_user[key]["ERROR"]] for key in sorted(per_user.keys(), key= operator.itemgetter(0), reverse=False)]

f.close()

error_list_sorted.insert(0, ('Error', 'Count'))   

user_stats_sorted.insert(0, ('Username', 'INFO', 'ERROR'))


with open('error_message.csv', 'w') as error_csv:

    writer = csv.writer(error_csv)

    for row in error_list_sorted:
        writer.writerow(row)

error_csv.close()


with open('user_statistics.csv', 'w') as user_csv:


    writer = csv.writer(user_csv)

    for row in user_stats_sorted:
        writer.writerow(row)

user_csv.close()