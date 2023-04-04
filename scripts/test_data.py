
import csv
from createmodels.models import StoreStatus,BusinessHours,StoreTimezone
from itertools import islice
from collections import Counter
from django.db import models 
from datetime import datetime, timezone,timedelta
from dateutil import tz
import numpy as np
from scipy import interpolate
import math
import pandas as pd
from django_thread import Thread
import string
import random
class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs , daemon=True)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def utc_to_local(utc_dt,timezone):
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz(timezone)
	utc = datetime.strptime(utc_dt, '%Y-%m-%d %H:%M:%S')
	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	utc = utc.replace(tzinfo=from_zone)

	# Convert time zone
	central = utc.astimezone(to_zone)
	return central.replace(tzinfo=None)

def to_hm_int(date):
	# convert hh:mm:ss into hour*60+min.. or just total minutes 
	return int(str(date)[:2])*60 + int(str(date)[3:5])

def get_day_uptime(id,date):
	# Get all the rows with specific store id and max_date and get the values list 
	all_entries = StoreStatus.objects.filter(storeid=id['storeid'])\
		.filter( date_utc = date).values_list('storeid','time_utc','status')
	
	if(len(all_entries) == 0 ): return False,0,0,0
	#fetch the store timezone 
	timezone = StoreTimezone.objects.filter( storeid=id['storeid']).values_list('timezone')
	
	#returning multiples values 
	if( len(timezone) == 0 ): timezone = 'America/Chicago'
	else: timezone = timezone[0][0]
	
	# Get time and status list for the current day 
	time_list = []
	status_list = []
	day = 0
	for row in all_entries:
		#conver from utc to local 
		date_time = str(date) + " " + str(row[1])[:-7] 
		local_time = utc_to_local( date_time ,timezone) 
		#print(f'utc_time:{date_time} local_time:{local_time}')
		day = local_time.weekday()
		time = datetime.strptime(str(date_time),'%Y-%m-%d %H:%M:%S') 
		#print( f' {row[0]} {local_time} {row[2]} weekday{local_time.weekday()}')
		time_list.append( to_hm_int ( str(time)[11:16] ) )
		status_list.append( 1 if row[2] =='active' else 0 );
		
	
	# Get business hours time range 
	timerange = BusinessHours.objects.filter(storeid=id['storeid'] ) \
		.filter(dayofweek = int(day))\
		.values('start_time','end_time')
	
	start_time , end_time = 0, 24*60 - 1
	if(len(timerange)>0):
		#if(len(timerange)>0):
		start_time = to_hm_int( timerange[0]['start_time'] )
		end_time = to_hm_int( timerange[0]['end_time'] )
		# Extropolate and fill all the values withing the time range  
		full_time = np.arange( start_time ,end_time , 1 )
	else:
		start_time , end_time = 0, 24*60 - 1
		full_time = np.arange(start_time,end_time,1)
	ip_func = interpolate.interp1d(time_list, status_list ,kind='nearest',fill_value="extrapolate")
	new_status_list = ip_func(full_time)
	
	return True,new_status_list,start_time,end_time

def get_results(id,week_list):
	week_uptime,week_downtime=0,0
	day_uptime,day_downtime=0,0
	hour_uptime,hour_downtime = 0,0 	
	for i,date in enumerate(week_list):
		valid,lis,st,et = get_day_uptime( id ,date ) 
		if(not valid): continue 
		elif( i == 0 ):
			# generate day and hour result 
			day_uptime = sum(lis) 
			day_downtime = (et-st) - day_uptime 
			day_uptime //= 60
			day_downtime //= 60
			hour_uptime = math.floor( sum(lis[-60:]) )
			hour_downtime = math.floor( 60-hour_uptime )
		else:
			t1 = sum(lis) 
			t2 = (et-st) - day_uptime 
			t1 //= 60
			t2 //= 60
			week_uptime += t1
			week_downtime += t2
	print(f'done')
	return id['storeid'],hour_uptime,day_uptime,week_uptime,hour_downtime,day_downtime,week_downtime


def randomstring(n):
	return  ''.join(random.choices(string.ascii_letters, k=n))
	
	 
def run():
	# Get a Storeid list 
	ids = StoreStatus.objects.order_by().values('storeid').distinct()
	df_list = [['store_id', 'uptime_last_hour', 'uptime_last_day','update_last_week', \
		'downtime_last_hour', 'downtime_last_day', 'downtime_last_week' ] ]
	thread_list = []
	for id in ids[:10]:
		x = StoreStatus.objects.filter(storeid=id['storeid'])
		max_date = x.aggregate(models.Max('date_utc'))
		week_list = [max_date['date_utc__max'] - timedelta(days=x) for x in range(7)]
		twrv = ThreadWithReturnValue( target=get_results, args=(id,week_list,)  )
		twrv.start()
		thread_list.append(twrv)
		#print(f'week:{week_uptime} day:{day_uptime} hour:{hour_uptime}')
	
	#id['storeid'],hour_uptime,day_uptime,week_uptime,hour_downtime,day_downtime,week_downtime
	for thread in thread_list:
		df_list.append(thread.join())
	
	df = pd.DataFrame(df_list)
	path = str( 'static/res' + randomstring(10) + '.csv' )
	df.to_csv(path, index=False,encoding='utf-8')
	
	print(df.head())
	return path 
		
		
			
			
			
			
		
		
		
		