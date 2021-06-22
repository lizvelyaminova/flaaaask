from flask import Flask, render_template

import config
import requests


app = Flask(__name__)


@app.route('/')
def index():
    data = get_data()
    cleaned_data = prepare_data(data)
    except Exception as e:
        return render_template('error.html', err=str(e))

    return render_template('index.html', data = cleaned_data)


def get_data():
    rows_url = config.API_MAIN_URL + 'datasets/1102/rows'
    count_url = config.API_MAIN_URL + 'datasets/1102/count'

    r = requests.get(count_url, params={'api_key' : config.API_KEY})
    if not r.ok:
        raise Exception('Failed to get dataset rows count: {0'.format(r.text))

    limit = int(r.text)
    skip = 0
    step = 100

    data = []
    while len(data) < limit:
        params = {
            '$top': step,
            '$skip': skip,
            'api_key': config.API_KEY,
        }

        r = requests.get(rows_url, params = params)
        if not r.ok:
            raise Exception ('Failed to load rows: {0'.format(r.text))

        print ('Response is: ', r.json())
        j = r.json()
        for element in j:
            data.append(element)

        skip += step

    return data

def prepare_data(data):
    result = []

    for element in data:
        if 'Cells' in element and element['Cells'] is not None:
            cell = element['Cells']

            if 'CompanyName' in cell and 'DebtSum' in cell:
                result.append({
                    'company_name': cell['CompanyName'],
                    'sum_count': cell['DebtSum'],

                })

    return result



data = get_data()
cleaned_data = prepare_data(data)

if __name__ == '__main__':
    app.run()
