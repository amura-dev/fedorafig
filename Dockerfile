FROM fedora:40

# Installing requied packages.
RUN \
  dnf install -y \
  python3 \
  neovim \
  ncurses

# Creates a typical user scenario.
RUN \
  useradd -m user             && \
  echo 'user:sudo' | chpasswd && \
  usermod -aG wheel user
USER user
WORKDIR /home/user
ENV USER=user
ENV HOME=/home/user
ENV FEDORAFIG_SRC_PATH=/home/user/bin/fedorafig-src
ENV FEDORAFIG_CFG_PATH=/home/user/.config/fedorafig


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
  chmod u+x bin/fedorafig-src/test.sh

# Runs tests.
CMD ["/home/user/bin/fedorafig-src/test.sh"]
