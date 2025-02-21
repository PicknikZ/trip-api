from pathlib import Path
import logging
import time
import os
import traceback

class Logger:
    LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    def __init__(self, name="Logger", level="INFO", log_path=None):
        """
        初始化本地日志记录器
        :param name: 记录器名称（显示在日志中）
        :param level: 日志级别 DEBUG/INFO/WARNING/ERROR/CRITICAL
        :param log_path: 自定义日志文件路径（默认：~/server_<timestamp>.log）
        """
        self._level = level.upper()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG) 
        
        # 清理旧处理器（防止重复）
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s [%(name)s] %(levelname)-8s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.LEVELS[self._level])
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件处理器
        if not log_path:
            home = str(Path.home())
            log_path = os.path.join(
                home, 
                f"server_{int(time.time())}.log"
            )
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG) 
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        """动态修改控制台日志级别"""
        self._level = level.upper()
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(self.LEVELS[self._level])

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exc=None):
        """
        记录错误信息（可携带异常）
        :param message: 错误描述
        :param exc: 异常对象（可选）
        """
        if exc:
            msg = f"{message}\nException: {str(exc)}\n{traceback.format_exc()}"
        else:
            msg = message
        self.logger.error(msg)

    def critical(self, message):
        self.logger.critical(message)


def get_logger():
    return Logger(name="trip-api", level="INFO")

logger = Logger(name="trip-api", level="INFO", log_path="./server.log")