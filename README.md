# GlobalIdMaker

[Derek Merck](email:derek_merck@brown.edu)  

<https://github.com/derekmerck/GlobalIdMaker>


## Overview

Flask app to create 1-way hashes for study anonymization.
 
It is intended to be used as an adjunct with an automatic anonymization framework like XNAT's DICOMEdit.


## Installation

`$ pip install git+https://github.com/derekmerck/GlobalIdMaker`


### Dependencies

- Python 2.7
- Flask


## Usage

```
$ python GlobalIdMaker.py &
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
$ wgets  http://localhost:5000/aoi?name=derek_merck&dob=030771
  77d33b6f82dc6482fed324c95754c77e
```

Input variable values are converted to lowercase and cleaned.  Output is a 64bit hex string.


### Arbitrary Object Identifier (AOI)

This is the basic functionality, which is simply intended to be unique and can be generated based on any consistent set object-specific variables.

e.g., `localhost:5000/aoi?ssn=123456789`

In the future, Given a GSI, an Institutional Subject Identifier (ISI) can be LINKED to it, so querying the ISI returns the subject GSI


### Global Subject Identifier (GSI)

A GSI is intended to be unique and shared across institutions.

Creating a GSI requires input:
- `fname` = given name
- `lname` = last name
- `sex` = sex at birth (M/F)
- `dob` = date of birth (8-digits, xxyyzzzz)

e.g., `localhost:5000/gsi?fname=derek&lname=merck&sex=M&dob=03071971`


### Institutional Record Identifier (IRI)

An IRI is intended to be unique and but will be common only within an institution.

Creating an ISI requires input:
- `institution` = institution code (RIH, TMH, etc.)
- `record_id` = medical or administrative record number

e.g., `localhost:5000/isi?institution=RIH&record_id=mrn100`


## Acknowledgements

- Based in part on NDAR's GUID as implemented in FITBIR


## License

[MIT](http://opensource.org/licenses/mit-license.html)



## Future Work

1. Database:
  - Link an already generated ISI (based on MRN) or AOI to a GSI, so that the GSI always returns the original hash
  - Check for collisions, query for whether a hash is in use

2. Translate to NDAR GUID generator