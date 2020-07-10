# Test with nginx

## 准备配置文件模板

从 container 中拷贝一份默认配置出来作为模板。

```console
$ docker run --name tmp-nginx-container -d nginx
$ docker cp tmp-nginx-container:/etc/nginx/nginx.conf nginx.conf
$ docker cp tmp-nginx-container:/etc/nginx/conf.d/default.conf conf.d/default.conf
$ docker rm -f tmp-nginx-container
```

## 准备测试用的域名和 SSL

为了模拟真实环境，准备一个本地域名，并且为其自签发一个 SSL 证书，让我们可以使用 HTTPS 来访问这个域名。

### 测试域名

先将下面的设定写入 `hosts` 文件中，让其生效。

```
127.0.0.1 test.local node1.test.local node2.test.local www.test.local
```

简单的 ping 一下检查设定是否生效。

```console
$ ping test.local
PING test.local (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=128 time=0.176 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=128 time=0.182 ms
64 bytes from localhost (127.0.0.1): icmp_seq=3 ttl=128 time=0.164 ms
64 bytes from localhost (127.0.0.1): icmp_seq=4 ttl=128 time=0.309 ms
64 bytes from localhost (127.0.0.1): icmp_seq=5 ttl=128 time=0.139 ms
^C
--- test.local ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4002ms
rtt min/avg/max/mdev = 0.139/0.194/0.309/0.059 ms
```

### 签发 SSL 证书

可以选择用 `openssl` 自签发一个证数，但是参数太多，为了方便我使用 `minica` 脚本代劳。

> `minica` 由 letsencrypt 推荐。

这是一个 go 脚本，所以先确保 golang 环境。去官网找到 go tools 的下载地址，跟随 guide 简单配置好 golang。不要忘记环境变量的配置。

https://golang.org/dl/

然后开始准备 `minica` 脚本。

```console
$ git clone https://github.com/jsha/minica.git
$ cd minica
$ go build
```

这时当前目录下会出现一个新文件 `minica`，输入下面命令一键生成证书。

```console
$ ./minica --domains test.local,*.test.local
```

# Working

```console
# run nginx
$ docker run -d -p 3001:3001 \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf \
    -v $(pwd)/conf.d/:/etc/nginx/conf.d/ \
    -v $(pwd)/test.local:/etc/nginx/ssl/test.local \
    --name nginx-test nginx

# for powershell
$ docker run -d -p 3001:3001 -v ${pwd}/nginx.conf:/etc/nginx/nginx.conf -v ${pwd}/conf.d/:/etc/nginx/conf.d/ -v ${pwd}/test.local:/etc/nginx/ssl/test.local --name nginx-test nginx
```

把 SSL 证书导入 nginx。

```nginx
    ssl_certificate     /etc/nginx/ssl/test.local/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/test.local/key.pem;
```
