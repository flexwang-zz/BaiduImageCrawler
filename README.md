# BaiduImageCrawler

This is a multithreaded tool for downloading search results of [Baidu image search](http://http://images.baidu.com/).

### Dependencies
  - Python 3.x
  - [workerpool](https://github.com/shazow/workerpool)

### Usage
```sh
$ python crawler.py KEYWORD DEST_FOLDER NUM_OF_IMAGES NUM_OF_THREADS
```

### Example
Below is an example of how to use the crawler to download the first 40 image search results of dog with 8 threads and save them to E:\dog.
```sh
$ python crawler.py 狗 E:\dog 40 8
```
Look at what we got here:

 <img src="https://github.com/flexwang/BaiduImageCrawler/raw/master/result.jpg" alt="GitHub" title="snapshot" width="700" height="203" />  
