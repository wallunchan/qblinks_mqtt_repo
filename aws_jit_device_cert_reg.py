import sys
import os
import subprocess

def generateDeviceCert():
    args = "openssl genrsa -out deviceCert.key 2048".split()
    subprocess.call(args)
    args = "openssl req -new -key deviceCert.key -out deviceCert.csr".split()
    p = subprocess.Popen(args, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.communicate("\n\n\n\n\n\n\n\n\n")
    args = "openssl x509 -req -in deviceCert.csr -CA sampleCACertificate.pem -CAkey sampleCACertificate.key -CAcreateserial -out deviceCert.crt -days 365 -sha256".split()
    subprocess.call(args)
    filenames = ["deviceCert.crt", "sampleCACertificate.pem"]
    with open("deviceCertAndCACert.crt", "w") as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())

def registerDeviceCert():
    args = "mosquitto_pub --cafile root.cert --cert deviceCertAndCACert.crt --key deviceCert.key -h a1ut5bep93klek.iot.us-east-1.amazonaws.com -p 8883 -q 1 -t topics/register_cert -i anyclientID --tls-version tlsv1.2 -m \"Hello\" -d".split()
    subprocess.call(args)

if __name__ == '__main__':
    generateDeviceCert()
    registerDeviceCert()
