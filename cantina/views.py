"""
Views for cantina app
"""

import itertools

from flask import Flask, render_template
from bokeh.plotting import Figure
from bokeh.palettes import Category20
from bokeh.models import Legend
from bokeh.embed import components
import fiasco
import roman

from cantina import app


@app.route('/')
@app.route('/index')
def index():
    masterlist = fiasco.util.get_masterlist(fiasco.util.setup_paths()['ascii_dbase_root'])['ion_files']
    elements = set([m.split('_')[0] for m in masterlist if m[0] != '.'])
    return render_template('index.html', elements=elements, title='cantina')


@app.route('/element-<element>')
def display_element(element):
    el = fiasco.ElementBase(element)
    ion_list = [(i.split('_')[0], i.split('_')[1], roman.toRoman(int(i.split('_')[1]))) 
                for i in el.ions]
    tmp_ion = el['{}_1'.format(element)]
    return render_template('element.html',
                           element=element,
                           title='cantina: {}'.format(element.capitalize()),
                           ions=ion_list,
                           abundances=tmp_ion.abundance.fields,
                           ioneqs=tmp_ion.ioneq.fields,
                           breadcrumbs=[('element-{}'.format(element), element.capitalize())])


@app.route('/element-<element>/ioneq-<ioneq_name>')
def plot_ioneq(element, ioneq_name):
    el = fiasco.ElementBase(element)
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"
    p = Figure(plot_width=900, plot_height=500, x_axis_type="log", tools=TOOLS)
    colors = itertools.cycle(Category20[20])
    legend_items = []
    for ion, c in zip(el.ions, colors):
        tmp = p.line(el[ion].ioneq[ioneq_name]['temperature'],
               el[ion].ioneq[ioneq_name]['ionization_fraction'],
               color=c)
        ion_name = ' '.join([ion.split('_')[0].capitalize(),roman.toRoman(int(ion.split('_')[1]))])
        legend_items.append(('{}'.format(ion_name),[tmp]))
    p.xaxis.axis_label = 'T [K]'
    p.yaxis.axis_label = 'Ionization Fraction'
    legend = Legend(items=legend_items, location=(0,1))
    legend.click_policy = 'hide'
    legend.orientation = 'vertical'
    legend.label_text_font_size = '8pt'
    p.add_layout(legend, 'right')
    plot_script, plot_div = components(p)
    breadcrumbs = [('/element-{}'.format(element), element.capitalize()),
                   ('/element-{}/ioneq-{}'.format(element, ioneq_name), ioneq_name)]
    return render_template('ioneq.html', plot_script=plot_script, plot_div=plot_div,
                           title='cantina: {}'.format(element.capitalize()), breadcrumbs=breadcrumbs)


@app.route('/element-<element>/ion-<ion>')
def display_ion(element, ion):
    pretty_ion = ' '.join([ion.split('_')[0].capitalize(),roman.toRoman(int(ion.split('_')[1]))])
    breadcrumbs = [('/element-{}'.format(element), element.capitalize()),
                   ('/element-{}/ion-{}'.format(element, ion), pretty_ion)]
    return render_template('ion.html', breadcrumbs=breadcrumbs)

