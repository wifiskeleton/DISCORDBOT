import os
from dotenv import load_dotenv


load_dotenv()

discord_api_secret = os.getenv("DISCORD_API_TOKEN")