# -*- encoding: utf-8 -*-
'''
@File    :   ssh.py
@Time    :   2019/08/05 11:05:23
@Author  :   hao qihan 
@Version :   0.1
@Contact :   2263310007@qq.com
'''
import time
import paramiko



class SSH:
    """
        定义连接服务器的类
    """

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        tran = paramiko.Transport(sock=(self.host, self.port))
        tran.connect(username=self.username, password=self.password)
        self.tran = tran

    def client_linux(self):
        """
        连接linux
        """
        self._client = paramiko.SSHClient()
        self._client._transport = self.tran

    def client_other(self):
        """
        连接其他的(例如：接口机、DPI等)
        """
        self.channel = self.tran.open_session()
        # 获取终端
        self.channel.get_pty()
        # 激活器
        self.channel.invoke_shell()

    def send_command(self, cmd):
        """
        只能发送shell命令
        :cmd 命令
        """
        stdin, stdout, stderr = self._client.exec_command(cmd)
        res = stdout.read().decode('utf-8')
        return res

    def send_string(self, cmd):
        """
        可以发送任何命令，如：DPI或接口机命令都可以
        :cmd 命令
        """
        self.channel.send(cmd + "\r")
        res = ''
        while True:
            time.sleep(0.2)
            response = self.channel.recv(1024).decode('utf8')
            res += response
            if res.strip().endswith("#") or res.strip().endswith("$"):
                break
            if res.strip().endswith("(yes/no)?"):
                self.channel.send("yes")
        print("结束")
        return res

    def close(self):
        """
        关闭链接
        """
        self.tran.close()


if __name__ == "__main__":
    cen = SSH("39.105.162.164",22,"root","hao142951.")
    cen.client_other()
    red = cen.send_string("cd /etc")
    print(red)
    res = cen.send_string("ls")
    print(res.replace("[01;34",""))
