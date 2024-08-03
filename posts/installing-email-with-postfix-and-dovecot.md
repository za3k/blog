---
author: admin
categories:
- Technical
date: 2015-11-07 17:31:25-07:00
has-comments: true
source: wordpress
tags:
- debian
- dovecot
- email
- linux
- postfix
- system administration
title: Installing email with Postfix and Dovecot (with Postgres)
updated: 2017-04-05 19:09:13-07:00
wordpress_id: 358
wordpress_slug: installing-email-with-postfix-and-dovecot
---
I’m posting my email setup here. The end result will:

-   Use Postfix for SMTP
-   Use Dovecot for IMAP and authentication
-   Store usernames, email forwards, and passwords in a Postgres SQL database
-   Only be accessible over encrypted channels
-   Pass all common spam checks
-   Support SMTP sending and IMAP email checking. I did not include POP3 because I don’t use it, but it should be easy to add
-   NOT add spam filtering or web mail (this article is long enough as it is, maybe in a follow-up)

Note: My set up is pretty standard, except that rDNS for smtp.za3k.com resolves to za3k.com because I only have one IP. You may need to change your hostnames if you’re using mail.example.com or smtp.example.com.

On to the install!

1.  Install debian packages
    
    ```
    sudo apt-get install postfix # Postfix \
          dovecot-core dovecot-imapd dovecot-lmtpd # Dovecot \
          postgresql dovecot-pgsql postfix-pgsql # Postgres \
          opendkim opendkim-tools # DKIM
    ```
    
