## 海鸥云ERP--开源ERP管理系统
### 项目介绍
#### 开源ERP管理系统，该前后端分离，api使用restful协议，方便二次开发，后端使用Python，Django，DRF等技术，前端代码使用AntD进行构建，包含采购管理，销售管理，库存管理等业务管理流程。
* Gitee地址: [Gitee](https://gitee.com/haioucloud/erp)
* Github地址: [Github](https://github.com/lianzhanshu/oms)
* Demo地址: [Demo](http://erp.haioucloud.com/) &nbsp;&nbsp;测试帐号：admin  密码：admin

### 使用前须知
* 软件开放源码(发行协议:GPL-3.0)，用户可免费使用，但禁止任何单位或个人修改软件后再次发行的行为。
* 我们欢迎对开源技术感兴趣的朋友一起加入到我们项目中来完善系统功能并为客户提供服务。欢迎扫描下方二维码添加技术交流群，添加时请备注来意

   ![微信群](https://gitee.com/haioucloud/erp/raw/main/raw/%E5%BE%AE%E4%BF%A1%E7%BE%A4.png)
* 功能定制：Tel:18761717855或扫描下方二维码联系

   ![微信](https://gitee.com/haioucloud/erp/raw/main/raw/%E5%BE%AE%E4%BF%A1.png)

### 项目背景
#### 目前市面上没有一款采用流行的前后端技术易用开源的ERP系统。有不少朋友也跟我们反应实施了ERP系统但是仍然会面临许多问题，尤其二开的费用高昂。于是我们总结了这些年ERP系统开发的经验，设计了这款开源的海鸥云ERP系统，支持高自由度的开发，来支持企业的自定义需求。我们的代码将持续更新，并且保持与[Demo](http://erp.haioucloud.com/)地址的同步。

### 开发环境
* Python版本为V3.9+
* Django版本为V3.2+
* Django-rest-framework版本为V3.12+
* Vue版本为2.6+
* 数据库为MySQL
* 前端组件为AntD
* 其他Python包可参考requirements.txt文件

### 搭建运行环境

* pip install -r requirements.txt
* cd frontend  #进入frontend文件夹
* npm install -g @vue/cli
* npm install

### 配置 MySQL

1. 数据库字符集设置为 utf8mb4
2. 创建 oms-db 数据库(先设置字符集, 再创建数据库)
    CREATE DATABASE oms_db;
3. 迁移数据库
    * python manage.py makemigrations
    * python manage.py migrate
4. 创建用户
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
![业务流程](https://gitee.com/haioucloud/erp/raw/main/raw/OMS%20Flow.JPG)

### 管理模块
* 报表管理 
   * 销售报表
   * 采购报表
   * 库存报表
   * 收支统计
   * 利润统计
* 基础数据 
   * 客户
   * 供应商
   * 仓库
   * 结算账户
   * 收支项目
* 商品管理
   * 商品分类
   * 商品信息
* 采购管理
   * 采购开单
   * 采购退货
   * 采购记录
   * 采购价变更记录
* 销售管理
   * 销售开单
   * 销售退货
   * 销售记录
   * 销售任务
* 库存管理
   * 入库
   * 出库
   * 盘点
   * 调拨
   * 库存流水
* 财务管理
   * 销售收款
   * 采购付款
   * 日常收支
   * 成本管理
* 系统管理
   * 角色权限
   * 员工账号
   * 配置管理

### 界面截图
![首页](https://gitee.com/haioucloud/erp/raw/main/raw/%E9%A6%96%E9%A1%B5.png)
![报表](https://gitee.com/haioucloud/erp/raw/main/raw/%E6%8A%A5%E8%A1%A8.png)
![商品](https://gitee.com/haioucloud/erp/raw/main/raw/%E5%95%86%E5%93%81.png)
![采购](https://gitee.com/haioucloud/erp/raw/main/raw/%E9%87%87%E8%B4%AD.png)
![库存](https://gitee.com/haioucloud/erp/raw/main/raw/%E5%BA%93%E5%AD%98.png)
![财务](https://gitee.com/haioucloud/erp/raw/main/raw/%E8%B4%A2%E5%8A%A1.png)
![设置](https://gitee.com/haioucloud/erp/raw/main/raw/%E8%AE%BE%E7%BD%AE.png)