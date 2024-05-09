from environs import Env
from dotenv import load_dotenv

env = Env()
env.read_env()


user_list = env.list("USERS")
print(f"users = {user_list}")
token = env.str("BOT_TOKEN")
api_key = env.str("API_KEY")
