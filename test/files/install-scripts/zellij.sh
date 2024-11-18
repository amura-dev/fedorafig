#!/bin/bash
curl -sSL https://github.com/zellij-org/zellij/releases/download/v0.41.1/zellij-x86_64-unknown-linux-musl.tar.gz -o zellij.tar.gz
tar -xvzf zellij.tar.gz
sudo mv zellij /usr/local/bin
