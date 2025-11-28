# Tools

## NAT（端口转发技术）
nat.py 中提供一个nat转发的python程序, 实现将主机A的端口映射到主机B的端口上(主机A和主机B有线或者无线相连)
使用方法如下：(在主机A下执行以下指令)
```python
python nat.py --localhost 0.0.0.0 --localport 8080 --remotehost 10.42.0.224 --remoteport 22
```
- `localhost`: 为监听的地址，`0.0.0.0`表示允许任何机器进行相连
- `localport`: 为监听的端口，建议选取不会被屏蔽或占用的端口
- `remotehost`: 为目标服务器的内网IP地址
- 'remoteport': 为目标服务器的端口

此指令的功能是将含有公网IP的主机A的端口8080映射到主机B(内网IP: '10.42.0.224')的端口22上
