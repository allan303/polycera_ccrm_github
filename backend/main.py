from app.factory import create_app
from app.core import config

ccrm = create_app()


if __name__ == '__main__':
    # 创建APP
    import uvicorn
    uvicorn.run(app=ccrm, host='127.0.0.1', port=config.PORT)
