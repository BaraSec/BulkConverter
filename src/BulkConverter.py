import os, requests, re, datetime
from subprocess import call

user_path = ""

def Main():
	global user_path
	folder = ""
	transfer = False
	sleep = False
	adbPath = ""
	androidPath = ""

	while folder.strip() == "":
		folder = input("\n\n\nDestination Folder -> ")
	print("\n")

	urls = []
	url = ""
	while url.strip() == "":
		url = input("Input URL -> ")
	urls.append(url)

	while True:
	    url = input("Input URL -> ")
	    if url:
	        urls.append(url)
	    else:
	        break

	answer = input("\nTrasfer using ADB to your Android device (yes/No) ? -> ")
	if answer != "":
		if answer[0].lower() == "y":
			transfer = True
			print("Yes")
		else:
			print("No")
	else:
		print("No")

	if transfer:
		while adbPath.strip() == "":
			adbPath = input("\n\"adb.exe\" Path -> ")
		while androidPath.strip() == "":
			androidPath = input("\nAndroid device target Path -> ")
	
	answer = input("\nSleep after completion (yes/No) ? -> ")
	if answer != "":
		if answer[0].lower() == "y":
			sleep = True
			print("Yes")
		else:
			print("No")
	else:
		print("No")

	if transfer:
		adbPath = adbPath.replace("\\", "/").replace("\"", "").replace("//", "/")
		if(not adbPath.endswith("/")):
			adbPath += "/"
		adbPath += "adb.exe"
		androidPath = androidPath.replace("\\", "/").replace("\"", "")

	print("\n\nFunctioning ...\n")

	user_path = folder.replace("\\", "/").replace("\"", "")
	if not user_path.endswith("/"):
		user_path += "/"
	user_path += str(datetime.datetime.now().strftime("%Y-%m-%d"))

	for url in urls:
		convert(url)

	if transfer:
		call('"' + adbPath + '" push "' + user_path + '" "' + androidPath + '"')

	print("\n\n--> Finished! <-- \nOutput folder is: \"" + user_path + "\"")

	if transfer:
		if not androidPath.endswith("/"):
			androidPath += "/"
		print("Android Output folder is: \"" + androidPath + str(datetime.datetime.now().strftime("%Y-%m-%d")) + "\"\n\n")
	else:
		print("\n\n")

	if sleep:
		print("Sleeping..\n")
		call("C:/WINDOWS/System32/rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

	input("\n\t\t\t>> Press Any Key To Exit <<")

def convert(url):
	data = {'quality':'1', 'format':'mp3', 'url':url}
	headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Content-Length': '138', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': '__cfduid=daca8e943195f582c9cfcd1caa51b0e311519247976; WSID=4569793895a8de2687e23fMfoNGMadkydqExKME4mGFq5ytMODELe4b18b7d5b5603a4c8c1fce9bb23161a; forcelng=en; __PPU_SESSION_1_813021_false=0|0|0|0|0', 'DNT': '1', 'Host': 'convert2mp3.net', 'Origin': 'http://convert2mp3.net', 'Referer': 'http://convert2mp3.net/en/index.php', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
	response = requests.post("http://convert2mp3.net/en/index.php?p=convert", headers=headers, data=data)

	response.connection.close()

	if response.status_code == 200:
		try:
			init = str(response.content)
			newUrl = init[init.index("http://c-api"):init.rindex("style=") - 2]
		except ValueError:
			print("\n\n** Error in covert() [substring not found]: \"" + url + "\" **\n\n")
			return

		if newUrl != "" and newUrl != None:
			step2(newUrl)
		else:
			print("\n\n** Error in covert() 1: \"" + url + "\" **\n\n")
	else:
		print("\n\n** Error in covert() 2: \"" + url + "\" **\n\n")

def step2(url):
	response = requests.get(url)

	response.connection.close()

	if response.status_code == 200:
		init = str(response.content)
		newUrl = init[init.index("http://convert2mp3.net"):init.index("\";")].replace("tags", "complete")

		if newUrl != "" and newUrl != None:
			step3(newUrl)
		else:
			print("\n\n** Error in step2() 1: \"" + url + "\" **\n\n")
	else:
		print("\n\n** Error in step2() 2: \"" + url + "\" **\n\n")

def step3(url):
	response = requests.get(url)

	response.connection.close()

	if response.status_code == 200:
		init = str(response.content)
		newUrl = init[init.index("http://cd"):init.index("&d=y")] + "&d=y"

		if newUrl != "" and newUrl != None:
			download(newUrl)
		else:
			print("\n\n** Error in step3() 1: \"" + url + "\" **\n\n")
	else:
		print("\n\n** Error in step3() 2: \"" + url + "\" **\n\n")

def download(url):
	global user_path

	response = requests.get(url, stream=True)

	if response.status_code == 200:
		name = response.headers['Content-Disposition']
		fname = re.findall("filename=(.+)", name)
		fname = ''.join(fname).replace("\"", "")

		if not os.path.exists(user_path):
			os.makedirs(user_path)

		path = user_path + "/" + fname
		print("\n\tDownloading: \"" + path + "\"") 
		out = open(path,'wb')
		out.write(response.content)
		print("\n\t--> Done <-- : " + path) 
	else:
		print("\n\n** Error in download(): \"" + path + "\" **\n\n")

	response.connection.close()


if __name__ == '__main__':
	try:
		Main()
	except KeyboardInterrupt:
		print("\n\n--> Converter was closed!\n")