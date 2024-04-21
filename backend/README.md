## 项目结构
1. ORM：采用MongoEngine，因此是非Async的
2. API: Pydantic 用于控制数据结构，Interface、API等
3. WebFrame: FastAPI
4. Database: MongoDB
5. Cache: 缓存较少，直接采用python dict
6. Env: 根目录建立.env文件用于生产环境设置，必须指定 ENV=production
7. python: 3.9


### 安装
1. poetry install

### 启动
1. 第一次布置先运行 poetry run python deploy_new.py
2. poetry run python main.py 
3. .ENV 文件中配置端口
4. 修改后可以通过 update.py 进行更新，会保存update log 到update_version.log

### 配置
1. app.core.config 中进行配置更改
2. .env 文件可以配置环境变量，将优先于config

### 默认
1. 一个Superadmin用户，su@admin.com,登录密码默认admin1111
2. 动态APIs: http://127.0.0.1:PORT/docs

# pytest
1. poetry run pytest -v -s
2. 没时间写test


