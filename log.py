# log.py
import logging
import os

# 自動定位 log 收集檔案路徑
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "network_test.log")

# 建立公用 logger
logger = logging.getLogger("network_tool")
logger.setLevel(logging.INFO)

# 確保不重複加 handler
if not logger.hasHandlers():
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(log_path, mode='w')
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 加入 handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
