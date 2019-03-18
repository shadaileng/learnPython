# 基于aiohttp的Web项目

## 安装虚拟环境

### 安装virtualenv
	```shell
	$ sudo pip3 install virtualenv
	```

### 安装虚拟环境venv
- `virtualenv`命令创建虚拟环境,参数`--no-site-packages`指明创建纯净环境，`venv`为存放创建环境的目录。
	```shell
	$ virtualenv --no-site-packages venv
	```

### 启动虚拟环境

#### Windows
	```shell
	$ .\venv\Scripts\activate.bat # Windows系统
	(venv) path\to\project>
	```

#### Linux
	```shell
	$ source venv/bin/activate # Linux系统
	(venv) path\to\project$ 
	```

## 安装项目依赖
	```shell
	$ pip3 install -r requirements.txt
	```

## 启动项目
	```shell
	$ python web_app.py
	```