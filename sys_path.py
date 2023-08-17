import sys
from os import getenv,path
from dotenv import load_dotenv

BASE_DIRS=path.abspath(path.dirname(__file__))   
# This line calculates the absolute path of the directory containing the current script file using __file__ and then gets its directory name using path.dirname().
#  This provides the base directory path for the project.
load_dotenv(path.join(BASE_DIRS,'.env'))

BASE_PATH=getenv("BASE_PATH","/home/ritesh/projects/testprojects/ScrapyLocalHost/Task")

sys.path.insert(0,BASE_PATH)
sys.path.insert(1,BASE_PATH+"/Task")
sys.path.insert(2,BASE_PATH+"/Task/spiders")
sys.path.insert(3,BASE_PATH+"/Task/spider_fd")
