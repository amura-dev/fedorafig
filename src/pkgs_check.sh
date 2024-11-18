trap 'exit' INT

cp -rf /etc/yum.repos.d/ /tmp/yum.repos.d.old/
sudo cp -rf "$FEDORAFIG_CFG_PATH"/repos/. /etc/yum.repos.d/
sudo chown -R root:root /etc/yum.repos.d/
sudo chmod 644 /etc/yum.repos.d/*.repo

cp -rf /etc/yum.repos.d/ /tmp/yum.repos.d.bak
sudo sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/*.repo

sudo dnf makecache
if ! sudo dnf repolist --refresh; then
  sudo rm -rf /etc/yum.repos.d
  sudo cp -rf /tmp/yum.repos.d.old /etc/yum.repos.d
  echo "In \`pkgs_check\`: Some \`.repo\`(s) file has syntax errors" >&2
  exit 1
fi
rm -rf /tmp/yum.repos.d.old

PKG_LIST='/tmp/fedorafig-packages.txt'
while IFS= read -r PKG; do
  echo "Searching for package: \`${PKG}\`..."
  if ! dnf info "$PKG" > /dev/null 2>&1; then
    sudo cp -rf /etc/yum.repos.d/
    sudo cp -rf /etc/yum.repos.bak/ /etc/yum.repos.d/
    echo "In \`pkgs_check\`: Package not found: \`$PKG\`" >&2
    exit 1
  fi
  echo "Found."
done < "$PKG_LIST"

sudo dnf clean all
rm /tmp/fedorafig-packages.txt
sudo cp -rf /tmp/yum.repos.d.bak/. /etc/yum.repos.d/.
rm -rf /tmp/yum.repos.d.bak/
