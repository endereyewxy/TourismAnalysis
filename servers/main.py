import flask

from data import update_raw_database, D

app = flask.Flask('tourism-analysis')

update_raw_database('loct.db.050')


@app.route('/')
def root():
    return flask.redirect('/lines3d.html')


@app.route('/<htm>.html')
def handle_htm(htm: str):
    return flask.render_template(htm.lstrip('/') + '.html')


@app.errorhandler(404)
def handle_404(_):
    return flask.render_template('404.html'), 404


@app.route('/api/<api>')
def handle_api(api: str):
    try:
        if api == 'spot_hot':
            prov = flask.request.args.get('prov', '')
            return {'code': 100, 'data': D.spot_hot[prov][0], 'max_hot': D.spot_hot[prov][1]}
        data = [row.asDict() for row in getattr(D, api)]
        if api == 'month_and_people':
            year1 = int(flask.request.args.get('year1', ''))
            year2 = int(flask.request.args.get('year2', ''))
            data = [
                {
                    'year': year1,
                    'month_and_people': [{'month': obj['date_start_m'], 'people_num': obj['count']}
                                         for obj in data if obj['date_start_y'] == year1]
                },
                {
                    'year': year2,
                    'month_and_people': [{'month': obj['date_start_m'], 'people_num': obj['count']}
                                         for obj in data if obj['date_start_y'] == year2]
                }
            ]
        if api == 'play_way_percent_topn':
            data = data[:int(flask.request.args.get('num', ''))]
        if api == 'prov_hot':
            new_data = {}
            for obj in data:
                new_data.setdefault(obj['year'], []).append({'name': obj['prov'], 'hot': obj['hot']})
            data = [{'year': year, 'prov': prov, 'max': max(map(lambda x: x['hot'], prov))}
                    for year, prov in new_data.items()]
        if api == 'city_everypeolple_avg_cost':
            new_data = {}
            for obj in data:
                new_data.setdefault(obj['year'], []).append({'name': obj['prov'], 'avg_cost': obj['avg(cost)']})
            data = [{'year': year, 'prov': prov} for year, prov in new_data.items()]
        if api == 'quarter_days':
            quarters = {days: [0, 0, 0, 0] for days in range(1, 6)}
            for obj in data:
                quarters[obj['days']][obj['quarter']] += obj['count']
            data = [{'days': key, 'quarter_list': val} for key, val in quarters.items()]
        return {'error_code': 100, 'data': data}
    except AttributeError:
        flask.abort(404)
    except ValueError:
        return {'error_code': 101}
