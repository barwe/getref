import os
from os import path

import requests
from requests.exceptions import ConnectionError

from fake_useragent import UserAgent

def getUserAgent():
    return UserAgent().random

class RefBase(object):
    
    def __init__(self):
        self.ref_type = 'ris'
        self.verbose = True
        self.querier = None
        self.output_dir = path.abspath("References")
        self.headers = {'User-Agent': getUserAgent()}
        
    def get(self, desc):
        desc = desc.strip().strip('.')
        filemeta = self.filemeta(desc)
        if path.exists(filemeta['path']):
            self.log('Same file found: "%s", stop!' % filemeta['shortname'])
        else:
            title, url = self.parse(desc)
            if self.to_qstr(title) != self.to_qstr(desc):
                self.log('Only similar paper searched: "%s"' % title)
                self.log('If this is not what you want, you can remove it manually and change other keywords to search')
            filemeta = self.filemeta(title)
            self.save(url, filemeta)
    
    ## 从未格式化的标题解析引用文件的下载链接
    def parse(self, title: str):
        ...
 
    ## 重复请求直到成功获取资源或者达到最大尝试次数
    def request(self, url: str, ntries = 5):
        '''
        Request resources repeatedly until success or reaching the maximum attempts.
        '''
        for i in range(ntries):
            try:
                return requests.get(url, headers = self.headers)
            except ConnectionError:
                self.log('New connection attemptted ({}), wait...'.format(i+1))
                continue
        self.log("Timeout, stop!")
        return None

    ## 将普通标题字符串格式化为查询字符串
    def to_qstr(self, title):
        title = title.strip().strip('.')
        if self.querier:
            for i, j in self.querier:
                title = title.replace(i, j)
            return title
        else:
            raise ValueError('querier cannot be none!')
    
    ## 构建标题对应的文件的元信息
    def filemeta(self, title: str):
        title = title.strip().strip('.')
        replaces = [(':', '#'), ('/', '_')]
        filekey = title.strip()
        for od, nw in replaces:
            filekey = filekey.replace(od, nw)
        filename = '%s.%s' % (filekey, self.ref_type)
        filepath = path.join(self.output_dir, filename)
        
        filekey_ls = filekey.split(' ')
        if len(filekey_ls) <= 6:
            shortkey = filekey
        else:
            shortkey = ' '.join([*filekey_ls[:3], '...', *filekey_ls[-3:]])
        file_shortname = '%s.%s' % (shortkey, self.ref_type)
        
        return {
            'title': title,
            'key': filekey, 
            'name': filename,
            'shortname': file_shortname,
            'path': filepath
        }
    
    def save(self, url, fm):
        if path.exists(fm['path']):
            self.log('Similar file found: "%s", stop!' % fm['shortname'])
        else:
            response = self.request(url)
            if response:
                text = response.text.replace('\r\n', '\n')
                if not path.exists(self.output_dir):
                    os.mkdir(self.output_dir)
                    self.log('New directory created: "%s"' % self.output_dir)
                with open(fm['path'], 'w', encoding = 'utf-8') as writer:
                    writer.write(text)
                self.log('New file created: "%s"' % fm['shortname'])
            else:
                self.log('Request for file content failed, stop!')
                self.log('URL: %s' % url)
            

    def log(self, msg):
        if self.verbose:
            print('[INFO] %s' % msg)