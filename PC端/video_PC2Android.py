import cv2
import time
import socket
from PIL import Image
import io
import os
import subprocess

# 获取电脑自带摄像头，若用usb摄像头则把0改为1
cap = cv2.VideoCapture(0)
# 调整采集图像大小为640*480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def server_picture_socket():
    while True:
        client_address = ('127.0.0.1', 7560)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #这个就是“拨打电话”了
        client_socket.connect(client_address)
        # print("准备发送")

        # 获取一帧图像
        ret, img = cap.read()
        # 如果ret为false，表示没有获取到图像，退出循环
        if ret is False:
            print("can not get this frame")
            continue    
     
        # 将opencv下的图像转换为PIL支持的格式
        image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        buf = io.BytesIO()# 缓存对象
        image.save(buf, format='JPEG')# 将PIL下的图像压缩成jpeg格式，存入buf中
        jpeg = buf.getvalue()# 从buf中读出jpeg格式的图像
        buf.close()
        jpeg_len = str(len(jpeg))
        
        client_socket.send(jpeg_len.encode("UTF-8"))            #接通了电话，告诉服务器端你可能要接收的图像大小，让他可以分配放图像空间的大小了，为我准备好包间
        
        eee= client_socket.recv(1024).decode()           #晓得服务器端接收到了长度

        client_socket.sendall(jpeg)         #发送图像数据给服务器端

        re = client_socket.recv(1024).decode()         #对面发过来消息他已经接收完图像


        # print("发送完毕")

    client_socket.close()
 
if __name__ == '__main__':
    subprocess.call("adb shell am broadcast -a NotifyServiceStop", shell=True)
    subprocess.call("adb forward tcp:7560 tcp:7561", shell=True)
    subprocess.call("adb shell am broadcast -a NotifyServiceStart", shell=True)
    server_picture_socket()

