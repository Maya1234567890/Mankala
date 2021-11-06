from socket import*
import sys

HOST = '109.66.29.58'
PORT = '45000'
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpcliesock = socket(AF_INET, SOCK_STREAM)
tcpcliesock.settimeout(5)

tcpcliesock.connect(ADDR)

