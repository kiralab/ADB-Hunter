#!/usr/bin/env python3

# Information
print (r"""
  ____    ____       ____                  _       _
 |  _ \  / ___|     / ___|  _ __    __ _  | |__   | |__     ___   _ __
 | |_) | \___ \    | |  _  | '__|  / _` | | '_ \  | '_ \   / _ \ | '__|
 |  __/   ___) |   | |_| | | |    | (_| | | |_) | | |_) | |  __/ | |
 |_|     |____/     \____| |_|     \__,_| |_.__/  |_.__/   \___| |_|
                                                    Created by LimerBoy

   Save all vulnerable device ips to file and connect with PhoneSploit

   * PS-Grabber : https://github.com/LimerBoy/PS-Grabber.git
   * PhoneSploit: https://github.com/metachar/PhoneSploit.git

""")

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
    '\nsudo pip3 install -r requirements.txt'
    )
    raise SystemExit

# Create logs folder
if not os.path.exists('logs'):
    os.mkdir('logs')

# Settings
pages_count = int(input('[?] How many pages need scan? : '))
api = shodan.Shodan('PSKINdQe1GyxGgecYz2191H2JoS9qvgD') # If this api key stops working just remove it from here and insert yours
date = datetime.datetime.today().strftime("%H.%M.%S-%d-%m")
results_file = r'logs/ips-' + date + '.txt'

# Load and save results from pages
page = 1
print('[?] If you press Ctrl + C scanning will be stopped!')
while page < pages_count:
    print('[' + str(page) + '/' + str(pages_count) + '] Loading page results... ')
    try:
        time.sleep(1)
        results = api.search('android debug bridge product:\"Android Debug Bridge\"', page = page)
    except KeyboardInterrupt:
        print('[!] Ctrl + C detected.. Stopping...')
        break
    except shodan.exception.APIError as error:
        print('[EXCEPTION] ' + str(error) + ' ' + 3 * '*')
        time.sleep(3)
        continue
    else:
        for result in results['matches']:
            with open(results_file, 'a') as file:
                file.write(result['ip_str'] + '\n')
        page += 1

# Display results after loading
print('\n[+] Okay, all results from page ' + str(page) + ', was saved to ' + results_file)
if input('[?] Show downloaded results? (y/n) : ').lower() in ['y', 'yes', 'true', '1', '+']:
    results = 0
    with open(results_file, 'r') as file:
        for line in file.readlines():
            print(line.replace('\n', ''))
            results += 1
    print('[+] Saved ' + str(results) + ' ips')

print('[$] Created by LimerBoy with Love.')
