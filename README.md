<p align="center">
	<img title="Logo" src="https://i.imgur.com/Jt0V0ce.png" width=550>
</p>
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/)

**vizex** is the terminal program for the UNIX/Linux systems which helps the user to visualize the disk space usage for every partition and media on the user's machine. **vizex** is highly customizable and can fit any user's taste and preferences.

----

## Installation
**vizex** is packaged through the `pypi` which makes it easy to install:
```
pip install vizex
```


## How it Works
[------video goes here-------]

After installing run the program with a single command `vizex` in your terminal. This will graphically display disk space and usage:

Change the graph type from horizontal bars or to the vertical bars or to the *pie charts (in works).
```
vizex barv
```

But the best part is that you can modify the colors and style of the display to your preferences with following commands:

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

For the full list of the available options please check:
```
vizex --help
```

## File Structure
```bash
├── cli.py
├── disk.py
├── LICENSE
├── pkg
│   └── __init__.py
├── README.md
├── requirements.txt
├── setup.py
└── tests
    ├── access.py
    ├── test_cli.py
    └── test_disk.py
```

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