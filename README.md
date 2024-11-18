# fedorafig v0.0.1

![License](https://img.shields.io/github/license/your-username/your-repo)
![Issues](https://img.shields.io/github/issues/your-username/your-repo)
![Stars](https://img.shields.io/github/stars/your-username/your-repo)

Have you ever had to go through the tedious task of writing your own configuration script for you Fedora Linux system? I have, and I didn't like it, which is why I made this utility for myself and perhaps it can help you too. `fedorafig` is a one-stop shop configuration utility for Fedora Linux. All you have to do is specify the configuration paths and their destinations, specify the packages, from a specific repository if needed, and/or the (post-)install scripts. Run the utility, and you're good to go.


## Table of Contents

- [About the project](#about-the-project)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## About the project

Provide a short introduction to your project:
- What does it do?
- Why did you create it?
- What problem does it solve?


## Features

### `check`
Checks the syntax of all configuration files and the paths specified in them. It also searches all specified repositories, even disabled ones, to check the existence of all specified packages (all `.repo` files will end up as you have specified them).

### `run`
Runs the configuration by first installing all specfied packages, then scripts, and moves all specified configurations into their respective locations.

### To be added
- `base`: Saves the initial "image" of the configurations for restoration purposes
- `archive`: Saves current "image" to be restored to later if needed. The methods will also be implemented to automatically install/uninstall and add/remove packages and files specified in new configurations depending on how they differ from older configurations.
- Setup of automatic scripts: By automatic scripts, I mean scripts that execute due to a certain system trigger, like after logging in or before shutting down. They will be easily configurable in a separate configuration path and how their own directory.


## Installation
Simply execute the following command in your terminal
```bash
git clone https://github.com/your-username/your-repo.git # will add later
```

## Usage


## FAQ


## Contributing


## License


## Contact
