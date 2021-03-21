import os

from flask import Flask
from flask import render_template

from . import apiratp

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')

@app.route('/')
def build_page():

    cfgline = open(app.instance_path + '/TERRE.conf', 'r')
    conflines = cfgline.readlines()

    ratpclient = apiratp.apiratp(app.instance_path + '/' + conflines[0].strip())

    html = render_template('base.html');

    conflines.pop(0)

    for line in conflines:
        tokens = line.strip().split('\t')
        if tokens[0][0] == 'R':
            html = html + table_RER(ratpclient, tokens[0], tokens[1], tokens[2], maxlines=int(tokens[3]), margin=int(tokens[4]), otherstops=tokens[5:])
        elif tokens[0][0] == 'B' or tokens[0][0] == 'M' or tokens[0][0] == 'T':
            html = html + table_busmetro(ratpclient, tokens[0], tokens[1], tokens[2], margin=int(tokens[4]), maxlines=int(tokens[3]))
        elif tokens[0] == 'twitter':
            html = html + twitter()

    return html


def table_RER(ratpclient, line, station, sens, margin=0, otherstops=[], maxlines=0):
    m = ratpclient.missions_rer(line, station, sens, margin=margin, otherstops=otherstops, maxlines=maxlines)
    name = "RER " + line[1]
    return render_template('missions_rer.html', missions=m, otherstops=otherstops, name=name, station=station, sens=sens)

def table_busmetro(ratpclient, line, station, sens, margin=0, maxlines=0):
    m = ratpclient.missions_busmetro(line, station, sens, maxlines=maxlines)
    if line[0] == 'M':
        name = 'Métro ' + line[1:]
    elif line[0:2] == 'BT':
        name = 'Tram ' + line[2:]
    elif line[0] == 'B':
        name = 'Bus ' + line[1:]
    return render_template('missions_busmetro.html', missions=m, name=name, station=station, sens=sens)

def twitter():
    return render_template('twitter.html')
