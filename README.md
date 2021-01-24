# AutoLogin
[parctice-level] if not connect to internet, start to got to login website and login, timer check
帮助自动连接校园网，如果断网，会重新连接，非常low的一种实现

# requires

~~selenium >= 3.141.0~~


~~chromedriver(replace the chromdriver to fit your chrome version)~~

PyExecJS

```
pip3 install PyExecJS 
# conda install selenium
```

# run
更改sim_verification.py中的line75为自己的校园网账户和密码
```
response_content = connection(username = 'xxxxxxxxxxxxxxx', password = 'xxxxxx')
```
```
python sim_verification.py
```
