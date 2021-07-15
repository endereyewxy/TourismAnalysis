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
        data = [row.asDict() for row in getattr(D, api)]
        if api == 'play_way_percent_topn':
            data = data[:int(flask.request.args.get('num', ''))]
        return {'error_code': 100, 'data': data}
    except AttributeError:
        flask.abort(404)
    except ValueError:
        return {'error_code': 101}
