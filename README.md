# GID_Mint

[Derek Merck](email:derek_merck@brown.edu)  

<https://github.com/derekmerck/GID_Mint>


## Overview

Python library and Flask app to generate 1-way hashes for globally consistent identifiers in study anonymization.
 
It is intended to be used as an adjunct with an automatic anonymization framework like [XNAT's](http://www.xnat.org) [DicomEdit](http://nrg.wustl.edu/software/dicomedit/)

A reference web implementation of the most recent master branch is available at <http://get-a-gid.herokuapp.com>.


## Dependencies

- Python 2.7
- [Flask](http://flask.pocoo.org)


## Usage

To use it as a Python library:

````python
>>> from GID_Mint import get_gid
>>> d = { 'name':'derek' }
>>> get_gid( d )
O2PSXCTVDAGB5DE3G7GLZ6PAJE
````

To create a local server instance:

```bash
$ python GID-Mint.py &  
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)  
$ curl -4 "localhost:5000/ggid?name=derek"
  O2PSXCTVDAGB5DE3G7GLZ6PAJE  
```

To create a public [Heroku](http://www.heroku.com) server instance:

```bash
$ heroku create
$ git push heroku master
$ heroku ps:scale web=1
$ curl "http://get-a-gid.herokuapp.com/ggid?name=derek"
  O2PSXCTVDAGB5DE3G7GLZ6PAJE 
```

Single dyno Heroku instances are free to run.


### Generic Global Identifier (GGID)

This is the basic functionality, which is simply intended to be unique and can be reproducibly generated against any consistent set object-specific variables.

Generation method:

1. Input variable values are converted to lowercase and sorted into key-alphabetical order.
2. The [md5](http://en.wikipedia.org/wiki/MD5) hash of the result is computed.
3. The result is encoded into [base32](http://en.wikipedia.org/wiki/Base32) and padding symbols are stripped.

Example: <http://get-a-gid.herokuapp.com/ggid?name=derek>  
`O2PSXCTVDAGB5DE3G7GLZ6PAJE`


### Global Subject Identifier (GSID)

A GSID is intended to be unique and shared across institutions.

It is generated as a GGID using specific, required input variables:

- `fname` = given name
- `lname` = last name
- `dob` = date of birth (8-digits, xxyyzzzz)

<http://get-a-gid.herokuapp.com/gsid?fname=derek&lname=merck&dob=01011999>  
`AXC3YH4QZE54EYBUFSHKQNAO4A`

It is also possible to pass in a [DICOM patient name format][pname_fmt] directly, and GID_Mint will parse it properly.

[pname_fmt]:(http://support.dcmtk.org/docs/classDcmPersonName.html#f8ee9288b91b6842e4417185d548cda9)

<http://get-a-gid.herokuapp.com/gsid?pname=Merck^Derek^^^&dob=01011999>  
`AXC3YH4QZE54EYBUFSHKQNAO4A`

### Global Institutional Record Identifier (GIRI)

A GIRI is intended to be unique and shared within an institution.

It is generated as a GGID using specific, required input variables:

- `institution` = institution code (Lifespan, etc.)
- `record_id` = medical or administrative record number

<http://get-a-gid.herokuapp.com/giri?institution=RIH&record_id=mrn100>  
`L6G7QENCBUURAFFE75WMG6JDXE`

The `GID_Mint` module knows how to check a set of input variables against a set of required keys, but it has no knowledge of the specific input variables required for a GSID or GIRI.  Relevant requirements must be provided by the accessor: in this case, by the `Get_a_GID` server module based on the `gsid` or `giri` query strings.


### Placeholder Patient Name Generator

Any base32 string with at least 5 values can be used to reproducibly generate a ["John Doe"](http://en.wikipedia.org/wiki/John_Doe) style placeholder name in [DICOM patient name format][pname_fmt].  This is very useful for referencing anonymized data sets according to memorable names.  The algorithm uses only the first 5 base32 A-Z,2-7 values, so there are $32^5$ possible combinations.  

By default the placeholder names are based on Shakespearean characters.  This map omits 12 values, so there are only $32*32*32*26*26=22,151,168$ combinations.

<http://get-a-gid.herokuapp.com/pname?ggid=AXC3YH4QZE54EYBUFSHKQNAO4A>  
`Andronicus^Xanthippe^C^^of York`

The default name map can be easily replaced to match your fancy.


## Acknowledgements

- Inspired in part by the [NDAR](https://ndar.nih.gov/ndarpublicweb/tools.html) and [FITBIR](https://fitbir.nih.gov) GUID schema.
- Thanks for the [Heroku](http://www.heroku.com) Flask tutorials at <http://virantha.com/2013/11/14/starting-a-simple-flask-app-with-heroku/> and <http://stackoverflow.com/questions/17260338/deploying-flask-with-heroku>
- GitHub markdown css from <https://github.com/sindresorhus/github-markdown-css>
- Placeholder names inspired by the [Docker names generator](https://github.com/docker/docker/blob/master/pkg/namesgenerator/names-generator.go)


## License

[MIT](http://opensource.org/licenses/mit-license.html)


## Future Work

- Use a database to link an already generated identifier hash to a different hash.  For example, an already generated MRN-based GIRI could be linked to a new GSID, so relevant GSID queries would return the original GIRI hash.  The main drawback to this is that it would require a single central server.

- Check for collisions in a given namespace and, if needed, create a new hash and link as above.  (Possibly using an alternate hash algorithm when collisions are detected.)

- Translate requests directly to the NDAR GUID generator.