# GID_Mint

[Derek Merck](email:derek_merck@brown.edu)  

<https://github.com/derekmerck/GID_Mint>


## Overview

Flask app to create 1-way hashes for global identifiers in study anonymization.
 
It is intended to be used as an adjunct with an automatic anonymization framework like [XNAT's](http://www.xnat.org) [DicomEdit](http://nrg.wustl.edu/software/dicomedit/)

A reference web implementation of the most recent master branch is available at <http://get-a-gid.herokuapp.com>.


### Dependencies

- Python 2.7
- [Flask](http://flask.pocoo.org)


## Usage

To create a local instance:

```bash
$ python GID-Mint.py &  
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)  
$ curl -4 localhost:5000/ggid?name=derek  
  O2PSXCTVDAGB5DE3G7GLZ6PAJE  
```

To create a [Heroku](http://www.heroku.com) instance:

```bash
$ heroku create
$ git push heroku master
$ heroku ps:scale web=1
$ curl "http://get-a-gid.herokuapp.com/ggid?name=derek  
  O2PSXCTVDAGB5DE3G7GLZ6PAJE 
```
  
To use it as a Python library:

```python
> from GID_Mint import get_gid
> d = { 'name':'derek' }
> get_gid( d )
O2PSXCTVDAGB5DE3G7GLZ6PAJE
```


### Generic Global Identifier (GGID)

This is the basic functionality, which is simply intended to be unique and can be generated based on any consistent set object-specific variables.

Example: <http://get-a-gid.herokuapp.com/ggid?name=derek>  
`O2PSXCTVDAGB5DE3G7GLZ6PAJE`

Generation method:

1. Input variable values are converted to lowercase and sorted into key-alphabetical order.
2. The [md5](http://en.wikipedia.org/wiki/MD5) hash of the result is computed.
3. The result is encoded into [base32](http://en.wikipedia.org/wiki/Base32) and padding symbols are stripped.


### Global Subject Identifier (GSID)

A GSID is intended to be unique and shared across institutions.

Creating a GSID requires input:

- `fname` = given name
- `lname` = last name
- `dob` = date of birth (8-digits, xxyyzzzz)

<http://get-a-gid.herokuapp.com/gsid?fname=derek&lname=merck&dob=01011999>  
`AXC3YH4QZE54EYBUFSHKQNAO4A`


### Global Institutional Record Identifier (GIRI)

A GIRI is intended to be unique and shared within an institution.

Creating an ISI requires input:

- `institution` = institution code (Lifespan, etc.)
- `record_id` = medical or administrative record number

<http://get-a-gid.herokuapp.com/giri?institution=RIH&record_id=mrn100>  
`L6G7QENCBUURAFFE75WMG6JDXE`


## Acknowledgements

- Inspired in part by [NDAR](https://ndar.nih.gov/ndarpublicweb/tools.html) and [FITBIR](https://fitbir.nih.gov) GUID schema.
- Thanks for the [Heroku](http://www.heroku.com) Flask tutorials at <http://virantha.com/2013/11/14/starting-a-simple-flask-app-with-heroku/> and <http://stackoverflow.com/questions/17260338/deploying-flask-with-heroku>


## License

[MIT](http://opensource.org/licenses/mit-license.html)


## Future Work

- Use a database to link an already generated identifier hash to a different hash.  For example, an already generated MRN-based GIRI could be linked to a new GSID, so relevant GSID queries would return the original GIRI hash.

- Check for collisions in a given namespace and, if needed, create a new hash and link as above

- Translate requests directly to the NDAR GUID generator