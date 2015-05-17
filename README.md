# GlobalIdMaker

[Derek Merck](email:derek_merck@brown.edu)  

<https://github.com/derekmerck/GlobalIdMaker>


## Overview

Flask app to create 1-way hashes for study anonymization.
 
It is intended to be used as an adjunct with an automatic anonymization framework like [XNAT's](http://www.xnat.org) [DicomEdit](http://nrg.wustl.edu/software/dicomedit/)


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

- Inspired in part by [NDAR](https://ndar.nih.gov/ndarpublicweb/tools.html) and [FITBIR](https://fitbir.nih.gov) GUID schema.


## License

[MIT](http://opensource.org/licenses/mit-license.html)



## Future Work

1. Database:
  - Link identifiers -- connect an already generated identifier hash to a different hash.  For example, an already generated IRI (based on MRN) could be linked to a new GSI, so relevant GSI queries would return the original IRI hash.
  - Check for collisions, query for whether a hash is in use (for a given namespace)

2. Translate requests directly to the NDAR GUID generator