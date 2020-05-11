import socket
import cv2
import numpy as np
 
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
 
# 接受图片大小的信息
def recv_size(m_sock, m_count):
    buf = bytes()
    while m_count:
        newbuf = m_sock.recv(m_count)
        if not newbuf: return None
        buf += newbuf
        m_count -= len(newbuf)
    return buf
 
 
HOST_IP = "192.168.1.104"  # 主机作为AP热点的ip地址
HOST_PORT = 7654  # 端口号
 
print("Starting socket: TCP...")
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket
 
print("TCP server listen @ %s:%d!" % (HOST_IP, HOST_PORT))
host_addr = (HOST_IP, HOST_PORT)
socket_tcp.bind(host_addr)  # 绑定主机的ip地址和端口号
socket_tcp.listen(1)  # listen函数的参数是监听客户端的个数，这里只监听一个，即只允许与一个客户端创建连接
 
print('waiting for connection...')
socket_con, (client_ip, client_port) = socket_tcp.accept()  # 接收客户端的请求
print("Connection accepted from %s." % client_ip)
 
# send_str = "this is string example....wow!!!"
# send_byte=send_str.encode()
# socket_con.send(send_byte)  # 发送数据
 
while True:
    data1 = recv_size(socket_con, 4)  # 接收开始标志
    start = int.from_bytes(data1, byteorder='little', signed=False)
    print(start)
    if start == 303030303:  # 收到开始标志，开始接收图像
        data2 = recv_size(socket_con, 4)  # 接收要接收的数据长度
        image_length = int.from_bytes(data2, byteorder='little', signed=False)
        data3 = recv_size(socket_con, image_length)
        buff = np.fromstring(data3, np.uint8)
        img_decode = cv2.imdecode(buff, cv2.IMREAD_COLOR)
        rotated = rotate_bound(img_decode,90)
        cv2.imshow('image', rotated )
        cv2.waitKey(33)
 
 
socket_tcp.close()
