# Logo
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
    import wget #pip3 install wget
    import datetime #pip3 install datetime
except ImportError as error:
    module = str(error).split()[-1].replace('\'', '')
    print(
    '\nModule ' + module + ' is not installed!',
    '\nsudo pip3 install -r requirements.txt'
    )
    raise SystemExit

# Settings
api = 'PSKINdQe1GyxGgecYz2191H2JoS9qvgD'
time = datetime.datetime.today().strftime("%H.%M.%S-%d-%m")
pages_count = int(input('[?] How many pages need? : '))
ip_file = 'logs_' + str(time) + '.txt'

# Load and save ips
for page in range(pages_count):
    print('[' + str(page) + '] Loading page... ')
    try:
        wget.download('https://api.shodan.io/shodan/host/search?key=' + api + '&query=android%20debug%20bridge%20product:%22Android%20Debug%20Bridge%22&facets={facets}&page=' + str(page), out = 'page.dat', bar = None)
    except Exception as error:
        print('\n[!] Something went wrong!\n' + str(error) + '\n[!] Exception while loading page. Please contact to developer...')
        raise SystemExit
    os.system('grep -oP \'(?<=\"ip_str\": \")[^\"]*\' page.dat >> ' + ip_file)
    os.remove('page.dat')

print('[+] Okay, all ' + str(pages_count) + ' pages was saved to ' + ip_file)
if input('[?] Show downloaded results? (y/n) : ').lower() in ['y', 'yes', 'true', '1', '+']:
    os.system('cat ' + ip_file)

print('[$] Created by LimerBoy with Love.')
