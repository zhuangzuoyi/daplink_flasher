import requests
import time
import sys
def downloader(url,path):
    start = time.time()
    size =0
    response = requests.get(url,stream=True)
    print(response)
    chunk_size = 1024
    content_size = int(response.headers['content-length'])
    print(content_size)
    if response.status_code == 200:
        with open(path,"wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size +=len(data)
                print('\r'+ '下载进度：%s%.2f%%' % (">" * int(size * 50/ content_size),float(size / content_size * 100)),end="")
    end = time.time()
    print(start-end)
if __name__ == '__main__':
    downloader("http://www.keil.com/pack/Keil.LPC1700_DFP.2.6.0.pack", sys.path[0]+"2.6.0.pack")
