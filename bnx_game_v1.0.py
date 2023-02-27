# -*- coding: utf-8 -*-
# @File     :bnx_game_v1.0.py
# @Software :PyCharm
import base64
import hashlib
import random
import time
import datetime
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from apscheduler.schedulers.blocking import BlockingScheduler
from eth_account import Account
from eth_account.messages import encode_defunct
from local_fake_useragent import UserAgent
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
    private_key = ['0x7f74ac56f229bf580fd603e92105f920899e1d72bc60fb571fde450dfcfae4c3',  # just test,no money
                   '0x4ebeaccc0a66a77a229473c0f2dc2dc56368da466987f4412479abf3e6829e53',
                   '0x36d92398c73ac12b70fe9564bcbf1e260845d0db56bffff04cce900fef9b2f01',
                   '0x42054a6f4b4e0a778044fe95298be8e146265797c421688c7c68b663c0cfa841',
                   '0x4e6497671c7050e01e717cfd4bb198b1867897fa276ab742800e0a97a66e688e']
    account = Account.from_key(private_key[j])
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
    global j
    for i in range(0, 5):  # (0,5) 中的 5 根据自己账号数量修改
        _account = Account().create()
        # TODO 登录
        token, uid = login(_account.key.hex())
        j = i + 1
        # TODO 打怪
        attack(token, uid)
        # TODO 查询数据
        enter_demon_king(token, uid)
        print("第" + str(j) + "个号")
        # time.sleep(random.randint(1, 3))  # 随机时间函数，如果出现连接报错可以去掉「#」开启该功能，(1,3)意思为随机延迟 1-3 秒
    j = 0


def auto_attack(text="默认值"):
    bnx_run()
    print(text, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    sched = BlockingScheduler()
    # 2023-2-28 12:00:00 每隔30分钟执行一次
    sched.add_job(auto_attack, 'interval', start_date=datetime.datetime(2023, 2, 28, 12, 0, 0), minutes=30,
                  args=['循环完成'])
    sched.start()
