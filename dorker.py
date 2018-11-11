import requests, urllib
import sys, argparse
from bs4 import BeautifulSoup

print("      ___           ___           ___           ___           ___           ___     \n     /  /\         /  /\         /  /\         /  /\         /  /\         /  /\    \n    /  /::\       /  /::\       /  /::\       /  /:/        /  /::\       /  /::\   \n   /  /:/\:\     /  /:/\:\     /  /:/\:\     /  /:/        /  /:/\:\     /  /:/\:\  \n  /  /:/  \:\   /  /:/  \:\   /  /::\ \:\   /  /::\____   /  /::\ \:\   /  /::\ \:\ \n /__/:/ \__\:| /__/:/ \__\:\ /__/:/\:\_\:\ /__/:/\:::::\ /__/:/\:\ \:\ /__/:/\:\_\:\ \n \  \:\ /  /:/ \  \:\ /  /:/ \__\/~|::\/:/ \__\/~|:|~~~~ \  \:\ \:\_\/ \__\/~|::\/:/\n  \  \:\  /:/   \  \:\  /:/     |  |:|::/     |  |:|      \  \:\ \:\      |  |:|::/\n   \  \:\/:/     \  \:\/:/      |  |:|\/      |  |:|       \  \:\_\/      |  |:|\/  \n    \__\::/       \  \::/       |__|:|~       |__|:|        \  \:\        |__|:|~   \n        ~~         \__\/         \__\|         \__\|         \__\/         \__\|    ")
print("\nDorker v0.1a")
print("Author: Bastian Muhlhauser, @xpl0ited1\n")

parser = argparse.ArgumentParser()
parser.add_argument("--site", help="Search for links related to a domain")
parser.add_argument("--ext", help="Search for links with a extension")
parser.add_argument("--inurl", help="Search for links containing a string in the URL")
parser.add_argument("--intitle", help="Search for links containing a string as title")
parser.add_argument("--search", help="Search for links containing a string")
parser.add_argument("--output", help="Specify the output file")
parser.add_argument("--pages", help="Specify the number of pages to look for in Google Search", type=int)
args = parser.parse_args()

site = "site:%s+" % args.site if args.site else ''
ext = "ext:%s+" % args.ext if args.ext else ''
inurl = "inurl:%s+" % args.inurl if args.inurl else ''
intitle = "intitle:%s+" % args.intitle if args.intitle else ''
search = "intitle:%s" % args.search if args.search else ''
pages = args.pages if args.pages else 0

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
}

base_url = "https://www.google.com/search?q="
url = base_url+site+ext+inurl+intitle+search
links = []

def initial_search():
    print("[+] Obtaining links...")
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    divs = soup.find_all('div', attrs={'class':'g'},recursive=True)
    print("[+] Parsing HTML tags")
    for div in divs:
        hrefs = div.find_all(href=True)
        for a in hrefs:
            if a['href'][0:4] == '/url':
                link = a['href'][7:].split('&sa')[0]
                if link[0:15] != 'http://webcache':
                    links.append(link)

if pages == 0:
    initial_search()
else:
    initial_search()
    i = 10
    end = (pages - 1) * 10
    while i < end:
        url = url+("&start=%d" % i)
        i = i + 10
        r = requests.get(url, headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        divs = soup.find_all('div', attrs={'class':'g'},recursive=True)
        print("[+] Page: %d" % ((i+1)/10))
        print("[+] Parsing HTML tags")
        for div in divs:
            hrefs = div.find_all(href=True)
            for a in hrefs:
                if a['href'][0:4] == '/url':
                    link = a['href'][7:].split('&sa')[0]
                    if link[0:15] != 'http://webcache':
                        links.append(link)
print("[+] Results:\n")
for link in links:
    print("%s\n" % link)
    
if args.output:
    print("[+] Writing results...\n")
    f=open(args.output,"w+")
    for link in links:
        f.write("%s\n" % link)
    f.close()
print("\n[#] Finished...")
