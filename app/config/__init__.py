import os
from .prd import *
from .dev import *
from .test import *

def get_settings():
    environment = os.getenv("ENV", "dev").lower()  # 默认为开发环境
    if environment == "production":
        return ProductionSettings()
    elif environment == "test":
        return TestSettings()
    else:
        return DevSettings()

# 获取当前环境的配置实例
settings = get_settings()