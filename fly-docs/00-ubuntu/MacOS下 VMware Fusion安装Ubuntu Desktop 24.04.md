#  MacOS下 VMware Fusion安装Ubuntu Desktop 24.04

在MacOS系统下通过VMware Fusion虚拟机软件安装`Ubuntu Desktop 24.04 LTS`，并配置静态IP地址的完整流程，帮助开发者快速搭建稳定的Linux开发环境

## 1. 环境准备与软件安装

### 1.1 硬件要求

- **Mac设备**：Apple Silicon芯片（M4/M5系列）
- **内存**：至少8GB（建议16GB用于多虚拟机）
- **磁盘空间**：至少50GB可用空间

### 1.2 软件安装

1. **VMware Fusion**：从官网下载最新版（13.x版本）

2. **`Ubuntu Desktop 24.04 ISO`**：从[Ubuntu 24.04官网](https://cdimage.ubuntu.com/ubuntu/releases/noble/release/)下载

   ![image-20260710215450542](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710215450542.png)

## 2. 虚拟机创建与系统安装

### 2.1 新建虚拟机

![image-20260710215544895](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710215544895.png)

1. 启动VMware Fusion，选择`文件→新建→从光盘或镜像安装`
2. 拖拽下载的ISO文件到指定区域

### 2.2 配置虚拟机参数



点击`自定设置`>修改参数

| 配置项     | 推荐值              | 说明                  |
| :--------- | :------------------ | :-------------------- |
| 处理器核心 | 4个                 | 根据物理CPU核心数分配 |
| 内存       | 6144MB（6GB）       | 开发环境建议至少4GB   |
| 硬盘       | 50GB                | 可根据需求调整        |
| 网络适配器 | 共享主机网络（NAT） | 后续修改为桥接模式    |

![image-20260710215947026](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710215947026.png)

安装完成后要改为从硬盘启动

![image-20260710220040770](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220040770.png)

### 2.3 系统安装流程

>  如果你的鼠标和键盘被虚拟机锁定在窗口内，无法移回外部的 Mac 系统：
>
> - **快捷键**：**`Control` + `Command`** (`⌃` + `⌘`)
> - **效果**：按下后，系统会立即释放输入焦点，鼠标指针会重新出现，你就可以正常操作 Mac 主机了。

1. **启动安装程序**：启动虚拟机后，在引导菜单中选择 `Try or Install Ubuntu`，按回车键继续。该选项会从 ISO 镜像启动 Ubuntu Desktop 安装环境。

   ![image-20260708181714191](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260708181714191.png)

   随后会显示 Ubuntu 启动画面，等待安装向导自动加载，此过程无需操作。

   ![image-20260710220200779](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220200779.png)

2. **选择安装语言**：选择 `English`，然后点击 `Next`。使用英文界面便于后续查阅英文技术文档和排查报错；如果更习惯中文，也可在此直接选择中文。

   ![image-20260710220651899](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220651899.png)

3. **辅助功能设置**：根据需要开启视觉、听觉、键入或指针辅助功能。如无特殊需求，保持默认设置并点击 `Next`。

   ![image-20260710220738639](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220738639.png)

4. **选择键盘布局**：根据实际键盘选择布局，常见 Mac 英文键盘可使用 `English (US)`。可在下方输入框中测试按键，确认无误后点击 `Next`。

   ![image-20260710220806239](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220806239.png)

5. **连接网络**：虚拟机已使用 VMware 虚拟网卡，通常选择 `Use wired connection` 即可通过 Mac 的网络联网。安装期间联网可获取更新和第三方软件；暂时无网时也可选择不连接，安装完成后再配置。

   ![image-20260710220817916](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220817916.png)

6. **安装器更新**：如果提示有新版安装器，可点击 `Update now` 先更新，也可点击 `Skip` 继续当前安装。更新安装器可获得最新的问题修复，但会多耗费一些下载时间。

   ![image-20260710220843039](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220843039.png)

7. **选择安装 Ubuntu**：选择 `Install Ubuntu`，然后点击 `Next`。`Try Ubuntu` 只会进入临时试用环境，不会将系统写入虚拟硬盘。

   ![image-20260710220851520](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220851520.png)

8. **选择安装方式**：选择 `Interactive installation`，按照向导逐项完成配置。`Automated installation` 需要事先准备自动安装配置文件，不适合本次手动安装。

   ![image-20260710220904808](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220904808.png)

9. **选择初始应用**：选择 `Default selection`，安装浏览器和常用基础工具，其他软件可在进入系统后按需安装。如果希望一次安装更多办公和工具类软件，可选择 `Extended selection`。

   ![image-20260710220914974](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220914974.png)

10. **第三方软件**：建议勾选第三方图形与 Wi-Fi 驱动选项，以及额外媒体编解码格式选项，以提高硬件和音视频格式的兼容性。这些内容需在安装过程中从网络下载。

![image-20260710220925423](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220925423.png)

11. **选择磁盘安装方式**：选择 `Erase disk and install Ubuntu`。这里擦除的是当前虚拟机的虚拟硬盘，不会删除 Mac 主机上的文件。如无自定义分区需求，不必选择 `Manual installation`。

![image-20260710220943454](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710220943454.png)

12. **创建用户账户**：填写姓名、计算机名、用户名和密码。用户名建议使用小写英文字母；计算机名将用于局域网识别。建议保留“登录时需要密码”，确认各项通过校验后点击 `Next`。

![image-20260710221231390](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710221231390.png)

13. **设置时区**：在地图上选择所在地区，中国大陆可选择 `Asia/Shanghai`。时区会影响系统时间、日志时间和定时任务，确认无误后点击 `Next`。   ![image-20260710221241889](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710221241889.png)

14. **等待安装完成**：确认安装摘要后开始安装。文件复制和系统配置期间请保持虚拟机运行，不要关闭 VMware Fusion。安装结束后按提示点击重启；重启前请确保虚拟机已改为从虚拟硬盘启动，避免再次进入安装界面。   ![image-20260710221258486](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710221258486.png)

15. 安装完重启，重启后输入刚设置的登录密码，就进入欢迎界面

![image-20260710224113078](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710224113078.png)

### 2.4 设置 root 用户密码

Ubuntu 的超级管理员用户名固定为 `root`，不能修改为其他用户名。Ubuntu 默认锁定 `root` 的密码登录，日常管理建议使用安装系统时创建的普通用户配合 `sudo` 执行管理命令。

如果确实需要启用 `root` 密码，请在 Ubuntu 终端中执行：

```bash
sudo passwd root
```

按提示操作：

1. 输入当前普通用户的登录密码，用于通过 `sudo` 身份验证。
2. 输入为 `root` 设置的新密码（密码设置为`root123456`）。
3. 再次输入新密码进行确认。

> 终端在输入密码时不会显示字符、星号或光标变化，这是 Linux 的正常安全机制。输入完成后直接按回车键即可。

显示以下信息表示密码设置成功：

```text
passwd: password updated successfully
```

使用新密码切换到 `root` 用户：

```bash
su -
```

输入刚设置的 `root` 密码后，可执行以下命令确认当前身份：

```bash
whoami
```

输出 `root` 即表示切换成功。完成管理操作后，执行 `exit` 退回普通用户：

```bash
exit
```

如果不再需要通过密码切换到 `root`，建议重新锁定该账户：

```bash
sudo passwd -l root
```

> 不建议开启 `root` 的 SSH 远程密码登录。远程管理时应使用普通用户登录，再通过 `sudo` 执行需要管理权限的命令。

### 2.5 允许 root 用户远程登录

Ubuntu 默认禁止 `root` 通过 SSH 密码远程登录。如果确实需要开启，请先完成前文的 `root` 密码设置，再按以下步骤操作。

> **安全提醒**：允许 `root` 使用密码直接远程登录会增加暴力破解和账户泄露风险。该方式只建议在本机 NAT 测试环境中临时使用。不要在桥接网络、公网或端口转发环境中使用简单密码。`root123456` 属于弱密码，应替换为唯一的高强度密码。

#### 2.5.1 安装并启动 SSH 服务

在 Ubuntu 终端中执行：

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

确认 SSH 服务已正常运行：

```bash
systemctl status ssh --no-pager
```

输出中应显示 `active (running)`。

#### 2.5.2 开启 root 密码登录

创建独立的 SSH 配置文件，避免直接修改主配置文件：

```bash
printf '%s\n' \
  'PermitRootLogin yes' \
  'PasswordAuthentication yes' | \
  sudo tee /etc/ssh/sshd_config.d/00-root-login.conf
```

检查 SSH 配置语法。命令没有任何输出即表示语法正确：

```bash
sudo sshd -t
```

只有在语法检查通过后才重启 SSH 服务：

```bash
sudo systemctl restart ssh
```

检查 SSH 最终生效的配置：

```bash
sudo sshd -T | grep -E '^(permitrootlogin|passwordauthentication) '
```

应看到：

```text
permitrootlogin yes
passwordauthentication yes
```

#### 2.5.3 检查 root 账户和防火墙

检查 `root` 账户密码状态：

```bash
sudo passwd -S root
```

第二列显示 `P` 表示已设置可用密码；显示 `L` 表示账户已锁定，需重新执行 `sudo passwd root` 设置密码。

如果 UFW 防火墙已启用，放行 SSH：

```bash
sudo ufw allow OpenSSH
sudo ufw status
```

#### 2.5.4 开放所有端口（仅限隔离测试环境）

如果需要从 Mac 访问 Ubuntu 中临时启动的 Web、数据库、Docker 或开发服务，但不想逐个配置端口，可以允许 VMware NAT 网段访问 Ubuntu 的全部端口：

```bash
sudo ufw allow from 192.168.230.0/24
sudo ufw status numbered
```

这条规则允许 `192.168.230.0/24` 网段中的设备访问 Ubuntu 上所有 TCP 和 UDP 端口。当前 VMware NAT 环境中，Mac 和虚拟机均位于该虚拟网段，比允许任意来源更安全。

如仅希望允许 Mac 主机 `192.168.230.1` 访问全部端口，可进一步缩小范围：

```bash
sudo ufw delete allow from 192.168.230.0/24
sudo ufw allow from 192.168.230.1
sudo ufw status numbered
```

如果是一次性的完全隔离测试，也可以直接关闭 UFW：

```bash
sudo ufw disable
sudo ufw status verbose
```

看到 `Status: inactive` 表示 UFW 已关闭。恢复防火墙并仅放行 SSH：

```bash
sudo ufw enable
sudo ufw allow OpenSSH
sudo ufw status verbose
```

如果确实需要在保持 UFW 启用的情况下允许任意来源访问全部端口，可执行：

```bash
sudo ufw default allow incoming
sudo ufw reload
```

完成测试后应立即恢复默认拒绝策略：

```bash
sudo ufw default deny incoming
sudo ufw allow OpenSSH
sudo ufw reload
```

> **高风险提醒**：`ufw disable` 或 `ufw default allow incoming` 会取消 Ubuntu 入站防护。只适用于本机 VMware NAT 隔离的测试虚拟机，不应在桥接网络、公司网络或公网服务器上使用。开放防火墙也不会自动启动服务；还需使用 `ss -lntup` 检查程序是否正在监听，并确保服务监听地址不是仅限 `127.0.0.1`。

检查当前监听端口：

```bash
sudo ss -lntup
```

例如服务显示为 `127.0.0.1:3000` 时，只能从 Ubuntu 本机访问；若需要从 Mac 连接，应用通常应监听 `0.0.0.0:3000` 或 Ubuntu 的虚拟机地址。具体监听地址应在应用自身配置中修改。

#### 2.5.5 从 Mac 连接 root 用户

正确的 SSH 命令只包含一个 `@`：

```bash
ssh root@192.168.230.10
```

以下写法是错误的：

```bash
ssh root@@192.168.230.10
```

`root@@192.168.230.10` 会将 SSH 用户名解析为 `root@`，而不是 `root`，因此即使密码正确也会提示 `Permission denied`。

首次连接时，确认主机指纹后输入 `yes`，然后输入前文设置的 `root` 密码。登录成功后可执行：

```bash
whoami
```

输出 `root` 即表示远程登录成功。

#### 2.5.6 使用完成后重新禁用

如果只是临时测试，建议完成后删除额外配置，并重新锁定 `root` 账户：

```bash
sudo rm /etc/ssh/sshd_config.d/00-root-login.conf
sudo sshd -t
sudo systemctl restart ssh
sudo passwd -l root
```

后续应改用普通用户登录：

```bash
ssh fly@192.168.230.10
```

需要管理员权限时，在登录后执行 `sudo <命令>` 或 `sudo -i`。

### 2.6 从 Mac 使用 Cursor 连接 Ubuntu 并配置免密登录

Cursor 的 Remote SSH 功能使用 Mac 本地 SSH 客户端连接 Ubuntu，然后在 Ubuntu 用户目录中安装 Cursor Server。本节按需求使用 `root` 用户连接，Cursor Server 和项目将以最高系统权限运行。

> **高风险提醒**：Cursor 扩展、终端命令、任务和项目脚本都将拥有 `root` 权限，误操作或恶意项目可以修改或删除整个 Ubuntu 系统。只应在本机 VMware NAT 隔离的测试虚拟机中使用，不要将 root SSH 暴露到桥接网络、不可信局域网或公网。

#### 2.6.1 准备 Ubuntu SSH 服务

在 Ubuntu 终端中执行：

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh.service
```

确认 SSH 服务和 22 端口正常：

```bash
systemctl status ssh.service --no-pager
sudo ss -lntp | grep ':22'
```

确认 `root` 账户状态和 Ubuntu 当前 IP：

```bash
sudo passwd -S root
ip -br address show enp2s0
```

本文以 Ubuntu 静态 IP `192.168.230.10` 和用户 `root` 为例。请先完成 2.4 和 2.5 小节，确保 `root` 已设置密码、SSH 服务已运行且 `PermitRootLogin` 已允许 root 登录。

#### 2.6.2 在 Mac 生成 Cursor 专用 SSH 密钥

以下命令必须在 **Mac 本地终端**中执行，不是在 Ubuntu 中执行：

```bash
ssh-keygen -t ed25519 \
  -f ~/.ssh/id_ed25519_ubuntu2404_cursor \
  -C "cursor@ubuntu2404"
```

生成两个文件：

| 文件 | 用途 |
| :--- | :--- |
| `~/.ssh/id_ed25519_ubuntu2404_cursor` | 私钥，只能保存在 Mac 本地，不得发送或上传 |
| `~/.ssh/id_ed25519_ubuntu2404_cursor.pub` | 公钥，需要添加到 Ubuntu |

建议为私钥设置 passphrase。macOS 可以将 passphrase 保存在钥匙串中，既保护私钥，又无需每次连接都重复输入。

设置本地文件权限：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519_ubuntu2404_cursor
chmod 644 ~/.ssh/id_ed25519_ubuntu2404_cursor.pub
```

#### 2.6.3 将 Mac 公钥添加到 Ubuntu

首次仍需要输入一次 Ubuntu `root` 用户密码。如 Mac 已安装 `ssh-copy-id`，执行：

```bash
ssh-copy-id \
  -i ~/.ssh/id_ed25519_ubuntu2404_cursor.pub \
  root@192.168.230.10
```

如 macOS 提示 `ssh-copy-id: command not found`，使用系统自带的 `ssh` 手动追加公钥：

```bash
cat ~/.ssh/id_ed25519_ubuntu2404_cursor.pub | \
  ssh root@192.168.230.10 \
  'umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys'
```

然后在 Ubuntu 中以 `root` 身份检查权限：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chown -R root:root /root/.ssh
```

> root 的公钥文件必须位于 `/root/.ssh/authorized_keys`，`.ssh` 目录权限应为 `700`，`authorized_keys` 应为 `600`，属主必须为 `root:root`。

#### 2.6.4 在 Mac 测试密钥登录

在 Mac 本地终端执行：

```bash
ssh \
  -i ~/.ssh/id_ed25519_ubuntu2404_cursor \
  -o IdentitiesOnly=yes \
  root@192.168.230.10
```

如能在不输入 Ubuntu 用户密码的情况下登录，说明公钥认证成功。如私钥设置了 passphrase，此时可能会询问私钥 passphrase，它不是 Ubuntu 用户密码。

将密钥加入 macOS `ssh-agent` 和钥匙串：

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_ubuntu2404_cursor
```

查看已加载的密钥：

```bash
ssh-add -l
```

#### 2.6.5 在 Mac 配置 SSH 主机别名

编辑 Mac 本地的 `~/.ssh/config`：

```bash
vim ~/.ssh/config
```

添加：

```sshconfig
Host ubuntu2404-cursor
  HostName 192.168.230.10
  User root
  Port 22
  IdentityFile ~/.ssh/id_ed25519_ubuntu2404_cursor
  IdentitiesOnly yes
  AddKeysToAgent yes
  UseKeychain yes
  ServerAliveInterval 60
  ServerAliveCountMax 3
  ForwardAgent no
```

设置配置文件权限：

```bash
chmod 600 ~/.ssh/config
```

使用别名测试：

```bash
ssh ubuntu2404-cursor
```

如有多个 SSH 主机配置，确保每个 `Host` 别名唯一。`HostName` 必须与 Ubuntu 当前实际 IP 一致。

#### 2.6.6 在 Cursor 中安装 Remote SSH 扩展

1. 在 Mac 上打开 Cursor。
2. 打开 Extensions（扩展）面板，搜索 `Anysphere Remote SSH` 或 `@id:anysphere.remote-ssh`。
3. 确认发布者为 **Anysphere**，安装 Cursor 自家的 Remote SSH 扩展。
4. 如已安装 Microsoft `ms-vscode-remote.remote-ssh` 且出现服务端下载、版本或路径冲突，卸载该扩展，保留 `anysphere.remote-ssh`，然后完全重启 Cursor。

也可在 Mac 终端中安装：

```bash
cursor --install-extension anysphere.remote-ssh
```

如提示 `cursor: command not found`，在 Cursor 命令面板中执行 `Shell Command: Install 'cursor' command in PATH`，或直接从扩展面板安装。

#### 2.6.7 从 Cursor 连接 Ubuntu

1. 在 Cursor 中按 `Command` + `Shift` + `P` 打开命令面板。
2. 执行 `Remote-SSH: Connect to Host...`。
3. 选择 `ubuntu2404-cursor`。
4. 如询问远端平台，选择 `Linux`。
5. 首次连接时，Cursor 会在 Ubuntu 的 `~/.cursor-server` 目录中下载和安装与 Mac 客户端版本匹配的 Cursor Server。
6. 连接成功后，选择 `File`→`Open Folder...`，打开 Ubuntu 中的项目目录，例如 `/root/projects`。

可在 Cursor 远端终端中执行以下命令确认当前身份和主机：

```bash
whoami
hostname
pwd
```

预期 `whoami` 输出 `root`。

#### 2.6.8 Cursor Server 下载与代理注意事项

Cursor Remote SSH 首次连接及 Cursor 客户端升级后，远端 Ubuntu 可能需要重新下载与当前 commit 匹配的 Cursor Server。官方 Remote SSH 扩展目前要求远端主机具备网络访问能力，不支持由扩展自动通过 SCP 复制服务端二进制文件。

在 Ubuntu 中先验证网络：

```bash
curl -I https://cursor.com
```

如 Ubuntu 需要使用 v2rayA，确保 `root` 用户的 `/root/.bashrc` 或 `/root/.profile` 已按前文步骤配置代理，并且通过 SSH 登录后执行以下命令也能成功：

```bash
ssh ubuntu2404-cursor 'curl -I https://cursor.com'
```

每个 Cursor 客户端 commit 的远端服务端通常保存在 `~/.cursor-server/bin/<commit>/`。如磁盘空间不足，可检查：

```bash
du -sh ~/.cursor-server 2>/dev/null
df -h ~
```

不要在 Cursor 正在连接时删除当前使用的 commit 目录。

#### 2.6.9 常见问题

| 现象 | 常见原因 | 处理方法 |
| :--- | :--- | :--- |
| Mac 终端仍要求 Ubuntu 用户密码 | 公钥未写入、权限错误或使用了其他私钥 | 使用 `ssh -v ubuntu2404-cursor` 查看密钥认证过程，检查 `.ssh` 和 `authorized_keys` 权限 |
| `Permission denied (publickey)` | `IdentityFile` 错误、Ubuntu 公钥缺失、root SSH 未启用或 `.ssh` 属主错误 | 检查 `PermitRootLogin`，重新复制公钥并执行 `chown -R root:root /root/.ssh` |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | 虚拟机重安装、重新生成 SSH 主机密钥，或相同 IP 指向了其他主机 | 先在 Ubuntu 控制台确认主机身份，再在 Mac 执行 `ssh-keygen -R 192.168.230.10` |
| Cursor 可以 SSH 认证但 Cursor Server 安装失败 | Ubuntu 无法访问 Cursor 下载服务、代理未对远端会话生效或磁盘空间不足 | 测试 `ssh ubuntu2404-cursor 'curl -I https://cursor.com'`，检查 `~/.cursor-server` 和 `df -h` |
| Cursor 连接后经常断开 | Ubuntu IP 变化、VMware NAT 网卡重连或 SSH 空闲超时 | 使用静态 IP，保留 `ServerAliveInterval` 和 `ServerAliveCountMax` |
| Cursor 报错提到 SOCKS/port forwarding | Ubuntu SSH 服务禁止 TCP 转发 | 执行 `sudo sshd -T | grep allowtcpforwarding`，应显示 `allowtcpforwarding yes` |

查看 Cursor Remote SSH 日志：在 Cursor 中打开 `View`→`Output`，然后在输出面板的下拉列表中选择 `Remote - SSH`。

### 2.7 从 Mac 使用 Codex 连接 Ubuntu

Codex 支持通过 SSH 直接打开 Ubuntu 中的项目。连接后，Codex 读取和修改的是 Ubuntu 上的文件，命令也在 Ubuntu 的 Shell 中执行，并不是先把项目复制到 Mac 再同步回虚拟机。

本节沿用前文的静态 IP `192.168.230.10`、root 用户和 SSH 密钥。官方建议远程连接使用最小权限账户；root 具有完整系统权限，仅应在可信的本机 NAT 虚拟机中使用。生产服务器建议改用普通用户，并按需执行 `sudo`。

#### 2.7.1 准备条件

开始前确认：

1. Ubuntu 虚拟机已经启动，网络适配器选择 VMware Fusion 的 `Share with my Mac`（NAT）。
2. 已完成 2.5 和 2.6 节中的 SSH 服务、root 密钥登录及 Mac SSH 主机别名配置。
3. Mac 已安装最新版 Codex/ChatGPT 桌面端，并已登录具有 Codex 权限的 ChatGPT 账户。
4. Ubuntu 可以访问 Codex 所需网络；如需代理，可参考第 5 节配置。

先在 Mac 终端确认 SSH 连接可用：

```bash
ssh ubuntu2404-cursor
```

也可以为 Codex 单独定义一个更直观的别名。在 Mac 上编辑 `~/.ssh/config`：

```sshconfig
Host ubuntu2404-codex
  HostName 192.168.230.10
  User root
  Port 22
  IdentityFile ~/.ssh/id_ed25519_cursor_ubuntu2404
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

保存后测试：

```bash
ssh ubuntu2404-codex
```

> Codex 会从 Mac 的 `~/.ssh/config` 中读取具体的 `Host` 别名。应先保证 `ssh ubuntu2404-cursor` 能免密连接，再在 Codex 中添加主机。只有通配符的 `Host *` 不会作为可选择的远程主机出现。

#### 2.7.2 在 Ubuntu 安装 Codex CLI

Codex 桌面端通过 SSH 启动远程 Codex app server，因此 Ubuntu 登录 Shell 中必须能直接找到 `codex` 命令。

先连接 Ubuntu，并检查 Node.js 和 npm：

```bash
ssh ubuntu2404-cursor
node -v
npm -v
```

如果提示命令不存在，先按第 7 节安装 Node.js 和 npm。当前使用 root 连接时，NVM 和 Node.js 也必须安装在 root 的家目录 `/root` 下；安装在普通用户目录中的 `node` 不会自动提供给 root。

安装最新版 Codex CLI：

```bash
npm install -g @openai/codex
```

检查命令及版本：

```bash
command -v codex
codex --version
```

如果交互式 SSH 中能找到 `codex`，但 Codex App 仍提示找不到命令，通常是 NVM 只在交互式 Shell 中加载。可先查看实际路径：

```bash
command -v node
command -v codex
bash -lc 'command -v codex && codex --version'
```

确保 `/root/.bashrc` 中存在 NVM 的加载配置：

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
```

然后重新建立 SSH 连接。也可以将 Node.js 安装到系统级路径，但不要直接复制 NVM 目录中的可执行文件。

#### 2.7.3 在 Ubuntu 完成 Codex 登录认证（可跳过，可从桌面端远程登录）

远程 Ubuntu 需要独立完成 Codex 登录。对于没有图形浏览器的 SSH 会话，优先使用设备码登录：

```bash
codex login --device-auth
```

终端会显示登录地址和一次性代码。在 Mac 浏览器中打开该地址，登录 ChatGPT 并输入代码。完成后检查状态：

```bash
codex login status
```

如果设备码选项不可用，可先在 ChatGPT 账户安全设置或工作区权限中启用设备码登录。还可以使用 OpenAI API Key 按量计费登录：

```bash
export OPENAI_API_KEY='替换为自己的_API_Key'
printenv OPENAI_API_KEY | codex login --with-api-key
unset OPENAI_API_KEY
```

不要把 API Key 写进文档、Git 仓库或 Shell 历史。认证缓存可能保存在 `~/.codex/auth.json`，应将其视为密码，不要共享或提交到 Git。

如果 Ubuntu 无法打开登录或模型服务，先参考第 5 节设置代理，再测试：

```bash
curl -I https://chatgpt.com
curl -I https://api.openai.com
```

#### 2.7.4 在 Mac Codex App 中添加 Ubuntu

1. 完全退出并重新打开最新版 Codex/ChatGPT 桌面端。

2. 打开 `Settings`（设置）→`Connections`（连接）→`SSH`。

3. 点击 `Add`，选择自动发现的 `ubuntu2404-cursor`。

   ![image-20260712062016336](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260712062016336.png)

4. 连接成功后（连接时候会让你跳转到浏览器登录），选择 Ubuntu 上的项目目录，例如 `/root/projects/demo`。

   ![image-20260712062242423](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260712062242423.png)

   ![image-20260712062307484](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260712062307484.png)

5. 创建任务，并先让 Codex 执行只读检查，例如“列出当前目录并说明项目结构”。

连接成功后可在任务中验证实际执行位置：

```bash
hostname
whoami
pwd
```

预期 `whoami` 输出 `root`，`pwd` 指向 Ubuntu 中选择的项目目录。此后 Codex 的文件读写、测试和终端命令均发生在 Ubuntu 虚拟机中。

> 新版官方文档已经直接提供 `Settings`→`Connections`→`SSH`。社区早期版本曾要求在 Mac 的 `~/.codex/config.toml` 中手工开启 `remote_connections` 等实验开关；最新版通常不需要添加这些旧版 feature flag。只有更新并重启应用后仍没有 SSH 入口时，才应结合当前版本说明排查，不要直接照搬旧配置。

#### 2.7.5 备用方式：通过 SSH 直接运行 Codex CLI

如果桌面端暂时没有 SSH 入口，或远程连接功能不稳定，可以在 Mac 终端直接进入 Ubuntu 后运行 Codex：

```bash
ssh ubuntu2404-cursor
cd /root/projects/demo
codex
```

首次进入项目时先确认目录和 Git 状态，再授权写入或执行操作。长时间任务建议在 Ubuntu 中使用 `tmux`，避免 Mac 终端关闭或 SSH 短暂断线导致前台会话丢失：

```bash
sudo apt update
sudo apt install -y tmux
tmux new -s codex
cd /root/projects/demo
codex
```

断线后重新连接并恢复会话：

```bash
ssh ubuntu2404-cursor
tmux attach -t codex
```

#### 2.7.6 常见问题

1. **Codex 中没有显示 Ubuntu 主机**：确认 `~/.ssh/config` 中存在具体的 `Host ubuntu2404-cursor`，且 Mac 终端可直接执行 `ssh ubuntu2404-cursor`；随后完全退出并重启桌面端。
2. **提示 `codex: command not found`**：在 Ubuntu 执行 `bash -lc 'command -v codex'`。若无输出，检查 Node/NVM 是否安装在当前远程用户的家目录，以及登录 Shell 是否加载 NVM。
3. **认证失败或一直等待浏览器回调**：远程无桌面环境时改用 `codex login --device-auth`，并确认 Ubuntu 的系统时间和网络代理正常。
4. **SSH 能连接但 Codex 连接失败**：检查 SSH 是否仍在要求密码、私钥权限是否为 `600`、Ubuntu 是否能运行 `codex --version`，以及 Mac 和 Ubuntu 是否都能访问所需服务。
5. **连接一段时间后断开**：保持虚拟机运行，禁止 Mac 睡眠，并保留 SSH 配置中的 `ServerAliveInterval`。CLI 长任务使用 `tmux`。
6. **root 创建的文件导致普通用户无法修改**：将项目改由普通用户管理，或谨慎执行 `chown -R 用户名:用户名 项目目录`。不要对系统目录递归修改属主。

## 3. 网络配置（静态 IP 设置）

![image-20260710230944216](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710230944216.png)

当前 VMware Fusion 网络适配器使用 `Share with my Mac`，即 NAT 模式。NAT 模式也可以设置静态 IP，不需要切换为桥接模式。

```bash
fly@ubuntu2404:~$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:23:ba:bd brd ff:ff:ff:ff:ff:ff
    inet 192.168.230.131/24 brd 192.168.230.255 scope global dynamic noprefixroute enp2s0
       valid_lft 1743sec preferred_lft 1743sec
    inet6 fe80::20c:29ff:fe23:babd/64 scope link
       valid_lft forever preferred_lft forever
```

从当前输出可知，虚拟网卡为 `enp2s0`，DHCP 分配的地址为 `192.168.230.131/24`：

```text
inet 192.168.230.131/24 scope global dynamic noprefixroute enp2s0
```

其中 `dynamic` 表示该地址由 VMware DHCP 动态分配，租约到期或虚拟机重启后可能变化。

### 3.1 确认当前 NAT 网络参数

本机 VMware Fusion 的 NAT 网络参数如下：

| 配置项 | 当前值 | 说明 |
| :--- | :--- | :--- |
| NAT 网段 | `192.168.230.0/24` | 虚拟机应使用 `192.168.230.x` 地址 |
| 子网掩码 | `255.255.255.0` | 对应 `/24` |
| NAT 网关 | `192.168.230.2` | Ubuntu 的默认网关 |
| DNS | `192.168.230.2` | 由 VMware NAT 转发 DNS 请求 |
| Mac 主机地址 | `192.168.230.1` | Mac 在 `vmnet8` 虚拟网络中的地址 |
| DHCP 地址池 | `192.168.230.128`–`192.168.230.254` | 不要手动固定使用该范围内的地址 |

> 当前的 `192.168.230.131` 位于 DHCP 地址池内。如果直接将它设为静态 IP，VMware DHCP 仍可能把该地址分配给其他虚拟机，从而造成 IP 冲突。因此下文选择 DHCP 地址池之外的 `192.168.230.10` 作为静态 IP，同时避开 VMware 已占用的 `.1` 和 `.2`。

如果 VMware Fusion 重置过虚拟网络，NAT 网段可能变化。可先在 Ubuntu 中执行以下命令确认当前网关：

```bash
ip route
```

当前环境应能看到类似输出：

```text
default via 192.168.230.2 dev enp2s0
```

### 3.2 在 Ubuntu Desktop 中设置 NAT 静态 IP

1. 点击 Ubuntu 桌面右上角的系统菜单，打开`设置`（Settings）。
2. 在左侧选择`网络`（Network），找到`有线`（Wired），点击右侧的齿轮按钮。
3. 打开 `IPv4` 选项卡，将 IPv4 Method 从 `Automatic (DHCP)` 改为 `Manual`。
4. 在 Addresses 区域填写：

   | 输入项 | 填写值 |
   | :--- | :--- |
   | Address | `192.168.230.10` |
   | Netmask | `255.255.255.0` |
   | Gateway | `192.168.230.2` |

5. 关闭 `Automatic DNS`，在 DNS 输入框中填写 `192.168.230.2`。如需备用 DNS，可填写 `192.168.230.2, 223.5.5.5`。
6. 保持 Routes 为默认设置，点击 `Apply`保存。
7. 返回网络设置页，关闭后再开启`有线`开关；如果地址没有更新，重启 Ubuntu。

### 3.3 通过命令行设置 NAT 静态 IP

Ubuntu Desktop 24.04 默认使用 NetworkManager 管理网络，可使用 `nmcli` 完成与图形界面相同的配置。图形界面和命令行两种方法选择其一即可，无需重复设置。

1. 确认网卡状态和 NetworkManager 连接名称：

   ```bash
   nmcli device status
   nmcli connection show --active
   ```

   输出信息

   ```bash
   fly@ubuntu2404:~$ nmcli device status
   DEVICE  TYPE      STATE                   CONNECTION
   enp2s0  ethernet  connected               netplan-enp2s0
   lo      loopback  connected (externally)  lo
   fly@ubuntu2404:~$ nmcli connection show --active
   NAME            UUID                                  TYPE      DEVICE
   netplan-enp2s0  7ea6f90b-3495-3533-948a-ef0035687c34  ethernet  enp2s0
   lo              76c59068-8e98-4228-9319-b3ad1069b501  loopback  lo
   fly@ubuntu2404:~$
   ```

   找到设备为 `enp2s0` 的连接。连接名通常为 `Wired connection 1` 或 `netplan-enp2s0`，实际名称以命令输出为准。

2. 将 `enp2s0` 当前使用的连接名保存到变量，并显示出来确认：

   ```bash
   CONNECTION="$(nmcli -g GENERAL.CONNECTION device show enp2s0)"
   echo "$CONNECTION"
   ```

   如果输出为 `--`、空白或不是预期的有线连接，请先停止操作，重新通过 `nmcli connection show --active` 确认连接名。

3. 将该连接改为手动 IPv4，配置静态 IP、网关和 DNS：

   ```bash
   sudo nmcli connection modify "$CONNECTION" \
     ipv4.method manual \
     ipv4.addresses 192.168.230.10/24 \
     ipv4.gateway 192.168.230.2 \
     ipv4.dns "192.168.230.2,223.5.5.5" \
     ipv4.ignore-auto-dns yes
   ```

4. 重新激活网络连接，使配置生效：

   ```bash
   sudo nmcli connection down "$CONNECTION"
   sudo nmcli connection up "$CONNECTION"
   ```

   执行 `down` 后网络会短暂中断。请直接在 VMware Fusion 的 Ubuntu 终端中执行，不要在 SSH 会话中操作，否则 SSH 会立即断开。

5. 查看 NetworkManager 中已保存的 IPv4 配置：

   ```bash
   nmcli connection show "$CONNECTION" | grep -E '^ipv4\.(method|addresses|gateway|dns)'
   ```


![image-20260710232306831](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710232306831.png)

如果静态 IP 填写错误导致无法联网，可在 Ubuntu 本地终端中执行以下命令恢复 DHCP：

```bash
CONNECTION="$(nmcli -g GENERAL.CONNECTION device show enp2s0)"
sudo nmcli connection modify "$CONNECTION" \
  ipv4.method auto \
  ipv4.addresses "" \
  ipv4.gateway "" \
  ipv4.dns "" \
  ipv4.ignore-auto-dns no
sudo nmcli connection down "$CONNECTION"
sudo nmcli connection up "$CONNECTION"
```

### 3.4 验证静态 IP 是否生效

在 Ubuntu 终端中执行：

```bash
ip -br address show enp2s0
ip route
ping -c 4 192.168.230.2
ping -c 4 1.1.1.1
ping -c 4 ubuntu.com
```

正常情况下：

- `enp2s0` 显示 `192.168.230.10/24`。
- 默认路由显示 `default via 192.168.230.2`。
- 能够 ping 通网关、外网 IP 和域名。

然后在 Mac 终端中测试连接：

```bash
ping 192.168.230.10
ssh fly@192.168.230.10
```

如果 ping 正常但 SSH 提示 `Connection refused`，说明网络已连通，但 Ubuntu 尚未启动 SSH 服务。执行：

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

### 3.5 NAT 模式的访问范围

NAT 模式适合 Ubuntu 访问互联网，也适合 Mac 主机通过 `192.168.230.10` 访问虚拟机。但该地址只存在于 Mac 内部的 `vmnet8` 虚拟网络中，局域网内的其他物理设备通常无法直接访问它。

- 只需要从当前 Mac 上 SSH 连接 Ubuntu：使用 NAT 即可。
- 需要让同一局域网中的其他设备直接访问 Ubuntu：使用桥接模式，或在 VMware NAT 中额外配置端口转发。

## 4. 配置 Git 用户信息与 SSH 密钥

在 Ubuntu 24.04 中使用 Git 提交代码前，需要配置提交者的用户名和邮箱。如果通过 GitHub、GitLab 或 Gitee 管理远程仓库，建议使用 SSH 密钥进行身份认证。

### 4.1 安装 Git 和 SSH 客户端

打开 Ubuntu 终端并执行：

```bash
sudo apt update
sudo apt install -y git openssh-client
```

检查安装结果：

```bash
git --version
ssh -V
```

### 4.2 配置 Git 用户名和邮箱

Git 会将 `user.name` 和 `user.email` 写入每一次提交的作者与提交者信息。使用 `--global` 配置后，设置会对当前 Ubuntu 用户的所有 Git 仓库生效。

通用命令格式：

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱地址"
```

示例：

```bash
git config --global user.name "FlyAIBox"
git config --global user.email "fly910905@sina.com"
```

> Git 提交用户名不必与 Ubuntu 登录用户名一致。邮箱建议使用 GitHub、GitLab 或 Gitee 账户中已验证的邮箱；如果不希望公开真实邮箱，可使用平台提供的隐私邮箱。

查看已生效的配置：

```bash
git config --global user.name
git config --global user.email
git config --global --list
```

如果某个项目需要使用不同的用户名或邮箱，进入该仓库目录后去掉 `--global` 单独配置：

```bash
git config user.name "项目专用用户名"
git config user.email "项目专用邮箱"
```

### 4.3 检查现有 SSH 密钥

查看 `~/.ssh` 目录：

```bash
ls -al ~/.ssh
```

如果同时存在以下某组文件，说明可能已生成过 SSH 密钥：

```text
id_ed25519
id_ed25519.pub
```

或：

```text
id_rsa
id_rsa.pub
```

其中 `.pub` 结尾的文件是可以上传到 Git 平台的公钥；不带 `.pub` 后缀的是私钥，必须严格保密，不得发送给他人或上传到仓库。

### 4.4 生成 Ed25519 SSH 密钥

如果尚未生成密钥，推荐使用 Ed25519 算法：

```bash
ssh-keygen -t ed25519 -C "fly910905@sina.com"
```

根据提示操作：

1. 出现 `Enter file in which to save the key` 时，直接按回车键，使用默认路径 `~/.ssh/id_ed25519`。
2. 出现 `Enter passphrase` 时，建议设置一个密钥口令，以防私钥文件泄露后被直接使用。
3. 再次输入口令进行确认。

如果目标平台不支持 Ed25519，可改用 4096 位 RSA：

```bash
ssh-keygen -t rsa -b 4096 -C "fly910905@sina.com"
```

生成后检查文件权限：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### 4.5 将密钥加入 ssh-agent

启动 `ssh-agent` 并加载私钥：

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

输入生成密钥时设置的 passphrase，然后查看已加载的密钥：

```bash
ssh-add -l
```

### 4.6 复制并添加 SSH 公钥

直接在终端显示公钥：

```bash
cat ~/.ssh/id_ed25519.pub
```

复制从 `ssh-ed25519` 开始到邮箱结束的整行内容。

将公钥添加到对应平台：

- **GitHub**：登录后点击右上角头像→`Settings`→`SSH and GPG keys`→`New SSH key`，输入便于识别的 Title，Key type 选择 `Authentication Key`，粘贴公钥并保存。
- **GitLab**：进入个人账户的 SSH Keys 设置页，粘贴公钥，填写 Title 后保存。
- **Gitee**：进入个人设置中的`SSH 公钥`页面，填写标题、粘贴公钥并保存。

### 4.7 测试 SSH 连接

根据使用的远程平台执行：

```bash
# GitHub
ssh -T git@github.com

# GitLab
ssh -T git@gitlab.com

# Gitee
ssh -T git@gitee.com
```

首次连接时会提示确认远程主机指纹。请先与对应平台公布的 SSH 指纹核对，确认一致后再输入 `yes`。

GitHub 连接成功时会看到类似信息：

```text
Hi FlyAIBox! You've successfully authenticated, but GitHub does not provide shell access.
```

GitHub 不提供普通 Shell，因此即使认证成功，`ssh -T` 也可能返回非零退出码，这不表示配置失败。

### 4.8 GitHub 22 端口被拦截时改用 443 端口

如果执行 `ssh -T git@github.com` 后出现以下错误，通常表示当前网络的防火墙、网关或代理限制了 SSH 默认的 22 端口：

```text
kex_exchange_identification: Connection closed by remote host
Connection closed by xxx.xxx.xxx.xxx port 22
```

先直接测试 GitHub 的 SSH 443 端口：

```bash
ssh -T -p 443 git@ssh.github.com
```

如果该命令能正常认证，创建或编辑 SSH 客户端配置：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/config
```

在文件中添加：

```sshconfig
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

保存后设置配置文件权限：

```bash
chmod 600 ~/.ssh/config
```

再次使用原命令测试：

```bash
ssh -T git@github.com
```

配置生效后，使用 `git@github.com:用户名/仓库名.git` 形式的 `clone`、`pull` 和 `push` 会自动改走 `ssh.github.com:443`。

### 4.9 验证仓库访问

使用 SSH 地址克隆仓库：

```bash
git clone git@github.com:用户名/仓库名.git
```

已经通过 HTTPS 克隆的仓库可将远程地址改为 SSH：

```bash
cd 仓库目录
git remote -v
git remote set-url origin git@github.com:用户名/仓库名.git
git remote -v
```

### 4.10 删除 Git 用户信息和 SSH 密钥

删除全局 Git 用户名和邮箱：

```bash
git config --global --unset user.name
git config --global --unset user.email
```

删除前先查看现有密钥：

```bash
ls -al ~/.ssh
```

确认文件名无误后，从 `ssh-agent` 卸载密钥并删除对应文件：

```bash
ssh-add -d ~/.ssh/id_ed25519
rm ~/.ssh/id_ed25519
rm ~/.ssh/id_ed25519.pub
```

> 删除私钥后，如果没有备份，将无法再使用该密钥进行身份认证。删除前必须确认它不再被任何仓库、服务器或账户使用，并在 GitHub、GitLab 或 Gitee 的账户设置中删除对应公钥记录。

如需取消 GitHub 443 端口配置，编辑 `~/.ssh/config`，删除 `Host github.com` 对应的整个配置块。

## 5. 配置 v2rayA 代理

v2rayA 是面向 Linux 的 V2Ray/Xray 图形化管理工具，通过 Web UI 管理连接、路由和代理模式。请仅在符合所在地法律法规、网络管理规定和服务条款的前提下使用。

> 当前 Ubuntu 虚拟机运行在 Apple Silicon 上，系统架构为 ARM64。不要使用文件名包含 `x64`、`amd64` 或 `linux-64` 的手动安装包。使用官方 APT 软件源可自动选择正确的 ARM64 软件包。

### 5.1 确认 Ubuntu 系统架构

执行：

```bash
dpkg --print-architecture
uname -m
```

当前环境应分别输出 `arm64` 和 `aarch64`。

### 5.2 从官方 GitHub Release 离线安装（当前推荐）

当前执行 `sudo apt update` 时，v2rayA APT 软件源可能报以下错误：

```text
EXPKEYSIG 354E516D494EF95F mzz2017 (apt) <mzz@tuta.io>
The repository 'https://apt.v2raya.org v2raya InRelease' is not signed.
```

这表示用于签署软件源的 GPG 密钥已过期，APT 因无法验证软件包来源而安全地禁用该仓库。随后出现 `Unable to locate package v2raya` 是软件源索引未成功更新的结果。

> 不要使用 `trusted=yes`、`--allow-unauthenticated` 或关闭 APT 签名验证来绕过报错。在官方更新 APT 签名密钥前，建议改用 GitHub Release 中提供校验值的 ARM64 `.deb` 文件。

#### 5.2.1 清理失效的 v2rayA APT 软件源

如果已按旧步骤添加该软件源，先删除软件源列表和专用密钥，避免以后每次 `apt update` 都报错：

```bash
sudo rm -f /etc/apt/sources.list.d/v2raya.list
sudo rm -f /etc/apt/keyrings/v2raya.asc
sudo apt update
```

这只会删除 v2rayA 的第三方软件源配置，不会删除 Ubuntu 自带软件源或已安装的其他软件。

#### 5.2.2 下载官方 ARM64 离线安装包

截至 2026 年 7 月 11 日，v2rayA 官方 GitHub 最新 Release 为 `v2.4.6`，对应 Ubuntu/Debian ARM64 安装包为 `installer_debian_arm64_2.4.6.deb`。

1. 打开 v2rayA 官方 Releases 页面，确认当前最新版本：

   ```text
   https://github.com/v2rayA/v2rayA/releases/latest
   ```

2. 安装下载和校验工具：

   ```bash
   sudo apt update
   sudo apt install -y ca-certificates wget coreutils
   ```

3. 以 `v2.4.6` 为例，下载 ARM64 Debian 安装包和官方 SHA-256 文件：

   ```bash
   VERSION=2.4.6
   wget "https://github.com/v2rayA/v2rayA/releases/download/v${VERSION}/installer_debian_arm64_${VERSION}.deb"
   wget "https://github.com/v2rayA/v2rayA/releases/download/v${VERSION}/installer_debian_arm64_${VERSION}.deb.sha256.txt"
   ```

4. 校验文件完整性：

   ```bash
   echo "$(cat "installer_debian_arm64_${VERSION}.deb.sha256.txt")  installer_debian_arm64_${VERSION}.deb" | \
     sha256sum -c -
   ```

   只有输出 `OK` 时才继续安装。官方发布页公布的 `2.4.6` ARM64 `.deb` SHA-256 为：

   ```text
   c02f0b61339bb75d6fd0f65e172d4ccb964e795286b2ed47600917e4a0a7db72
   ```

5. 使用 APT 安装本地 `.deb`，以便自动检查和处理依赖：

   ```bash
   sudo apt install "./installer_debian_arm64_${VERSION}.deb"
   ```

6. 检查安装结果：

   ```bash
   dpkg-query -W -f='${Package} ${Version} ${Architecture}\n' v2raya
   command -v v2raya
   command -v v2raya_core
   file "$(command -v v2raya)"
   file "$(command -v v2raya_core)"
   systemctl cat v2raya.service
   ```

已对官方 `installer_debian_arm64_2.4.6.deb` 进行解包核对，该安装包已包含：

```text
/usr/bin/v2raya
/usr/bin/v2raya_core
/usr/share/v2raya/geoip.dat
/usr/share/v2raya/geosite.dat
/usr/lib/systemd/system/v2raya.service
```

因此使用 `v2.4.6` ARM64 `.deb` 时无需再从签名已过期的 APT 软件源单独安装 `v2ray` 或手动下载 `geoip.dat`/`geosite.dat`。

> 版本号会随官方发布而变化。如 Releases 页面已不是 `v2.4.6`，应同时替换 `VERSION`、安装包名和校验文件，不要将新版本文件与旧版本校验值混用。

### 5.3 启动服务并设置开机自启

从 v2rayA 1.5 开始，安装后不一定默认启动服务或设置开机自启。执行：

```bash
sudo systemctl enable --now v2raya.service
```

检查运行状态：

```bash
systemctl status v2raya.service --no-pager
```

输出中应显示 `active (running)`。如启动失败，查看最近日志：

```bash
journalctl -u v2raya.service -n 100 --no-pager
```

### 5.4 打开 Web UI 并创建管理账户

在 Ubuntu 的浏览器中访问：

```text
http://127.0.0.1:2017
```

首次打开时，按页面提示创建 v2rayA 管理员用户名和高强度密码。该账户只用于登录 v2rayA Web UI，与 Ubuntu 用户和 `root` 密码无关。

如果忘记 Web UI 密码，执行：

```bash
sudo v2raya --reset-password
sudo systemctl restart v2raya.service
```

> 默认情况下建议只从 Ubuntu 虚拟机内访问 Web UI，不要将 2017 端口映射到公网。

### 5.5 导入连接配置并启动服务

1. 登录 Web UI，使用“导入”或“创建”功能添加已合法获取且信任的连接配置。
2. 导入完成后，在 `SERVER` 或对应标签中选择需要使用的服务器。
3. 如有需要，先执行延迟或可用性测试。不建议一次连接过多节点。
4. 点击左上角的启动按钮。连接状态变为蓝色后，表示代理核心已启动。

![image-20260711102810146](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260711102810146.png)

### 5.6 选择代理模式

v2rayA 默认通过核心提供以下本地端口：

| 端口 | 协议 | 用途 |
| :--- | :--- | :--- |
| `20170` | SOCKS5 | 供支持 SOCKS5 的应用使用 |
| `20171` | HTTP | 普通 HTTP 代理 |
| `20172` | HTTP | 使用 v2rayA 分流规则的 HTTP 代理 |

可根据实际需求选择以下一种方式。

#### 5.6.1 透明代理

在 Web UI 的`设置`中配置透明代理的分流方式和实现方式，保存后启动服务。透明代理可覆盖大多数不主动支持 HTTP/SOCKS 代理的应用，但会修改系统的 nftables/iptables 路由规则。

首次使用时建议保持默认规则，不要同时手动修改系统路由和防火墙。如使用需要规则库的分流模式，先在 Web UI 右上角更新规则库。

#### 5.6.2 Ubuntu 系统代理

如果不需要透明代理，可在 Ubuntu 中打开`设置`→`网络`→`网络代理`，将模式设为`手动`，填写：

| 配置项 | 主机 | 端口 |
| :--- | :--- | :--- |
| HTTP 代理 | `127.0.0.1` | `20171` |
| HTTPS 代理 | `127.0.0.1` | `20171` |
| SOCKS 主机 | `127.0.0.1` | `20170` |

系统代理只对主动读取桌面代理设置的应用生效，部分命令行程序仍需要单独配置。

#### 5.6.3 临时为命令行设置代理

仅对当前终端会话生效：

```bash
export http_proxy=http://127.0.0.1:20171
export https_proxy=http://127.0.0.1:20171
export all_proxy=socks5h://127.0.0.1:20170
```

取消当前终端的代理环境变量：

```bash
unset http_proxy https_proxy all_proxy
```

> 如同时设置 HTTP 和 SOCKS 代理，具体使用哪个取决于应用程序。排查问题时建议每次只测试一种代理方式。

#### 5.6.4 为命令行永久设置代理

如希望每次打开 Bash 终端时都自动设置代理，可将环境变量写入当前用户的 `~/.bashrc`：

```bash
cat >> ~/.bashrc <<'EOF'

# v2rayA proxy start
export http_proxy="http://127.0.0.1:20171"
export https_proxy="http://127.0.0.1:20171"
export all_proxy="socks5h://127.0.0.1:20170"
export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$https_proxy"
export ALL_PROXY="$all_proxy"
export no_proxy="localhost,127.0.0.1,::1"
export NO_PROXY="$no_proxy"
# v2rayA proxy end
EOF
```

使配置立即对当前终端生效：

```bash
source ~/.bashrc
```

检查已加载的代理环境变量：

```bash
env | grep -iE '^(http|https|all|no)_proxy='
```

验证 HTTP 代理：

```bash
curl -I https://github.com
```

> 上述配置只对写入配置的当前 Linux 用户生效。在 `fly` 用户中修改 `~/.bashrc` 不会影响 `root`，反之亦然。如果常用普通用户开发，应在普通用户中进行配置，不要只写入 `/root/.bashrc`。

如使用 Zsh，将上述内容写入 `~/.zshrc`，并执行 `source ~/.zshrc`。

永久取消该代理配置：

```bash
sed -i '/# v2rayA proxy start/,/# v2rayA proxy end/d' ~/.bashrc
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY no_proxy NO_PROXY
```

如配置在 `~/.zshrc`，将上述命令中的 `~/.bashrc` 替换为 `~/.zshrc`。

> 终端代理环境变量不会自动传递给 Docker daemon 或其他 systemd 系统服务，APT 也可能需要独立的 `Acquire::http::Proxy`/`Acquire::https::Proxy` 配置。这些情况应按各工具的专用配置方式处理。

### 5.7 验证代理连接

确认端口已监听：

```bash
sudo ss -lntp | grep -E ':2017|:20170|:20171|:20172'
```

直接测试 HTTP 代理：

```bash
curl -I --proxy http://127.0.0.1:20171 https://github.com
```

测试 SOCKS5 代理：

```bash
curl -I --proxy socks5h://127.0.0.1:20170 https://github.com
```

如果返回 HTTP 响应头，说明本地代理端口可用。还应确认目标网站允许当前访问，不要将单个网站的访问失败直接判定为 v2rayA 故障。

### 5.8 处理 `geoip.dat` 或 `geosite.dat` 缺失

如果 v2rayA 提示：

```text
failed to start v2ray-core: geoip.dat or geosite.dat file does not exist
```

先查看 v2rayA 离线安装包已安装的核心和数据文件：

```bash
dpkg -L v2raya | grep -E '(/v2raya_core$|/(geoip|geosite)\.dat$)'
```

正常应包含：

```text
/usr/bin/v2raya_core
/usr/share/v2raya/geoip.dat
/usr/share/v2raya/geosite.dat
```

如果文件缺失，回到 5.2.2 小节重新下载并校验官方 ARM64 `.deb`，然后使用本地安装包重新安装：

```bash
VERSION=2.4.6
sudo apt install --reinstall "./installer_debian_arm64_${VERSION}.deb"
sudo systemctl restart v2raya.service
```

再次检查：

```bash
dpkg -L v2raya | grep -E '(/v2raya_core$|/(geoip|geosite)\.dat$)'
systemctl status v2raya.service --no-pager
journalctl -u v2raya.service -n 100 --no-pager
```

如数据文件已存在但仍然报错，检查 v2rayA 是否被手动配置为使用另一个 V2Ray/Xray 二进制文件：

```bash
systemctl cat v2raya.service
systemctl show v2raya.service -p Environment
```

不要将 ARM64 环境的 `/usr/bin/v2raya_core` 替换为附件旧步骤中的 `v2ray-linux-64.zip`，该文件为 x86_64 架构，无法在当前虚拟机中正常运行。

### 5.9 常用服务管理命令

```bash
# 查看状态
systemctl status v2raya.service --no-pager

# 重启服务
sudo systemctl restart v2raya.service

# 停止服务
sudo systemctl stop v2raya.service

# 禁用开机自启
sudo systemctl disable v2raya.service

# 重新启用并立即启动
sudo systemctl enable --now v2raya.service

# 查看实时日志
journalctl -u v2raya.service -f
```

### 5.10 局域网共享的安全提醒

如确实需要让 Mac 或局域网内其他设备使用 Ubuntu 中的代理，需要在 v2rayA 设置中开启“局域网共享”，并使用 Ubuntu 的 IP（如 `192.168.230.10`）和对应代理端口。

但开启共享前必须注意：

- NAT 模式下通常只有 Mac 主机可直接访问该虚拟网段，其他物理设备默认无法访问。
- HTTP/SOCKS 入站不适合直接暴露到公网或不可信网络。
- 不要在路由器或 VMware NAT 中将 `2017`、`20170`、`20171` 或 `20172` 端口转发到公网。
- 如已启用 UFW，只允许确实需要的来源 IP 访问指定代理端口，不要对所有地址放行。

## 6. 安装 Docker Engine 和 Docker Compose

本节使用 Docker 官方 APT 软件源安装 Docker Engine、Buildx 和 Compose 插件。Docker 官方软件源支持 Ubuntu 24.04 `noble` 和 ARM64 架构。

### 6.1 卸载可能冲突的软件包

如果从 Ubuntu 软件源安装过 `docker.io`、`docker-compose`、`podman-docker` 或独立 `containerd`，先按 Docker 官方建议移除冲突包：

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  sudo apt remove -y "$pkg"
done
```

如果这些软件包未安装，APT 显示未找到或未安装可忽略。此步不会自动删除 `/var/lib/docker` 中的现有镜像、容器和数据卷。

### 6.2 添加 Docker 官方签名密钥

1. 更新软件包索引并安装基础工具：

   ```bash
   sudo apt update
   sudo apt install -y ca-certificates curl
   ```

2. 创建 APT 密钥目录，下载 Docker 官方 ASCII 签名密钥：

   ```bash
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
     -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc
   ```

3. 可选：查看密钥指纹：

   ```bash
   gpg --show-keys --fingerprint /etc/apt/keyrings/docker.asc
   ```

### 6.3 添加 Docker 官方软件源

使用 Docker 官方当前推荐的 deb822 `.sources` 格式：

```bash
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

检查生成的配置：

```bash
cat /etc/apt/sources.list.d/docker.sources
```

当前 Ubuntu 24.04 ARM64 环境中，`Suites` 应为 `noble`，`Architectures` 应为 `arm64`。

### 6.4 安装 Docker Engine、Buildx 和 Compose

添加 Docker 官方软件源后，先更新 APT 索引：

```bash
sudo apt update
```

确认输出中 `https://download.docker.com/linux/ubuntu noble InRelease` 正常下载，没有 `Ign`、`Err` 或 `Failed to fetch`，然后安装 Docker 官方软件包：

```bash
sudo apt install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin
```

本文安装的 Compose 是 Docker CLI 插件，命令为 `docker compose`，不是旧版独立命令 `docker-compose`。

### 6.5 启动并验证 Docker

安装完成后先检查 Docker 服务：

```bash
sudo systemctl status docker
```

如 Docker 未运行，手动启动：

```bash
sudo systemctl start docker
```

检查各组件版本：

```bash
sudo docker version
sudo docker info
sudo docker buildx version
sudo docker compose version
```

运行官方测试容器：

```bash
sudo docker run hello-world
```

如看到 `Hello from Docker!`，表示 Docker Engine 可以正常拉取镜像和启动容器。

### 6.6 允许普通用户运行 Docker（可选）

默认情况下需要使用 `sudo docker ...`。如希望当前普通用户不加 `sudo` 运行 Docker，执行：

```bash
sudo usermod -aG docker "$USER"
```

然后完全注销 Ubuntu 桌面会话并重新登录，或在当前终端临时执行：

```bash
newgrp docker
```

验证：

```bash
docker run --rm hello-world
```

> `docker` 用户组可通过 Docker daemon 获得接近 `root` 的主机控制权。只应将可信用户加入该组，不要在多用户或不可信环境中随意授权。

### 6.7 使用 Docker Compose 进行测试

创建测试目录：

```bash
mkdir -p ~/docker-compose-test
cd ~/docker-compose-test
```

创建 `compose.yaml`：

```bash
cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
EOF
```

启动服务：

```bash
docker compose up -d
docker compose ps
```

在 Ubuntu 浏览器中访问 `http://127.0.0.1:8080`，能显示 Nginx 欢迎页即表示 Compose 可用。测试完成后停止并删除容器：

```bash
docker compose down
```

### 6.8 Docker 网络故障排查

#### 6.8.1 APT 访问 Docker 软件源时 TLS 握手失败

如 `sudo apt update` 出现 `Could not handshake` 或无法下载 Docker `InRelease`，先检查系统时间、DNS 和直连情况：

```bash
timedatectl status
curl -I https://download.docker.com/linux/ubuntu/dists/noble/InRelease
```

如直连失败但前文 v2rayA HTTP 代理可用，可仅在故障排查时为当次 APT 命令指定代理：

```bash
curl -I --proxy http://127.0.0.1:20171 \
  https://download.docker.com/linux/ubuntu/dists/noble/InRelease

sudo apt \
  -o Acquire::http::Proxy="http://127.0.0.1:20171" \
  -o Acquire::https::Proxy="http://127.0.0.1:20171" \
  update
```

只有 Docker 仓库索引成功下载后才继续安装。不要使用 `trusted=yes`、`--allow-unauthenticated` 或关闭 TLS 证书验证。

#### 6.8.2 `registry-1.docker.io` DNS 查询超时

如执行 `sudo docker run hello-world` 时出现：

```text
failed to resolve reference "docker.io/library/hello-world:latest"
dial tcp: lookup registry-1.docker.io on 127.0.0.53:53
read udp 127.0.0.1:xxxxx->127.0.0.53:53: i/o timeout
```

说明 Docker daemon 已经正常运行，但 Ubuntu 的 `systemd-resolved` 未能将 `registry-1.docker.io` 解析为 IP 地址。`127.0.0.53` 是 Ubuntu 本机 DNS stub，不是 Docker Hub 或公网 DNS 服务器。

Docker 日志中如同时出现以下信息：

```text
Deleting nftables IPv4 rules ... No such file or directory
Deleting nftables IPv6 rules ... No such file or directory
```

这通常是 Docker 启动时尝试清理尚不存在的旧规则，在日志后续显示 `Loading containers: done` 和 `Daemon has completed initialization` 时可忽略，它不是本次 DNS 超时的原因。

1. 检查 Ubuntu 当前 DNS 状态：

   ```bash
   resolvectl status
   resolvectl query registry-1.docker.io
   cat /etc/resolv.conf
   ```

2. 确认网关和外网 IP 可达：

   ```bash
   ping -c 4 192.168.230.2
   ping -c 4 1.1.1.1
   ```

   - 网关也无法访问：检查 VMware Fusion NAT 网卡和 Ubuntu 静态 IP、网关配置。
   - 网关和外网 IP 正常，但域名解析失败：继续修复 DNS。

3. 先重启 Ubuntu DNS 服务：

   ```bash
   sudo systemctl restart systemd-resolved.service
   resolvectl flush-caches
   resolvectl query registry-1.docker.io
   ```

4. 如仍然超时，查看 `enp2s0` 当前使用的 NetworkManager 连接名：

   ```bash
   nmcli device status
   nmcli connection show --active
   CONNECTION="$(nmcli -g GENERAL.CONNECTION device show enp2s0)"
   echo "$CONNECTION"
   ```

5. 为该连接配置 VMware NAT DNS 和备用 DNS：

   > `nmcli connection up` 可能让 SSH 短暂断开，建议在 VMware Fusion 的 Ubuntu 本地终端中执行。

   ```bash
   sudo nmcli connection modify "$CONNECTION" \
     ipv4.ignore-auto-dns yes \
     ipv4.dns "192.168.230.2,223.5.5.5"
   sudo nmcli connection up "$CONNECTION"
   sudo systemctl restart systemd-resolved.service
   resolvectl flush-caches
   ```

   如使用的不是本文示例 NAT 网段，将 `192.168.230.2` 替换为 `ip route` 显示的实际默认网关/DNS。

6. 验证 DNS 已恢复：

   ```bash
   resolvectl query registry-1.docker.io
   getent ahosts registry-1.docker.io
   curl -I https://registry-1.docker.io/v2/
   ```

   `curl` 返回 `HTTP/1.1 401 Unauthorized` 或类似的 Docker Registry 认证响应，说明 DNS 和 HTTPS 网络已经连通；该 `401` 是未携带 Registry 令牌时的正常响应。

7. 重启 Docker 并重试：

   ```bash
   sudo systemctl restart docker.service
   sudo docker pull hello-world:latest
   sudo docker run --rm hello-world
   ```

#### 6.8.3 DNS 正常但 Docker 仍无法拉取镜像

如 `resolvectl query registry-1.docker.io` 已成功，但 Docker Hub 的 HTTPS 连接仍然超时，需要注意 Docker daemon 不会自动继承用户终端中的 `http_proxy`/`https_proxy`。如前文 v2rayA HTTP 代理已在 `127.0.0.1:20171` 监听，可为 Docker systemd 服务单独配置代理。

1. 确认 v2rayA 代理可以访问 Docker Registry：

   ```bash
   curl -I --proxy http://127.0.0.1:20171 \
     https://registry-1.docker.io/v2/
   ```

2. 创建 Docker systemd 服务覆盖配置：

   ```bash
   sudo mkdir -p /etc/systemd/system/docker.service.d
   sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf > /dev/null <<'EOF'
   [Service]
   Environment="HTTP_PROXY=http://127.0.0.1:20171"
   Environment="HTTPS_PROXY=http://127.0.0.1:20171"
   Environment="NO_PROXY=localhost,127.0.0.1,::1"
   EOF
   ```

3. 重载 systemd 并重启 Docker：

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart docker.service
   ```

4. 检查代理环境是否已加载：

   ```bash
   systemctl show docker.service --property=Environment
   sudo docker info | grep -i proxy
   ```

5. 重试拉取和运行：

   ```bash
   sudo docker pull hello-world:latest
   sudo docker run --rm hello-world
   ```

如后续不再需要 Docker daemon 代理，删除配置并重启：

```bash
sudo rm -f /etc/systemd/system/docker.service.d/http-proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker.service
```

查看 Docker 最近日志：

```bash
journalctl -u docker.service -n 100 --no-pager
```

## 7. 通过 NVM 安装 Node.js 和 npm

NVM（Node Version Manager）可为同一用户安装和切换多个 Node.js 版本。本节安装指定的 Node.js `22.14.0` 和 npm `10.9.2`。

> NVM 是按用户安装的工具。建议使用普通用户 `fly` 执行本节命令，不要使用 `root` 或 `sudo` 安装 NVM/Node.js，否则安装结果只会写入 `/root/.nvm` 并对 root 用户生效。

### 7.1 切换到普通用户

检查当前用户：

```bash
whoami
```

如输出 `root`，执行以下命令切换到安装 Ubuntu 时创建的普通用户：

```bash
su - fly
```

再次执行 `whoami`，确认输出为 `fly`。

### 7.2 安装 NVM

安装 `curl`：

```bash
sudo apt update
sudo apt install -y curl ca-certificates
```

根据 NVM 官方仓库的当前安装命令，安装受支持的 `v0.40.5`：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.5/install.sh | bash
```

> 上述命令会从 GitHub 下载脚本并立即执行。高安全环境中可先将 `install.sh` 下载到本地并审查内容，再手动执行。

### 7.3 加载并验证 NVM

安装脚本会根据当前 Shell 修改 `~/.bashrc`、`~/.profile` 或 `~/.zshrc`。可关闭并重新打开终端，或对 Ubuntu 默认 Bash 执行：

```bash
source ~/.bashrc
```

如仍提示 `nvm: command not found`，在当前会话手动加载：

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
```

验证：

```bash
command -v nvm
nvm --version
```

`command -v nvm` 应输出 `nvm`，而不是某个二进制文件路径，因为 NVM 以 Shell 函数的形式运行。

### 7.4 安装 Node.js 22.14.0

执行：

```bash
nvm install 22.14.0
nvm use 22.14.0
```

NVM 会根据当前 `arm64` 架构下载对应的 Node.js Linux ARM64 官方二进制文件，并自动验证下载校验值。

查看安装位置：

```bash
nvm which 22.14.0
command -v node
command -v npm
```

路径应位于当前普通用户的 `~/.nvm` 目录中。

### 7.5 验证 Node.js 和 npm 版本

```bash
node --version
npm --version
```

预期输出：

```text
v22.14.0
10.9.2
```

如 npm 版本不是 `10.9.2`，可在确认当前正在使用 Node.js `22.14.0` 后安装指定版本：

```bash
nvm use 22.14.0
npm install --global npm@10.9.2
npm --version
```

NVM 管理的全局 npm 包会安装到当前 Node.js 版本的用户目录中，因此不要在 `npm install --global` 前添加 `sudo`。

### 7.6 设置默认 Node.js 版本

```bash
nvm alias default 22.14.0
```

关闭并重新打开终端后再次验证：

```bash
node --version
npm --version
nvm current
```

### 7.7 使用 `.nvmrc` 固定项目版本（推荐）

在项目根目录中执行：

```bash
echo "22.14.0" > .nvmrc
nvm use
```

其他开发者进入该项目后可执行 `nvm install` 和 `nvm use`，安装并切换到项目指定的 Node.js 版本。

### 7.8 常用 NVM 命令

```bash
# 查看已安装版本
nvm ls

# 查看可安装版本
nvm ls-remote

# 切换版本
nvm use 22.14.0

# 安装当前最新 LTS
nvm install --lts

# 删除指定版本
nvm uninstall 22.14.0
```

## 8. 通过 pyenv 安装 Python 3.13

Ubuntu 24.04 默认使用 Python 3.12，APT、GNOME 和部分系统工具依赖该版本。为避免破坏系统环境，本节使用 `pyenv` 在普通用户目录中编译安装 Python `3.13.14`，与系统 Python 并存。

> 不要删除 Ubuntu 自带的 `python3`、不要手动替换 `/usr/bin/python3` 软链接，也不要将 pyenv 安装的 Python 复制到 `/usr/bin`。

### 8.1 确认当前用户和系统 Python

使用普通用户执行：

```bash
whoami
python3 --version
command -v python3
```

如当前用户为 `root`，先切换到普通用户：

```bash
su - fly
```

pyenv 按用户安装。如在 root 下操作，所有内容都会写入 `/root/.pyenv`，普通用户无法直接使用。

### 8.2 安装 Python 编译依赖

pyenv 在 Linux 上通常会下载 CPython 源码并在本机编译，因此需要先安装编译器和常用标准库的开发包：

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  curl \
  git \
  libbz2-dev \
  libffi-dev \
  liblzma-dev \
  libncursesw5-dev \
  libreadline-dev \
  libsqlite3-dev \
  libssl-dev \
  libxml2-dev \
  libxmlsec1-dev \
  tk-dev \
  xz-utils \
  zlib1g-dev
```

这些依赖用于构建 `ssl`、`sqlite3`、`bz2`、`lzma`、`readline`、`tkinter` 等 Python 标准库模块。如缺少对应开发包，Python 即使编译成功，也可能缺少功能。

### 8.3 安装 pyenv

使用 pyenv 官方 README 推荐的安装器：

```bash
curl -fsSL https://pyenv.run | bash
```

> 该命令会从 GitHub 下载并执行 pyenv-installer。如对供应链安全有更高要求，应先将脚本下载到本地、检查内容，再执行。

### 8.4 配置 Bash 环境

将 pyenv 配置加入 `~/.bashrc`：

```bash
cat >> ~/.bashrc <<'EOF'

# pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
EOF
```

为了让 Bash 登录 Shell 也能找到 pyenv，将基础 PATH 配置加入 `~/.profile`：

```bash
cat >> ~/.profile <<'EOF'

# pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
EOF
```

重新启动当前 Shell：

```bash
exec "$SHELL"
```

验证 pyenv：

```bash
command -v pyenv
pyenv --version
pyenv root
```

`pyenv root` 应输出当前普通用户的 `~/.pyenv`。

### 8.5 安装 Python 3.13.14

先确认 pyenv 已包含该版本的安装定义：

```bash
pyenv install --list | grep -E '^  3\.13\.[0-9]+$' | tail
```

安装 Python `3.13.14`：

```bash
pyenv install 3.13.14
```

编译时间取决于虚拟机的 CPU 和内存配置。如下载受当前网络限制，可临时使用前文的 v2rayA HTTP 代理：

```bash
export http_proxy=http://127.0.0.1:20171
export https_proxy=http://127.0.0.1:20171
pyenv install 3.13.14
unset http_proxy https_proxy
```

### 8.6 选择 Python 版本

将 Python `3.13.14` 设为当前用户的默认版本：

```bash
pyenv global 3.13.14
```

或者只在某个项目中使用 Python 3.13：

```bash
mkdir -p ~/projects/python313-demo
cd ~/projects/python313-demo
pyenv local 3.13.14
```

`pyenv local` 会在当前目录创建 `.python-version` 文件，进入该目录时会自动切换版本。如只需在项目中使用 Python 3.13，建议使用 `local` 而不是 `global`。

恢复使用 Ubuntu 系统 Python：

```bash
pyenv global system
```

### 8.7 验证 Python、pip 和标准库

```bash
python --version
python3 --version
pip --version
pyenv version
pyenv which python
```

选中 pyenv Python 时，`python --version` 和 `python3 --version` 应输出：

```text
Python 3.13.14
```

检查常用标准库模块：

```bash
python -c 'import bz2, ctypes, lzma, readline, sqlite3, ssl, tkinter; print("Python 3.13 modules OK")'
```

如某个模块导入失败，通常表示编译 Python 时缺少对应的 Ubuntu 开发包。补齐依赖后重新安装：

```bash
pyenv uninstall 3.13.14
pyenv install 3.13.14
```

### 8.8 更新 pip 和创建虚拟环境

更新当前 Python 版本中的 pip：

```bash
python -m pip install --upgrade pip
```

为项目创建独立虚拟环境：

```bash
cd ~/projects/python313-demo
python -m venv .venv
source .venv/bin/activate
```

验证虚拟环境：

```bash
python --version
python -m pip --version
```

退出虚拟环境：

```bash
deactivate
```

> 不建议把项目依赖直接安装到 pyenv 的全局 Python 环境。每个项目应使用独立 `.venv`，并将 `.venv/` 加入 `.gitignore`。

### 8.9 常用 pyenv 命令

```bash
# 查看已安装版本
pyenv versions

# 查看当前生效版本
pyenv version

# 设置用户默认版本
pyenv global 3.13.14

# 设置当前项目版本
pyenv local 3.13.14

# 临时设置当前 Shell 版本
pyenv shell 3.13.14

# 恢复系统 Python
pyenv global system

# 删除 Python 3.13.14
pyenv uninstall 3.13.14
```

## 9. 导出并分享完整虚拟机

完成 Ubuntu 系统、软件和网络配置后，可将虚拟机导出给其他人使用。VMware Fusion 中常用的分享方式有两种：

| 方式 | 适用场景 | 优点 | 注意事项 |
| :--- | :--- | :--- | :--- |
| 导出为单个 `.ova` 文件 | 分发给其他人，或导入 Fusion、Workstation 等 VMware 产品 | 单文件，便于传输和导入 | 不用于保留虚拟机的运行状态，快照也不应视为会完整迁移 |
| 复制整个 `.vmwarevm` 包 | 在 VMware Fusion 之间迁移或备份 | 最接近原虚拟机，可保留 Fusion 配置和现有快照文件 | 文件多且体积可能更大，更适合 Fusion 接收方 |

### 9.1 导出前的准备

1. 在 Ubuntu 中正常关机，确认虚拟机状态为“已关闭”，不要在运行、暂停或挂起状态下复制或导出。
2. 在 VMware Fusion 的虚拟机设置中打开 `CD/DVD`，取消“连接”和“启动时连接”，避免导出时继续引用本机的 Ubuntu ISO 文件。
3. 删除不再需要的临时文件，并确保虚拟机可以正常启动。
4. 检查虚拟机中是否包含密码、SSH 私钥、API 密钥、浏览器登录状态或业务数据。导出的虚拟机包含完整虚拟硬盘，获得文件的人可能读取其中的所有内容。
5. 确保 Mac 的目标磁盘具有足够可用空间。导出过程需要读取完整虚拟磁盘，所需时间取决于已使用的磁盘容量。

> 当前安装的是 Ubuntu 24.04 ARM64，导出后仍然是 ARM 架构虚拟机。接收方建议使用 Apple Silicon Mac 和支持 ARM 客户机的 VMware Fusion；它不能直接变成 x86_64/AMD64 虚拟机。

### 9.2 方式一：使用 OVF Tool 导出单文件 OVA

VMware Fusion 已内置 OVF Tool，可将虚拟机的 `.vmx` 配置和虚拟磁盘打包为一个 `.ova` 文件。这是分发给其他人时更方便的方式。

1. 退出 VMware Fusion，或至少确保目标虚拟机已完全关闭。
2. 在 Mac 终端中确认 OVF Tool 可用：

   ```bash
   "/Applications/VMware Fusion.app/Contents/Library/VMware OVF Tool/ovftool" --version
   ```

3. 执行导出命令。以当前虚拟机名称为例：

   ```bash
   "/Applications/VMware Fusion.app/Contents/Library/VMware OVF Tool/ovftool" \
     "$HOME/Virtual Machines.localized/Ubuntu 64-bit Arm 24.04.4.vmwarevm/Ubuntu 64-bit Arm 24.04.4.vmx" \
     "$HOME/Documents/vmfusion bak/Ubuntu-Desktop-24.04-ARM64.ova"
   ```

   路径中包含空格，因此必须保留命令中的英文双引号。导出期间请不要启动或修改虚拟机。

4. 命令显示 `Completed successfully` 后，确认 OVA 文件已生成：

   ```bash
   ls -lh "$HOME/Desktop/Ubuntu-Desktop-24.04-ARM64.ova"
   ```

5. 生成 SHA-256 校验值，将输出结果与 OVA 文件一起发给接收方：

   ```bash
   shasum -a 256 "$HOME/Documents/vmfusion bak/Ubuntu-Desktop-24.04-ARM64.ova"
   ```

如果需要导出为多文件 OVF 包，将目标文件后缀改为 `.ovf` 即可。OVF 通常会生成 `.ovf`、`.vmdk` 和 `.mf` 等多个文件，分发时必须保持这些文件在同一目录中。

### 9.3 接收方导入 OVA/OVF

1. 接收方先安装与当前硬件架构兼容的 VMware Fusion。
2. 如果提供了 SHA-256 校验值，先在接收方 Mac 上执行：

   ```bash
   shasum -a 256 "/path/to/Ubuntu-Desktop-24.04-ARM64.ova"
   ```

   确认计算结果与发送方提供的值完全一致，以排除文件传输损坏。
3. 启动 VMware，选择`文件`→`导入`，选中 `.ova` 或 `.ovf` 文件。也可直接双击 OVA 文件启动导入。
4. 按向导选择新虚拟机的名称和保存位置，等待虚拟磁盘转换完成。
5. 首次启动前检查处理器、内存和网络适配器设置。如导入时提示虚拟硬件规范不兼容，可按界面提示使用较低的兼容性规格重试。
6. 启动 Ubuntu，验证系统、网络和常用软件。如果导入后与原虚拟机同时运行，需检查静态 IP、主机名和 SSH 主机密钥，避免出现 IP 或身份冲突。

### 9.4 方式二：复制完整 `.vmwarevm` 虚拟机包

macOS 会将 VMware Fusion 虚拟机目录显示为一个 `.vmwarevm` 包。如果接收方也使用 VMware Fusion，直接复制该包可最大程度保留原始虚拟机。

1. 完全关闭虚拟机并退出 VMware Fusion。
2. 在 Finder 中打开用户主目录下的`虚拟机`（`Virtual Machines.localized`）目录。
3. 找到 `Ubuntu 64-bit Arm 24.04.4.vmwarevm`，将整个包复制到移动硬盘或其他传输位置。不要只复制包内的 `.vmx` 或某一个 `.vmdk` 文件。
4. 如需要先压缩再传输，可在 Finder 中右键点击 `.vmwarevm` 包并选择`压缩`。压缩和解压过程都需要额外磁盘空间。
5. 接收方将 `.vmwarevm` 包复制到本机，双击该包，或在 Fusion 中选择`文件`→`打开`。
6. 如果 Fusion 询问“已移动还是已复制”，用于分发的副本建议选择`我已复制它`（I Copied It），让 Fusion 生成新的虚拟机 UUID 和网卡 MAC 地址，减少与原虚拟机冲突的风险。

### 9.5 导出后的检查清单

- 使用生成的 OVA 或复制的 `.vmwarevm` 在另一个位置试导入一次，确认文件可用。
- 确认 Ubuntu 能正常启动和登录。
- 确认网络适配器已连接，并根据接收方的 Fusion NAT 网段重新设置静态 IP，或先恢复为 DHCP。
- 如果多人同时使用同一份虚拟机，分别修改主机名、用户密码和静态 IP。
- 确认 OVA 的 SHA-256 校验值与原文件一致。
- 不要将未加密且含有敏感数据的 OVA 或 `.vmwarevm` 包上传到公开网盘。

## 10. 故障排查与常见问题

### 10.1 网络不通问题（本地 Shell 无法连接 Ubuntu 虚拟机）

![image-20260710224258618](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/mag/image-20260710224258618.png)

从 Mac 终端通过 SSH 连接 Ubuntu 时，应先确认虚拟机的实际 IP，再检查 SSH 服务。Ubuntu Desktop 默认可能未安装 SSH 服务端，因此即使虚拟机可以正常上网，也不一定能直接使用 `ssh` 连接。

#### 10.1.1 确认 Ubuntu 的实际 IP 地址

在 Ubuntu 终端中执行：

```bash
ip -br address
```

找到状态为 `UP` 的有线网卡，常见名称如 `enp2s0`、`ens33` 或 `ens160`，记录其 `inet` 后的 IPv4 地址。例如截图中虚拟机的实际地址是 `192.168.230.131/24`，SSH 连接时应使用 `192.168.230.131`，不要将 `/24` 写入连接命令。

在 Mac 终端中先测试该 IP 是否可达：

```bash
ping -c 4 192.168.230.131
```

- 如果能收到回复，说明 Mac 与 Ubuntu 之间的网络已经连通，继续检查 SSH 服务。
- 如果提示超时或无法到达，确认 VMware Fusion 网络适配器已连接，并检查 Mac 和 Ubuntu 是否处于同一网段。如前文已配置桥接网络，还需确认桥接到了 Mac 当前使用的 Wi-Fi 或以太网接口。

#### 10.1.2 安装并启动 SSH 服务

如果 Mac 上显示 `Connection refused`，通常表示 Ubuntu 的 IP 可以访问，但 22 端口没有 SSH 服务在监听。在 Ubuntu 终端中执行：

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

检查 SSH 服务状态：

```bash
systemctl status ssh --no-pager
```

输出中应显示 `active (running)`。如果服务未运行，可查看最近的错误日志：

```bash
sudo journalctl -u ssh -n 50 --no-pager
```

#### 10.1.3 检查 22 端口和防火墙

在 Ubuntu 中确认 SSH 已监听 22 端口：

```bash
sudo ss -lntp | grep ':22'
```

如果 Ubuntu 防火墙已启用，放行 OpenSSH：

```bash
sudo ufw status
sudo ufw allow OpenSSH
```

`ufw status` 如果显示 `inactive`，说明 UFW 未拦截连接，无需专门启用防火墙。

在 Mac 中也可以直接测试 22 端口：

```bash
nc -vz 192.168.230.131 22
```

显示 `succeeded` 说明 SSH 端口已可访问。

#### 10.1.4 从 Mac 连接 Ubuntu

在 Ubuntu 中执行 `whoami` 确认用户名，然后在 Mac 终端中使用“Ubuntu 用户名 + Ubuntu IP”连接：

```bash
ssh fly@192.168.230.131
```

首次连接会询问是否信任主机指纹，确认 IP 无误后输入 `yes`，再输入 Ubuntu 用户的登录密码。输入密码时终端不会显示字符，这是正常的安全行为。

#### 10.1.5 根据错误信息快速定位

| Mac 终端提示 | 常见原因 | 处理方法 |
| :--- | :--- | :--- |
| `Operation timed out` | IP 写错、虚拟网卡未连接、桥接网卡选错或局域网隔离 | 重新用 `ip -br address` 确认 IP，再检查 VMware Fusion 网络设置 |
| `No route to host` | Mac 与 Ubuntu 不在可互通的网段，或路由配置错误 | 检查 IP、子网掩码、默认网关和桥接模式 |
| `Connection refused` | SSH 服务端未安装、未启动或未监听 22 端口 | 安装 `openssh-server` 并执行 `sudo systemctl enable --now ssh` |
| `Permission denied` | 用户名或密码错误，或 SSH 认证配置不允许当前登录方式 | 用 `whoami` 确认 Ubuntu 用户名，检查密码和 `/etc/ssh/sshd_config` |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | 虚拟机重装后 SSH 主机密钥已变更 | 确认连接的确实是目标虚拟机后，在 Mac 执行 `ssh-keygen -R 192.168.230.131` 删除旧记录 |

结合上图可知：连接 `192.168.230.130` 时超时，是因为使用了错误的 IP；改用虚拟机实际 IP `192.168.230.131` 后出现 `Connection refused`，说明网络已经可达，接下来只需在 Ubuntu 中安装并启动 `openssh-server`。

### 10.2 登录 Ubuntu 后经常黑屏

Ubuntu Desktop 24.04 存在登录过程偶发黑屏的已知问题，Apple Silicon Mac 上还可能与 VMware Fusion 的 ARM 图形显示、3D 加速或 Wayland/Xorg 会话有关。建议按以下顺序处理，每完成一项就重新测试，问题解决后不必继续修改。

#### 10.2.1 先尝试恢复当前桌面

1. 黑屏后先等待 30–60 秒，避免在 GNOME 登录会话尚未完全加载时反复点击或拖动鼠标。
2. 尝试使用 VMware Fusion 菜单向虚拟机发送 `Ctrl` + `Alt` + `F3`，切换到 TTY 文本终端。如 Mac 的 F3 键被用作系统功能键，需同时按住 `Fn`，或使用 Fusion 的“发送按键”菜单。
3. 在 TTY 中输入 Ubuntu 用户名和密码，然后重启图形登录管理器：

   ```bash
   sudo systemctl restart gdm3
   ```

   该命令会结束当前图形会话，未保存的桌面工作会丢失。

4. 如果无法切换到 TTY，可使用前文已配置的 SSH 从 Mac 登录 Ubuntu，执行同一条重启 `gdm3` 命令。如 SSH 也不可用，在 VMware Fusion 中选择`虚拟机`→`重启`作为临时恢复方法。

#### 10.2.2 更新 Ubuntu 和图形组件

Broadcom 将 Ubuntu 24.04 登录后黑屏列为已知的 Ubuntu 问题，建议优先更新到最新的系统修复版本。在 TTY、SSH 或可正常使用的终端中执行：

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

重启后确认当前系统和内核版本：

```bash
cat /etc/os-release
uname -r
```

#### 10.2.3 修复 VMware Tools 桌面集成

Ubuntu 24.04 应使用系统软件源中的 `open-vm-tools` 和 `open-vm-tools-desktop`，不要再安装旧的光盘版 VMware Tools。执行：

```bash
sudo apt update
sudo apt install --reinstall -y open-vm-tools open-vm-tools-desktop
sudo systemctl enable --now open-vm-tools
sudo reboot
```

重启后检查服务状态：

```bash
systemctl status open-vm-tools --no-pager
```

#### 10.2.4 测试关闭 VMware 3D 图形加速

1. 在 Ubuntu 中正常关机，不要使用暂停或挂起。
2. 在 VMware Fusion 中选中虚拟机，打开`设置`→`显示器`（Display）。
3. 取消勾选`加速 3D 图形`（Accelerate 3D Graphics），再启动 Ubuntu 测试。

如果关闭 3D 加速后黑屏消失，可暂时保持关闭。这可能降低桌面动画和高分辨率显示的流畅度，但通常不影响终端、开发工具和 SSH 使用。后续更新 VMware Fusion 和 Ubuntu 后可重新开启测试。

#### 10.2.5 切换 Wayland/Xorg 图形会话

不同 Fusion 版本和 Ubuntu 更新状态可能对 Wayland 或 Xorg 有不同表现。建议先查看当前会话类型：

```bash
echo "$XDG_SESSION_TYPE"
```

如果当前为 `x11`，Apple Silicon 上可优先测试 Wayland：

```bash
sudo cp /etc/gdm3/custom.conf /etc/gdm3/custom.conf.bak
sudo sed -i 's/^#\?WaylandEnable=.*/WaylandEnable=true/' /etc/gdm3/custom.conf
sudo reboot
```

如果当前为 `wayland` 且黑屏仍频繁出现，可改为 Xorg 进行对比测试：

```bash
sudo cp /etc/gdm3/custom.conf /etc/gdm3/custom.conf.bak
sudo sed -i 's/^#\?WaylandEnable=.*/WaylandEnable=false/' /etc/gdm3/custom.conf
sudo reboot
```

每次只测试一种会话模式。如果修改后问题更严重，在 TTY 或 SSH 中恢复备份：

```bash
sudo cp /etc/gdm3/custom.conf.bak /etc/gdm3/custom.conf
sudo reboot
```

#### 10.2.6 收集诊断信息

如果以上步骤均无效，在黑屏发生后通过 TTY 或 SSH 执行：

```bash
systemctl status gdm3 --no-pager
journalctl -b -u gdm3 --no-pager | tail -100
journalctl -b -p err --no-pager | tail -100
dmesg -T | grep -Ei 'vmwgfx|drm|gpu|error|fail' | tail -100
df -h
```

重点检查：

- `gdm3` 是否为 `active (running)`。
- 日志中是否有 `gnome-shell`、`vmwgfx`、`drm` 或 GPU 错误。
- 根分区或用户主目录是否已满。磁盘空间耗尽也会导致图形会话无法完成登录。

> 不建议在未确认日志错误前直接删除整个 GNOME 用户配置目录或禁用 `vmwgfx` 内核模块，这些操作可能导致个人桌面设置丢失或完全无图形输出。

### 10.3 性能优化建议

1. 为虚拟机分配足够内存（至少4GB）

2. 定期清理无用软件包：

   ```
   sudo apt autoremove
   ```

## 11. 参考

1. Ubuntu22.04：https://cdimage.ubuntu.com/ubuntu/releases/22.04/release/
2. Ubuntu24.04：https://cdimage.ubuntu.com/ubuntu/releases/noble/release/
3. VMware OVF Tool：https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest
4. OVF Tool 导出与导入命令：https://knowledge.broadcom.com/external/article/340425/ovf-tool-command-syntax-to-export-and-de.html
5. Ubuntu 24.04 登录后黑屏：https://knowledge.broadcom.com/external/article/395190/vm-console-black-screen-upon-login-on-ub.html
6. Ubuntu 24.04 安装 open-vm-tools：https://knowledge.broadcom.com/external/article/430963/downloading-and-installing-openvmtools-f.html
7. Fusion ARM Linux 图形重绘问题：https://knowledge.broadcom.com/external/article/315604/black-frame-content-noticed-on-guest-scr.html
8. Git 用户配置：https://git-scm.com/docs/git-config
9. GitHub 添加 SSH 公钥：https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
10. GitHub 通过 443 端口使用 SSH：https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port
11. v2rayA 在 Debian/Ubuntu 上的安装：https://v2raya.org/docs/prologue/installation/debian/
12. v2rayA 快速上手：https://v2raya.org/docs/prologue/quick-start/
13. v2rayA 官方 GitHub 仓库：https://github.com/v2rayA/v2rayA
14. v2rayA 官方 Releases：https://github.com/v2rayA/v2rayA/releases/latest
15. Docker Engine 在 Ubuntu 上的安装：https://docs.docker.com/engine/install/ubuntu/
16. Docker Engine Linux 安装后配置：https://docs.docker.com/engine/install/linux-postinstall/
17. NVM 官方 GitHub 仓库：https://github.com/nvm-sh/nvm
18. Node.js 官方下载：https://nodejs.org/en/download
19. Python 3.13.14 发布页：https://www.python.org/downloads/release/python-31314/
20. pyenv 官方 GitHub 仓库：https://github.com/pyenv/pyenv
21. pyenv-installer：https://github.com/pyenv/pyenv-installer
22. Cursor Anysphere Remote SSH 公告：https://forum.cursor.com/t/new-in-house-extensions-c-c-ssh-devcontainers-wsl-python/94531
23. OpenAI Codex 远程连接官方文档：https://learn.chatgpt.com/docs/remote-connections
24. OpenAI Codex 认证官方文档：https://learn.chatgpt.com/docs/auth
25. OpenAI Codex CLI 官方文档：https://learn.chatgpt.com/docs/codex/cli
26. OpenAI Codex IDE 扩展官方文档：https://learn.chatgpt.com/docs/codex/ide
27. Codex Desktop 本地与远程服务器教程（社区参考）：https://openeuler.csdn.net/6a178c95662f9a54cb77b0e4.html
28. Codex SSH 远程开发教程（社区参考）：https://linux.do/t/topic/2031256
