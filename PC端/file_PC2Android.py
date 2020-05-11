import subprocess
import socket
import time
import copy
import json
import os


class SendInfoData(object):

    def __init__(self, percent="", sendSize=0):
        self.__percent = percent
        self.__sendSize = sendSize

    def toJson(self):
        return json.dumps({
            "percent": self.__percent,
            "sendSize": self.__sendSize,
        })


# int转byte数组
def intToBytes(intNumber=0): return intNumber.to_bytes(4, "little")


# str转utf-8 byte数组
def strToUtf8Bytes(value): return bytes(value, encoding="utf-8")


if __name__ == '__main__':

    subprocess.call("adb shell am broadcast -a NotifyServiceStop", shell=True)
    subprocess.call("adb forward tcp:9999 tcp:9000", shell=True)
    subprocess.call("adb shell am broadcast -a NotifyServiceStart", shell=True)

    client = socket.socket()
    result = client.connect(("127.0.0.1", 9999))

    # 文件路径
    filePath = "./1.mp4"

    # 文件大小
    allSize = os.path.getsize(filePath)
    fileSize = copy.deepcopy(allSize)
    print("%s\n" % fileSize)
    defaultReadSize = 1024 * 10
    progress = 0

    h = time.time()
    # 读取 文件
    with open(filePath, mode="rb") as readFile:
        while True:
            if fileSize <= 0: 
                break
            readSize = defaultReadSize if fileSize > defaultReadSize else fileSize
            progress += readSize
            percent = '{: .2f}'.format(progress * 1.0 / allSize * 100)
            print("进度：%s" % percent)
            # 读取内容
            readBytes = readFile.read(readSize)
            if not readBytes: break
            tagH = strToUtf8Bytes("@tag:h")
            tagF = strToUtf8Bytes("@tag:f")
            # 携带信息
            infoJson = SendInfoData(percent, readSize).toJson()
            print("json:%s\n" % infoJson)
            infoBytes = strToUtf8Bytes(infoJson)
            infoSize = intToBytes(len(infoBytes))
            # 包裹传输数据
            client.send(tagH)  # 标记开头
            client.send(infoSize)  # 携带参数byte数据长度
            client.send(infoBytes)  # 携带参数内容
            client.send(readBytes)  # 真实传输的内容
            client.send(tagF)  # 标记结尾
            fileSize -= readSize

    client.close()

    f = time.time()
    print("用时：{: .0f}s".format((f - h)))

