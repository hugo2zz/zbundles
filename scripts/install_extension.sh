#!/usr/bin/env zsh
eval ". ~/.zshrc"

echo "Install zbundles..."
pip3 install .

echo "Copy extension.py to zipline folder..."
cp zbundles/extension.py ~/.zipline/

echo "Refreshing cookies..."
python3 scripts/refresh_cookies.py
