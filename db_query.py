import psycopg2
import json
from numpy import *
import pylab
from sklearn import *
import math

locahost="host=localhost dbname=cotweet_dev user=charlesq password=cotweet"
def open_db(conn_string):
	conn=psycopg2.connect(conn_string)
	return conn

def open_local_db():
	return open_db(locahost)

def query_db(conn, query_str):
	cur =conn.cursor()
	cur.execute(query_str)
	return cur

def get_test_timeseries():
	c=open_local_db()
	q=query_db(c, "select tweeted_at from updates order by tweeted_at;")
	return q.fetchall()

def get_timeseries_as_daily_modulo(timeseries):
	array = []
	for elem in timeseries:
		minutes = elem[0].hour * 60.0 + elem[0].minute
		array.append([minutes])
	return array


def get_training_sample_from_timeseries(timeseries):
	return get_timeseries_as_daily_modulo(timeseries)

def get_hour_from_minute_of_day(minute_of_day):
	hour = float(int(minute_of_day/60))
	remainder = float(int(minute_of_day%60))
	return (hour + remainder/60.0)

def get_better_training_sample_with_time_and_frequency(timeseries):
	xx,hist = get_daily_histogram(timeseries)
	training_sample = [[get_hour_from_minute_of_day(i*10), hist[i]] for i in range(len(hist))]
	ss=svm.OneClassSVM()
	ss.fit(training_sample)
	return ss,training_sample

def demo():
	data=get_test_timeseries()
	return get_better_training_sample_with_time_and_frequency(data)

def get_daily_histogram(timeseries, bins = 24*6):
	array = [0.0]* bins #10 minutes wide bins
	l = len(timeseries)
	for elem in timeseries:
		binIdx = (elem[0].hour * 6.0 + 0.1*elem[0].minute) % bins
		array[int(binIdx)] += 1.0
	for bin in range(len(array)):
		array[bin] /= l
	#hist=[() for i in range(len(array))]
	return [i for i in range(len(array))], array

def create_plot(xdata,ydata):
	pylab.ion()
	line, = pylab.plot(xdata,ydata,'m.',markersize=6)
	line.set_xdata(xdata)  # update the data
	line.set_ydata(ydata)
	return line

def update_plot(line,xdata,ydata):
	pylab.ion()
	line.set_xdata(xdata)  # update the data
	line.set_ydata(ydata)
	pylab.draw()

