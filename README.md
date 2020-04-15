# PyWD2015
A Qt4 GUI written in Python for Wilson - Devinney eclipsing binary modeling software.
## Warning!
This is the old version of PyWD2015 and might contain serious bugs. This repository is kept for archival purposes. Current version of PyWD2015 is located at here: https://github.com/Varnani/pywd2015-qt5
## First Things First
If you happen to use this software in a scientific work, we kindly ask you to cite these relevant Wilson - Devinney papers:  
[ApJ (1971), 166, 605](https://ui.adsabs.harvard.edu/abs/1971ApJ...166..605W/abstract)  
[ApJ (1979), 234, 1054](https://ui.adsabs.harvard.edu/abs/1979ApJ...234.1054W/abstract)  
[ApJ (1990), 356, 613](https://ui.adsabs.harvard.edu/abs/1990ApJ...356..613W/abstract)  
[ApJ (2008), 672, 575](https://ui.adsabs.harvard.edu/abs/2008ApJ...672..575W/abstract)  

Plus PyWD2015 release proceeding:  
[CAOSP (2020), 50, 535](https://ui.adsabs.harvard.edu/abs/2020CoSka..50..535G/abstract)  

## Getting Started
PyWD2015 is written with Python 2.7. It also relies on Numpy, Scipy, Matplotlib libraries. You can install those with the following command:  

```pip install numpy scipy matplotlib``` 

Pip should be automatically installed alongside Python on Windows. On Linux, you may need to install pip with your package manager. On Ubuntu and Debian, you can issue:  

```sudo apt install python-pip```   

to install pip.

On Debian, you may encounter a "backports.functools_lru_cache" and/or "tkinter" error on a fresh matplotlib installation. To fix this, you can issue:  

```sudo apt install python-backports.functools-lru-cache python-tk```  

After that, you need to install the PyQt4 library.  
### Linux
Installing PyQt4 on Linux depends on your distro and package manager. On Ubuntu and Debian you can use:

```sudo apt install python-qt4 python-qt4-gl```  

### Windows
You need precompiled PyQt4 binaries. These can be downloaded from [SourceForge](https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/). The file you are looking for is
```PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x64.exe``` .

After this steps, you can start up PyWD2015 with the command:  

```python pywd2015.py```  

And the GUI should appear. To run calculations, you need to provide the paths of compiled DC and LC programs of the Wilson - Devinney code. Precompiled versions are hosted here with the permission of Dr. Robert E. Wilson. These can be found on the "Releases" page. If you want to, you can head to ftp://ftp.astro.ufl.edu/pub/wilson/lcdc2015/ (the WD Homepage), download source codes for DC and LC, then compile them yourself.
