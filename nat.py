import socket
import threading
import sys
import argparse

# ================= 配置区域 =================

parser = argparse.ArgumentParser(description="NAT端口转发技术")

parser.add_argument("--localhost", default="0.0.0.0", help="监听地址")
parser.add_argument("--localport", default="8080", help="监听端口")
parser.add_argument("--remotehost", default="169.254.4.238", help="服务器地址")
parser.add_argument("--remoteport", default="22", help="服务器端口")

# 监听的地址 (0.0.0.0 表示允许任何机器连接)
LOCAL_HOST = parser.parse_args().localhost
# 监听的端口 (你希望外部连接的端口)
LOCAL_PORT = parser.parse_args().localport

# 目标服务器 (服务器 B) 的内网 IP
REMOTE_HOST = parser.parse_args().remotehost
# 目标服务器的端口 (SSH 默认为 22)
REMOTE_PORT = parser.parse_args().remoteport
# ===========================================

def handle_traffic(source_socket, destination_socket):
    """
    从源 socket 读取数据并发送到目标 socket
    """
    try:
        while True:
            data = source_socket.recv(4096)
            if len(data) == 0:
                break
            destination_socket.send(data)
    except Exception:
        pass
    finally:
        source_socket.close()
        destination_socket.close()

def handle_client(client_socket):
    """
    处理新的客户端连接：建立到目标的连接，并开启双向转发
    """
    # 连接到目标服务器 (服务器 B)
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((REMOTE_HOST, REMOTE_PORT))
    except Exception as e:
        print(f"[!] 无法连接到目标服务器 {REMOTE_HOST}:{REMOTE_PORT} - {e}")
        client_socket.close()
        return

    # 创建两个线程进行双向数据转发
    # 1. 客户端 -> 目标服务器
    t1 = threading.Thread(target=handle_traffic, args=(client_socket, remote_socket))
    # 2. 目标服务器 -> 客户端
    t2 = threading.Thread(target=handle_traffic, args=(remote_socket, client_socket))

    t1.start()
    t2.start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 允许端口复用，防止程序重启时报 Address already in use
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((LOCAL_HOST, LOCAL_PORT))
    except Exception as e:
        print(f"[!] 绑定端口失败: {e}")
        sys.exit(1)

    server.listen(5)
    print(f"[*] 正在监听 {LOCAL_HOST}:{LOCAL_PORT} ...")
    print(f"[*] 流量将被转发到 {REMOTE_HOST}:{REMOTE_PORT}")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"[+] 收到连接: {addr[0]}:{addr[1]}")

            # 为每个连接开启一个线程处理
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except KeyboardInterrupt:
            print("\n[*] 停止转发.")
            break
        except Exception as e:
            print(f"[!] 发生错误: {e}")


if __name__ == '__main__':
    main()
