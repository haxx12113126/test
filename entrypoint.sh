
mkdir ./pipcache
pip download -r requirements.txt -d ./pipcache -i https://mirrors.aliyun.com/pypi/simple/
pip install --no-index --find-links=./pipcache -r requirements.txt
python main.py