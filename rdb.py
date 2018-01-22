#!/usr/bin/python
# --*-- coding: utf-8 --*--
import sys
import base64
import hmac
import urllib
from hashlib import sha256
import json
import datetime

access_key_id = 'MCIALTWYFUDNAEOOUUKZ'
secret_access_key = ''
#获取时间
now = ( datetime.datetime.now() - datetime.timedelta(minutes=480)).strftime("%Y-%m-%d %H:%M:%S")
five_min_ago = ( datetime.datetime.now() - datetime.timedelta(minutes=485)).strftime("%Y-%m-%d %H:%M:%S")
#转换时间格式 "2011-07-11T11:07:00Z"
start = five_min_ago[0:10] +'T' + five_min_ago[11:] + 'Z'
end = now[0:10] +'T' + now[11:] + 'Z'
print start
print end


#构造请求，放到一个字典里
D = {
  "zone":"pek3a",
  "signature_version":1,
  "signature_method":"HmacSHA256",
  "version":1,
  "access_key_id":"MCIALTWYFUDNAEOOUUKZ",
  "action":"GetRDBMonitor",
  "resource":"rmi-9enmu2ra",
  "meters.1":"cpu",
  "meters.2":"memory",
  "meters.3":"disk-us-volume",
  "step":"5m",
  "start_time":start,
  "end_time":end,
  "time_stamp":end,
  "meter_set":"Array",
}
#print D

#按参数名对构造出的请求进行升序排列 
sortedD = sorted(D.items(), key=lambda x: x[0])

#对参数名称和参数值进行URL编码
def percentEncode(str):
        res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'))
        res = res.replace('+', '%20')
        res = res.replace(':', '%3A')
        return res

#构造url请求
canstring = ""

for k,v in sortedD:
        canstring += '&' + percentEncode(k) + '=' + percentEncode(str(v))
#print canstring[1:]

#构造被签名串
string_to_sign = 'GET' + '\n' + "/iaas/" + '\n' + canstring[1:]
#print string_to_sign


#计算签名
h = hmac.new(secret_access_key, digestmod=sha256)
h.update(string_to_sign)
sign = base64.b64encode(h.digest()).strip()
signature = urllib.quote_plus(sign)
#print signature

#构造真实请求url
re = canstring[1:] + '&' + 'signature=' + signature
url = "https://api.qingcloud.com/iaas/?" + re
#print url

def get_values(key):

#使用urlopen获取监控数据，为str类型
    url_out = urllib.urlopen(url)
    data = url_out.readlines()
    print data

#转换为dict,并获取dict中键为meter_set的值，是list，只用一个值，为dict，作为中转
    out_dict = eval(data[0])
#print out_dict
    data_tmp = out_dict['meter_set']
    cpu = data_tmp[0]['data'][0][1]
    mem = data_tmp[1]['data'][0][1]
    disk = data_tmp[2]['data'][0][1]

#print cpu
#print mem
#print disk 


#c_use = cpu['data']
#m_use = mem['data']
#d_use = disk['data']

#cpu_use = c_use[0][1] 
#mem_use = m_use[0][1] 
#disk_use_tmp = d_use[0][1] 
    disk_use = disk.split('|')
    print "disk useage is %s%%" % disk_use[1]
    print "disk used is %sM" % disk_use[2]
    print "disk free is %sM " % disk_use[3]
    print "cpu useage is %.2f%%" % (int(cpu)/10.0) 
    print "memory useage is %.2f%%" % (int(mem)/10.0)
    if sys.argv[1] == "cpu":
        print int(cpu)/10.0
    if sys.argv[1] == "memory":
        print int(mem)/10.0
    if sys.argv[1] == "disk":
        print disk_use[1]
    if sys.argv[1] == "disk_used":
        print disk_use[2]
    if sys.argv[1] == "disk_free":
        print disk_use[3]


if __name__ == '__main__':
    key=sys.argv[1]

    if key is not None:
        try:
            get_values(key)
        except NameError:
            print -0.99
