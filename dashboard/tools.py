import os
import json
import plotly
import plotly.graph_objects as go


def loadfile(path):
    """Load data by path"""
    with open(path) as f:
        return f.read()


def load(token, kind, name=None):
    """Load data from storage

    Args:
        token (str): token of user.
        kind {'figures', 'data'}: type of data.
        name (str, optional): name of file.
    """
    if name:
        return loadfile('storage/{token}/{kind}/{name}')

    else:
        return [loadfile(f'storage/{token}/{kind}/{name}')
                for name in os.listdir(f'storage/{token}/{kind}')]


def write(source, token, kind, name=None):
    name = name or source['name']
    with open(f"storage/{token}/{kind}/{name}", "w") as f:
        if isinstance(source, (list, dict)):
            json.dump(source, f)

        else:
            f.write(source)


def createfigure(data):
    fig = {
        'data': [go.Scatter(x=data['x'], y=data['y'])],
        'layout': {
            'title': {'text': data['title']},
            'xaxis': {'title': {'text': data['xlabel']}},
            'yaxis': {'title': {'text': data['ylabel']}},
        }
    }
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
