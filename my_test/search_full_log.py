#coding=utf-8
# python2.7

# @bloke 提供指定的卡号、点播时间，来搜索关于此卡号在此时间的点播信息。

'''
import os
import sys
import datetime
import re
import threading
import time

siteadminsvc_list = []
weiwoo_list = []
weiwoo_path = []
pho_vss = []
pho_erm = []

# 区域网段地址
area_list = {
    'A' : '172.16.72.',
    'B' : '172.16.73.',
    'C' : '172.16.74.',
    'D' : '172.16.75.',
    'E' : '172.16.76.',
    'F' : '172.16.77.',
    'G' : '172.16.78.',
    'H' : '172.16.84.',
}

re_time = re.compile(r'\d{1,2}\:\d{1,2}')
try:
    while 1:    # 获取卡号
        card_num = raw_input('Card Num: ').strip()
        if card_num: break
    while 1:    # 获取时间点
        the_time = raw_input('Time [HH:MM]: ').strip()
        if len(the_time) == 0: continue
        if not re_time.match(the_time):
            print "Please enter a valid time format !"
            continue
        if the_time: break
    while 1:       #获取时间范围
        range_time = raw_input('Range time [min]: ').strip()
        if not range_time or not range_time.isdigit(): continue
        else:
            range_time *= 60
            break
    while 1:    #获取区域
        area = raw_input('Area: ').strip().upper()
        if len(area) == 0: continue
        if len(area) > 1 or not area_list.has_key(area):
            print "Please enter a valid area number !"
            continue
        else: break
except KeyboardInterrupt, e:
    sys.exit('\nExit ...')
    
# 定义不同日志的主机地址
host_list = {
    'rtspproxy' : ['21', '25', '29'],
    'ssm_tianshan' : ['21', '25', '29'],
    'mod' : ['29'],
    'weiwoo' : ['27'],
    'stream1' : ['23'],
    'stream2' : ['31'],
    'siteadminsvc' : ['21'],
}
# 定义各区域的OSTR2的主机地址
address_list = {
    'A' : '172.27.19.52',
    'B' : '172.27.27.52',
    'C' : '172.27.35.52',
    'E' : '172.27.51.52',
    'H' : '172.27.26.52',
}
for h in area_list:
    for i,l in host_list.iteritems():
        for n in l:
            address_list[h + '_' + i] = area_list[h] + n

# 文件路径
dir_path = r'\c$\TianShan\logs'
rtspproxy_files = ['RtspProxy.log'] + ['RtspProxy.%s.log' % n for n in range(5)]
ssm_tianshan_files = ['ssm_tianshan_s1.log'] + ['ssm_tianshan_s1.%s.log' % n for n in range(10)]
mod_files = ['MODSvc.log'] + ['MODSvc.%s.log' % n for n in range(5)]
weiwoo_files = [['weiwoo.log'] + ['weiwoo.%s.log' % n for n in range(5)], ['Path.log'] + ['Path.%s.log' % n for n in range(10)], ['pho_VSS.log'] + ['pho_VSS.%s.log' % n for n in range(10)], ['pho_ERM.log'] + ['pho_ERM.%s.log' % n for n in range(5)]]
siteadminsvc_files = ['SiteAdminSvc.log'] + ['SiteAdminSvc.%s.log' % n for n in range(5)]
stream_files1 = [['NSS2.log'] + ['NSS2.%s.log' % n for n in range(5)], ['NSS.log'] + ['NSS.%s.log' % n for n in range(5)]]
stream_files2 = [['NSS3.log'] + ['NSS3.%s.log' % n for n in range(5)], ['NSS4.log'] + ['NSS4.%s.log' % n for n in range(5)]]
ostr2_files = [['RtspProxy.log'] + ['RtspProxy.%s.log' % n for n in range(1,6)], ['ssm_ngod2.log'] + ['ssm_ngod2.%s.log' % n for n in range(1,6)], ['StreamSmith.log'] + ['StreamSmith.%s.log' % n for n in range(1,6)]]

logfile_list = {
    'rtspproxy' : rtspproxy_files,
    'ssm_tianshan' : ssm_tianshan_files,
    'mod' : mod_files,
    'weiwoo' : weiwoo_files,
    'stream1' : stream_files1,
    'stream2' : stream_files2,
    'siteadminsvc' : siteadminsvc_files,
}

# 生成主机地址对应的日志文件列表，例：{20:[file_list]} 
def get_file(sign, area):
    file_abspath_dict = {}
    for l in logfile_list[sign]:
        if isinstance(l, list):
            for i in l:
                for n in host_list[sign]:
                    if file_abspath_dict.has_key(n):
                        file_abspath_dict[n].extend(['\\\\' + area_list[area] + n + dir_path + '\\' + i])
                    else:
                        file_abspath_dict[n] = ['\\\\' + area_list[area] + n + dir_path + '\\' + i]
        else:
            for n in host_list[sign]:
                if file_abspath_dict.has_key(n):
                    file_abspath_dict[n].extend(['\\\\' + area_list[area] + n + dir_path + '\\' + l])
                else:
                    file_abspath_dict[n] = ['\\\\' + area_list[area] + n + dir_path + '\\' + l]
    return file_abspath_dict
rtspproxy_abs_path = get_file('rtspproxy', area)
ssm_tianshan_abs_path = get_file('ssm_tianshan', area)
mod_abs_path = get_file('mod', area)
weiwoo_abs_path = get_file('weiwoo', area)
stream1_abs_path = get_file('stream1', area)
stream2_abs_path = get_file('stream2', area)
siteadminsvc_abs_path = get_file('siteadminsvc', area)

# 定义正则匹配
re_number = re.compile(r'%s' % card_num)
re_time = re.compile(r'(\d{2}:\d{2}):')
#re_socket = re.compile(r'(\d*\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d*)')
re_socket = re.compile(r'(\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d*)')
re_session = re.compile(r'processed: session\[([\d\]]+)]')
re_stream_session = re.compile(r'STREAM\/(\S*)')
re_stream_num = re.compile(r'-h (\S*)\ -p (\S*)')
re_weiwoo_session = re.compile(r'weiwoo session\((\w+)\)')
re_mod_session = re.compile(r'ModPur\/(\S*)')

# 在rtspproxy日志中搜索指定卡号和对应时间的相关信息
def search_card_number(card_num, the_time):
    info_card_number = []
    session_num = ''
    for the_ip, files in rtspproxy_abs_path.iteritems():
        for the_file in files:
            with file(the_file, 'rb') as f:
                for line in f.xreadlines():
                    if re.findall(re_number, line):
                        log_time = re_time.findall(line)[0]
                        #扩展时间
                        if abs((datetime.datetime.strptime(the_time, '%H:%M') - datetime.datetime.strptime(log_time, '%H:%M')).total_seconds()) < range_time:  
                            info_card_number.append(line)
                else:
                    # 一旦在一个文件中匹配到相关信息，则退出循环
                    if len(info_card_number) > 0: break
            if len(info_card_number) > 0: break
        if len(info_card_number) > 0: break
    print info_card_number
# 返回对应卡号和时间点的信息，日志文件所在机器的IP地址的最后一位，匹配到信息的日志文件名
    return info_card_number, the_ip, the_file

# 从得到的卡号的相关信息中匹配出进程相关信息
def search_socket(info_card_number, the_ip, the_file, n=0):
    info_socket = []
    # 如果在指定卡号和时间内，匹配出多行信息，需要选择
    if len(info_card_number) > 1:
        for l in enumerate(info_card_number): 
            print l
        try:
            n = int(raw_input('Number: ').strip())
            info_socket_num = re_socket.findall(info_card_number[n])[0]
        except KeyboardInterrupt, e:
            sys.exit('\nExit ...')
        except IndexError, e:
            print "Please enter the correct serial number ! [%s]" % e
            sys.exit('Error.')
        except TypeError, e:
            print "Please enter the correct serial number ! [%s]" % e
        
    else:
        try:
            info_socket_num = re_socket.findall(info_card_number[n])[0]
        except IndexError, e:
            sys.exit('No relevant information. [ %s ]' % e)
    with file(the_file, 'rb') as f:
        for line in f.xreadlines():
            if info_socket_num in line:
                info_socket.append(line)
    if not info_socket:
        raise NameError('No socket information.')
    else:
        for i in info_socket:
            if re_session.findall(i):
                try:
                    session_num = re_session.findall(i)[0]
                except IndexError,e:
                    pass
    return info_socket, session_num, the_ip #返回socket相关信息，session号
    
def search_ssm_tianshan(info_socket, session_num, the_ip):
    info_tianshan = []
    for file_n in ssm_tianshan_abs_path[the_ip]:
        with file(file_n) as f:
            for line in f.xreadlines():
                if session_num in line:
                    info_tianshan.append(line)
    return info_tianshan

def search_id(info_tianshan):
    stream_session, weiwoo_session, mod_session, stream_h, stream_p = '','','','',''
    for i in info_tianshan:
        if re_stream_session.findall(i):
            stream_session = re_stream_session.findall(i)[0]
            if re_stream_num.findall(i):
                stream_h, stream_p = re_stream_num.findall(i)[0]
        if re_weiwoo_session.findall(i):
            weiwoo_session = re_weiwoo_session.findall(i)[0]
        if re_mod_session.findall(i):
            mod_session = re_mod_session.findall(i)[0]
    return stream_session, weiwoo_session, mod_session, stream_h, stream_p

def search_mod_info(mod_session=''):
    the_mod_info = []
    if mod_session:
        for the_ip, file_l in mod_abs_path.iteritems():
            for file_n in file_l:
                with file(file_n, 'rb') as f:
                    for line in f.xreadlines():
                        if mod_session in line:
                            the_mod_info.append(line)
                if len(the_mod_info) > 0: break
            if len(the_mod_info) > 0: break
    return the_mod_info

def generate_flist(s, s_list):
    ss = []
    for i in s_list:
        if s in i:
            ss.append(i)
    return ss

def search_weiwoo_siteadminsvc_log(weiwoo_session, f):
    global siteadminsvc_list
    siteadminsvc_list.append('\n' + 'Siteadminsvc'.center(40, '*') + '\n')
    if weiwoo_session:
        siteadminsvc_dict = siteadminsvc_abs_path
        for the_ip, items in siteadminsvc_dict.iteritems():
            for item in items:
                with file(item, 'rb') as f:
                    for line in f.xreadlines():
                        if weiwoo_session in line:
                            siteadminsvc_list.append(line)
                if len(siteadminsvc_list) > 1: break

def search_weiwoo_weiwoo_log(weiwoo_session, f):
    global weiwoo_list
    weiwoo_list.append('\n' + 'Weiwoo'.center(40, '*') + '\n')
    if weiwoo_session:
        for the_ip, file_n in weiwoo_abs_path.iteritems():
            weiwoo_file_list = generate_flist('weiwoo', file_n)
        for item in weiwoo_file_list:
            with file(item, 'rb') as f:
                for line in f.xreadlines():
                    if weiwoo_session in line:
                        weiwoo_list.append(line)
            if len(weiwoo_list) > 1: break 

def search_weiwoo_path_log(weiwoo_session, f):
    global weiwoo_path
    weiwoo_path.append('\n' + 'Path'.center(40, '*') + '\n')
    if weiwoo_session:
        for the_ip, file_n in weiwoo_abs_path.iteritems():
            path_file_list = generate_flist('Path', file_n)
        for item in path_file_list:
            with file(item, 'rb') as f:
                for line in f.xreadlines():
                    if weiwoo_session in line:
                        weiwoo_path.append(line)
            if len(weiwoo_path) > 1: break

def search_weiwoo_pho_vss_log(weiwoo_session, f):
    global pho_vss
    pho_vss.append('\n' + 'Pho_vss'.center(40, '*') + '\n')
    if weiwoo_session:
        for the_ip, file_n in weiwoo_abs_path.iteritems():
            pho_vss_file_list = generate_flist('pho_VSS', file_n)
        for item in pho_vss_file_list:
            with file(item, 'rb') as f:
                for line in f.xreadlines():
                    if weiwoo_session in line:
                        pho_vss.append(line)
            if len(pho_vss) > 1: break 

def search_weiwoo_pho_erm_log(weiwoo_session, f):
    global pho_erm
    pho_erm.append('\n' + 'Pho_erm'.center(40, '*') + '\n')
    if weiwoo_session:
        for the_ip, file_n in weiwoo_abs_path.iteritems():
            pho_erm_file_list = generate_flist('pho_ERM', file_n)
        for item in pho_erm_file_list:
            with file(item, 'rb') as f:
                for line in f.xreadlines():
                    if weiwoo_session in line:
                        pho_erm.append(line)
            if len(pho_erm) > 1: break 

def search_stream_info(stream_session, stream_h, stream_p):
    nss_log = []
    if stream_session != '':
        if stream_h == 'sss6_ss_cl':
            sign1 = 'stream2'
            if stream_p == '10800':
                sign2 = 'NSS3'
            else:
                sign2 = 'NSS4'
        else:
            sign1 = 'stream1'
            if stream_p == '20800':
                sign2 = 'NSS2'
            else: sign2 = 'NSS'
        if sign1 == 'stream2':
            for the_ip, file_l in stream2_abs_path.iteritems():
                for file_n in file_l:
                    if sign2 in file_n:
                        with file(file_n, 'rb') as f:
                            for line in f.xreadlines():
                                if stream_session in line:
                                    nss_log.append(line)
                    if len(nss_log) > 0:
                        break
                if len(nss_log) > 0:
                    break
        else:
            for the_ip, file_l in stream1_abs_path.iteritems():
                for file_n in file_l:
                    if sign2 in file_n:
                        with file(file_n, 'rb') as f:
                            for line in f.xreadlines():
                                if stream_session in line:
                                    nss_log.append(line)
                    if len(nss_log) > 0:
                        break
                if len(nss_log) > 0:
                    break
    return nss_log

if __name__ == '__main__':
    f = file('log_%s.txt' % str(card_num), 'wb')
    info_card_number, the_ip, the_file = search_card_number(card_num, the_time)
    if not info_card_number: 
        f.close()
        sys.exit('No relevant information.\nExit !')
    f.write('RTSPPROXY'.center(40, '*') + '\n')
    for i in info_card_number: f.write(i)
    try:
        info_socket, session_num, the_ip = search_socket(info_card_number, the_ip, the_file)
        for i in info_socket: f.write(i)
    except NameError, e:
        f.write(e)
        f.close()
        sys.exit(e)
    print "RTSPPROXY logging searches completed ..."
    
    info_tianshan = search_ssm_tianshan(info_socket, session_num, the_ip)
    f.write('\n' + 'TIANSHAN'.center(40,'*') + '\n')
    for i in info_tianshan: f.write(i)
    print "TIANSHAN logging searches completed ..."
    
    stream_session, weiwoo_session, mod_session, stream_h, stream_p = search_id(info_tianshan)
    the_mod_info = search_mod_info(mod_session)
    f.write('\n' + 'MOD'.center(40, '*') + '\n')
    for i in the_mod_info: f.write(i)
    print "MOD logging searches completed ..."
    
    nss_log = search_stream_info(stream_session, stream_h, stream_p)
    f.write('\n' + 'NSS'.center(40, '*') + '\n')
    for i in nss_log: f.write(i)
    print "NSS logging searches completed ..."

    q = []    
    for n in [search_weiwoo_siteadminsvc_log, search_weiwoo_weiwoo_log, search_weiwoo_path_log, search_weiwoo_pho_vss_log, search_weiwoo_pho_erm_log]:
        p = threading.Thread(target=n, name=str(n), args=(weiwoo_session, f))
        p.start()
        q.append(p)
    for i in q: i.join()
    for l in [siteadminsvc_list, weiwoo_list, weiwoo_path, pho_vss, pho_erm]:
        for i in l:
            f.write(i)
    print "WEIWOO logging searches completed ...\n"
    t=5
    ll = range(1,6)
    for t in reversed(ll):
        sys.stdout.write( "[ %s seconds after the exit. ] \r" % t )
        t -= 1
        time.sleep(1)
'''