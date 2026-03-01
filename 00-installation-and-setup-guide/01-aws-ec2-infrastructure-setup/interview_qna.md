# 🎤 Interview Q&A — Project 01: AWS EC2 Foundation Setup (SOC / SOAR Ecosystem)

---

## 1) Why did you create a custom VPC instead of using the default VPC?
A custom VPC gives full control over subnet design, routing, DNS settings, and security boundaries, which reduces deployment issues for SOC tools.

---

## 2) What is the role of an Internet Gateway (IGW) in AWS?
An IGW allows traffic between the VPC and the public internet. Without it, the instance cannot reach the internet even if it has a public IP.

---

## 3) Why is the route table important for internet connectivity?
The route table decides where traffic goes. A public subnet must have a `0.0.0.0/0` route pointing to the IGW for outbound internet access.

---

## 4) What does “Auto-assign public IPv4” do on a subnet?
It ensures instances launched in that subnet automatically receive a public IPv4 address (if enabled during launch), which is required for direct SSH access.

---

## 5) What is the difference between Security Groups and NACLs?
Security Groups are stateful and apply at the instance level, while NACLs are stateless and apply at the subnet level, requiring inbound and outbound rules for return traffic.

---

## 6) Why did you restrict SSH (port 22) to your IP only?
To reduce exposure to brute-force attacks and scanning. Allowing SSH from `0.0.0.0/0` is risky, especially when SOC dashboards will be deployed later.

---

## 7) Why do you test `ping 8.8.8.8` before installing anything?
If `8.8.8.8` fails, it indicates a routing or outbound connectivity issue. Installing tools before fixing network causes repeated failures and wasted time.

---

## 8) What does it mean if `ping 8.8.8.8` works but `curl google.com` fails?
That usually indicates a DNS problem (name resolution). Internet is reachable, but domain names are not resolving correctly.

---

## 9) Why is correct timezone and NTP time sync important for SOC tools?
SOC tools rely on accurate timestamps for correlation, investigation timelines, alert ordering, and report credibility. Time drift can break detection logic.

---

## 10) Why did you set hostnames like “thehive” on new machines?
Clear hostnames improve service management, log readability, and multi-tool deployments. It also helps when integrating components across multiple servers.

---

## 11) Why do you update `/etc/hosts` after changing hostname?
It ensures local name resolution works properly for applications and services. Some tools may fail or behave inconsistently if hostname resolution is broken.

---

## 12) What is the purpose of creating a base SOC directory layout (`logs/ scripts/ reports/ evidence/`)?
It keeps the environment organized from day one, makes investigation workflow cleaner, and supports repeatable documentation for the portfolio.

---

## 13) Why would you consider using an Elastic IP?
Elastic IP gives a stable public IP, which avoids access issues when instances are stopped/started and their public IP changes.

---

## 14) What is the biggest lesson from this setup phase?
Most SOC lab failures happen due to network misconfiguration (IGW/route table/subnet/SG). Fixing connectivity first prevents tool installation problems later.

---

## 15) How does this EC2 foundation help future SOC/SOAR projects?
It provides a clean, validated base where every tool installation becomes smoother, troubleshooting becomes faster, and integrations are more predictable.

---
