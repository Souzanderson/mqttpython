from library.mqttclient import MqttClient, MqttMessageData

def callback(message:MqttMessageData):
    print("Mensagem recebida => ", message.payload)
    print("Mensagem recebida (QoS) => ", message.qos)
    print("Mensagem recebida (Topic) => ", message.topic)


if __name__ == '__main__':
    location = "locahost"
    user = "malbizer"
    password = "12345"
    
    # For subscribe (usando o método thread_subscribe você pode continuar seu programa normalmente)
    MqttClient(location, user=user, password=password).thread_subscribe((("teste",1)), callback)
    print("Mqtt por thread ativado!")
    
    #for send message
    MqttClient(location, user=user, password=password).publish("teste", {"message": "Nova mensagem!"})
    
    
    