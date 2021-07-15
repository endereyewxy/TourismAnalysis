import flask

from data import update_raw_database, D

app = flask.Flask('tourism-analysis')

update_raw_database('/home/endereye/Workspace/TourismAnalysis/spiders/db/data.db.050')


@app.route('/<htm>.html')
def handle_htm(htm: str):
    return flask.render_template(htm.lstrip('/') + '.html')


@app.route('/api/<api>')
def handle_api(api: str):
    try:
        return {'error_code': 100, 'data': [row.asDict() for row in getattr(D, api)]}
    except AttributeError:
        flask.abort(404)
