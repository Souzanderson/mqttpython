from paho.mqtt.client import Client, MQTTv311
import json
import uuid

class MqttMessageData:
    
    def __init__(self):
        self._payload = None
        self.topic = None
        self.qos = None
        self.retain = None

    @staticmethod
    def fromMessage(message):
        message_data = MqttMessageData()
        message_data._payload = str(message.payload.decode("utf-8"))
        message_data.topic = message.topic
        message_data.qos = message.qos
        message_data.retain = message.retain
        
        return message_data
    
    @property
    def payload(self):
        try:
            return json.loads(self._payload)
        except:
            return self._payload


class MqttClient():
    def __init__(self, host, port=1883, qos=1, user=None, password=None):
        self.id = uuid.uuid4().hex
        self.client = Client(self.id, clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp", reconnect_on_failure=True)
        self.host = host
        self.port = port
        self.qos = qos
        if user and password:
            self.client.username_pw_set(user, password)
        self.client.on_connect = self.__on_connect__
        self.client.connect(host=self.host, port=self.port, keepalive=120, bind_address="")
        
    def publish(self, topic: str, payload, retain = False):
        res = payload
        if isinstance(payload, dict):
            res = json.dumps(payload)
        self.client.publish(topic, res, qos=self.qos, retain=retain)
        print(f"[INFO] Mensagem enviada por MQTT => ID: {self.id}")
        
    def subscribe(self, topic, fn_callback):
        self.__on_message__(fn_callback)
        self.client.subscribe(topic)
        self.client.loop_forever()
        
    def thread_subscribe(self, topic, fn_callback):
        from threading import Thread
        Thread(target=self.subscribe, args=(topic, fn_callback)).start()
        
        
        
    def __on_message__(self,fn_callback):
        self.client.on_message = lambda client, userdata, message: fn_callback(MqttMessageData.fromMessage(message))
    
    
    def __on_connect__(self, client, userdata, flags, rc):
        print(f"[INFO] Conexão estabelecida! => Result: {rc} => ID {self.id}")
    