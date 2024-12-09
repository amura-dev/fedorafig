# fedorafig v0.1.0-alpha
<img alt="version static badge" src="https://img.shields.io/badge/version-0.1.0-blue" height=25> <img alt="unlicense license static badge" src="https://img.shields.io/badge/license-Unlicense-red" height="25"> <img alt="issues static badge" src="https://img.shields.io/github/issues/amura-dev/fedorafig?color=yellow" height="25"> <img alt="stars" src="https://img.shields.io/github/stars/amura-dev/fedorafig?color=white" height="25">

Have you ever had to go through the tedious task of writing your own configuration scripts for you Fedora Linux system? I have, and I didn't like it, which is why I made this utility for myself and perhaps it can help you too. `fedorafig` is a one-stop shop configuration utility for Fedora Linux. All you have to do is specify the configuration paths and their destinations, specify the packages, optionally from a specific repository, and any post-installation scripts.

## Installation
In a directory where the path `fedorafig` does not yet exist, execute the following commands
```bash
git clone https://github.com/amura-dev/fedorafig
cd fedorafig && chmod u+x && ./install.sh
cd .. && rm -rf fedorafig
```

## Uninstallation
If you would like to uninstall this utility, simply download `uninstall.sh`, and run
```bash
chmod u+x uninstall.sh
./uninstall.sh
rm uninstall.sh
```

## Quick guide
This is a guide on how to use the utility with concrete examples.
### Directory structure
Ensure `$CFG_DIR`, typically `~/.config/fedorafig/` looks like this:
```bash
~/.config/fedorafig
├── configs     # Configuration files/folders for `cfgpath`.
├── repos       # `.repo` files for repositories.
├── scripts     # Scripts for `script` subentries.
└── cfg1.json   # Main JSON configuration file.
```

### Configuration file entries and subentries

**Copy files**
```json
"entry-can-have-any-name": {
  "syspath": "cfgs/intended/dir/path/"
  "_COMMENT": "Usually a directory in ~/.config/ related to the package"
  "cfgpath": "cfgs/in/cfg/dir/or/file"
  "_COMMENT": "Usualy ~/.config/fedorafig/configs/"
}
```
Copies files from `cfgpath` (`configs/`) to `syspath`.

**Install a package**
```json
"htop": {
  "pkg": "htop"
}
```
Installs `pkg`.

**Activate repository**
```json
"just-repo-entry": {
  "repo": "my-repo"
}
```
Adds a `.repo` file from `repos/`.

**Execute a script (happens last of all subentries)**
```json
"hello": {
  "script": "hello.sh"
}
```
Executes a script from `$CFG_DIR/scripts/`.

**Install and configured the package**
```json
"neofetch": {
  "syspath": "~/.config/neofetch",
  "cfgpath": "neofetch/",
  "pkg": "neofetch"
}
```
Copies files and installs `pkg`, which is in this case `neofetch`.

**Install package from specific repository**
```json
"telegram": {
  "pkg": "telegram",
  "repo": "rpmfusion-free"
}
```
Installs `pkg` from `repo`.

**Activate all epositories**
```json
"all-repos": {
  "repo": "all"
}
```
Actvates all repositories specified in `.repo` files in `$CFG_DIR/repos/`.

**Comments**
All values with the key `"_COMMENT"` are ignored.

### Workflow
Follow these steps to maintain a functional setup.

**Prepare Directory**: Populate `configs/`, `repos/`, and `scripts/`. \
**Create a JSON configuration file**: Write JSON entries for tasks that the utility will execute. \
**Run `check`**: Validate the configuration.

## Features
### Set utility configuration path
By default, the `fedorafig` configuration directory is set to `~/.config/fedorafig`. If you wish to change it to `$CFG_DIR`, first ensure that the directory exists, then pass it to the utility with `-f` or `--new-cfg-dir`.
```bash
mkdir -p $CFG_DIR
fedorafig -f $CFG_DIR
```

Example:
```bash
mkdir -p ~/.fedorafig
fedorafig -f ~/.fedorafig
```

### Utility configuration check
`check` looks at your configuration specified for the OS in a JSON file. To check the OS configuration `$CFG_FILE`, a JSON file, it must located with `$CFG_DIR`, and for `check` to run successfully, the following must be satisfied:
+ In `$CFG_DIR`, there must be directories named `configs`, `repos`, and `scripts`.
+ For each entry in `$CFG_FILE`, `syspath` and `cfgpath` must exist together.
+ In `$CFG_FILE`, a specified `repo` subentry must exist in `$CFG_DIR/repos`, and be valid `.repo` file, ending in `.repo` in its name.
+ In `$CFG_FILE`, all `package` subentries must exist in at least one repository specified in all `repo` subentries that are not accompanied by a `package` subentry (when `package` and `repo` are not in the same entry). If `package` and `repo` are found in the same entry, then that `package` is only required to exist in that `repo`.
+ In `$CFG_FILE`, all `script` subentries must exist in `$CFG_DIR/scripts`, but not necessarily be valid. This is up to the user to ensure.

Note this does not prevent all runtime errrors, as the scripts specified may have raise runtime errors. The rest of the OS configuration will not raise runtime errors if `check` is successful.

Given that your `$CFG_DIR` looks like this:
```bash
$CFG_DIR
├── configs
│   └── ...
├── repos
│   └── ...
├── scripts
│   └── ...
└── $CFG_FILE
```
To run a check of `$CFG_FILE`, simply execute:
```bash
fedorafig check $CFG_FILE
```
Example:
```bash
~/.fedorafig
├── configs
│   └── ...
├── repos
│   └── ...
├── scripts
│   └── ...
├── cfg1.json
├── cfg2.json
└── cfg3.json
```
```bash
fedorafig check cfg1.json
```
You can have as many JSON files to configure your OS as you want. Note that checksum are used to check if anything has changed to see whether check will need to be rerun. The following flags can be used for some extra options:
+ `-c` or `--only-checksum`: Only calculate the checksum.
+ `-s` or `--show-checksum`: Show checksum after its calculated.
+ `-n` or `--no-checksum`: Does not calculate the potentially new checksum.

## Coming features
### Silent output
No output is printed to `stdout` when the utility is running. Can be specified with `-q` or `--quiet`

### Verbose output
Very detailed output is printed to `stdout` when the utility is running. Can be specified with `-v` or `--verbose`

### Apply system configuration
Moves files, installs packages, and scripts as specified in `$CFG_FILE`. For example `fedorafig run $CFG_FILE`. `CFG_FILE` has no associated checksum, it will be calculated.

### Access to commonly-used scripts
Scripts that one may want to execute on occasion and have immediate access to it can be executed with `fedorafig exec $SCRIPT`. All instances of `$SCRIPT` will be stored in `$CFG_DIR/common-scripts`.

### Triggering scripts with OS events
You may want to execute some scripts after a certain OS event occurs. This functionality will be added later to the `$CFG_FILE`.
