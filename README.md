# CyberNetLabs-LoadBalancer

Secure Python Load Balancer with SSL/TLS Encryption and Real-time Web Dashboard  
**Developed by CyberNet Labs**

---

## Overview

The **CyberNetLabs-LoadBalancer** is a lightweight, secure, and real-time network load balancer.  
It distributes incoming HTTPS connections across multiple backend servers, and provides a beautiful dashboard to monitor traffic.

---

## Features
- **SSL/TLS encryption** for secure client communication
- **Load balancing modes**: Round Robin or Random
- **Real-time Dashboard** (view total requests and backend server stats)
- **Cross-platform**: Works on **Mac**, **Windows**, **Linux**, and even **Android** (using Termux or Pydroid)
- **Simple setup** — only requires Python 3

---

## Project Structure
CyberNetLabs-LoadBalancer/



├── CNL-loadBalancer.py       # Main Load Balancer

├── cnl-dashboard.html        # Dashboard Webpage

├── cnl-style.css             # Dashboard Styling

├── README.md                 # Documentation

├── server.key (not uploaded) # SSL Private Key

├── server.crt (not uploaded)# SSL #Certificate

> **Note**: `server.key` and `server.crt` are intentionally not uploaded for security reasons.

---

## Requirements

- Python 3.x (works with Python 3.7+)
- Basic Terminal/Command Prompt
- Internet connection (for backend servers)

No external libraries required — everything uses Python's built-in modules!

---

## How to Install and Run

### 1. Install Python 3
- **Mac**: Installed by default or update via [brew](https://brew.sh/):  
  ```bash
  brew install python
  •	Windows: Download Python and install it.
	•	Android: Install Pydroid 3 (Play Store) or Termux and run:
  pkg install python

  ###2. Clone or Download This Project
  git clone https://github.com/your-username/CyberNetLabs-LoadBalancer.git
```bash
cd CyberNetLabs-LoadBalancer

```
(Or download as a ZIP and extract it.)

### 3. Generate SSL Certificates

(Skip if you already have them.)

In the project folder, open terminal and run: 
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt

•	When asked for info, just press Enter or fill as needed.
	•	This creates your encryption keys.
### 4. Run the Load Balancer
python CNL-loadBalancer.py
The program will ask you:
	•	Backend servers (example: 127.0.0.1:5000, 127.0.0.1:5001, etc.)
	•	Listening port (example: 8443)
	•	Mode: round_robin or random
 ### 5. Access the Dashboard

After starting:
	•	Go to the Dashboard:
http://localhost:9090/dashboard

It shows:
	•	Load balancing mode
	•	Total requests
	•	Hits per backend server
## Example Usage

Enter backend server IP (e.g., 127.0.0.1:5000) or type 'done' to finish: 127.0.0.1:5000
Enter backend server IP (e.g., 127.0.0.1:5000) or type 'done' to finish: 127.0.0.1:5001
done

Enter Load Balancer listening port (e.g., 8443): 8443

Select balancing mode - [round_robin/random]: random

Now your Load Balancer is running securely on HTTPS!

⸻

## Important Notes
	•	Backends must be ready before connecting (they can be simple HTTP servers).
	•	Certificate is self-signed — browsers will warn you about security (expected for testing).
	•	Private keys must be kept secure and should NOT be pushed to GitHub.

## License

Licensed under the MIT License.
Feel free to modify, improve, and use it in your own projects.

## About

CyberNetLabs-LoadBalancer is proudly developed by CyberNet Labs
Innovating the future of secure networking.

