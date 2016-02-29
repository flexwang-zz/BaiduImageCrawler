import urllib.request
import re
import os
import sys
from multiprocessing.dummy import Pool

def download(download_info):
    (url, file_name) = download_info
    for i in range(6):
        try:
            with urllib.request.urlopen(url, timeout=20) as response, open(file_name, 'wb') as out_file:
                data = response.read() 
                out_file.write(data)
            return
        except:
            pass
    print('Download failed: %s'%(url))

def mass_download(urls, nthread):
    print('Downloading...')
    download_infos = [(url, os.path.basename(url)) for url in urls]
    with Pool(nthread) as pool:  
        pool.map(download, download_infos)

def get_html(url_path):
    print('Fetching html...')
    for i in range(5):
        try:
            with urllib.request.urlopen(url_path) as url:
                s = str(url.read())
            return s
        except:
            pass
    print('Fetching html failed...')

def get_image_urls(html_content):
    print('Parsing html...')
    exp = 'objURL":"([a-z.:/_A-Z0-9]*)"'
    image_urls = re.findall(exp, html_content)
    print('%d images found in this page'%(len(image_urls)))
    return image_urls

#reading parameters
if (len(sys.argv) < 5):
    print('Usage: python crawler.py $key_word $dest_folder $num_of_images $num_of_threads')
    exit()
key_word = repr(sys.argv[1].encode('UTF-8')).replace('\\x', '%').upper()[2:-1]
dest_folder = sys.argv[2]
num_image = eval(sys.argv[3])
nthread = eval(sys.argv[4])

#create and change working directory
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)
os.chdir(dest_folder)

pn = 0
cnt = 0
downloaded = set()
while cnt < num_image:
    print("Page %d:"%(pn+1))
    image_urls = []
    try:
        url = "http://images.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%d&gsm=0"%(key_word, pn*15)
        html_content = get_html(url)
        temp_urls = get_image_urls(html_content)
        for i in temp_urls:
            if i not in downloaded:
                downloaded.add(i)
                image_urls.append(i)
        mass_download(image_urls, nthread)
    except KeyboardInterrupt:
        exit()
    except:
        pass
    pn += 1
    cnt += len(image_urls)
print("Done.")