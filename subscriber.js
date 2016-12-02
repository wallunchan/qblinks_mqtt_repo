var awsIot = require('aws-iot-device-sdk');

if (process.argv.length <= 4) {
  console.log('Usage: node ' + __filename + ' <clientId> <topicName> <region>');
  process.exit(1);
}

var clientId = process.argv[2];
var topicName = process.argv[3];
var region = process.argv[4];

var device = awsIot.device({
   keyPath: './deviceCert.key',
  certPath: './deviceCert.crt',
    caPath: './root.cert',
  clientId: clientId,
    region: region 
});

device.on('connect', function() {
  console.log('Connected to ' + region);
  device.subscribe(topicName,
                   { qos : 0 },
                   function(err, granted) {
                     if (err) {
                       console.log('Failed to subscribe to ' + topicName);
                     } else {
                       console.log('Subscribed to ' + topicName);
                     }
                   });
});
 
device.on('message', function(topic, payload) {
  console.log('message', topic, payload.toString());
  device.publish('topics/topic_ack', JSON.stringify({ data : 'Ack from ' + clientId + ' for ' + topicName }));
});
