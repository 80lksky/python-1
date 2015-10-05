# encoding: utf-8
__author__ = 'zhanghe'


import requests
import random
import json
import time
import re


# 配置User-Agent
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}


NAME = 875270022
ClientID = 53999199
MsgId = 3030001

qq_hash = ''
user_list_dict = {}
group_list_dict = {}
s = requests.session()


qq_cookie = {
    'supertoken': '',
    'skey': '',
    'pt2gguin': '',
    'superuin': '',
    'superkey': '',
    'uin': '',
    'ptisp': '',
    'ptnick_' + str(NAME): '',
    'u_' + str(NAME): '',
    'ptwebqq': '',
    # 验证
    'pt4_token': '',
    'p_uin': '',
    'p_skey': '',
}


def get_login_img():
    """
    获取登录二维码图片
    """
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
    payload = {
        'appid': '501004106',
        'e': '0',
        'l': 'M',
        's': '5',
        'd': '72',
        'v': '4',
        't': random.random()
    }
    header['Host'] = 'ssl.ptlogin2.qq.com'
    response = s.get(url, params=payload, headers=header)
    with open('ptqrshow.png', 'wb') as f:
        for item in response:
            f.write(item)


def check_login_status():
    """
    检查登录状态
    """
    url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
    payload = {
        'webqq_type': '10',
        'remember_uin': '1',
        'login2qq': '1',
        'aid': '501004106',
        'u1': 'http://w.qq.com/proxy.html?login2qq=1&webqq_type=10',
        'ptredirect': '0',
        'ptlang': '2052',
        'daid': '164',
        'from_ui': '1',
        'pttype': '1',
        'dumy': '',
        'fp': 'loginerroralert',
        'action': '0-0-36375',
        'mibao_css': 'm_webqq',
        't': time.time(),
        'g': '1',
        'js_type': '0',
        'js_ver': '10135',
        'login_sig': '',
        'pt_randsalt': '0'
    }
    header['Host'] = 'ssl.ptlogin2.qq.com'
    response = s.get(url, params=payload, headers=header)
    print response.content
    print response.url
    print response.cookies
    if 'ptwebqq' in response.cookies:
        qq_cookie['ptwebqq'] = response.cookies['ptwebqq']
    return response.content


def check_sig(url):
    header['Host'] = 'ptlogin4.web2.qq.com'
    response = s.get(url, headers=header)
    print response.content
    print response.url
    print response.cookies


def read_login_status(status=None):
    """
    读取登录状态
    """
    # login_status = "ptuiCB('66','0','','0','二维码未失效。(3380616416)', '');"
    # login_status = "ptuiCB('0','0','http://ptlogin4.web2.qq.com/check_sig?pttype=1&uin=875270022&service=ptqrlogin&nodirect=0&ptsigx=60659e61c2dfdd3f21e34809d0a2d3baedb5e4f6a7703334382fb29629e6ee623f7295a85c63834cfb8898cbc44ba8f38246d5afcf2140036b83aff7d8a96c37&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&f_url=&ptlang=2052&ptredirect=100&aid=501004106&daid=164&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=3&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0','0','登录成功！', '╰微微.ヾ迷╮');"
    login_status_rule = r'ptuiCB\((.*?)\);'
    login_status_list = re.compile(login_status_rule, re.S).findall(status)
    result_list = []
    if login_status_list:
        result_list = [i.strip(' \'') for i in login_status_list[0].split(',')]
    # for item in result_list:
    #     print item
    # return result_list
    if not result_list:
        return None
    else:
        if result_list[0] == '66' and result_list[1] == '0':
            print result_list[4]
            return {'status': result_list[4]}
        elif result_list[0] == '0' and result_list[1] == '0':
            print result_list[2]
            return {'check_url': result_list[2]}


def get_session_id():
    """
    获取sessionId
    :return:
    """
    session_id_url = 'http://d.web2.qq.com/channel/login2'
    header['Host'] = 'd.web2.qq.com'
    header['Origin'] = 'http://d.web2.qq.com'
    header['Referer'] = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
    session_id_dict = {
        "ptwebqq": qq_cookie['ptwebqq'],
        "clientid": ClientID,
        "psessionid": "",
        "status": "online"
    }
    session_id_payload = {'r': json.dumps(session_id_dict)}
    response = s.post(session_id_url, data=session_id_payload, headers=header)
    data = json.loads(response.content)
    return data['result']['psessionid']


