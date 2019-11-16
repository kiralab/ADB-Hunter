#!/usr/local/bin/python3
# coding: utf-8

# Information
print (r"""

 █████╗ ██████╗ ██████╗       ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
███████║██║  ██║██████╔╝█████╗███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██╔══██║██║  ██║██╔══██╗╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║██████╔╝██████╔╝      ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚═════╝ ╚═════╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                Created by LimerBoy

   Save all vulnerable device ips to file and connect with PhoneSploit

   * PS-Grabber  > https://github.com/LimerBoy/ADB-Hunter.git
   * PhoneSploit > https://github.com/metachar/PhoneSploit.git

""")

# If this shodan api key stops working just remove it from here and insert your key.
api_key = 'PSKINdQe1GyxGgecYz2191H2JoS9qvgD'

# Modules
try:
    import os
    import time
    import shodan #pip3 install shodan
    import datetime #pip3 install datetime
except ImportError as error:
    module = str(error).split()[-1].replace('\'', '')
    print(
    '\nModule ' + module + ' is not installed!',
    '\npip3 install -r requirements.txt'
    )
    raise SystemExit

# Create logs folder
if not os.path.exists('logs'):
    os.mkdir('logs')

# Settings
api          = shodan.Shodan(api_key) 
date         = datetime.datetime.today().strftime("%H.%M.%S-%d-%m")
product      = 'android debug bridge product:\"Android Debug Bridge\"'
pages_start  = int(input('[?] Start scanning from page : '))
pages_stop   = int(input('[?] Stop  scanning on   page : '))
results_file = r'logs/ips-' + date + '.txt'

# Load and save results from pages
print('[?] If you press Ctrl + C scanning will be stopped!')
for page in range(pages_start, pages_stop, 1):
    try:
        print('[' + str(page) + '/' + str(pages_stop) + '] Loading page results... ')
        time.sleep(1)
        results = api.search(product, page = page)
    except KeyboardInterrupt:
        print('\n[!] (Ctrl + C) detected.. Stopping...')
        break
    except shodan.exception.APIError as error:
        print('[EXCEPTION] ' + str(error))
        time.sleep(3)
        continue
    else:
        for result in results['matches']:
            with open(results_file, 'a') as file:
                file.write(result['ip_str'] + '\n')

# Display results after loading
if os.path.exists(results_file):
	print('\n[+] Okay, all results from page ' + str(pages_start) + ' to page ' + str(pages_stop) +  ', was saved to ' + results_file)
	if input('[?] Show downloaded results? (y/n) : ').lower() in ('y', 'yes', 'true', '1', '+'):
	    with open(results_file, 'r') as file:
	        lines = file.readlines()
	        for line in lines:
	            print(line.replace('\n', ''))
	    print('[+] Saved ' + str(len(lines)) + ' ips')

print('[$] Created by LimerBoy with Love.')
