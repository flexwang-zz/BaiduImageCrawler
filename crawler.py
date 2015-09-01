import urllib.request
import re
import os
import sys
import workerpool

def download(url, file_name):
    for i in range(5):
        try:
            with urllib.request.urlopen(url, timeout=20) as response, open(file_name, 'wb') as out_file:
                data = response.read() 
                out_file.write(data)
            return
        except:
            pass
    print('fetch failed: %s'%(url))

def mass_download(urls, nthread):
    pool = workerpool.WorkerPool(size=nthread)
    saveto = [os.path.basename(url) for url in urls]
    pool.map(download, urls, saveto)
    pool.shutdown()
    pool.wait()

def get_html(url_path):
    with urllib.request.urlopen(url_path) as url:
        s = str(url.read())
    return s

def get_image_urls(html_content):
    exp = 'objURL":"([a-z.:/_A-Z0-9]*)"'
    return re.findall(exp, html_content)

#reading parameters
key_word = repr(sys.argv[1].encode('UTF-8')).replace('\\x', '%').upper()[2:-1]
dest_folder = sys.argv[2]
num_image = eval(sys.argv[3])
nthread = eval(sys.argv[4])

#create and change working directory
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)
os.chdir(dest_folder)

for pn in range(0, num_image, 15):
    print("Page %d:"%(pn+1))
    try:
        url = "http://images.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%d&gsm=0"%(key_word, pn)
        html_content = get_html(url)
        image_urls = get_image_urls(html_content)
        mass_download(image_urls, nthread)
    except KeyboardInterrupt:
        exit()
    except:
        pass