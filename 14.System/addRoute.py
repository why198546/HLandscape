import socket
import subprocess

def add_route(domain, gateway, interface, metric):
    try:
        # 解析域名以获取IP地址
        ip_addresses = socket.getaddrinfo(domain, None)
        for ip_info in ip_addresses:
            ip_address = ip_info[4][0]
            # 为每个IP地址添加路由
            command = f'route add {ip_address} mask 255.255.255.255 {gateway} metric {metric} if {interface}'
            process = subprocess.run(command, shell=True, capture_output=True)
            if process.returncode == 0:
                print(f'Route added: {ip_address} -> {gateway} on interface {interface} with metric {metric}')
            else:
                # 解码stderr输出，假设它是使用系统默认编码
                error_output = process.stderr.decode()
                print(f'Failed to add route: {error_output}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    # 调用函数以为指定域名添加路由
    add_route('www.hlylsj.com', '192.168.1.1', '12', metric=3)
    add_route('cloud.hlylsj.com', '192.168.1.1', '12', metric=3)
    add_route('app.plex.tv', '192.168.1.1', '12', metric=3)