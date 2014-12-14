# -*- coding: utf-8 -*-

"""dbank http://pan.dbank.com/
dbank search interface.

@author: sniper
@since: 2014-12-13
"""

import re
import md5
import base64

import requests

def b(d, e):
    k = len(e)
    f = len(d)
    g = ''
    h = 0
    while h < f:
        j = ord(d[h]) ^ ord(e[h%k])
        g += chr(j)
        h += 1
    return g

def c(h, l):
    k = range(256)
    e = 0
    g = ''
    for f in range(256):
        e = (e + k[f] + ord(h[f%len(h)])) % 256
        d = k[f]
        k[f] = k[e]
        k[e] = d
    f = 0
    e = 0
    for m in range(len(l)):
        f = (f + 1) % 256
        e = (e + k[f]) % 256
        d = k[f]
        k[f] = k[e]
        k[e] = d
        g += chr(ord(l[m]) ^ k[(k[f] + k[e]) % 256])
    return g

def decrypt(g, e):
    g = base64.decodestring(g)
    if e[:2] == 'ea':
        d = g
    elif e[:2] == 'eb':
        d = b(g, c(e, e))
    elif e[:2] == 'ed':
        d = b(g, md5.md5(e).hexdigest())
    else:
        d = g
    return d

def dbank_final_url(url):
    resp = requests.get(url)
    html = resp.content
    g = re.findall(r'"downloadurl":"(.*?)"', html)[0]
    e = re.findall(r'"encryKey":"(.*?)"', html)[0]
    return decrypt(g, e)

if __name__ == '__main__':
    print dbank_final_url('http://dl.vmall.com/c0xn8jav5v')