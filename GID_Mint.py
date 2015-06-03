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
import csv


__package__ = "GID_Mint"
__description__ = "Flask app to create 1-way hashes for study anonymization"
__url__ = "https://github.com/derekmerck/GID_Mint"
__author__ = 'Derek Merck'
__email__ = "derek_merck@brown.edu"
__license__ = "MIT"
__version_info__ = ('1', '3', '0')
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

# Name file should be definable separately
name_file = "shakespeare_names.csv"


names_dict = {}
with open(name_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        names_dict[row['Base32']] = row


def get_pname_for_gid(gid):
    pname = '^'.join([
        names_dict[gid[0]]['Last'],
        names_dict[gid[1]]['First'],
        names_dict[gid[2]]['Middle'],
        names_dict[gid[3]]['Prefix'],
        names_dict[gid[4]]['Suffix']
        ])
    return pname



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



if __name__ == '__main__':

    gid = get_gid({'pname': 'Merck^Derek^L'})
    logger.info(gid)
    logger.info(get_pname_for_gid(gid))

    gid = get_gid({'pname': 'Merck^Lisa^H'})
    logger.info(gid)
    logger.info(get_pname_for_gid(gid))

    logger.info(get_pname_for_gid('AXC3YH4QZE54EYBUFSHKQNAO4A'))