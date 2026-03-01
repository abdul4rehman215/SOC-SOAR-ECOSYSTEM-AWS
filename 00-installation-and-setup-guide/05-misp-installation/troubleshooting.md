# 🚨 MISP Deployment – Troubleshooting Guide
### AWS EC2 | Ubuntu 24.04 | LAMP Stack

---

# 1️⃣ Apache Not Running

## Symptoms
- https://EC2_PUBLIC_IP not loading
- Connection refused
- 502 / 503 error

## Check

```bash
systemctl status apache2
````

## Fix

```bash
sudo systemctl restart apache2
sudo systemctl enable apache2
```

If still failing:

```bash
sudo tail -f /var/log/apache2/error.log
```

---

# 2️⃣ MariaDB Not Running

## Symptoms

* MISP UI shows database connection error
* database.php exists but login fails

## Check

```bash
systemctl status mariadb
```

## Fix

```bash
sudo systemctl restart mariadb
sudo systemctl enable mariadb
```

Check DB file:

```bash
ls /var/www/MISP/app/Config/database.php
```

If missing → installer failed → re-run installer.

---

# 3️⃣ Redis Not Running

## Symptoms

* Background jobs stuck
* Correlation not working
* Workers inactive in MISP UI

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

* Redirecting to misp.local
* Cannot access from browser
* SSL certificate mismatch

## Fix

Get public IP:

```bash
curl -s http://169.254.169.254/latest/meta-data/public-ipv4
```

Set correct base URL:

```bash
sudo -u www-data /var/www/MISP/app/Console/cake Admin setSetting MISP.baseurl "https://EC2_PUBLIC_IP"
```

Reload Apache:

```bash
sudo systemctl reload apache2
```

---

# 5️⃣ SSL Not Working

## Symptoms

* Browser shows insecure site
* SSL module disabled
* HTTPS not loading

## Fix

```bash
sudo a2enmod ssl
sudo systemctl reload apache2
```

Check:

```bash
apachectl -M | grep ssl
```

---

# 6️⃣ 500 Internal Server Error

## Most Common Causes

* PHP memory limit too low
* Permissions issue
* MariaDB failure
* Redis stopped

## Check logs

```bash
sudo tail -f /var/www/MISP/app/tmp/logs/error.log
```

Also check:

```bash
sudo tail -f /var/log/apache2/error.log
```

---

# 7️⃣ Workers Not Running

## Symptoms

* Correlation disabled
* Scheduled tasks not executing
* Email notifications not sent

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

# 8️⃣ Installer Fails Midway

## Causes

* Low RAM
* Interrupted execution
* Network instability
* Disk space full

## Check memory

```bash
free -h
```

Minimum recommended for this deployment:

16GB RAM (t2.xlarge)

Check disk:

```bash
df -h
```

If corrupted → safest fix:

```bash
sudo rm -rf /var/www/MISP
Re-run installer clean
```

---

# 9️⃣ Permission Issues

## Symptoms

* Cannot write to logs
* Errors saving events
* Attachment upload fails

## Fix

```bash
sudo chown -R www-data:www-data /var/www/MISP
sudo chmod -R 755 /var/www/MISP
```

---

# 🔟 Performance Slow

## Common Causes

* Low RAM
* MariaDB heavy load
* Large event correlation
* Redis queue backlog

## Check CPU usage

```bash
htop
```

## Check MySQL processes

```bash
sudo mysqladmin processlist
```

Production sizing used in this project:

* 4 vCPU
* 16GB RAM
* SSD storage

---

# 🔎 Log Locations Summary

| Component | Log Location               |
| --------- | -------------------------- |
| MISP      | /var/www/MISP/app/tmp/logs |
| Apache    | /var/log/apache2/error.log |
| MariaDB   | /var/log/mysql/error.log   |
| Redis     | journalctl -u redis-server |

---

# 🧠 Advanced Debug Mode

Enable debug (temporary only):

```bash
sudo nano /var/www/MISP/app/Config/config.php
```

Set:

```php
'debug' => 1,
```

After troubleshooting → revert to:

```php
'debug' => 0,
```

---

# 🏁 Final Validation Checklist

✔ Apache running
✔ MariaDB running
✔ Redis running
✔ database.php exists
✔ BaseURL correct
✔ SSL enabled
✔ Workers active
✔ Login successful

---

If everything above passes, your MISP deployment is production-ready.

---
