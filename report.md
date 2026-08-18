# Security Log Analysis Report

## Executive Summary
**Two significant threats detected** requiring immediate attention.

---

## 🔴 THREAT 1: Brute Force Attack + Suspicious Post-Login Activity
**Severity: CRITICAL**

### Evidence
```
10:23:01–10:23:05  5 failed logins in 4 seconds  user=admin  ip=192.168.1.105
10:23:06           Successful login               user=admin  ip=192.168.1.105
10:25:33           Accessed /etc/passwd           user=admin  ip=192.168.1.105
```

### Why This Is Alarming
| Indicator | Detail |
|-----------|--------|
| Login speed | 5 attempts in **4 seconds** — automated/scripted |
| Brute force success | Attack **succeeded** — credentials compromised |
| /etc/passwd access | Contains user account data; classic **privilege escalation** recon |
| Attack origin | Internal IP (192.168.1.105) — **insider threat or compromised internal host** |

### Recommended Actions
- [ ] **Immediately disable** the admin account
- [ ] **Isolate** host 192.168.1.105 from the network
- [ ] Audit all actions taken during the 10:24–session
- [ ] Check if /etc/passwd was exfiltrated
- [ ] Rotate all credentials on affected systems
- [ ] Enforce MFA on privileged accounts

---

## 🟠 THREAT 2: External Brute Force Attempt
**Severity: HIGH**

### Evidence
```
10:45:02–10:45:04  3 failed logins in 2 seconds  user=root  ip=203.0.113.42
```

### Why This Is Concerning
| Indicator | Detail |
|-----------|--------|
| Target account | **root** — highest privilege account |
| Attack speed | Automated — 3 attempts in 2 seconds |
| Source IP | **203.0.113.42** — external/public IP address |
| Attack status | **Blocked so far** — but ongoing risk |

### Recommended Actions
- [ ] **Block 203.0.113.42** at the firewall immediately
- [ ] Verify root SSH login is **disabled** (`PermitRootLogin no`)
- [ ] Scan for other IPs attempting similar patterns
- [ ] Consider deploying **fail2ban** or equivalent

---

## 🟢 CLEAN EVENT
```
10:31:44  SUCCESS LOGIN  user=sara  ip=10.0.0.12
```
Normal internal login. No anomalies detected.

---

## System-Wide Recommendations

```
Priority  Action
────────────────────────────────────────────────────
1         Account lockout after 3–5 failed attempts
2         Enforce MFA on all privileged accounts
3         Alert on /etc/passwd, /etc/shadow access
4         Block direct root login via SSH
5         Implement real-time SIEM alerting
6         Regular credential audits
```

---

**Bottom Line:** The admin account on `192.168.1.105` was very likely compromised. The subsequent `/etc/passwd` access suggests active reconnaissance. Treat this as an **active incident** until proven otherwise.