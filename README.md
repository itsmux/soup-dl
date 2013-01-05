soup-dl
=======

Python script for downloading images from soup.io rss feeds. Download the script to your computer and run from 
a terminal. 

This will create a ``data`` folder in your current directory and download all the images from your soup into that 
folder. 

The script will not download images that were embedded via HTML code. Only images that were uploaded directly to 
your soup will be fetched.

Usage:
------
  $ python soup.py <your soup rss file>.rss
