var awsIot = require('aws-iot-device-sdk');

if (process.argv.length <= 5) {
  console.log('Usage: node ' + __filename + ' <clientId> <topicName> <region> <data>');
  process.exit(1);
}

var clientId = process.argv[2];
var topicName = process.argv[3];
var region = process.argv[4];
var data = process.argv[5];

var device = awsIot.device({
   keyPath: './deviceCert.key',
  certPath: './deviceCert.crt',
    caPath: './root.cert',
  clientId: clientId,
    region: region
});

device.on('connect', function() {
  console.log('Connected to ' + region);
  device.publish(topicName,
                JSON.stringify({ data : data }),
                { qos : 0 },
                function(err) {
                  if (err) {
                    console.log('Failed to publish data: ' + err);
                  } else {
                    console.log('Published data to topic: ' + topicName);
                  }
                });
  device.subscribe('topics/topic_ack');
});

device.on('message', function(topic, payload) {
  console.log('message', topic, payload.toString());
  process.exit(0);
});

