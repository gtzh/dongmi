from typing import List
import requests
from lxml import etree
import time
import os
from copyheaders import headers_raw_to_dict
import json

global_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}


def all_candidates():
    res = requests.get(
        'http://magwe.ikuyu.cn/xcfwx/weixin/SecretariesVoteAction/getIRStockCandidateList', headers=global_headers).json()
    print(res['datas'])
    # 68 candidates
    candidates: List = res['datas']
    return candidates


def get_candidats_detail(id, filename):
    candidate_url = 'http://magwe.ikuyu.cn/xcfwx/weixin/SecretariesVoteAction/getIRStockCandidateDetail'
    # formatting headers
    headers = headers_raw_to_dict(b"""
		Accept: application/json, text/javascript, */*; q=0.01
		Accept-Encoding: gzip, deflate
		Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
		Cache-Control: no-cache
		Connection: keep-alive
		Content-Length: 17
		Content-Type: application/x-www-form-urlencoded; charset=UTF-8
		Cookie: JSESSIONID=DB4246BA3B34CF51135A6ED0BEC0530E; Hm_lvt_7e33a05d51b20201a7b63aadcfcfc0bc=1645841864; Hm_lpvt_7e33a05d51b20201a7b63aadcfcfc0bc=1645842650
		Host: magwe.ikuyu.cn
		Origin: http://magwe.ikuyu.cn
		Pragma: no-cache
		User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
		X-Requested-With: XMLHttpRequest
 	""")
    print(headers)
    data = {'candidateid': id}
    res = requests.post(candidate_url, headers=headers, data=data).json()
    try:
        file_url = res['data']['files'][1]['fileaddr']
        print(file_url)
        res = requests.get(file_url, headers=global_headers)
        fn = filename + file_url.split('.')[-1]
        if not os.path.exists(filename):
            with open(fn, 'wb') as file:
                file.write(res.content)
    except Exception as e:
        print(e)


def main():
    candidates = all_candidates()
    for candidate in candidates:
        id = candidate['candidateid']
        print(id)
        filename = 'C:\\Users\\tzh\\Documents\\dongmi\\IR\\' + '2021-' + \
            candidate['stockname'] + candidate['name'] + '.'
        get_candidats_detail(id, filename)


if __name__ == '__main__':
    main()
