# GID-Mint

[Derek Merck](email:derek_merck@brown.edu)  

<https://github.com/derekmerck/GID-Mint>


## Overview

Flask app to create 1-way hashes for global identifiers in study anonymization.
 
It is intended to be used as an adjunct with an automatic anonymization framework like [XNAT's](http://www.xnat.org) [DicomEdit](http://nrg.wustl.edu/software/dicomedit/)

A reference web implementation of the most recent master branch is available at <http://get-a-gid.heroku.com>.


### Dependencies

- Python 2.7
- [Flask](http://flask.pocoo.org)


## Usage

For a local instance:

```
$ python GID-Mint.py &
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
$ wgets  http://localhost:5000/ggid?name=derek_merck&dob=030771
  77d33b6f82dc6482fed324c95754c77e
```

### Generic Global Identifier (GGID)

This is the basic functionality, which is simply intended to be unique and can be generated based on any consistent set object-specific variables.

e.g., `localhost:5000/ggid?ssn=123456789`

For all methods, input variable values are converted to lowercase and sorted into alphabetical order.  Output is the 32-hexdigit [md5](http://en.wikipedia.org/wiki/MD5) hash of the result.


### Global Subject Identifier (GSID)

A GSID is intended to be unique and shared across institutions.

Creating a GSID requires input:
- `fname` = given name
- `minitial` = middle initial
- `lname` = last name
- `dob` = date of birth (8-digits, xxyyzzzz)

e.g., `localhost:5000/gsi?fname=derek&minitial=l&lname=merck&dob=xxyyzzzz`


### Global Institutional Record Identifier (GIRI)

A GIRI is intended to be unique and shared within an institution.

Creating an ISI requires input:
- `institution` = institution code (RIH, TMH, etc.)
- `record_id` = medical or administrative record number

e.g., `localhost:5000/giri?institution=RIH&record_id=mrn100`


## Acknowledgements

- Inspired in part by [NDAR](https://ndar.nih.gov/ndarpublicweb/tools.html) and [FITBIR](https://fitbir.nih.gov) GUID schema.
- Thanks for the Heroku Flask tutorial at <http://virantha.com/2013/11/14/starting-a-simple-flask-app-with-heroku/>


## License

[MIT](http://opensource.org/licenses/mit-license.html)



## Future Work

1. Database:
  - Link identifiers -- connect an already generated identifier hash to a different hash.  For example, an already generated IRI (based on MRN) could be linked to a new GSI, so relevant GSI queries would return the original IRI hash.
  - Check for collisions, query for whether a hash is in use (for a given namespace)

2. Translate requests directly to the NDAR GUID generator