## 安装完整VIM

```
pkg install vim
```

其中同时安装了不少和桌面系统相关的文件，内容比较大。

## 下载unpv12e代码

### 安装wget

```
pkg install wget
```

### 下载源码

```
wget http://unpbook.com/unpv13e.tar.gz
```

### 解压

```
tar -xzvf unpv13e.tar.gz
```

## 安装Git

需要通过Git获取`vimrc`和相关的插件

```
pkg install git
```

### 下载vimrc

下载我的[`vimrc`](https://github.com/knowncold/vim)，并复制到用户目录

```
git clone https://github.com/knowncold/vim.git
cd vim
cp .vimrc ~/.vimrc
cp -r colors ~/.vim/colors
```

## 安装Vundle

可以参考之前的文章[Windows安装Vundle](http://blog.knowncold.me/wiki/2016/08/22/vundle-install-on-windows.html)

```
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

## vim插件

打开vim，使用`PluginInstall`命令

### 自动补全

自动补全通过`YouCompleteMe`插件来实现，相关的更详细的步骤可以看[这个文章](http://blog.knowncold.me/wiki/2016/09/24/youcompleteme-install.html)或者[官方文档](http://valloric.github.io/YouCompleteMe/#freebsdopenbsd)。

```
pkg install llvm38 boost-all boost-python-libs clang38
pkg install python
cd ~/.vim/bundle/YouCompleteMe
./install.py --clang-completer --system-libclang --system-boost
```

编译完成之后，需要一个配置文件才能完全使用YCM

可以使用YCM自己的配置文件`ycmd/cpp/ycm/.ycm_extra_conf.py`，放在用户根目录，然后打开c或者C++时，按照提示载入配置文件，YCM就会开始提供语义级的自动补全而不是简单的`ctags`。

### 补全配置

为了更好的使用YCM，`.ycm_extra_conf.py`对于每个项目每个文件都应该单独配置，这个配置文件主要定义的是当前项目需要的头文件，定义正确的配置文件之后，YCM才能到相应路径的头文件去寻找定义来补全。

可以手写`.ycm_extra_conf.py`，也可以使用工具自动配置，需要用到`YCM Generater`，按上面的步骤，在`PluginInstall`中，已经安装好了，使用时需要项目文件中有`Makefile`。

```
./config_gen.py PROJECT_DIRECTORY
```

## 安装xfce

```
pkg install xorg
pkg install slim
pkg install xfce
```     

向`/etc/rc.conf `写入

```
moused_enable="YES"
dbus_enable="YES"
hald_enable="YES"
slim_enable="YES"
```

向`~/.xinitrc`写入

```
exec xfce4-session
```

`init 6`重启之后就能进入桌面了

## 常用VIM命令
