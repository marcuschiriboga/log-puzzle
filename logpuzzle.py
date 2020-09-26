#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
__author__ = """marcus w/ help from
 https://github.com/bjshively/logpuzzle/blob/master/logpuzzle.py
 and joe
 """

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    path = "http://" + filename.split("_")[1]
    f = open(filename, 'r')
    # i need to learn about this regex line still
    urls = re.findall(r'GET (\S*puzzle\S*) HTTP', f.read())
    urls = set(urls)
    urls = sorted(urls)

    i = 0
    while i < len(urls):
        urls[i] = path + urls[i]
        i += 1

    def url_sort_key(img_file):
        img_sort = img_file.split('-')[-1]
        return img_sort
    img_name = urls[0].split('/')[-1]
    if(len(img_name.split("-")) == 3):
        return sorted(urls, key=url_sort_key)
    return urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # Check to see if the directory exists. If not, create it.
    if not (os.path.exists(dest_dir)):
        os.mkdir(dest_dir)

    index = open(os.path.join(dest_dir, 'index.html'), 'w+')
    index.write('<html>\n<body>\n')

    # Download the images into the destination dir
    for i in range(len(img_urls)):
        # build image name string
        img_name = "img" + str(i)

        # build image path string
        img_link = os.path.join(dest_dir, img_name)

        # Print a status for each img
        print("Retrieving " + img_name + "...")

        # Download each image to the destination dir
        urllib.request.urlretrieve(img_urls[i], img_link)

        # Add the image to the index.html file
        index.write('<img src="' + img_name + '">')

    # Wrap up the index file
    index.write("\n</body>\n</html>")
    index.close()


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
