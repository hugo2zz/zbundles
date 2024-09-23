# zbundles

Xueqiu data bundle for zipline.


## Installation

Install directly from GitHub 

```sh
git clone https://github.com/hugo2zz/zbundles.git
cd zbundles

pip3 install .
cp zbundles/extension.py ~/.zipline/
```


## Usage

### Load Cookies

Load cookies used by your web browser into local file - make sure you have accessed [xueqiu.com](https://xueqiu.com) from your chrome browser before.

```sh
python3 scripts/refresh_cookies.py
```

Rerun this script to refresh cookies is also needed when cookies are expired.

### Ingest Data

```sh
SYMBOLS=AAPL,MSFT zipline ingest -b xueqiu
```
