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
    for i in range(0,50):
        key = [0xe5f8e01ba8e74a5da6ce017ed94d50fbd65d5d1b1937b2818aaf1d881cd5ff82,  #just test
                0x3fb4c2c2ff545c27300886e7a32d6a8920c38a8f8d21ab8a02361c1ab8834305,
                0xe224bef742e25a89d8ba21a5686e88fdc8ae99ad74b1d5c44a76d737740144a7]
        account = Account.from_key(key[i])
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
    global k
    k = k + 1
    for i in range(0,3):
        j = str(i + 1)
        _account = Account().create()
        logger.debug(_account.address)
        logger.debug(_account.key.hex())
        # TODO 登录
        token, uid = login(_account.key.hex())
        # TODO 打怪
        attack(token, uid)
        # TODO 查询数据
        enter_demon_king(token, uid)
        print("第"+j+"个号")
    print("第" + str(k) + "次循环")

if __name__ == '__main__':
    bnx_run()
    schedule.every(10).seconds.do(bnx_run)
    while True:
        schedule.run_pending()
