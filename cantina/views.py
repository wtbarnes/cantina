from flask import Flask, render_template

import fiasco

from cantina import app


@app.route('/')
@app.route('/index')
def index():
    masterlist = fiasco.util.get_masterlist(fiasco.util.setup_paths()['ascii_dbase_root'])['ion_files']
    elements = set([m.split('_')[0] for m in masterlist if m[0] != '.'])
    return render_template('index.html', elements=elements, title='cantina')

@app.route('/element-<element>')
def display_element(element):
    return render_template('element.html', element=element, title='cantina: {}'.format(element.capitalize()))

