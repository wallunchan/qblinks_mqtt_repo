import sys
import os
import subprocess

def generateCACert():
    args = "openssl genrsa -out sampleCACertificate.key 2048".split()
    subprocess.call(args)
    args = "openssl req -x509 -new -nodes -key sampleCACertificate.key -sha256 -days 365 -out sampleCACertificate.pem".split()
    p = subprocess.Popen(args, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.communicate("\n\n\n\n\n\n\n")

def getRegistrationCode():
    args = "aws iot get-registration-code".split()
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = p.communicate()
    start = out.find('": "')
    end = out.find('"', start + 4)
    return out[start + 4 : end]

def generatePrivateKeyVerification():
    args = "openssl genrsa -out privateKeyVerification.key 2048".split()
    subprocess.call(args)
    args = "openssl req -new -key privateKeyVerification.key -out privateKeyVerification.csr".split()
    p = subprocess.Popen(args, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    registrationCode = getRegistrationCode()
    p.communicate("\n\n\n\n\n" + registrationCode + "\n\n\n\n")

def registerPrivateKeyVerification():
    args = "openssl x509 -req -in privateKeyVerification.csr -CA sampleCACertificate.pem -CAkey sampleCACertificate.key -CAcreateserial -out privateKeyVerification.crt -days 365 -sha256".split()
    subprocess.call(args)
    args = "aws iot register-ca-certificate --ca-certificate file://sampleCACertificate.pem --verification-certificate file://privateKeyVerification.crt".split()
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = p.communicate()
    searchKey = "\"certificateId\": \""
    start = out.find(searchKey) + len(searchKey)
    end = out.find("\"", start)
    caCertId = out[start : end]
    with open("certification-id", "w") as text_file:
        text_file.write(caCertId)

def getCACertId():
    with open("certification-id", "r") as text_file:
        data = text_file.read().replace('\n', '')
    return data

def enableCACert():
    caCertId = getCACertId()
    args = "aws iot update-ca-certificate --certificate-id " + caCertId + " --new-status ACTIVE"
    args = args.split()
    subprocess.call(args)
    args = "aws iot update-ca-certificate --certificate-id " + caCertId + " --new-auto-registration-status ENABLE"
    args = args.split()
    subprocess.call(args)

if __name__ == '__main__':
    generateCACert()
    generatePrivateKeyVerification()
    registerPrivateKeyVerification()
    enableCACert()
