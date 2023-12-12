## 语言/Language

- [中文](#中文)
- [English](#english)

## 中文
## Himool ERP--开源ERP管理系统

### 使用前须知
#### 软件开放源码(发行协议:GPL-3.0)，个人用户可免费学习使用，但禁止任何单位或个人修改软件后再次发行的行为。商业使用需得到我司授权，否则我们将通过法律途径解决侵权问题。
#### 我们欢迎对开源技术感兴趣的朋友一起加入到我们项目中来完善系统功能并为客户提供服务。欢迎扫描下方二维码添加技术交流群<br /><br />
   ![微信群](https://gitee.com/himool/erp/raw/master/img/%E5%BE%AE%E4%BF%A1%E7%BE%A4.png)

### 公司介绍
盒木科技是一家专注于供应链领域数字化的科技创新企业。Himool是盒木科技自主研发的软件产品系列品牌,目前已发布[盒木Himool ERP进销存管理系统](https://www.himool.com/erp)，[盒木Himool WMS仓库管理系统](https://www.himool.com/wms)及[盒木Himool WCS仓库控制系统](https://www.himool.com/wcs)。其中ERP社区版为开源产品，涵盖了采购，销售，库存等主要功能，为中小企业提供功能丰富、操作便捷、成本低廉的专业进销存服务。

#### ERP的服务模式
* SaaS网络版。如需购买可点击[该淘宝链接](https://item.taobao.com/item.htm?id=619069183482)
* 客户定制服务。我们设计的开源ERP社区版可供您学习和自用，针对有定制需求的客户我们将提供定制开发服务。
* 商业授权。开源社区需要您的支持以得以发展，如果您希望将我们的系统或源码二次开发后出售给其他客户，请先联系我们获得商业授权，否则将承担法律风险。

#### 欢迎有软件需求的客户或意向成为代理（[代理条件](https://www.himool.com/partner)）的公司/个人扫描下方销售经理二维码或致电18251313531咨询。<br />
添加微信时请备注单位/个人称呼+目的（如代理合作，客户咨询等，个人学习请直接添加交流群），否则不予通过。<br /><br />
![微信](https://gitee.com/himool/erp/raw/master/img/%E5%BE%AE%E4%BF%A1.png)

### 项目介绍
#### 开源ERP管理系统，该系统前后端分离，包含PDA移动端扫码操作，api使用restful协议，方便二次开发，后端使用Python，Django，DRF等技术，前端代码使用AntD进行构建，包含采购管理，销售管理，库存管理等业务管理流程。移动端使用Uniapp，包含产品标签打印，出入库扫码等功能。
* Gitee地址: [Gitee](https://gitee.com/himool/erp)
* Github地址: [Github](https://github.com/himool/HimoolERP)
* Demo地址: [Demo](https://erp.himool.com)

### 项目背景
#### 目前市面上没有一款采用流行的前后端技术易用开源的ERP系统。有不少朋友也跟我们反应实施了ERP系统但是仍然会面临许多问题，尤其二开的费用高昂。于是我们总结了这些年ERP系统开发的经验，设计了这款开源的Himool ERP系统，支持高自由度的开发，来支持企业的自定义需求。我们的代码将持续更新，并且保持与[Demo](https://erp.himool.com)地址的同步。

### 硬件要求及开发环境
* 移动端打印功能需指定型号PDA，请联系作者购买
* Python版本为V3.9+
* Django版本为V3.2+
* Django-rest-framework版本为V3.12+
* Vue版本为2.6+
* PDA端使用Uniapp
* 数据库为MySQL
* 前端组件为AntD
* 其他Python包可参考requirements.txt文件

### 搭建运行环境

* pip install -r requirements.txt
* cd frontend  #进入frontend文件夹
* npm install -g @vue/cli  #安装vue脚手架
* npm install  #安装依赖包

### 配置 MySQL

1. 数据库字符集设置为 utf8mb4
2. 创建 erp-db 数据库(先设置字符集, 再创建数据库)
    CREATE DATABASE erp_db;
3. 创建配置文件
    * python tools/create_configs.py
4. 迁移数据库
    * python manage.py makemigrations
    * python manage.py migrate
5. 创建用户
    * python manage.py runscript create_user

### 本地运行

1. 启动后端服务
    python manage.py runserver
2. 启动前端服务
    npm run serve
3. 浏览器访问前端地址

### 服务器运行

1. 配置 uwsgi
    pip install uwsgi
2. 运行 uwsgi
    uwsgi --ini [项目路径]/configs/uwsgi.ini
3. 配置 nginx(配置文件在 /configs/nginx)
4. 构建前端文件
    进入 frontend 目录, npm run build

### 业务流程
![业务流程](https://gitee.com/himool/erp/raw/master/img/ERP%20Workflow.png)

### 管理模块
![管理模块](https://gitee.com/himool/erp/raw/master/img/ERP%E6%A8%A1%E5%9D%97.png)

### PDA界面截图
![PDA界面](https://gitee.com/himool/erp/raw/master/img/PDA%E7%95%8C%E9%9D%A2.png)

### PC界面截图
![首页](https://gitee.com/himool/erp/raw/master/img/%E9%A6%96%E9%A1%B5.png)
![报表](https://gitee.com/himool/erp/raw/master/img/%E6%8A%A5%E8%A1%A8.png)
![产品](https://gitee.com/himool/erp/raw/master/img/%E4%BA%A7%E5%93%81.png)
![采购](https://gitee.com/himool/erp/raw/master/img/%E9%87%87%E8%B4%AD.png)
![销售](https://gitee.com/himool/erp/raw/master/img/%E9%94%80%E5%94%AE.png)
![生产](https://gitee.com/himool/erp/raw/master/img/%E7%94%9F%E4%BA%A7.png)
![库存](https://gitee.com/himool/erp/raw/master/img/%E5%BA%93%E5%AD%98.png)
![财务](https://gitee.com/himool/erp/raw/master/img/%E8%B4%A2%E5%8A%A1.png)
![设置](https://gitee.com/himool/erp/raw/master/img/%E8%AE%BE%E7%BD%AE.png)

## English
## Himool ERP--Open Source ERP System

### Read me
#### License Agreement:GPL-3.0，you can use this project for learning, business purpose is prohibited, please request authority from us before you use it for business.
#### If you're interested to join us and make this project perfect, please send email to me. marketing@himool.com<br /><br />

### Company Introduction
Himool Technology is focus on supply chain digitalization. All the products are developed by ourselves, now we have published [Himool ERP](https://www.himool.com/erp), [Himool WMS](https://www.himool.com/wms) and [Himool WCS](https://www.himool.com/wcs).  ERP is free，only charge fee to customized demands and agency who requests authorit, we're aiming to be the leader of open-source ERP providers, we offer professional ERP service to our customers.<br />
#### If you're interested in join as an agent([Conditions to be an agent](https://www.himool.com/partner)), please scan below wechat QR code, call me +86 18761717855 or email me.<br />
![Wechat](https://gitee.com/himool/erp/raw/master/img/%E5%BE%AE%E4%BF%A1.png)

### Project Introduction
#### Himool ERP contains core processes like master data, purchasing, sales, inbound, outbound and payment.
* Gitee地址: [Gitee](https://gitee.com/himool/erp)
* Github地址: [Github](https://github.com/himool/HimoolERP)
* Demo地址: [Demo](https://erp.himool.com)

### Devlopment Environment
* Python version V3.9+
* Django version V3.2+
* Djangorestframework version V3.12+
* Vue version 2.6+
* Uniapp for mobile device
* MySQL for database
* AntD for frontend UI element
* Please refer to requirement.txt for other python package

### Build Environment

* Install Pythonpip install -r requirements.txt
* Go to frontend foldercd frontend
* Install vuenpm install -g @vue/cli
* Install package dependenciesnpm install

### Config MySQL

1. utf8mb4 for Database character setting
2. Create datebase: CREATE DATABASE erp_db;
    CREATE DATABASE erp_db;
3. Migrate Database
    * python manage.py makemigrations
    * python manage.py migrate
4. Create User
    * python manage.py runscript create_user

### Run in Local Machine

1. Start Backend service
    python manage.py runserver
2. Start frontend service
    npm run serve
3. Access frontend address

### Run in Server

1. Config uwsgi
    pip install uwsgi
2. Run uwsgi
    uwsgi --ini [project path]/configs/uwsgi.ini
3. Config nginx(Config file in /configs/nginx)
4. Build frontend file
    Go to frontend directory, npm run build

### Business Workflow
![Business Workflow](https://gitee.com/himool/erp/raw/master/img/ERP%20Workflow.png)

### Functional Modules
![Functional Modules](https://gitee.com/himool/erp/raw/master/img/ERP%E6%A8%A1%E5%9D%97.png)

### PDA Demo
![PDA Demo](https://gitee.com/himool/erp/raw/master/img/PDA%E7%95%8C%E9%9D%A2.png)

### PC Demo
![Kanban](https://gitee.com/himool/erp/raw/master/img/%E9%A6%96%E9%A1%B5.png)
![Report](https://gitee.com/himool/erp/raw/master/img/%E6%8A%A5%E8%A1%A8.png)
![Product](https://gitee.com/himool/erp/raw/master/img/%E4%BA%A7%E5%93%81.png)
![Purchase](https://gitee.com/himool/erp/raw/master/img/%E9%87%87%E8%B4%AD.png)
![Sales](https://gitee.com/himool/erp/raw/master/img/%E9%94%80%E5%94%AE.png)
![Production](https://gitee.com/himool/erp/raw/master/img/%E7%94%9F%E4%BA%A7.png)
![Inventory](https://gitee.com/himool/erp/raw/master/img/%E5%BA%93%E5%AD%98.png)
![Finance](https://gitee.com/himool/erp/raw/master/img/%E8%B4%A2%E5%8A%A1.png)
![System](https://gitee.com/himool/erp/raw/master/img/%E8%AE%BE%E7%BD%AE.png)