from dotenv import load_dotenv
from typing import Tuple, List
import ast
import os

load_dotenv()

class Settings:
    SECRET_KEY:str = os.getenv("SECRET_KEY")
    ALGORITHM:str = os.getenv("ALGORITHM")

    ALLOWED_ORIGINS:List = ["https://centralportal.insurecow.com", "http://localhost:3000", "https://cropploting.dev.insurecow.com"]
    
    DEFAULT_BUFFER_ZONE:int = 7 
    DEFAULT_PLOT_SIZE:int = 5
    DEFAULT_FIG_SIZE: Tuple = (17, 17)

    MINIMUM_LAND_AREA: float = 400.00  # minimum land area in square meter (m²), required for a plotting the box

    DEBUG: bool = True

settings = Settings()
