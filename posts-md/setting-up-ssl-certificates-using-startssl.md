---
author: admin
categories:
- Technical
date: 2014-10-29 04:41:31-07:00
markup: html
source: wordpress
tags:
- http
- ssl
- system administration
- tls
title: Setting up SSL certificates using StartSSL
updated: 2016-02-10 18:48:39-07:00
wordpress_id: 28
wordpress_slug: setting-up-ssl-certificates-using-startssl
---
1.  Generate an SSL/TLS key, which will be used to actually encrypt traffic.
    
    ```
    DOMAIN=nntp.za3k.com
    openssl genrsa -out ${DOMAIN}.key 4096
    chmod 700 ${DOMAIN}.key
    ```
    
2.  Generate a Certificate Signing Request, which is sent to your authentication provider. The details here will have to match the details they have on file (for StartSSL, just the domain name).
    
    ```
    # -subj "/C=US/ST=/L=/O=/CN=${DOMAIN}" can be omitted to fill in custom identification details
    # -sha512 is the hash of your key used for identification. This was the reasonable option in Oct 2014. It isn't supported by IE6
    openssl req -new -key ${DOMAIN}.key -out ${DOMAIN}.csr -subj "/C=US/ST=/L=/O=/CN=${DOMAIN}" -sha512
    ```
    
3.  Submit your Certificate Signing Request to your authentication provider. Assuming the signing request details match whatever they know about you, they’ll return you a certificate. You should also make sure to grab any intermediate and root certificates here.
    
    ```
    echo "Saved certificate" > ${DOMAIN}.crt
    wget https://www.startssl.com/certs/sca.server1.crt https://www.startssl.com/certs/ca.crt # Intermediate and root certificate for StartSSL
    ```
    
4.  Combine the chain of trust (key, CSR, certificate, intermediate certificates(s), root certificate) into a single file with concatenation. Leaving out the key will give you a combined certificate of trust for the key, which you may need for other applications.
    
    ```
    cat ${DOMAIN}.crt sca.server1.crt >${DOMAIN}.pem # Main cert
    cat ${DOMAIN}.key ${DOMAIN}.crt sca.server1.crt ca.crt >${DOMAIN}.full.pem
    chmod 700 ${DOMAIN}.full.pem
    ```
    

See also: [https://github.com/Gordin/StartSSL\_API](https://github.com/Gordin/StartSSL_API)
