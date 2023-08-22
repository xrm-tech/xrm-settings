from st2reactor.sensor.base import PollingSensor
import requests
__all__ = [
    'XRMOvirtLogSensor'
]


class XRMOvirtLogSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(XRMOvirtLogSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        
        self._logger = self._sensor_service.get_logger(__name__)
        self._string_ref = {}

    def setup(self):
        self._last_id = None

        #if type(self._config['query']) is not list:
        #    self._logger.exception('Twitter sensor failed. "query" config \
        #                            value is not a list')
        #    raise ValueError('[TwitterSearchSensor]: "query" is not a list')


    def poll(self):
        self._logger.info("log.info: poll started")
        events = []

        try:

            req = requests.get("http://37.187.132.140:8081/st2test")
            print("status", req.status_code)
            print(req.text)
        except:
            pass

        if events:
            self._set_last_id(last_id="123")

        #for event in events:
         #   self._dispatch_trigger_for_event(event=event)
        

        self._logger.info("before dispatch")

        
        lines_from_log = []
        # lines_from_log = pool_log_from_ovirt()
        
        if self._string_ref:
            
            lines_from_log.append(list(self._string_ref.keys())[0]); # add 1 line for debug
            self._logger.info(lines_from_log)
            for line in lines_from_log: 
                for search_string in self._string_ref.keys():
                    if line.casefold() == search_string.casefold():
                        trigger = self._string_ref[search_string];
                        eventdata= {
                            'description':"Storage Domain nfstst (Data Center Default) was deactivated by system because it's not visible by any of the hosts.",
                            'time':"2023-06-27T17:12:09.531+02:00",
                            'severity':"error",
                            'code':"9803",
                            'origin':"XRM",
                            'index':"62197",
                            'custom_id':"1467879758"          
                        }    
                        self._dispatch_trigger_for_event(eventdata=eventdata,trigger=trigger)
        self._logger.info("poll ended")
        '''tso = TwitterSearchOrder()
        tso.set_keywords(self._config['query'], True)

        language = self._config.get('language', None)
        if language:
            tso.set_language(language)

        tso.set_result_type('recent')
        tso.set_count(self._config.get('count', 30))
        tso.set_include_entities(False)

        last_id = self._get_last_id()

        if last_id:
            tso.set_since_id(int(last_id))

        try:
            tweets = self._client.search_tweets(tso)
            tweets = tweets['content']['statuses']
        except Exception as e:
            self._logger.exception('Polling Twitter failed: %s' % (str(e)))
            return

        tweets = list(reversed(tweets))

        if tweets:
            self._set_last_id(last_id=tweets[-1]['id'])

        for tweet in tweets:
            self._dispatch_trigger_for_tweet(tweet=tweet)
        '''

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        self._logger.info("started add trigger")
        self._server_address = trigger["parameters"].get("01_engine_url", None)
        self._server_username = trigger["parameters"].get("02_engine_login", None)
        self._server_password = trigger["parameters"].get("03_engine_password", None)
        self._server_search_text = trigger["parameters"].get("04_event_search_text", None)
        trigger = trigger.get("ref", None)
        self._string_ref[self._server_search_text] = trigger
        self._logger.info(f"Added string '{self._server_search_text}' ({trigger}) to watch list.")
        self._logger.info("ended add trigger")

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_last_id(self):
        if not self._last_id and hasattr(self._sensor_service, 'get_value'):
            self._last_id = self._sensor_service.get_value(name='last_id')

        return self._last_id

    def _set_last_id(self, last_id):
        self._last_id = last_id

        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(name='last_id', value=last_id)

    def _dispatch_trigger_for_event(self, eventdata,trigger):
       

        '''
        url = '%s/%s/status/%s' % (BASE_URL, tweet['user']['screen_name'], tweet['id'])
        payload = {
            'id': tweet['id'],
            'created_at': tweet['created_at'],
            'lang': tweet['lang'],
            'place': tweet['place'],
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count'],
            'user': {
                'screen_name': tweet['user']['screen_name'],
                'name': tweet['user']['name'],
                'location': tweet['user']['location'],
                'description': tweet['user']['description'],
            },
            'text': tweet['text'],
            'url': url
        }
        '''
        
        payload  = {
            'description':eventdata['description'],
            'time':eventdata['time'],
            'severity':eventdata['severity'],
            'code':eventdata['code'],
            'origin':eventdata['origin'],
            'index':eventdata['index'],
            'custom_id':eventdata['custom_id']
        }
        
        self._logger.info("before service dispatch")
        self._logger.info(f"Sending payload {payload} for trigger {trigger} to sensor_service.")
        self.sensor_service.dispatch(trigger=trigger, payload=payload)
        self._logger.info("after service dispatch")