2.  Set up security. smtp.za3k.com cert is at /etc/certs/zak3.com.pem, the key is at /etc/ssl/private/smtp.za3k.com.key. dhparams for postfix are at /etc/postfix/dhparams.pem. (If you need a certificate and don’t know how to get one, you can read [Setting up SSL certificates using StartSSL](https://blog.za3k.com/setting-up-ssl-certificates-using-startssl/ "Setting up SSL certificates using StartSSL"))
3.  Install Postfix
    
    ```
    # /etc/postfix/master.cf
    smtp       inet  n       -       -       -       -       smtpd
    submission inet  n       -       -       -       -       smtpd
      -o syslog_name=postfix/submission
      -o smtpd_tls_security_level=encrypt
      -o smtpd_sasl_auth_enable=yes
      -o smtpd_reject_unlisted_recipient=no
      -o milter_macro_daemon_name=ORIGINATING
    ```
    
    ```
    # /etc/postfix/main.cf additions
    # TLS parameters
    smtpd_tls_cert_file=/etc/ssl/certs/smtp.za3k.com.pem
    smtpd_tls_key_file=/etc/ssl/private/smtp.za3k.com.key
    smtpd_use_tls=yes
    smtpd_tls_mandatory_protocols=!SSLv2,!SSLv3
    smtp_tls_mandatory_protocols=!SSLv2,!SSLv3
    smtpd_tls_protocols=!SSLv2,!SSLv3
    smtp_tls_protocols=!SSLv2,!SSLv3
    smtpd_tls_exclude_ciphers = aNULL, eNULL, EXPORT, DES, RC4, MD5, PSK, aECDH, EDH-DSS-DES-CBC3-SHA, EDH-RSA-DES-CDC3-SHA, KRB5-DE5, CBC3-SHA
    
    # Relay and recipient settings
    myhostname = za3k.com
    myorigin = /etc/mailname
    mydestination = za3k.com, smtp.za3k.com, localhost.com, localhost
    relayhost =
    mynetworks_style = host
    mailbox_size_limit = 0
    inet_interfaces = all
    smtpd_relay_restrictions = permit_mynetworks,
      permit_sasl_authenticated,
      reject_unauth_destination
    
    alias_maps = hash:/etc/aliases
    local_recipient_maps = $alias_maps
    mailbox_transport = lmtp:unix:private/dovecot-lmtp
    ```
    
4.  Install Dovecot
    
    ```
    # /etc/dovecot/dovecot.cf
    mail_privileged_group = mail # Local mail
    disable_plaintext_auth = no
    
    protocols = imap
    
    ssl=required
    ssl_cert = </etc/ssl/certs/imap.za3k.com.pem
    ssl_key = </etc/ssl/private/imap.za3k.com.key
    
    # IMAP Folders
    namespace {
     inbox = yes
     mailbox Trash {
     auto = create
     special_use = \Trash
     }
     mailbox Drafts {
     auto = no
     special_use = \Drafts
     }
     mailbox Sent {
     auto = subscribe
     special_use = \Sent
     }
     mailbox Spam {
     auto = subscribe
     special_use = \Junk
     }
    }
    
    # Expunging / deleting mail should FAIL, use the lazy_expunge plugin for this
    namespace {
     prefix = .EXPUNGED/
     hidden = yes
     list = no
     location = maildir:~/expunged
    }
    mail_plugins = $mail_plugins lazy_expunge
    plugin {
     lazy_expunge = .EXPUNGED/
    }
    ```
    
    ```
    # /etc/postfix/main.cf
    # SASL authentication is done through Dovecot to let users relay mail
    smtpd_sasl_type = dovecot
    smtpd_sasl_path = private/auth
    ```
    
5.  Set up the database and virtual users. Commands
    
    ```
    # Create the user vmail for storing virtual mail
    # vmail:x:5000:5000::/var/mail/vmail:/usr/bin/nologin
    groupadd -g 5000 vmail
    mkdir /var/mail/vmail
    useradd -M -d /var/mail/vmail --shell=/usr/bin/nologin -u 5000 -g vmail vmail
    chown vmail:vmail /var/mail/vmail
    chmod 700 /var/mail/vmail
    ```
    
    ```
    psql -U postgres
    ; Set up the users
    CREATE USER 'postfix' PASSWORD 'XXX';
    CREATE USER 'dovecot' PASSWORD 'XXX';
    
    ; Create the database
    CREATE DATABASE email;
    \connect email
    
    ; Set up the schema 
    
    CREATE TABLE aliases (
        alias text NOT NULL,
        email text NOT NULL
    );
    
    CREATE TABLE users (
        username text NOT NULL,
        domain text NOT NULL,
        created timestamp with time zone DEFAULT now(),
        password text NOT NULL
    );
    
    REVOKE ALL ON TABLE aliases FROM PUBLIC;
    GRANT ALL ON TABLE aliases TO postfix;
    GRANT ALL ON TABLE aliases TO dovecot;
    
    REVOKE ALL ON TABLE users FROM PUBLIC;
    GRANT ALL ON TABLE users TO dovecot;
    GRANT ALL ON TABLE users TO postfix;
    ```
    
    ```
    # /etc/dovecot/dovecot.conf
    # Since we're giving each virtual user their own directory under /var/mail/vmail, just use that directly and not a subdirectory
    mail_location = maildir:~/
    
    # /etc/dovecot/dovecot-sql.conf defines the DB queries used for authorization
    passdb {
      driver = sql
      args = /etc/dovecot/dovecot-sql.conf
    }
    userdb {
      driver = prefetch
    }
    userdb {
      driver = sql
      args = /etc/dovecot/dovecot-sql.conf
    }
    ```
    
    ```
    # /etc/postfix/main.cf
    pgsql:/etc/postfix/pgsql-virtual-aliases.cf
    local_recipient_maps = pgsql:/etc/postfix/pgsql-virtual-mailbox.cf 
    ```
    
    ```
    # /etc/postfix/pgsql-virtual-aliases.cf
    # hosts = localhost
    user = postfix
    password = XXXXXX
    dbname = email
    
    query = SELECT email FROM aliases WHERE alias='%s'
    ```
    
    ```
    # /etc/postfix/pgsql-virtual-mailbox.cf
    # hosts = localhost
    user = postfix
    password = XXXXXX
    dbname = email
    
    query = SELECT concat(username,'@',domain,'/') as email FROM users WHERE username='%s'
    ```
    
    ```
    # /etc/dovecot/dovecot-sql.conf
    driver = pgsql
    connect = host=localhost dbname=email user=dovecot password=XXXXXX
    default_pass_scheme = SHA512
    password_query = SELECT \
      CONCAT(username,'@',domain) as user, \
      password, \
      'vmail' AS userdb_uid, \
      'vmail' AS userdb_gid, \
      '/var/mail/vmail/%u' as userdb_home \
      FROM users \
      WHERE concat(username,'@',domain) = '%u';
    
    user_query = SELECT username, \
      CONCAT('maildir:/var/mail/vmail/',username,'@',domain) as mail, \
      '/var/mail/vmail/%u' as home, \
      'vmail' as uid, \
      'vmail' as gid \
      FROM users \
      WHERE concat(username,'@',domain) = '%u';
    ```
    
6.  Set up users. Example user creation:
    
    ```
    # Generate a password
    $ doveadm pw -s sha512 -r 100
    Enter new password: ...
    Retype new password: ...
    {SHA512}.............................................................==
    ```
    
    ```
    psql -U dovecot -d email
    ; Create a user za3k@za3k.com
    mail=# INSERT INTO users (
        username,
        domain,
        password
    ) VALUES (
        'za3k',
        'za3k.com'
        '{SHA512}.............................................................==',
    );
    ```
    
7.  Set up aliases/redirects. Example redirect creation:
    
    ```
    psql -U dovecot -d email
    ; Redirect mail from foo@example.com to bar@example.net
    mail=# INSERT INTO users ( email, alias ) VALUES (
        'bar@example.net',
        'foo@example.com'
    );
    ```
    
8.  Test setup locally by hand. Try using [TELNET](https://www.port25.com/how-to-check-an-smtp-connection-with-a-manual-telnet-session-2/). Test remote setup using STARTSSL. This is similar to the previous step, but to start the connection use:
    
    ```
    openssl s_client -connect smtp.za3k.com:587 -starttls smtp
    ```
    
    Make sure to test email to addresses at your domain or that you’ve set up (final destination), and emails you’re trying to send somewhere else (relay email)
    
    A small [digression](https://www.fastmail.com/help/technical/ssltlsstarttls.html): port 25 is used for unencrypted email and support STARTTLS, 587 is used for STARTTLS only, and 465 (obsolete) is used for TLS. My ISP, Comcast, blocks access to port 25 on outgoing traffic.
    
9.  Make sure you’re not running an open relay at [http://mxtoolbox.com/diagnostic.aspx](http://mxtoolbox.com/diagnostic.aspx)
10.  Set your DNS so that the [MX](https://en.wikipedia.org/wiki/MX_record) record points at your new mailserver. You’ll probably want a [store and forward](https://en.wikipedia.org/wiki/Store_and_forward) backup mail server (mine is provided by my registrar). Email should arrive at your mail server from now on. This is the absolute minimum setup. Everything from here on is to help the community combat spam (and you not to get blacklisted).
11.  Set up [DKIM](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail) (DomainKeys Identified Mail). DKIM signs outgoing mail to show that it’s from your server, which helps you not get flagged as spam.  
    None of these files or folders exist to begin with in debian.
    
    ```
    # Add to /etc/opendkim.conf
    KeyTable                /etc/opendkim/KeyTable
    SigningTable            /etc/opendkim/SigningTable
    ExternalIgnoreList      /etc/opendkim/TrustedHosts
    InternalHosts           /etc/opendkim/TrustedHosts
    LogWhy yes
    ```
    
    ```
    # /etc/opendkim/TrustedHosts
    127.0.0.1
    [::1]
    localhost
    za3k.com
    smtp.za3k.com
    ```
    
    ```
    mkdir -p /etc/opendkim/keys/za3k.com
    cd /etc/opendkim/keys/za3k.com
    opendkim-genkey -s default -d za3k.com
    chown opendkim:opendkim default.private
    ```
    
    ```
    # /etc/opendkim/KeyTable
    default._domainkey.za3k.com za3k.com:default:/etc/opendkim/keys/za3k.com/default.private
    ```
    
    ```
    # /etc/opendkim/SigningTable
    za3k.com default._domainkey.za3k.com
    ```
    
    Display the DNS public key to set in a [TXT](https://en.wikipedia.org/wiki/TXT_Record) record with:
    
    ```
    # sudo cat /etc/opendkim/keys/za3k.com/default.txt
    default._domainkey      IN      TXT     ( "v=DKIM1; k=rsa; "
              "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCggdv3OtQMek/fnu+hRrHYZTUcpUFcSGL/+Sbq+GffR98RCgabx/jjPJo3HmqsB8czaXf7yjO2UiSN/a8Ae6/yu23d7hyTPUDacatEM+2Xc4/zG+eAlAMQOLRJeo3z53sNiq0SmJET6R6yH4HCv9VkuS0TQczkvME5hApft+ZedwIDAQAB" )  ; ----- DKIM
    
    # My registrar doesn't support this syntax so it ends up looking like: 
    $ dig txt default._domainkey.za3k.com txt
    default._domainkey.za3k.com. 10800 IN   TXT     "v=DKIM1\; k=rsa\; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCggdv3OtQMek/fnu+hRrHYZTUcpUFcSGL/+Sbq+GffR98RCgabx/jjPJo3HmqsB8czaXf7yjO2UiSN/a8Ae6/yu23d7hyTPUDacatEM+2Xc4/zG+eAlAMQOLRJeo3z53sNiq0SmJET6R6yH4HCv9VkuS0TQczkvME5hApft+ZedwIDAQAB"
    ```
    
    ```
    # Uncomment in /etc/default/opendkim
    SOCKET="inet:12345@localhost" # listen on loopback on port 12345
    ```
    
    ```
    # /etc/postfix/main.cf
    # DKIM
    milter_default_action = accept
    milter_protocol = 6
    smtpd_milters = inet:localhost:12345
    non_smtpd_milters = inet:localhost:12345
    ```
    
12.  Set up [SPF](https://en.wikipedia.org/wiki/Sender_Policy_Framework) (Sender Policy Framework). SPF explains to other services which IPs can send email on your behalf. You can set up whatever policy you like. A guide to the syntax is at: [http://www.openspf.org/SPF\_Record\_Syntax](http://www.openspf.org/SPF_Record_Syntax).  Mine is
    
    ```
    @ 10800 IN TXT "v=spf1 +a:za3k.com +mx:za3k.com ~all"
    ```
    
    You should also be verifying this on your end as part of combating spam, but as far as outgoing mail all you need to do is add a TXT record to your DNS record.
    
13.  Set your [rDNS](https://en.wikipedia.org/wiki/Reverse_DNS_lookup) (reverse DNS) if it’s not already. This should point at the same hostname reported by Postfix during SMTP. This will be handled by whoever assigns your IP address (in my case, my hosting provider).
14.  Test your spam reputability using [https://www.mail-tester.com](https://www.mail-tester.com/) or [https://www.port25.com/support/authentication-center/email-verification](https://www.port25.com/support/authentication-center/email-verification/). You can monitor if you’re on any blacklists at [http://mxtoolbox.com/blacklists.aspx](http://mxtoolbox.com/blacklists.aspx).
15.  Set up [DMARC](https://dmarc.org/overview/). DMARC declares your policy around DKIM being mandatory. You can set up whatever policy you like.  Mine is
    
    ```
    _dmarc 10800 IN TXT "v=DMARC1;p=reject;aspf=s;adkim=s;pct=100;rua=mailto:postmaster@za3k.com"
    ```
    

My sources writing this:

-   [https://wiki.archlinux.org/index.php/Postfix](https://wiki.archlinux.org/index.php/Postfix) and [http://www.postfix.org/postconf.5.html](http://www.postfix.org/postconf.5.html) on Postfix
-   [https://wiki.archlinux.org/index.php/Dovecot](https://wiki.archlinux.org/index.php/Dovecot%20) on Dovecot
-   [https://help.ubuntu.com/community/PostfixVirtualMailBoxClamSmtpHowto](https://help.ubuntu.com/community/PostfixVirtualMailBoxClamSmtpHowto) on SASL auth integration between Dovecot and Postfix
-   [https://www.digitalocean.com/community/tutorials/how-to-set-up-a-postfix-email-server-with-dovecot-dynamic-maildirs-and-lmtp](https://www.digitalocean.com/community/tutorials/how-to-configure-a-mail-server-using-postfix-dovecot-mysql-and-spamassassin) and [https://www.digitalocean.com/community/tutorials/how-to-configure-a-mail-server-using-postfix-dovecot-mysql-and-spamassassin](https://www.digitalocean.com/community/tutorials/how-to-configure-a-mail-server-using-postfix-dovecot-mysql-and-spamassassin) on SQL integration in Dovecot
-   [https://scaron.info/blog/debian-mail-spf-dkim.html](https://scaron.info/blog/debian-mail-spf-dkim.html) for setting up SPF, DKIM, and rDNS

Takeaways

-   You can set up store-and-forward mail servers, so if your mail server goes down, you don’t lose all the email for that period. It’s generally a free thing.
-   Postfix’s configuration files were badly designed and crufty, so you might pick a different SMTP server.
-   Email was REALLY not designed to do authentication, which is why proving you’re not a spammer is so difficult. This would all be trivial with decent crypto baked in (or really, almost any backwards-incompatible change)
-   The option to specify a SQL query as a configuration file option is wonderful. Thanks, Dovecot.
-   Overall, although it was a lot of work, I do feel like it was worth it to run my own email server.
