# coding=utf-8
import os,subprocess,re

'''
Automatically generate multipath information for multipath.
eg： python3 multipath_autobuild.py
'''

welcome = '''
              _ _   _             _   _         _         _          ___       _ _     _ 
  /\/\  _   _| | |_(_)_ __   __ _| |_| |__     /_\  _   _| |_ ___   / __\_   _(_) | __| |
 /    \| | | | | __| | '_ \ / _` | __| '_ \   //_\\| | | | __/ _ \ /__\// | | | | |/ _` |
/ /\/\ \ |_| | | |_| | |_) | (_| | |_| | | | /  _  \ |_| | || (_) / \/  \ |_| | | | (_| |
\/    \/\__,_|_|\__|_| .__/ \__,_|\__|_| |_| \_/ \_/\__,_|\__\___/\_____/\__,_|_|_|\__,_|
                     |_|                                                                 

Multipath AutoBuild Tool 
Version 1.0
Bioinformatics Laboratory of South China Agricultural University - Wangzt
                          
'''
print(welcome)

device_list = list()

reg = re.compile(r'^sd\D+$')

for device_name in os.listdir('/dev'):

    res = reg.match(device_name)
    if res == None: continue
    device_list.append(res.group())

wwid_all_list = list()

for device_name in device_list:
    cmd = '/lib/udev/scsi_id --whitelisted --device=/dev/' + device_name
    res = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).stdout.decode('utf8').strip()
    wwid_all_list.append(res)

wwid_count = dict()

for wwid in wwid_all_list:
    if wwid in wwid_count:
        wwid_count[wwid] += 1
    else:
        wwid_count[wwid] = 1

multipath_list = list()
blacklist = list()

for wwid,num in wwid_count.items():
    if num > 1:
        multipath_list.append(wwid)
    else:
        blacklist.append(wwid)

print('============= Multipath Information =============');
print('            WWID                   | Paths       ');
print('-------------------------------------------------');
for wwid,num in wwid_count.items():
    print(f'{wwid}  |  {num}')
print('=================================================')
print('Current number of storage devices: ',len(wwid_count))
print('Number of multipath LUNs: ',len(multipath_list))
print('Number of single path devices: ',len(blacklist))
print('---------------------------------------------------')
print('Writing to multipath.conf >> multipath.txt')

with open('multipath.txt','w') as file:
    file.write('blacklist {\n')
    for wwid in blacklist:
        file.write(f'wwid\t{wwid}\n')
    file.write('}\n')

    file.write('multipaths {\n')
    for index,wwid in enumerate(multipath_list):
        msg = f'''
    multipath {{
        wwid                    {wwid}
        alias                   vol_{index+1}
        path_grouping_policy    multibus
        path_selector           "queue-length 0"
        failback                immediate
        rr_weight               priorities
        no_path_retry           5
        }}
    '''
        file.write(msg)
    file.write('}\n')
print('Done.')