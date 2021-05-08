
<br>
<p align="center">
	<img title="Logo" src="https://i.imgur.com/0afEXvj.png" width=550>
	<br>
	<br>
	<br>
</p>

<p>
	<a href="https://pypi.org/project/vizex/"><img src="https://img.shields.io/github/v/release/bexxmodd/vizex?color=red&style=flat-square"></a>
	<a href=""><img src="https://img.shields.io/pypi/pyversions/vizex?color=orange&style=flat-square"></a>
	<a href="./LICENSE.md"><img src="https://img.shields.io/pypi/l/vizex?color=g&style=flat-square"></a>
</p>




**vizex** is the terminal program for the UNIX/Linux systems which helps the user to visualize the disk space usage for every partition and media on the user's machine. **vizex** is highly customizable and can fit any user's taste and preferences.

**vizexdf** is a new feature that allows to organize and print directory data in the terminal.


<br>
<br>

# Installation

## pip

**vizex** can be installed through your terminal and requires `Python >= 3.7` and the `pip package manager`. Here's [how to set up Python](https://realpython.com/installing-python/) on your machine.


If you don't have PyPackage Index (PyPI or just `pip`) installed, [Here's the guide on how to install it](https://www.tecmint.com/install-pip-in-linux/). Install **vizex** with the following command:
```
pip install vizex
```

If you already have vizex install you'll need to upgrade it:
```
pip install vizex --upgrade
```

If you encounter any problems during installation, know that some `vizex` dependencies require a Python 3 development package on Linux and you need to set up that manually.

For **Debian** and other derived systems (Ubuntu, Mint, Kali, etc.) you can install this with the following command:
```
sudo apt-get install python3-dev
```

For **Red Hat** derived systems (Fedora, RHEL, CentOS, etc.) you can install this with the following command:
```
sudo yum install python3-devel
```


## AUR
**vizex** is available as a package on the AUR (Arch user repository), distributions with AUR support may install directly from the command line using their favorite `pacman` helper.

Example using `yay`:
```
yay -S vizex
```

# How it Works

After installing you can use two terminal commands: `vizex` to display the disk usage/space and `vizexdf`, which will print the data of a current working directory with sizes, file types and last modified date.

This will graphically display disk space and usage:

```
vizex
```

![demo](https://i.imgur.com/OiPWWJf.png)

-----

```
vizexdf
```

![demo1](https://i.imgur.com/At7MFgu.png)

## vizex

The best part is that you can modify the colors and style of the display to your preferences with the following commands. For the example above command has excluded two partitions. You can also do give the following options:

```
-d --header <color>
-s --style <attribute>
-t --text <color>
-g --graph <color>
```

Display additional details, like `fstype` and `mount point`, for each partition:
```
vizex --details
```
![details-img](https://i.imgur.com/ThILQMo.png)

If you are interested in visualizing a specific path run with the following command:
```
vizex --path </full/path>
```

You can also exclude any combination of partitions/disks with multiple `-X` or for verbose `--exclude` option:
```
vizex -X <PartitionName1> -X <PartitionName2> ...
```

You can also save the partitions full information in `csv` or in `json` file, just by calling `--save` option with the full path where you want your output to be saved:
```
vizex --save "/home/user/disk_info.json"
```

And if you are on laptop you can even call your battery information with simple argument:
```
vizex battery
```

For a full list of the available options please check:
```
vizex --help
```


## vizexdf

You can include hidden files and folders by calling `--all` or `-a` for short and sort the output with `--sort` or `-s` for short based on name, file type, size, or date. Put it in descending order with the `--desc` option.

You can chain multiple options but make sure to put the `-s` at the end as it requires a text argument. Example:

```
vizexdf -ads name
```

This will print current directory data sorted by name and in descending order and will include hidden files.

----
**Lastly, you save all the modifications by adding -l at the end of the command**:

```
vizex -d red -t blue --details -l
```

The next time you call `vizex` it will include all options listed above. If you decided to change the default calling command for vizex/vizexdf just include `-l` and it will be overwritten


If you want to contribute to the project you are more than welcome! But first, make sure all the tests run after you fork the project and before the pull request. First, run the `access.py`, that way `tests` folder will obtain a path to the `main` folder and you can run all the tests.

You can get the full set of features by calling `--help` option with command.


# Release History
- v2.0.2:
	- Performance optimization. Runtime is reduced by ~250%
	- When program has no access to the folder it prints on the terminal instead of raising error

- v1.9.9:
	- Added `vizexdf` which prints directory data in style
	- Added alias `-l` option to save edited line as alias for a command
	- New logo
	- Refactoring and more explicit docstrings
	
- v1.5.3:
	- Added battery information  display
	- Now you can save output in csv or json formats
	- Small bug corrections
	- Updated --help info

- v1.3.5:
	- Major refactoring
	- Now charts can print string data
	- Options class is separated with all the correct getters and setters
	
- v1.3.2:
	- Refactored module disks.py
	- Unit Tests created
	- Set up the color for all the text
	- Updated docstrings

- v1.1.0:
	- Displayes media and network partitions
	- Print all the partitions with `--every` cmd
	- Print additional (fstype and mount point) with `--details`

----
## Special Thanks to the Contributors!
<p>
	<a href="https://github.com/bexxmodd/vizex/graphs/contributors">
  		<img src="https://contributors-img.web.app/image?repo=bexxmodd/vizex" />
	</a>
</p>

------
## Follow Me on Social Media
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


Repo is distributed under the MIT license. Please see the `LICENSE` for more information.
