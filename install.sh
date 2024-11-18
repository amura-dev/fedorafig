mkdir -p .config/fedorafig
mkdir -p bin/fedorafig-src
cp -rf src/ bin/fedorafig-src
sudo chown -R "$USER":"$USER"
chmod u+x bin/fedorafig-src/main.py
ln -s ~/bin/fedorafig-src/main.py ~/bin/fedorafig
