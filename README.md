<p align="center">
	<img title="Logo" src="https://i.imgur.com/Jt0V0ce.png" width=550>
</p>



![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/bexxmodd/vizex?color=red&include_prereleases&style=flat-square) ![Python](https://img.shields.io/pypi/pyversions/vizex?color=yellow&style=flat-square) ![LICENSE](https://img.shields.io/pypi/l/vizex?color=g&style=flat-square)

**vizex** is the terminal program for the UNIX/Linux systems which helps the user to visualize the disk space usage for every partition and media on the user's machine. **vizex** is highly customizable and can fit any user's taste and preferences.

----

## Installation

### pip
**vizex** can be installed through your terminal and requires `Python 3.7` or above and the `pip package manager`.

Here's [how to set up Python](https://realpython.com/installing-python/) on your machine.

Some `vizex` dependencies require a Python 3 development package on Linux.

For Debian and other derived systems (Ubuntu, Mint, Kali, etc.) you can install this with the following command:
```
sudo apt-get install python3-dev
```

For Red Hat derived systems (Fedora, RHEL, CentOS, etc.) you can install this with the following command:
```
sudo yum install python3-devel
```

If you don't have PyPackage Index (PyPI) installed, [Here's the guide on how to install it](https://www.tecmint.com/install-pip-in-linux/). After everything is set up run the following command:
```
pip install vizex
```

### AUR
**vizex** is available as a package on the AUR (Arch user repository), distributions with AUR support may install directly from the command line using their favorite `pacman` helper.

Example using `yay`:
```
yay -S vizex
```

## How it Works

After installing run the program with a single command `vizex` in your terminal. This will graphically display disk space and usage:

Change the graph type from horizontal bars or to the vertical bars or to the *pie charts (in works).
```
vizex
```

![demo](https://i.imgur.com/dsWFE1v.png)

But the best part is that you can modify the colors and style of the display to your preferences with following commands. For example above command has excluded two partitions. You can aslo do give the following options:

```
-d --header <color>
-s --style <attribute>
-t --text <color>
-g --graph <color>
```

Or exclude any combination of partitions/disks with:
```
-I <PartitionName1> -I <PartitionName2> ...
```

For a full list of the available options please check:
```
vizex --help
```

## File Structure
```bash
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── src
│   ├── charts.py
│   ├── cli.py
│   ├── disks.py
│   └── tools.py
└── tests
    ├── access.py
    ├── test_cli.py
    └── test_disk.py
```

## Release History

- v1.1.0:
    - Displayes media and network partitions
    - Print all the partitions with `--every` command
    - Print additional (fstype and mount point) with `--details`
    - Refactored for a better reusability

------
## Follow me on Social Media
<p align="center">
	<a href="https://www.twitter.com/bexxmodd">
        	<img alt="twitter" src="https://i.imgur.com/fFlVB1c.png" height=50>
	</a>
	<a href="https://www.linkedin.com/in/bmodebadze">
        	<img alt="linkedin" src="https://i.imgur.com/wcvwfoZ.png" height=50>
	</a>
	<a href="https://www.github.com/bexxmodd">
        	<img alt="github" src="https://i.imgur.com/gnDF5oQ.png" height=50>
	</a>
</p>

--------
Repo is distributed under the MIT license. Please see the `LICENSE` for more information.
