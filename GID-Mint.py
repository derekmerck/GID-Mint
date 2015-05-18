"""
GID-Mint
A Flask app to create 1-way hashes for study anonymization

[Derek Merck](derek_merck@brown.edu)
Spring 2015

<https://github.com/derekmerck/GID-Mint>

Dependencies: Flask

See README.md for usage, notes, and license info.

"""
import os
import markdown
import logging
import hashlib
from flask import Flask, request, render_template, Markup

__package__ = "GID-Mint"
__description__ = "Flask app to create 1-way hashes for study anonymization"
__url__ = "https://github.com/derekmerck/GID-Mint"
__author__ = 'Derek Merck'
__email__ = "derek_merck@brown.edu"
__license__ = "MIT"
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


# Salting the UID generator will make any id's specific to a particular instance of this script
salt = ''

# TODO: Add sqlite database in here to keep track of assigned ids and links for a namespace (salting)

app = Flask(__name__)


def check_vars(reqs, args):
    # TODO: Should also check correct format for dob (i.e., xx-yy-zzzz), mrn (i.e., 10 digits at Lifespan), etc.
    values = []
    for key in reqs:
        if key not in args:
            # Failed completeness
            logger.warn("Failed completeness")
            return None
        else:
            values.append(args.get(key, ''))
    return values


def hash_it(values):
    m = hashlib.md5()
    for val in values:
        m.update(val.lower())
    m.update(salt)
    return m.hexdigest()


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

@app.route('/')
def index():
    content = read('README.md')
    content = Markup(markdown.markdown(content))
    return render_template('index.html', **locals())


@app.route('/ggid')
def get_generic_global_id():
    return hash_it(request.args.values())


@app.route('/giri')
def get_global_institutional_record_id():
    reqs = ['institution', 'record_id']
    values = check_vars(reqs, request.args)

    if values is not None:
        return hash_it(values)
    else:
        return "Request has missing variables"


@app.route('/gsid')
def get_global_subject_id():
    reqs = ['fname', 'lname', 'dob']
    vars = check_vars(reqs, request.args)

    if vars is not None:
        return hash_it(vars)
    else:
        return "Request has missing variables"

@app.route('/ndar')
def get_ndar_guid():
    # TODO: Add NDAR translator
    return "NDAR GUID translator is not implemented yet"

@app.route('/link')
def link_hashes():
    # TODO: Add DB for hash linking
    return "hash linking is not implemented yet"



if __name__ == '__main__':

    # Setup logging
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info('version %s' % __version__)

    app.run()
