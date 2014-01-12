# wikitree-api

This library provides access to WikiTree genealogical data. It uses the microdata embedded in WikiTree's public pages.

## Installation

There are a few different ways you can install wikitree-api:

* Download the zipfile with the [latest code](https://github.com/jeroenl/wikitree-api/archive/master.zip) and install it. 
* Checkout the source: `git clone git://github.com/jeroenl/wikitree-api` and install it yourself.

## Usage

To retrieve data, use the classes in the `wikitree.public` package. Each requires an identifier or full URL to be passed when creating the object. For example:

```python
# Pass an identifier or full URL
p = Person('Sloan-518')
p2 = Person('http://www.wikitree.com/wiki/Carvell-50')

# The data for this person is only retrieved when first accessing any of its properties.
p.name
# 'Clayton Sloan'

# Any references to other persons are returned as Person objects, which makes it easy to retrieve additional details.
p.children[0].birthDate
# '1922-05-07'
```
