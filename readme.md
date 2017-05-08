## Visualization Panel for Zika Tweets Exploration 
Final Project - INFO 5602

Collaborators:

	Linzi Xing
	Hayeong Song

## File Structure
* data:
	* collect_zika.json: raw zika related tweets
	* sentimet.csv: contains tweets' sentiment coordination and score, output of sentiment analysis code
	* time_series.csv: contains two columns: collected time and content of tweets
	* topic.csv: contains two columns: tweet index and number of topic tweet belongs to, output of topic model code
	* tst.csv: all views above are integrated into this csv file and this is used as direct input of visualization code
* static: some source files and documentations
* csv_generate.py: py code used to generate the final csv file
* topic.model.py: py code used to get most possible topic of each tweets, the output is topic.csv
* tst.csv: the integrated data file used as input of visualization code

## Run the Code



## References
* For the bootstrap page:
[Bootstrap CSS](http://getbootstrap.com/css/)
[Bootstrap Components](http://getbootstrap.com/components/)
[Bootstrap Javascript](http://getbootstrap.com/javascript/)

* Visualization part:
	* [dc.js heatmap example](https://github.com/dc-js/dc.js/blob/master/web/examples/heat.html)

	* [dc.js row chart example](https://github.com/dc-js/dc.js/blob/master/web/examples/row.html)

	* [dc.js datatable example](https://github.com/dc-js/dc.js/blob/master/web/examples/table-on-aggregated-data.html)

	* [dc.js line chart time series](http://www.d3noob.org/2013/08/add-line-chart-in-dcjs.html)

* Pre-processing part:
	* [topic modeling](https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/)
	
	* [sentiment analysis](https://github.com/jdwittenauer/twitter-viz-demo)
	
	* [tokenizer](http://sentiment.christopherpotts.net/code-data/happyfuntokenizing.py)
	
* data collecting:
	
	

