import os
from dotenv import load_dotenv

load_dotenv()

HA_URL = "http://localhost:8123"

headers = {
    "Authorization": f"Bearer {os.getenv('HOME_LAB_TOKEN')}",
    "content-type": "application/json"
}
