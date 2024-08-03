---
author: admin
categories:
- Technical
date: 2015-08-04 20:12:09-07:00
has-comments: false
source: wordpress
tags:
- cgi
- sql
- sqlite
- website
title: SQL views
updated: 2015-10-17 19:28:02-07:00
wordpress_id: 243
wordpress_slug: sql-views
---
I decided I wanted to show (restricted) data views on the web in table form. Specifically, ‘stylish.db’ is a database provided by a chrome plugin. Here’s an example script, [stylish.view](https://za3k.com/stylish.view), which displays the contents of that. It contains a comment saying which database it’s a query on, together with the query.

```
-- stylish.db
SELECT style, code, GROUP_CONCAT(section_meta.value) as 'website(s)' FROM
 (SELECT styles.name AS style,
 sections.code AS code,sections.id AS sections_id
 FROM styles INNER JOIN sections ON sections.style_id = styles.id)
LEFT JOIN section_meta
 ON section_meta.section_id = sections_id
GROUP BY style;
```

The cool part here is that none of this was specific to stylish. I can quickly throw together a .view file for any database and put it on the web.

I add put any databases in cgi-bin/db, and add view.cgi to cgi-bin:

```
#!/bin/bash
# view.cgi
echo "Content-type: text/html"
echo

QUERY_FILE="${PATH_TRANSLATED}"
DB_NAME=$(head -n1 "${QUERY_FILE}" | sed -e 's/--\s*//')
DB="/home/za3k/cgi-bin/db/${DB_NAME}"

echo "<html><head><title>Query on #{DB_NAME}</title><link rel="stylesheet" type="text/css" href="db.css"></head><body><table id=\"${DB_NAME}\">"
sqlite3 "$DB" -html -header <"${QUERY_FILE}"
echo "</table></body></html>"
```

I add this to apache’s \`.htaccess\`:

```
Action view /cgi-bin/view.cgi
AddHandler view .view
```
