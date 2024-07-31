---
author: admin
categories:
- Technical
date: 2014-11-08 09:52:14-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- backup
- git
- github
- system administration
title: Archiving github
updated: 2014-11-22 09:47:39-07:00
wordpress_id: 41
wordpress_slug: archiving-github
---
[GitHub-Backup](https://github.com/clockfort/GitHub-Backup "GitHub-Backup") is a small project to archive github repos to a local computer. It advertises that one reason to use it is

> You are paranoid tinfoil-hat wearer who needs to back up everything in triplicate on a variety of outdated tape media.

which describes why I was searching it out perfectly.

I made a new account on my server (github) and cloned their repo.

```
sudo useradd -m github
sudo -i- u github
git clone git@github.com:clockfort/GitHub-Backup.git
```

Despite being semi-unmaintained, everything mostly works still. There were two exceptions–some major design problems around private repos. I only need to back up my public repos really, so I ‘solved’ this by issuing an Oauth token that only knows about public repos. And second, a small patch to work around a bug with User objects in the underlying Github egg:

```
￼-       os.system("git config --local gitweb.owner %s"%(shell_escape("%s <%s>"%(repo.user.name, repo.user.email.encode("utf-8"))),))
+       if hasattr(repo.user, 'email') and repo.user.email:
+               os.system("git config --local gitweb.owner %s"%(shell_escape("%s <%s>"%(repo.user.name, repo.user.email.encode("utf-8"))),))
```

Then I just shoved everything into a cron task and we’re good to go.

```
@hourly GitHub-Backup/github-backup.py -m -t  vanceza /home/github/vanceza
```

Edit: There’s a similar project for bitbucket I haven’t tried out: [https://bitbucket.org/fboender/bbcloner](https://bitbucket.org/fboender/bbcloner)
