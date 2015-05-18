import os
from flask import Flask, request, render_template, Markup
import markdown
from GID_Mint import *


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


app = Flask(__name__)


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
    # This works nicely with Heroku
    port = int(os.environ.get('PORT', 5000))
    if port is 5000:
        host = None
    else:
        host = '0.0.0.0'

    app.run(host=host, port=port)
