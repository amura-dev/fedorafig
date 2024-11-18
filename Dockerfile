FROM fedora:40

# Installing requied packages.
RUN \
  dnf install -y \
  python3 \
  neovim

# Creates a typical user scenario.
RUN \
  useradd -m user             && \
  echo 'user:sudo' | chpasswd && \
  usermod -aG wheel user
USER user
ENV USER=user
ENV HOME=/home/user
WORKDIR /home/user


# Copies files and configures `fedorafig` with the test configuration.
ENV PATH="$HOME/bin:$PATH"
RUN \
  mkdir -p .config/fedorafig && \
  mkdir -p bin/fedorafig-src

COPY test/files .config/fedorafig
COPY src bin/fedorafig-src
RUN \
  echo 'sudo' | sudo -S chown -R user:user "$HOME"                && \
  chmod u+x bin/fedorafig-src/main.py                             && \
  ln -s "$HOME"/bin/fedorafig-src/main.py "$HOME"/bin/fedorafig   && \
  chmod u+x .config/fedorafig/test.sh

# Runs tests.
CMD ["/home/user/.config/fedorafig/test.sh"]
# CMD ["bash"]
