# C4

Connect Four challenge

A multi-dimensional, multi-player, multi-goal "Connect Four"-like game.

Run with ```python MainWindow.py```.

## Dependencies
Python 2.7, Numpy, Scipy, PyQt4

On Linux (Ubuntu/Debian): `apt-get install python python-numpy python-scipy python-qt4`

On windows: [just install Python(x,y)](http://python-xy.github.io/downloads.html)

## Installation: Windows
Ensure the C4 parent folder is in your PYTHONPATH environment variable
before trying to execute MainWindow.py. Ensure the folder is called "C4" and nothing different.

For example, if you place the folder in your desktop like that:
```
C:\Users\Foo\Desktop\parentfolder\C4\MainWindow.py
```

Concatenate to PYTHONPATH the ```parentfolder``` using the semicolon as separator from previous paths:
```
PYTHONPATH=..some\path:C:\some\other/path;C:\Users\Foo\Desktop\parentfolder
```
