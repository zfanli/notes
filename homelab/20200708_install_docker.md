# Install Docker

在 CentOS 8 上安装 Docker。参考官网文档。

https://docs.docker.com/engine/install/centos/

这里使用官方推荐的方法进行安装并记录一下步骤。

## 设置仓库

安装 `yum-utils`，使用其中的 `yum-config-manage` 工具将 docker 的 repo 添加到仓库。

```shell
$ sudo yum install -y yum-utils

$ sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

## 安装 Docker Engine

接着直接安装必要的组件。

```shell
$ sudo yum install docker-ce docker-ce-cli containerd.io
```

安装过程中可能提示接受 GPG key，出于风险考虑先确认提示的指纹是否和下面匹配。

`060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`

> 指纹也许会变，到 https://docs.docker.com/engine/install/centos/ 确认最新信息。

> 安装过程可能会出现下面的失败信息。

```log
$ sudo yum install docker-ce docker-ce-cli containerd.io
Docker CE Stable - x86_64                        11 kB/s |  25 kB     00:02
 Last metadata expiration check: 0:00:01 ago on Wed 08 Jul 2020 11:46:44 AM CST.
 Error:
 Problem: package docker-ce-3:19.03.12-3.el7.x86_64 requires containerd.io >= 1.2.2-3, but none of the providers can be installed
  - cannot install the best candidate for the job
  - package containerd.io-1.2.10-3.2.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.13-3.1.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.13-3.2.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.2-3.3.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.2-3.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.4-3.1.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.5-3.1.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.6-3.3.el7.x86_64 is filtered out by modular filtering
(try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
```

> 这时可能是 `container-tools` 依赖了低版本的 `containerd.io` 导致的，可以通过下面的命令禁用 `container-tools` 解决。

```shell
$ yum module disable container-tools
```

## 启动 Docker Engine

使用下面命令启动 Docker。

```shell
$ sudo systemctl start docker
```

> 如果希望使用其他非 root 用户运行 Docker，将其添加到 `docker` 用户组。

```shell
$ sudo usermod -aG docker richard
```

结束。
