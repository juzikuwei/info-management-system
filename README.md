# 信息管理系统

一个基于Flask框架的轻量级信息管理系统，用于个人信息的记录与管理。

## 功能特点

- 简洁现代的用户界面
- 用户登录验证
- 信息的增删改查
- 信息分类与搜索
- 移动端自适应布局
- 数据持久化存储

## 技术栈

- **后端**: Flask, SQLite
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **数据库**: SQLite (本地文件型数据库)

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

```bash
python app.py
```

应用将在 http://127.0.0.1:5000/ 上运行。

### 默认账户

- 用户名: admin
- 密码: admin123

## 系统结构

```
info_management_system/
├── app.py                  # Flask应用主文件
├── config.py               # 配置文件
├── database/               # 数据库文件夹
│   └── data.db             # SQLite数据库
├── static/                 # 静态文件
│   ├── css/                # CSS样式
│   ├── js/                 # JavaScript文件
│   └── img/                # 图片资源
├── templates/              # HTML模板
│   ├── base.html           # 基础模板
│   ├── login.html          # 登录页面
│   ├── dashboard.html      # 信息列表页面
│   ├── add_information.html # 添加信息页面
│   └── edit_information.html # 编辑信息页面
└── requirements.txt        # 项目依赖
```

## 自定义配置

可以通过修改 `config.py` 文件来自定义配置，或者通过环境变量来覆盖默认配置。

## 开发说明

本项目使用SQLite数据库进行数据存储，无需额外配置数据库服务器，适合个人使用的轻量级应用。