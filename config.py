import os

BOT_TOKEN = "8679861924:AAE4XPNnpKsG48gcpr7wX_BtX_g3jTaO0_A"          # 替换为你的机器人令牌
ADMIN_IDS = [6863213861]               # 机器人管理员用户ID列表
DATABASE_PATH = "bot_database.db"     # SQLite数据库文件路径
SP_DIR = "sp"                         # 存放视频/GIF的文件夹

os.makedirs(SP_DIR, exist_ok=True)