import os
from flask import Flask, request, render_template, Markup
import markdown
import GID_Mint
from GID_Mint import logger, get_gid, get_yob_for_dob, get_pname_for_gid, get_pmdname_for_gid


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


app = Flask(__name__)


@app.route('/')
def index():
    content = read('README.md')
    content = content + "\n\nversion {0}".format(GID_Mint.__version__)
    content = Markup(markdown.markdown(content, ['markdown.extensions.extra']))
    return render_template('index.html', **locals())


@app.route('/version')
def version():
    logger.info(GID_Mint.__version__)
    return "version {0}".format(GID_Mint.__version__)


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


@app.route('/ppname')
def get_placeholder_pname():
    return get_pname_for_gid(request.args)


@app.route('/pmdname')
def get_placeholder_pmdname():
    return get_pmdname_for_gid(request.args)


@app.route('/yob')
def get_placeholder_yob():
    return get_yob_for_dob(request.args)


@app.route('/ndar')
def get_ndar_guid():
    # TODO: Add NDAR translator
    return "NDAR GUID translator is not implemented yet"


@app.route('/link')
def link_hashes():
    # TODO: Add DB for hash linking
    return "Hash linking is not implemented yet"


if __name__ == '__main__':
    # This works nicely with Heroku
    port = int(os.environ.get('PORT', 5000))
    if port is 5000:
        host = None
    else:
        host = '0.0.0.0'

    app.run(host=host, port=port)
