# calvin and hobbes

downloader of calvin-hobbes comics

## Installation

    $ pip install calvin-hobbes-get

## Requirements

* bs4
* grequests

## Usage

    $ # Downloads all calvin-hobbes comics to ~/Downloads/calvin-hobbes
    $ calvin-hobbes-get

    $ # Downloads calvin-hobbes comics [1999-01-03..2012-10-20] to /tmp/calvin-hobbes
    $ calvin-hobbes-get --start=1999-01-03 --end=2012-10-20 --output-dir=/tmp/calvin-hobbes
