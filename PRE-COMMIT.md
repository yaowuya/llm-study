# 基于 Git 的 pre-commit 配置指南

##  1 . 背景

为了尽早发现代码问题，防止不符合规范的代码提交到仓库，强烈推荐每位开发者配置 `pre-commit` 代码提交前检查

## 2 . Git Hooks 本地配置

`pre-commit` 检查通过本地配置实现，因此每个开发者在开发之前都必须先配好本地的 Git Hooks。

推荐使用 [pre-commit](https://pre-commit.com/) 框架对 Git Hooks 进行配置及管理。**pre-commit**是由 python 实现的，用于管理和维护多个 pre-commit hooks 的实用框架。它提供了插件式的管理机制，并拥有大量的官方与第三方插件（需要时可自行开发），能够快速实现常见的代码检查任务，如 `eslint` 检查（支持跨语言），`flake8` 检查，`isort` 代码美化等。


### 配置方式 (新接入项目)

#### Unix/Linux

在 git 项目根目录下执行以下命令

```shell
# py2
git clone https://code.canway.net/rd-fy19-canway-frame/pre-commit.git && pre-commit/setup.sh

# py3
git clone https://code.canway.net/rd-fy19-canway-frame/pre-commit.git && pre-commit/setup.sh -v 3

```

#### Windows

```
# py2
git clone https://code.canway.net/rd-fy19-canway-frame/pre-commit.git && pre-commit\setup.bat

# py3
git clone https://code.canway.net/rd-fy19-canway-frame/pre-commit.git && pre-commit\setup.bat -v 3

```

执行后，查看 `.git/hooks` 目录，若存在名为 `pre-commit` 和 `commit-msg` 新文件，则配置成功 。

> 注意：以上新增到的文件都需要提交到git仓库，以便项目内共享配置

### 配置方式（项目中已有 .pre-commit-config.yaml）

在 git 项目根目录下执行以下命令

```shell
# py2
pip install zipp==0.5.1
pip install pre-commit
pre-commit install --allow-missing-config
pre-commit install --hook-type commit-msg --allow-missing-config

# py3
pip install pre-commit -i https://mirrors.aliyun.com/pypi/simple/
pre-commit install --allow-missing-config
pre-commit install --hook-type commit-msg --allow-missing-config
```

### 触发 Git Hooks

- pre-commit 代码检查无需手动触发，只要执行 `git commit ` 命令，就会自动触发（无论是在终端还是IDE）。请注意，代码检查的范围只是本次提交所修改的文件，而非全局。

- 若代码检查不通过，提交会被中断。可以根据具体的错误信息去调整代码，只有所有的检查项全部通过方可 push。

- 配置 `pre-commit` 后，第一次执行 `git commit` 命令时会联网下载所需的插件依赖，大概需要一分钟的时间，请耐心等待。

## 3 . 常用插件说明

### pyupgrade

提升Python代码风格

https://github.com/asottile/pyupgrade

### python-modernize

**【Python2项目专用】** 将python2风格代码自动转换为2-3兼容风格。 **Python3 项目无需安装此插件**

https://python-modernize.readthedocs.io/en/latest/fixers.html#

### check-merge-conflict

通过匹配conflict string，检查是否存在没有解决冲突的代码

### isort

自动调整 python 代码文件内的 import 顺序

若该项结果为 `failed`，通过 `git diff` 查看自动调整的地方，确认无误后，重新 `git add` 和 `git commit` 即可

### seed-isort-config

提升isort排序的准确度，会在项目根目录下生成 `.iosrt.cfg` 配置文件，需要提交

### autopep8

根据 `.flake8` 给出的配置自动调整 python 代码风格。

若该项结果为 `failed`，通过 `git diff` 查看自动调整的地方，确认无误后，重新 `git add` 和 `git commit` 即可

### flake8

根据 `.flake8` 给出的配置检查代码风格。

若该项结果为 `failed`，需要根据给出的错误信息手动进行调整。（autopep8 会尽可能地把能自动修复的都修复了，剩下的只能手动修复）


关于 flake8 规则代码与具体示例，可查阅 https://lintlyci.github.io/Flake8Rules/

### check-commit-message

检查 git 提交信息是否符合蓝鲸 SaaS 开发规范，需要将附录中的 `check_commit_message.py` 拷贝到项目中


commit message 必须包含以下前缀之一:

`feature`     	- 新特性

`bugfix`      	- 线上功能bug

`minor`       	- 不重要的修改（换行，拼写错误等）

`optimization`	- 功能优化

`sprintfix`   	- 未上线代码修改 （功能模块未上线部分bug）

`refactor`    	- 功能重构

`test`        	- 增加测试代码

`docs`        	- 编写文档

`merge`       	- 分支合并及冲突解决

### check-migrate

检查新增或修改的模型字段是否符合规范。

第一次提交时发现脚本认为不符合规范的字段，会返回错误并打印建议修改字段，修改后再次提交即可。

如果提交者认是沿用过去的标准或者字段有其特定用法，可以直接再次提交，第二次提交会跳过第一次检测的错误信息不再报错。


### check-requirements

检查项目 requirements.txt 是否包含黑名单中的 SDK，以及 SDK 的安装版本号是否满足最低版本要求。

## 4. 已知问题

- Stackless 版本的 Python 可能无法使用 pre-commit 
- black 和 isort 在某些情况下会冲突，导致两个插件修改同一个文件，无法提交；此时可以屏蔽 black 解决，结局后开启 black 后再次提交