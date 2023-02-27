# -*- coding: utf-8 -*-
# @File     :bnx_game_v1.0.py
# @Software :PyCharm
import base64
import hashlib
import time
import schedule
import random
import requests
from local_fake_useragent import UserAgent
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from eth_account import Account
from eth_account.messages import encode_defunct
from loguru import logger

s = 'O&FPGp+on=vX.V@Nc17dsat85TWwgSzfyZLIuq4AYJK6r2kmC3lhbBR9HiEeUDj0MxQ'
j = 0
k = 0

def get_uk(account_address):
    _o = account_address[2:]
    key = b"d36704ca8f0daf9f1d0be610cef86d87"
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(_o.encode(), AES.block_size))
    r = base64.b64encode(ciphertext).decode()
    return r


def get_key():
    f = ['x', '7', 'p', 'y', 's', '2', 'i', '9', 'c', 'k', '3', 'm', 'd', 'z', 'l', 't', '5', 'j', 'u', '4', 'v', 'f',
         'r', 'n', 'h', 'q', 'w', 'e', '8', 'a', '6', 'b', 'g']
    e = int(time.time() * 1000)
    a = 4096 * (e - 1668096000000) + (0 << 11) + (0 << 10) + 0
    d, c, u = 33, '', a
    while u / d > 0:
        p = u % d
        c = f[int(p)] + c
        u = (u - p) / d
    c = '_p' + c
    return c, a


def get_sign(e, t, n):
    i, l = "", ""
    if isinstance(e, dict):
        for s in e:
            i += s + "=" + str(e[s]) + "&"
    elif isinstance(e, str) and e != "":
        i += e + "&"
    i += "tk=" + str(t)

    c = [0] * len(n)
    for f in range(len(i)):
        h = n.find(i[f])
        if h >= 0:
            c[h] += 1
    for d in range(len(n)):
        if c[d] > 0:
            for p in range(c[d]):
                l += n[d]

    return hashlib.md5(l.encode()).hexdigest()


def login(private_key):
    """
    登录
    :param private_key: 私钥
    :return:
    """
    key = ['0xe5f8e01ba8e74a5da6ce017ed94d50fbd65d5d1b1937b2818aaf1d881cd5ff82',  #just test,no money
            '0xd8ea7e91b9fc8d998f1dfd8665d655941a8ab8efe84fbde695fff934e4b381cf',
            '0xa197f86b4efcd834fde56e309827f10c76dc5a4853db3827f195d7bc001a498e',
            '0xad4d57ae5078218c3a1bd86776ac67675116f5eeb898777fa699d6cdaf85f6f9',
            '0x20280ffc0767d4be12683f53c7eae687f2dca5d9b566cf40ecc6fd2c65b0cfb5']
    account = Account.from_key(key[j])
    msg = 'You are better than you know!'
    signature = Account.sign_message(encode_defunct(text=msg), account.key.hex()).signature.hex()
    uk = get_uk(account.address.lower())
    key, _tk = get_key()
    value = get_sign({
        "account": account.address.lower(), "uk": uk, "ukSign": signature, "shareCode": "", "w": 1, "cv": 212
    }, _tk, s)
    params = {
        'account': account.address.lower(), 'uk': uk, 'ukSign': signature, 'shareCode': '', 'w': 1, 'cv': 212,
        key: value, '_tk': _tk, '_cv': '212'}
    response = requests.get(url='https://raid.binaryx.pro/chess/login/doChainLogin', params=params).json()
    logger.debug(response)
    if response.get('uid', False):
        return response['token'], response['uid']
    else:
        raise ValueError('登录失败')


def attack(_token, _uid, _consume=200):
    """
    打怪
    :param _token: 账户token
    :param _uid: 账户uid
    :param _consume: 攻击数量
    :return:
    """
    u = UserAgent("chrome")
    headers = {
        'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', 'Cache-Control': 'no-cache',
        'Connection': 'keep-alive', 'Pragma': 'no-cache',
        'Referer': 'https://raid.binaryx.pro/212/web-desktop/index.html?v=14287257',
        'User-Agent': str(u),
        'language': 'en', 'token': _token}
    key, _tk = get_key()
    value = get_sign({"_consume": _consume}, _tk, s)
    params = {'consume': str(_consume), key: value, '_tk': _tk, '_cv': '212', '_uid': _uid}
    response = requests.get('https://raid.binaryx.pro/chess/demonKing/attack', params=params, headers=headers)
    logger.debug(response.text)


def enter_demon_king(_token, _uid):
    key, _tk = get_key()
    value = get_sign({}, _tk, s)
    u = UserAgent("chrome")
    headers = {
        'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', 'Cache-Control': 'no-cache',
        'Connection': 'keep-alive', 'Pragma': 'no-cache',
        'Referer': 'https://raid.binaryx.pro/212/web-desktop/index.html?v=14287257',
        'User-Agent': str(u),
        'language': 'en', 'token': _token}
    params = {key: value, '_tk': _tk, '_cv': '212', '_uid': _uid}

    response = requests.get('https://raid.binaryx.pro/chess/demonKing/enterDemonKing', params=params,
                            headers=headers).json()
    logger.debug(response)

def bnx_run():
    global k,j
    k = k + 1
    for i in range(0,5):  #(0,10) 中的 10 根据自己需要的循环次数修改
        _account = Account().create()
        logger.debug(_account.address)
        logger.debug(_account.key.hex())
        # TODO 登录
        token, uid = login(_account.key.hex())
        j = i + 1
        # TODO 打怪
        attack(token, uid)
        # TODO 查询数据
        enter_demon_king(token, uid)
        print("第"+str(j)+"个号")
        time.sleep(random.randint(1,3))  # 随机时间函数，如果出现连接报错可以尝试开启，(1,3)意思为随机延迟 1-3 秒，可自行修改
    j = 0

    print("第" + str(k) + "次循环")

if __name__ == '__main__':
    bnx_run()
    schedule.every(30).minutes.do(bnx_run)
    while True:
        schedule.run_pending()
