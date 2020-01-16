# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import sys


# chrome://version get driver for your version
class AutoLogin(object):
    def __init__(self, name, pwd, chromedriver='./chromedriver'):
        self.name = name
        self.pwd = pwd
        self.browser = webdriver.Chrome(chromedriver)

        self.ping_test_hosts = {"www.baidu.com": 1, "www.csdn.net":1}  # host: score
        self.ping_interval = 60  # second
        self.ping_dynamic_interval = True
        self.ping_dynamic_interval_rate = {'min': 60, 'max': 60 * 60, 'grow_rate': 1.5}
        self.ping_count = 3
        self.time_out = 5         # second
        
        self.max_login_count = 10
        self.log_website = 'http://210.77.16.21/'

    """def net_ok(self):
        hosts = self.ping_test_hosts
        scores, sum_score = 0, 0
        for host, score in hosts.items():
            if os.system("ping {} -c {} -W {}".format(host, self.ping_count, self.time_out)) == 0:
                scores += score
            sum_score += score
        if scores >= sum_score * 0.5:
            return True
        return False
    """
    def net_ok(self):
        for host, score in self.ping_test_hosts.items():
            for r in os.popen("curl --connect-timeout {} -I https://{}".format(self.time_out, host)).readlines():
                if "200 OK" in r: return True
        return False

    def login(self, name, pwd):
        browser = self.browser
        self.browser.get(self.log_website)
        username = browser.find_element_by_name("username")
        username.clear()
        username.send_keys(name)
        browser.find_element_by_id("pwd_hk_posi").click()
        password = browser.find_element_by_name("pwd")
        password.clear()
        password.send_keys(pwd)
        # elem.send_keys(Keys.RETURN)
        browser.find_element_by_id("loginLink").click()
        result = browser.find_element_by_id("errorInfo_center")
        return result.text.strip().encode("utf-8") != str("用户不存在,请输入正确的用户名!"), result.text.strip()
    
    def main(self):
        while True:
            print("check link, try ping (ping interval {}s).....".format(self.ping_interval))
            if not self.net_ok():
                print("ping not OK, try login (max try login count {}) ......".format(self.max_login_count))
                
                for i in range(self.max_login_count):
                    print(i, self.max_login_count)
                    state, text = self.login(self.name, self.pwd)
                    print("try login {} time:".format(i+1), "success" if state else "failed", text)
                    if state: break
                
                if self.ping_dynamic_interval and self.ping_interval > self.ping_dynamic_interval_rate['min']:
                    self.ping_interval /= self.ping_dynamic_interval_rate['grow_rate']
            else:
                if self.ping_dynamic_interval and self.ping_interval < self.ping_dynamic_interval_rate['max']:
                    self.ping_interval *= self.ping_dynamic_interval_rate['grow_rate']
            print('sleep {}'.format(int(self.ping_interval)))
            os.system('sleep {}'.format(int(self.ping_interval)))


# browser.find_element_by_id()
# source = browser.page_source
# source = source.encode('gb2312','ignore')


if len(sys.argv) >= 3:
    for i in range(100):
        try:
            AutoLogin(sys.argv[1], sys.argv[2]).main()
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                break
            print(e)
else:
    print("[Usage]: python autoogin.py student_number passwd")
