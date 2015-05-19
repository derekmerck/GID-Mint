"""
GID_Mint
A library and Flask app to create 1-way hashes for study anonymization

[Derek Merck](derek_merck@brown.edu)
Spring 2015

<https://github.com/derekmerck/GID-Mint>

Dependencies: Flask

See README.md for usage, notes, and license info.

"""
import logging
import hashlib
import base64


__package__ = "GID_Mint"
__description__ = "Flask app to create 1-way hashes for study anonymization"
__url__ = "https://github.com/derekmerck/GID_Mint"
__author__ = 'Derek Merck'
__email__ = "derek_merck@brown.edu"
__license__ = "MIT"
__version_info__ = ('0', '2', '0')
__version__ = '.'.join(__version_info__)


# Setup logging
logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info('version %s' % __version__)


# Salting the UID generator will make any id's specific to a particular instance of this script
salt = ''


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