def get_self_info():
    """
    获取个人信息
    """
    url_self_info = 'http://s.web2.qq.com/api/get_self_info2?t=1434857217484'
    header['Host'] = 's.web2.qq.com'
    header['Referer'] = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
    response = s.get(url_self_info, headers=header)
    return json.dumps(response.content, ensure_ascii=False, indent=4)


def get_vf_web_qq():
    """
    获取验证令牌
    :return:
    """
    vf_web_qq_url = 'http://s.web2.qq.com/api/getvfwebqq'
    vf_web_qq_payload = {
        'ptwebqq': qq_cookie['ptwebqq'],  # 从cookie中获取
        'clientid': ClientID,
        'psessionid': '',
        't': time.time()
    }
    response = s.get(vf_web_qq_url, params=vf_web_qq_payload, headers=header)
    print response.content
    return json.loads(response.content)['result']['vfwebqq']


def get_hash(x, K):
    """
    获取hash令牌（由js转化过来）
    获取群组信息，好友信息需要用到
    """
    # x += ""
    N = [0, 0, 0, 0]
    for T in range(0, len(K)):
        N[T % 4] ^= ord(K[T])
    U = ["EC", "OK"]
    V = []
    V.append(int(x) >> 24 & 255 ^ ord(U[0][0]))
    V.append(int(x) >> 16 & 255 ^ ord(U[0][1]))
    V.append(int(x) >> 8 & 255 ^ ord(U[1][0]))
    V.append(int(x) & 255 ^ ord(U[1][1]))
    U = []
    for T in range(0, 8):
        U.append(T % 2)
        if U[T] == 0:
            U[T] = N[T >> 1]
        else:
            U[T] = V[T >> 1]
    N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    V = ""
    for T in range(0, len(U)):
        V += N[U[T] >> 4 & 15]
        V += N[U[T] & 15]
    return V


def get_group_list():
    """
    获取群组列表信息
    """
    group_list_url = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
    group_list_payload = {'r': json.dumps({"vfwebqq": vfwebqq, "hash": qq_hash})}
    header['Host'] = 's.web2.qq.com'
    header['Origin'] = 'http://s.web2.qq.com'
    header['Referer'] = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
    response = s.post(group_list_url, data=group_list_payload, headers=header)
    print json.dumps({"vfwebqq": vfwebqq, "hash": qq_hash})

    group_list = json.loads(response.content)['result']['gnamelist']
    for group_item in group_list:
        group_list_dict[group_item['name']] = group_item
    print json.dumps(group_list_dict, ensure_ascii=False, indent=4)
    return json.loads(response.content)


def get_group_detail(group_code):
    """
    获取群组详细信息
    包含群组成员信息
    """
    group_detail_url = 'http://s.web2.qq.com/api/get_group_info_ext2'
    group_detail_payload = {
        'gcode': group_code,
        'vfwebqq': vfwebqq,
        't': time.time()
    }
    header['Host'] = 's.web2.qq.com'
    header['Referer'] = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
    response = s.get(group_detail_url, params=group_detail_payload, headers=header)
    group_detail = json.loads(response.content)
    return group_detail


def get_friends_info():
    """
    获取好友信息
    """
    friends_info_url = 'http://s.web2.qq.com/api/get_user_friends2'
    friends_info_payload = {'r': json.dumps({"vfwebqq": vfwebqq, "hash": qq_hash})}
    header['Host'] = 's.web2.qq.com'
    header['Origin'] = 'http://s.web2.qq.com'
    header['Referer'] = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
    response = s.post(friends_info_url, data=friends_info_payload, headers=header)
    print json.dumps({"vfwebqq": vfwebqq, "hash": qq_hash})
    return json.loads(response.content)


def get_group_uin_by_name(group_name):
    if group_name in group_list_dict:
        print '找到对应群组'
        print group_list_dict[group_name]['gid']
        return group_list_dict[group_name]['gid']
    print '没有对应群组'


