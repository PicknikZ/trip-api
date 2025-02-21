# **项目简介**

本项目基于 **FastAPI** 框架构建，旨在提供一个高效、模块化的后端服务。通过清晰的目录结构和灵活的配置，支持快速开发和部署。

------

## **技术栈**

- **框架** : FastAPI
- **Python 版本** : 3.11
- **数据库** : MySQL（或其他支持的数据库）
- **容器化** : Docker + Docker Compose

------

## **目录结构**

项目的目录结构如下，按照功能模块进行划分，便于维护和扩展：
```python
-- app
    -- models            # 数据库模型定义
    -- routers           # 路由配置，按业务模块拆分，包含每个模块的路由和 Schemas 定义
    -- services          # 服务类，按业务模块拆分，封装核心业务逻辑
    -- utils             # 工具类，存放通用工具函数
    -- config            # 配置类，存放全局配置
    -- database.py       # 数据库相关配置
    -- dependencies.py   # 依赖项管理
    -- middlewares.py    # 自定义中间件
```



------

## **本地开发环境**

### **1. 环境准备**

确保你的系统已安装以下工具：

- Python 3.11
- pip
- virtualenv（可选）

### **2. 启动步骤**

在本地开发环境中，可以通过以下命令启动项目：

#### **(1) 克隆代码**

```bash
git clone <repository-url>
cd trip-api
```

#### **(2) 创建虚拟环境**

推荐使用虚拟环境隔离项目依赖：

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# 或
venv\Scripts\activate     # Windows
```

#### **(3) 安装依赖**

安装项目所需的依赖包：

```bash
pip install -r requirements/requirements.txt
```



#### **(4) 启动应用**

```bash
uvicorn app.main:app --reload
```

- `--reload` 参数会在代码更改时自动重启服务器，适合开发环境。

访问 `http://localhost:8000/docs` 查看自动生成的 API 文档。

------

## **Docker 容器化部署**

### **1. 使用 Docker Compose 启动**

项目支持通过 Docker Compose 快速启动服务，包括 FastAPI 应用和 MySQL 数据库。

#### **(1) 构建并启动服务**

```bash
docker-compose up --build
```

docker-compose up --build

#### **(2) 后台运行**

如果希望服务在后台运行，可以添加 `-d` 参数：

```bash
docker-compose up --build -d
```

#### **(3) 停止服务**

停止并移除容器：

```bash
docker-compose down
```

#### **(4) 清理数据（可选）**

如果需要清理 MySQL 数据（例如重新初始化数据库），可以删除持久化卷：

```bash
docker volume rm trip-api_mysql_data
```

------

## **其他说明**

### **1. 数据库连接**

默认的数据库连接信息如下：

- **数据库类型** : MySQL
- **用户名** : `root`
- **密码** : `test-Trip123`
- **数据库名称** : `trip`
- **主机** : `db`（Docker Compose 内部网络中的服务名）

### **2. 环境变量**

项目支持通过环境变量动态加载配置。常用环境变量包括：

- `ENVIRONMENT`: 设置运行环境（如 `development`、`production`、`testing`）。
- `DATABASE_URL`: 数据库连接字符串。
- `SECRET_KEY`: 应用密钥。

### **3. API 文档**

FastAPI 提供了自动生成的交互式 API 文档：

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`