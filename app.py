# -*- coding: utf-8 -*

from flask import Flask, render_template, request, jsonify
import json
import csv
import requests

from datetime import datetime, timedelta

app=Flask(__name__)

@app.route('/price')
def index():
	ticker=request.args.get('ticker').upper()
	end_date=datetime.now().strftime('%Y-%m-%d')
	start_date=(datetime.now()+timedelta(days=-300)).strftime('%Y-%m-%d')
	print(start_date,end_date)
	CSV_URL = 'https://www.quandl.com/api/v3/datasets/WIKI/' + ticker \
					+ '.csv?&api_key=xgnhYnpkFuqTgBDX4bjK&start_date='+start_date+'&end_date='+end_date+'&order=asc&collapse=weekly'

	dt_out=[]
	with requests.Session() as s:
		download = s.get(CSV_URL)
		decoded_content = download.content.decode('utf-8')
		cr = csv.reader(decoded_content.splitlines(), delimiter=',')
		
		items_selected=[0,11]
		my_list = list(cr)
		dt_out.append([my_list[0][index] for index in items_selected])

		for row in my_list[1:]:
			
			dt_r=[row[0]]
	
			for r in row[1:]:
				dt_r.append(float(r))
			dt_out.append([dt_r[index] for index in items_selected])


	return render_template('index.html', dt_out=dt_out)







if __name__=='__main__':
    app.run(debug=True)


