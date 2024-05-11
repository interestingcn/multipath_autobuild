# multipath_autobuild
----

适用于Linux 系统下自动构建`multipath`多路径软件路径配置信息。

## 运行前准备

请确认当前系统中已安装python3.x环境。
```
python3 -V
```


## Quick Start
```
python3 multipath_autobuild.py
```

运行示例：
```
              _ _   _             _   _         _         _          ___       _ _     _
  /\/\  _   _| | |_(_)_ __   __ _| |_| |__     /_\  _   _| |_ ___   / __\_   _(_) | __| |
 /    \| | | | | __| | '_ \ / _` | __| '_ \   //_\| | | | __/ _ \ /__\// | | | | |/ _` |
/ /\/\ \ |_| | | |_| | |_) | (_| | |_| | | | /  _  \ |_| | || (_) / \/  \ |_| | | | (_| |
\/    \/\__,_|_|\__|_| .__/ \__,_|\__|_| |_| \_/ \_/\__,_|\__\___/\_____/\__,_|_|_|\__,_|
                     |_|

Multipath AutoBuild Tool
Version 1.0
Bioinformatics Laboratory of South China Agricultural University - Wangzt


============= Multipath Information =============
            WWID                   | Paths
-------------------------------------------------
3600xxxxxxxxxxxxxxxxxxxxxxx000010  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx00000f  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx00000e  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx00000d  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx00000c  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx00000b  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx00000a  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx000009  |  4
3600xxxxxxxxxxxxxxxxxxxxxxx000008  |  4
3600xxxxxxxxxxxxxxxxxxxxxxxe7ff13  |  1
=================================================
Current number of storage devices:  10
Number of multipath LUNs:  9
Number of single path devices:  1
---------------------------------------------------
Writing to multipath.conf >> multipath.txt
Done.
```
会在当前路径下生成配置内容文件：`multipath.txt`


生成配置文件示例：
```
blacklist {
wwid    3600605b00e45e0a02d842cee11e7ff13
}
multipaths {

    multipath {
        wwid                    3600xxxxxxxxxxxxxxxxxxxxxxxe7ff13
        alias                   vol_1
        path_grouping_policy    multibus
        path_selector           "queue-length 0"
        failback                immediate
        rr_weight               priorities
        no_path_retry           5
        }

    multipath {
        wwid                    3600xxxxxxxxxxxxxxxxxxxxxxxx0000f
        alias                   vol_2
        path_grouping_policy    multibus
        path_selector           "queue-length 0"
        failback                immediate
        rr_weight               priorities
        no_path_retry           5
        }
	...

```

请将该文件内容填写到mutipath配置文件(`/etc/multipath.conf`)对应部分即可。 


## 其他

有关multipath中的个性化配置项请修改脚本line79 - line87 内容。
