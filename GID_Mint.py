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
import logging
import hashlib
import base64
from flask import Flask, request, render_template, Markup
import markdown

__package__ = "GID_Mint"
__description__ = "Flask app to create 1-way hashes for study anonymization"
__url__ = "https://github.com/derekmerck/GID_Mint"
__author__ = 'Derek Merck'
__email__ = "derek_merck@brown.edu"
__license__ = "MIT"
__version_info__ = ('0', '1', '1')
__version__ = '.'.join(__version_info__)


# Salting the UID generator will make any id's specific to a particular instance of this script
salt = ''

# TODO: Add sqlite database in here to keep track of assigned ids and links for a namespace (salting)

app = Flask(__name__)


def get_gid(args, reqs=None):

    if reqs:
        values = check_vars(reqs, args)
    else:
        values = [args[key] for key in sorted(args)]

    if values is not None:
        return hash_it(values)
    else:
        return "Request is malformed"


def check_vars(reqs, args):
    reqs = sorted(reqs)
    # TODO: Should also check correct format for dob (i.e., xx-yy-zzzz), mrn (i.e., 10 digits at Lifespan), ssn, etc.
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
    return base64.b32encode(m.digest()).strip('=')


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
    return get_gid(request.args)


@app.route('/giri')
def get_global_institutional_record_id():
    reqs = ['institution', 'record_id']
    return get_gid(request.args, reqs)


@app.route('/gsid')
def get_global_subject_id():
    reqs = ['fname', 'lname', 'dob']
    return get_gid(request.args, reqs)


@app.route('/ndar')
def get_ndar_guid():
    # TODO: Add NDAR translator
    return "NDAR GUID translator is not implemented yet"


@app.route('/link')
def link_hashes():
    # TODO: Add DB for hash linking
    return "Hash linking is not implemented yet"


if __name__ == '__main__':

    # Setup logging
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info('version %s' % __version__)

    # This works nicely with heroku
    port = int(os.environ.get('PORT', 5000))
    if port is 5000:
        host = None
    else:
        host = '0.0.0.0'

    app.run(host=host, port=port)
