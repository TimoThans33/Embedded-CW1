# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("rpi")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("rpi", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint("arn:aws:iot:eu-north-1:100732055442:thing/rpi", 8883)
# For Websocket
# myMQTTClient.configureEndpoint("arn:aws:iot:eu-north-1:100732055442:thing/rpi", 443)
# For TLS mutual authentication with TLS ALPN extension
# myMQTTClient.configureEndpoint("arn:aws:iot:eu-north-1:100732055442:thing/rpiT", 443)
myMQTTClient.configureCredentials("AmazonRootCA1.pem", "13816e7464-private.pem.key", "13816e7464-certificate.pem.crt")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("AmazonRootCA1.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
myMQTTClient.publish("myTopic", "myPayload", 0)
myMQTTClient.subscribe("myTopic", 1, customCallback)
myMQTTClient.unsubscribe("myTopic")
myMQTTClient.disconnect()