# YAFBLOG - yet another flask blog
基于 flask 的极简 blog

## 安装

1. clone 代码到本地
```
git clone git@github.com:jifegg/yafblog.git
```

2. 安装 virtualenv
```
pip install virtualenv
cd yafblog
virtualenv venv
venv/bin/activate or venv\scripts\activate(windows)
```

3. 安装依赖
```
npm install .
```

4. 创建数据库，导入数据表
```
create database yafblog
source yafblog/schema.sql
```
> 或者可以通过 flask initdb 方式来导入数据表（需要设置FLASK_APP）

5. 运行
```
python run.py
```
前台地址：http://127.0.0.1:5000

后台地址：http://127.0.0.1:5000/admin（默认为 admin/admin）

6. 样式修改
```
npm install
gulp or gulp watch
```

## 部署
flask 自带的 server 不适用于生产环境，需要使用其它 server 代替，[请参考文档说明](http://flask.pocoo.org/docs/0.12/deploying/#deployment)。
推荐使用 gunicorn + nginx + supervisor 方式，[详情参考](http://blog.gutown.com/article/2) 。


## 功能
* 分类
* 标签
* 归档
* 分页
* code highlight
* markdown
* toc


## 依赖
* [flask](https://github.com/pallets/flask)
* [mistune](https://github.com/lepture/mistune)
* [pygments](http://pygments.org/)
* [pymysql](https://github.com/PyMySQL/PyMySQL)
* [bootstrap v4](https://github.com/twbs/bootstrap)
* [simplemde-markdown-editor](https://github.com/NextStepWebs/simplemde-markdown-editor)

## TODO
* 优化界面的自适应
* 添加 about 页面
* 评论功能
