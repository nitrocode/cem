# Chrome Extension Manager

The missing package manager for Google Chrome.

Eventually, it will be nice to create this for all browsers. Once we have support for Mozilla Firefox, the app will be renamed BAM for Browser Addon Manager.

## Install

    pip install -r requirements.txt
    install cem.py /usr/local/bin/cem

## Run

    $ cem tampermonkey behindtheoverlay autoscroll
    Tampermonkey downloaded to extensions/dhdgffkkebhmkfjojejmpbldmpobfkfo.crx
    BehindTheOverlay downloaded to extensions/ljipkdpcjbmhkdjjmbbaggebcednbbme.crx
    AutoScroll downloaded to extensions/occjjkgifpmdgodlplnacmkejpdionan.crx

Search terms can also be put into a `Cemfile` and the app will read the file.

After the app downloads the extensions, you will have to manually add the `crx` files which is NOT user friendly at all... working on a way to automate this.

## TODO

* prompt to install with `-y` option
* create `install` keyword
    * `cem install tampermonkey`
* create `search` keyword
* find a way to [automatically install extensions](https://developer.chrome.com/extensions/external_extensions) for every OS
* support for Firefox and a `firefox` (`ff`) and `chrome` (`c`) keywords
    * `cem ff install greasemonkey`
    * `cem c install tampermonkey`
* rename app to BAM
    * `bam ff install greasemonkey`
    * rename `Cemfile` to `Bamfile` and place browser before extension name

## Future

* create a pip package
* create a brew formula
* select a browser, select a profile, and dump current installed extensions and settings
* profile creation
    * chrome flags and settings
    * firefox settings
