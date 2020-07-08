# Install nginx

安装 nginx 进行反向代理和端口转发。在进行之前确保 Docker 已经安装。

## 准备工作

先找个目录放 nginx 的配置文件。我在用户目录下面准备了一块地方来专门放这些文件。你也可以找个你熟悉的位置。

```shell
$ cd ~

$ mkdir -p work/nginx

$ cd work/nginx
```

接着准备一份配置文件模版。

```shell
$ docker run --name tmp-nginx-container -d nginx

$ docker cp tmp-nginx-container:/etc/nginx/nginx.conf nginx.conf

$ docker rm -f tmp-nginx-container
```

来看看这个模版的内容。

```shell
$ cat nginx.conf

user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```
