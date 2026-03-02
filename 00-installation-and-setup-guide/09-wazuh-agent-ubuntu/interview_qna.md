# 🎯 Interview Q&A –  Wazuh Agent Deployment – Ubuntu 24.04
### Endpoint Security Integration with Wazuh Manager (AWS SOC)

---

### What is Wazuh Agent?

Wazuh Agent is the endpoint data collector that sends logs, integrity events, and security telemetry to the Wazuh Manager.

---

### What does FIM do?

Monitors file changes in critical directories and generates alerts on unauthorized modifications.

---

### Why enable real-time monitoring for /tmp?

Because malware often drops payloads in /tmp.

---

### Why skip /proc and /sys?

They are virtual filesystems and generate noise.

---

### What happens if port 1514 is blocked?

Agent cannot communicate with manager.

---

### Why use AES encryption?

Secure communication between agent and manager.

---