def send_group_msg(group_uin, msg):
    """
    发送群消息
    """
    group_msg_url = 'http://d.web2.qq.com/channel/send_qun_msg2'
    header['Host'] = 'd.web2.qq.com'
    header['Origin'] = 'http://d.web2.qq.com'
    header['Referer'] = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
    group_msg_dict = {
        "group_uin": group_uin,
        "content": "[\"" + msg + "\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]",
        "face": 0,
        "clientid": ClientID,
        "msg_id": MsgId,  # todo 这个值怎么确定?
        "psessionid": PSessionID
    }
    group_msg_payload = {'r': json.dumps(group_msg_dict)}
    response = s.post(group_msg_url, data=group_msg_payload, headers=header)
    print json.loads(response.content)
    return json.loads(response.content)


def get_friends_account(friends_uin):
    """
    获取好友QQ号码与uin的对应关系
    """
    friends_account_dict = {}
    friends_account_url = 'http://s.web2.qq.com/api/get_friend_uin2'
    header['Host'] = 's.web2.qq.com'
    header['Referer'] = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
    friends_account_payload = {
        'tuin': friends_uin,
        'type': 1,
        'vfwebqq': vfwebqq,
        't': time.time(),
    }
    response = s.get(friends_account_url, params=friends_account_payload, headers=header)
    result_dict = json.loads(response.content)
    # friends_account_dict['account'] = result_dict['result']['account']
    # friends_account_dict['uin'] = result_dict['result']['uin']
    # FriendsList.append(friends_account_dict)
    return result_dict['result']['account']


def get_uin_by_qq(qq):
    """
    根据QQ号码获取uin
    :param qq:
    :return:
    """
    return user_list_dict[qq]['uin']


def get_nick_by_qq(qq):
    """
    根据QQ号码获取昵称
    :param qq:
    :return:
    """
    return user_list_dict[qq]['nick']


def send_qq_msg(qq, msg):
    qq_msg_url = 'http://d.web2.qq.com/channel/send_buddy_msg2'
    header['Host'] = 'd.web2.qq.com'
    header['Referer'] = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
    qq_msg_dict = {
        "to": get_uin_by_qq(qq),
        "content": "[\""+str(msg)+"\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]",
        "face": 0,
        "clientid": ClientID,
        "msg_id": MsgId,  # todo 这个值怎么确定，随机，需要自增?
        "psessionid": PSessionID
    }
    qq_msg_payload = {'r': json.dumps(qq_msg_dict)}
    response = s.post(qq_msg_url, data=qq_msg_payload, headers=header)
    qq_msg_result = json.loads(response.content)
    if qq_msg_result['retcode'] == 0 and qq_msg_result['result'] == 'ok':
        print '发送成功'
    else:
        print '发送失败'
    # return json.loads(response.content)
    # {"retcode":0,"result":"ok"}


def get_new_msg():
    """
    获取最新消息（轮询）
    备注：请求到返回时间大概10S
    可以用死循环模拟轮询
    """
    new_msg_url = 'http://d.web2.qq.com/channel/poll2'
    header['Host'] = 'd.web2.qq.com'
    header['Referer'] = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
    new_msg_dict = {
        "ptwebqq": qq_cookie['ptwebqq'],
        "clientid": ClientID,
        "psessionid": PSessionID,
        "key": ""
    }
    new_msg_payload = {'r': json.dumps(new_msg_dict)}
    response = s.post(new_msg_url, data=new_msg_payload, headers=header)
    content = json.loads(response.content)
    if content['retcode'] == 0:
        for row in content['result']:
            # 接收群组消息
            if row['poll_type'] == 'group_message':
                group_code = row['value']['group_code']
                send_uin = row['value']['send_uin']
                send_qq = get_friends_account(send_uin)
                group_name = ''
                member_name = ''
                # 获取群组详细信息
                group_detail = get_group_detail(group_code)
                if group_detail['retcode'] == 0:
                    group_name = group_detail['result']['ginfo']['name']
                    for group_row in group_detail['result']['minfo']:
                        if group_row['uin'] == send_uin:
                            member_name = group_row['nick']
                msg = row['value']['content'][1]
                msg_info = '群组消息：%s\t成员[%s]：%s\t消息：%s\n' % (group_name, send_qq, member_name, msg)
                print msg_info
                # yield msg_info
            # 接收好友消息
            if row['poll_type'] == 'message':
                from_uin = row['value']['from_uin']
                send_time_stamp = row['value']['time']
                send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(send_time_stamp))
                # 获取好友详细信息
                from_qq = get_friends_account(from_uin)
                nick = get_nick_by_qq(from_qq)
                msg = row['value']['content'][1]
                msg_info = '好友消息：%s\t好友[%s]：%s\t消息：%s\n' % (send_time, from_qq, nick, msg)
                print msg_info
                # yield msg_info


