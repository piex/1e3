# -*- coding: utf-8 -*-
"""
Create On 2018-1-13

@thor: Mervyn Zhang
"""

import re
import sys
import requests


class Extractor:
    def __init__(self, url='', blockSize=1):
        self.url = url
        self.blockSize = blockSize

        # Compile re
        self.reDATA = re.compile(r'<!DOCTYPE.*?>', re.I | re.S)
        # HTML Commed
        self.reCommed = re.compile(r'<!--[\s\S]*?-->')
        # Script
        self.reScript = re.compile(
            r'<\s*script[^>]*>[\w\W]*?<\s*/\s*script\s*>', re.I)
        # Style
        self.reStyle = re.compile(r'<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',
                                  re.I)
        # HTML Tag
        self.reTag = re.compile(r'<[\s\S]*?>')
        # Special charcaters
        self.reSpecial = re.compile('&.{1,5};|&#.{1,5};')
        # Spaces
        self.reSpace = re.compile('\s+')
        # Word wrap transform
        self.reWrap = re.compile('\r\n|\r')
        # Reduce redundancy
        self.reRedun = re.compile('\n{%s,}' % (self.blockSize + 1))

    def reset(self):
        self.url = ''
        self.raw_page = ''
        self.text = ''
        self.isGB = True
        self.textLines = []
        self.blocksLen = []
        self.isCharsetGB = True

    def getRawPage(self, sourceType):
        if sourceType == 'url':
            res = requests.get(self.url)
            self.raw_page = res.text
        elif sourceType == 'path':
            f = open(self.url)
            self.raw_page = f.read()
            f.close()
        elif sourceType == 'text':
            self.raw_page = self.url

    def handleEncoding(self):
        """
        获取网页编码格式
        """
        match = re.search(r'charset\s*=\s*"?([\w\d-]*)"?', self.raw_page, re.I)
        if match:
            charset = match.group(1).lower()
            if charset.find('gb') == -1:
                self.isCharsetGB = False

    def preProcess(self, doc):
        doc = self.reDATA.sub('', doc)
        doc = self.reCommed.sub('', doc)
        doc = self.reScript.sub('', doc)
        doc = self.reStyle.sub('', doc)
        doc = self.reTag.sub('', doc)
        doc = self.reSpecial.sub('', doc)
        doc = self.reWrap.sub('\n', doc)
        doc = self.reRedun.sub('\n' * (self.blockSize + 1), doc)
        return doc

    # Split the preprocessed text into lines by '\n'
    def get_text_lines(self, text):
        lines = text.split('\n')
        for line in lines:
            if line:
                line = self.reSpace.sub('', line)
                self.textLines.append(line)

    # Calculate the length of every block
    def calc_block_lens(self):
        text_line_count = len(self.textLines)
        block_len = 0
        block_size = min([text_line_count, self.blockSize])
        for i in range(block_size):
            block_len = block_len + len(self.textLines[i])
        self.blocksLen.append(block_len)

        if (self.blockSize != self.blockSize):
            return

        for i in range(1, text_line_count - self.blockSize):
            block_len = self.blocksLen[i - 1]\
                + len(self.textLines[i - 1 + self.blockSize])\
                - len(self.textLines[i - 1])
            self.blocksLen.append(block_len)

    def get_plain_text(self, data='', sourceType='url'):
        self.reset()
        self.url = data
        self.getRawPage(sourceType)
        self.handleEncoding()
        pre_proc_doc = self.preProcess(self.raw_page)
        self.get_text_lines(pre_proc_doc)
        self.calc_block_lens()

        i = max_text_len = 0
        blocks_count = len(self.blocksLen)
        cur_text_len = 0
        part = ''
        while i < blocks_count:
            if self.blocksLen[i] > 0:
                if self.textLines[i]:
                    part = '%s%s\n' % (part, self.textLines[i])
                    cur_text_len += len(self.textLines[i])
            else:
                cur_text_len = 0
                part = ''

            if cur_text_len > max_text_len:
                self.text = part
                max_text_len = cur_text_len
            i += 1

        if self.isCharsetGB:
            try:
                self.text = self.text.decode('gb2312').encode('utf8')
            except Exception:
                pass
        return self.text


if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 0:
        print('Usage: extractor.py [url] [[filename]]')
    else:
        ext = Extractor()
        filename = 'plain.txt'
        if len(args) >= 3:
            filename = args[2]
        f = open(filename, 'w')
        text = ext.get_plain_text(
            'https://www.cnblogs.com/ivictor/p/4834864.html')
        print(text)
        f.close
