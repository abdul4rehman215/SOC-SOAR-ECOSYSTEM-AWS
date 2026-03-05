# 🚨 Troubleshooting Guide - MISP Deployment
### AWS EC2 | Ubuntu 24.04 | LAMP Stack | Feed-Enabled SOC Deployment

---

# 1️⃣ Apache Not Running

## Symptoms

* https://EC2_PUBLIC_IP not loading
* Connection refused
* 502 / 503 error

## Check

```bash
systemctl status apache2
```

## Fix

```bash
sudo systemctl restart apache2
sudo systemctl enable apache2
```

Check logs:

```bash
sudo tail -f /var/log/apache2/error.log
```

---

# 2️⃣ MariaDB Not Running

## Symptoms

* Database connection error in UI
* Login fails
* Events not loading

## Check

```bash
systemctl status mariadb
```

## Fix

```bash
sudo systemctl restart mariadb
sudo systemctl enable mariadb
```

Verify DB file:

```bash
ls /var/www/MISP/app/Config/database.php
```

If missing → installer failed → re-run installer clean.

---

# 3️⃣ Redis Not Running

## Symptoms

* Workers inactive
* Correlation disabled
* Feed caching stuck
* Background jobs failing

## Check

```bash
systemctl status redis-server
```

## Fix

```bash
sudo systemctl restart redis-server
sudo systemctl enable redis-server
```

---

# 4️⃣ BaseURL Incorrect (AWS Issue)

## Symptoms

* Redirects to misp.local
* SSL mismatch
* Login loops

## Fix

Get IP:

```bash
curl -s http://169.254.169.254/latest/meta-data/public-ipv4
```

Set:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Admin setSetting MISP.baseurl "https://EC2_PUBLIC_IP"
```

Reload:

```bash
sudo systemctl reload apache2
```

---

# 5️⃣ SSL Not Working

## Symptoms

* Browser insecure warning
* HTTPS not loading

## Fix

```bash
sudo a2enmod ssl
sudo systemctl reload apache2
```

Verify:

```bash
apachectl -M | grep ssl
```

---

# 6️⃣ 500 Internal Server Error

## Common Causes

* PHP memory limit low
* Permission issue
* MariaDB failure
* Redis stopped

## Check Logs

```bash
sudo tail -f /var/www/MISP/app/tmp/logs/error.log
sudo tail -f /var/log/apache2/error.log
```

---

# 7️⃣ Workers Not Running

## Symptoms

* Correlation not working
* Feeds not fetching
* Scheduled tasks inactive

## Fix

Restart workers:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake CakeResque.CakeResque start
```

Or restart services:

```bash
sudo systemctl restart redis-server
sudo systemctl restart apache2
```

---

# 8️⃣ Feed Stuck in "Not Cached"

## Symptoms

* Red “Not cached” label
* Feed enabled but not usable

## Causes

* Redis stopped
* Permissions issue
* Feed URL unreachable

## Fix (CLI preferred)

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Server cacheFeed all
```

Or specific feed:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Server cacheFeed FEED_ID
```

Check Redis:

```bash
systemctl status redis-server
```

---

# 9️⃣ Fetch & Store Not Importing Events

## Symptoms

* Feed cached but no events visible
* Events → List Events empty

## Causes

* Timestamp filter too strict
* Tag filter blocking events
* Fetch not executed

## Fix

Test without filter temporarily:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Server fetchFeed FEED_ID
```

Check logs:

```bash
sudo tail -f /var/www/MISP/app/tmp/logs/error.log
```

---

# 🔟 Feed Import Causing High CPU / RAM

## Symptoms

* Server slow
* MariaDB high CPU
* Redis backlog
* System freezing

## Check

```bash
htop
free -h
df -h
```

## Fix

* Reduce timestamp window (`30d` instead of `90d`)
* Disable unused feeds
* Fetch one feed at a time
* Increase RAM (recommended 16GB for production)

---

# 1️⃣1️⃣ Cron Not Running Feed Updates

## Symptoms

* Feeds not updating automatically
* Old events only

## Check cron

```bash
sudo crontab -u www-data -l
```

If missing, add:

```bash
0 * * * * /var/www/MISP/app/Console/cake Server cacheFeed all
30 * * * * /var/www/MISP/app/Console/cake Server fetchFeed all
```

Restart cron:

```bash
sudo systemctl restart cron
```

---

# 1️⃣2️⃣ Permission Issues

## Symptoms

* Cannot write logs
* Cannot save events
* Attachment upload fails

## Fix

```bash
sudo chown -R www-data:www-data /var/www/MISP
sudo chmod -R 755 /var/www/MISP
```

---

# 1️⃣3️⃣ Installer Fails Midway

## Causes

* Low RAM
* Disk full
* Interrupted execution

## Check Memory

```bash
free -h
```

## Check Disk

```bash
df -h
```

Minimum recommended:

* 4 vCPU
* 16GB RAM
* SSD storage

If corrupted:

```bash
sudo rm -rf /var/www/MISP
Re-run installer
```

---

# 🔎 Log Locations Summary

| Component | Location                   |
| --------- | -------------------------- |
| MISP      | /var/www/MISP/app/tmp/logs |
| Apache    | /var/log/apache2/error.log |
| MariaDB   | /var/log/mysql/error.log   |
| Redis     | journalctl -u redis-server |

---

# 🧠 Advanced Debug Mode (Temporary Only)

Edit:

```bash
sudo nano /var/www/MISP/app/Config/config.php
```

Set:

```php
'debug' => 1,
```

After troubleshooting revert to:

```php
'debug' => 0,
```

Never leave debug enabled in production.

---

# 🏁 Final Validation Checklist (Feed-Enabled Production Mode)

- ✔ Apache running
- ✔ MariaDB running
- ✔ Redis running
- ✔ database.php exists
- ✔ BaseURL correct
- ✔ SSL enabled
- ✔ Workers active
- ✔ Feeds enabled
- ✔ Feeds cached
- ✔ Events imported
- ✔ Cron configured
- ✔ Events visible in UI

---

If all above pass:

Your MISP deployment is:

- ✔ Stable
- ✔ Feed-enabled
- ✔ Automated
- ✔ SOC-ready
- ✔ Production-grade

---
