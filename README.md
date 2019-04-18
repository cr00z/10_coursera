# Coursera Dump

Simple courses list grabber from Coursera.org

Load [Coursera XML feed](https://www.coursera.org/sitemap~www~courses.xml), dump information about courses:

* course name
* language
* start date
* duration in weeks
* average course grade

and save it into xlsx file.

You may stop a little, use *--start* and *--limit* options for continue (please note: xml feed may change).

# How to Install

Python 3 should be already installed. 

Script use:
* [requests](https://pypi.org/project/requests/2.21.0/)
* [openpyxl](https://pypi.org/project/openpyxl/2.3.5/)
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/4.5.1/)
* [lxml](https://pypi.org/project/lxml/4.3.3/)

Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# Quickstart

Example of script launch on Linux, Python 3.5:

```bash

$ python coursera.py result.xlsx --start 777 --limit 3 -v
777 https://www.coursera.org/learn/gcp-big-data-ml-fundamentals-es Google Cloud Platform Big Data and Machine Learning Fundamentals en Español es 2019-04-17 4.6 1
778 https://www.coursera.org/learn/mecanique-solide Mécanique : Solide Indéformable fr 2019-04-17 4.8 5
779 https://www.coursera.org/learn/develop-windows-apps-gcp Develop and Deploy Windows Applications on Google Cloud Platform en 2019-04-17 4.4 1

```

Use in Windows similarly.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
