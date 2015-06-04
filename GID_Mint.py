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

# First 8 bytes of 32 = 64 bits = 2^64 values
bitspace = 64  # Keeping the id's short has some advantages for usability

# Name file should be definable separately
name_file = "shakespeare_names.csv"


names_dict = {}
with open(name_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        names_dict[row['Base32']] = row


def get_pname_for_gid(args):
    # TODO: Need some better error checking
    gid = args.get('gid')
    if gid is not None:
        return'^'.join([
            names_dict[gid[0]]['Last'],
            names_dict[gid[1]]['First'],
            names_dict[gid[2]]['Initial'],
            names_dict[gid[3]]['Prefix'],
            names_dict[gid[4]]['Suffix']
            ])
    else:
        return "Request is malformed"


def get_pmdname_for_gid(args):
    # Placeholder for ordering physician name, "F Last DeG"
    # TODO: Need some better error checking
    gid = args.get('gid')
    if gid is not None:
        return'^'.join([
            names_dict[gid[0]]['Author'],
            names_dict[gid[1]]['Initial'],
            '',
            '',
            names_dict[gid[2]]['Degree']
            ])
    else:
        return "Request is malformed"

from datetime import date
import struct

def get_pdob_for_dob_and_gid(args):
    # TODO: Need some better error checking
    dob = args.get('dob')
    gid = args.get('gid')
    if dob is not None and gid is not None:
        if len(dob) < 4:
            # This thing is empty or malformed, so return something obviously wrong
            return '19000101'
        year = int(dob[:4])
        start_date = date(day=1, month=1, year=year).toordinal()
        end_date = date(day=31, month=12, year=year).toordinal()
        [number] = struct.unpack("<H", hashlib.sha256(gid).digest()[:2])
        t = number / float(0xFFFF)
        dif = end_date - start_date
        random_day =int(start_date + t * dif)
        new_dob = date.fromordinal(random_day)
        return new_dob.strftime('%Y%m%d')
    else:
        return "Request is malformed"


def get_gid(_args, reqs=None):

    # _args is immutable
    args = _args.copy()

    # Parse 'pname' into 'fname' and 'lname' if it is declared in args
    if args.get('pname') is not None:
        args['lname'] = ''
        args['fname'] = ''

        if args.get('pname') is u'':
            pass
        elif len(args.get('pname').split('^')) > 1:
            # Plausible DICOM format
            args['lname'], args['fname'] = args['pname'].split('^')[:2]
            # Do some clean up
            args['lname'] = args['lname'].split(' ')[0]  # Get rid of any suffix
            args['fname'] = args['fname'].split(' ')[0]  # Get rid of any middle initial
        else:
            # Just stash it
            args['lname'] = args['pname']

        del args['pname']

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
    # m = hashlib.md5()
    m = hashlib.sha256()
    for val in values:
        m.update(val.lower())
    m.update(salt)
    # byte slicing -- divide target bitspace by 8
    return base64.b32encode((m.digest()[:bitspace/8])).strip('=')



if __name__ == '__main__':

    args = {'name': 'Derek'}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)
    logger.info(get_pname_for_gid({'gid': gid}))

    args = {'pname': 'Merck^Derek^L^^', 'dob': '19710101'}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)
    logger.info(get_pname_for_gid({'gid': gid}))

    args = {'pname': 'Merck PhD^Derek L^^^', 'dob': '19710101'}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)
    logger.info(get_pname_for_gid({'gid': gid}))

    args = {'fname': 'Derek', 'lname': 'Merck', 'dob': '19710101'}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)
    logger.info(get_pname_for_gid({'gid': gid}))

    logger.info(get_pdob_for_dob_and_gid({'gid': gid, 'dob': '19710101'}))

    args = {'institution': 'RIH', 'record_id': '111222333'}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)

    args = {'pname': 'Merck PhD^Derek', 'dob': '19710101'}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)
    logger.info(get_pmdname_for_gid({'gid': gid}))

    args = {'pname': 'derek merck'}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)
    logger.info(get_pmdname_for_gid({'gid': gid}))

    args = {}
    gid = get_gid(args)
    logger.info(args)
    logger.info(gid)
    logger.info(get_pmdname_for_gid({'gid': gid}))
