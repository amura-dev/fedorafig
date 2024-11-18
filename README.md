# fedorafig

<img alt="version static badge" src="https://img.shields.io/badge/version-0.0.1-blue" height=25> <img alt="unlicense license static badge" src="https://img.shields.io/badge/license-Unlicense-red" height="25"> <img alt="issues static badge" src="https://img.shields.io/github/issues/amura-dev/fedorafig?color=yellow" height="25"> <img alt="stars" src="https://img.shields.io/github/stars/amura-dev/fedorafig?color=white" height="25">

Have you ever had to go through the tedious task of writing your own configuration script for you Fedora Linux system? I have, and I didn't like it, which is why I made this utility for myself and perhaps it can help you too. `fedorafig` is a one-stop shop configuration utility for Fedora Linux. All you have to do is specify the configuration paths and their destinations, specify the packages, from a specific repository if needed, and/or the (post-)install scripts. Run the utility, and you're good to go.


## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## About

`fedorafig` is a powerful and user-friendly configuration management utility designed specifically for Fedora Linux systems. It automates the process of configuring your system by allowing you to define the paths for configuration files, the packages you need (from specific repositories if necessary), and any installation or post-installation scripts to be executed.

Currently, testing involves starting a Fedora 40 Docker container and applying the example configuration in [test/files/](test/files). The packages that are installed and whose configuration is changed are [neofetch](https://github.com/dylanaraps/neofetch), [zellij](https://github.com/zellij-org/zellij), and [freetuxtv](https://github.com/freetuxtv/freetuxtv) as their configuration effects are easier and more convenient to observe, though this is subject to change.


## Features

### `check`
Checks the syntax of all configuration files and the paths specified in them. It also searches all specified repositories, even disabled ones, to check the existence of all specified packages (all `.repo` files will end up as you have specified them).

### `run`
Runs the configuration by first installing all specfied packages, then scripts, and moves all specified configurations into their respective locations.


## Installation
Simply execute the following command in your terminal
```bash
rm -rf fedorafig || true
git clone https://github.com/amura-dev/fedorafig
cd fedorafig
chmod u+x install.sh
bash install.sh
cd .. && rm -rf fedorafig
```

## Usage
```bash
Commands:
  {run,check}
    run        
               Installs packages (from a particular repository if specified,
               does not need to be enabled), runs installation scripts, and
               moves all configuration files to the specified location on
               the system.
    check      
               Checks syntax of and paths specified in all configuration
               files, checks all repositories for validity and the
               existence of all specified packages
```

## Upcoming features

### `base`
Saves the initial "image" of the configurations for restoration purposes.

### `archive`
`archive`: Saves current "image" to be restored to later if needed. The methods will also be implemented to automatically install/uninstall and add/remove packages and files specified in new configurations depending on how they differ from older configurations.

### Set-up of automatic scripts
By automatic scripts, I mean scripts that execute due to a certain system trigger, like after logging in or before shutting down. They will be easily configurable in a separate configuration path and how their own directory.


## FAQ
Not much to ask about at the moment.


## Contributing
This is currently a project that I am working on independently. It will definititely be open to contributions by the first full release.


## License
This project is licensed under the terms of the [Unlicense](LICENSE) license.


## Contact
My contact details are listed in my profile.

LinkedIn: [linkedin.com/in/andrei-murashev](https://www.linkedin.com/in/andrei-murashev)

Gmail: [andrei.murashev.1@gmail.com](andrei.murashev.1@gmail.com)