if __name__ == "__main__":
    get_login_img()
    raw_input('扫描完毕请回车')
    login_status_response = check_login_status()
    login_status = read_login_status(login_status_response)
    if 'status' in login_status:
        print login_status['status']
        raw_input('扫描完毕请回车')
    if 'check_url' in login_status:
        print login_status['check_url']
        check_sig(login_status['check_url'])

        print get_self_info()

        vfwebqq = get_vf_web_qq()
        print vfwebqq

        qq_hash = get_hash(NAME, qq_cookie['ptwebqq'])
        print('----------------群组列表 START----------------')
        group_list_info = get_group_list()
        print json.dumps(group_list_info, ensure_ascii=False, indent=4)
        print('----------------群组列表   END----------------')
        print('----------------好友列表 START----------------')
        friends_info = get_friends_info()
        print json.dumps(friends_info, ensure_ascii=False, indent=4)
        print('----------------好友列表   END----------------')
        print('----------------好友字典 START----------------')
        user_info_dict = {}
        user_mark_dict = {}
        for i in friends_info['result']['info']:
            user_info_dict[i['uin']] = i
        for i in friends_info['result']['marknames']:
            user_mark_dict[i['uin']] = i
        print len(user_info_dict)
        print len(user_mark_dict)
        user_dict = {}
        for i in user_info_dict:
            for j in user_mark_dict:
                if i == j:
                    user_dict[i] = dict(user_info_dict[i], **user_mark_dict[j])
                    break
                else:
                    user_dict[i] = user_info_dict[i]
        print json.dumps(user_dict, ensure_ascii=False, indent=4)
        print('----------------好友字典   END----------------')
        print('----------------好友信息 START----------------')
        for i in user_dict:
            user_account = get_friends_account(i)
            print 'QQ号码：' + str(user_account)
            user_list_dict[user_account] = user_dict[i]
        print json.dumps(user_list_dict, ensure_ascii=False, indent=4)
        print('----------------好友信息   END----------------')
        PSessionID = get_session_id()
        # # 给指定好友发送消息
        # send_qq_msg(455091702, 'this is a test by python')
        # while 1:
        #     raw_input_msg = raw_input("请输入消息: ")
        #     send_qq_msg(455091702, raw_input_msg)
        #     MsgId += 1
        # # 给指定群组发送消息
        # MsgId += 15
        # group_uin = get_group_uin_by_name(u'中环V领地小区交流群')
        # send_group_msg(group_uin, 'this is a test by python')
        # {u'retcode': 0, u'result': u'ok'}

        # group_uin = int(get_group_uin_by_name(u'Python爬虫群'))
        # group_uin = get_group_uin_by_name(u'中环V领地小区交流群')
        group_uin = get_group_uin_by_name(u'iQQ')
        for i in range(120):
            group_msg = 'Hello World!\nSend by python\n%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            send_group_msg(group_uin, group_msg)
            MsgId += 1
            time.sleep(60)
        while 1:
            get_new_msg()
            time.sleep(5)
        # while 1:
        #     raw_input_msg = raw_input("请输入消息: ")
        #     send_group_msg(group_uin, raw_input_msg)
        #     MsgId += 1
        # while 1:
        #     print '1、发送好友消息'
        #     print '2、发送群组消息'
        #     send_type = raw_input("请输入类型: ")
        #     if send_type == 1:
        #         continue
        #     if send_type == 2:
        #         raw_input_msg = raw_input("请输入消息: ")
        #         send_group_msg(group_uin, raw_input_msg)
        #         MsgId += 1
        #         continue


# todo 状态提醒
# {"retcode":0,"result":[{"poll_type":"buddies_status_change","value":{"uin":1166353395,"status":"online","client_type":4}}]}
# {"retcode":0,"result":[{"poll_type":"buddies_status_change","value":{"uin":3019820949,"status":"offline","client_type":1}}]}
# {"retcode":0,"result":[{"poll_type":"buddies_status_change","value":{"uin":3019820949,"status":"online","client_type":21}}]}
