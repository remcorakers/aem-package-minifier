# AEM package minifier

Python script to minify AEM content packages by replacing original asset files by small dummy files. Use case is when AEM content is transferred from production instances to accept,  test and dev environments to streamline content in all environments. Its good practice to do this frequently, but when assets are large this can become time and resource consuming.

## Prerequisites

- Python 3 (Python 2 has issues with zipfiles larger than 2Gb)

## Getting started

Clone this repository and minify an AEM content package (zip file) by executing the following command: `python3 aem_package_minifier.py -f /path/to/content/package.zip`

## Minification details

- Currently the script replaces content items of the following file types: bmp, gif, jpg, mp3, mp4, ogg, pdf, png, zip.
- Only the `original` files in rendition directories will be replaced; other renditions are left untouched.

## Credits

Minified files are retrieved from https://github.com/mathiasbynens/small.
