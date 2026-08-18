# Security Log Analysis Report

## 🔴 Critical Threats Identified

---

### Threat #1 — Brute Force Attack → Successful Compromise
**Severity: CRITICAL**

```
Time Window:  10:23:01 – 10:24:10 (69 seconds)
Source IP:    192.168.1.105 (INTERNAL network)
Target User:  admin
```

**Evidence Chain:**
```
10:23:01-05  5 failed logins in 5 seconds     ← Automated brute force
10:24:10     Successful login                  ← Account compromised
10:25:33     Accessed /etc/passwd              ← Credential harvesting
```

**Why This Is Severe:**
- 5 failures in **5 seconds** = scripted/automated attack
- Attack **succeeded** — account is actively compromised
- `/etc/passwd` access immediately post-login suggests **privilege escalation recon**
- Internal IP means **insider threat OR compromised internal machine**

**Immediate Actions:**
- [ ] Disable `admin` account NOW
- [ ] Isolate or investigate host `192.168.1.105`
- [ ] Audit all actions taken by this session
- [ ] Check if `/etc/passwd` data was exfiltrated

---

### Threat #2 — External Brute Force in Progress
**Severity: HIGH**

```
Time Window:  10:45:02 – 10:45:04 (ongoing)
Source IP:    203.0.113.42 (EXTERNAL — public internet)
Target User:  root
```

**Evidence:**
```
10:45:02-04  3 failed logins in 3 seconds     ← Active brute force
             Attack still ongoing at log end   ← May have continued
```

**Why This Is Concerning:**
- Targeting `root` directly = maximum privilege goal
- External IP = likely automated botnet or targeted attacker
- Pattern matches Threat #1 — **may be coordinated**

**Immediate Actions:**
- [ ] Block `203.0.113.42` at firewall immediately
- [ ] Verify root login is disabled via SSH (`PermitRootLogin no`)
- [ ] Check if attack continued beyond log window
- [ ] Add rate limiting / fail2ban rule if not present

---

### ✅ Legitimate Activity Noted

```
10:31:44  SUCCESS LOGIN  user=sara  ip=10.0.0.12
```
- Single login, internal IP, no suspicious follow-up
- **Monitor** but no action required

---

## Summary Table

| # | Threat | Source | Severity | Status |
|---|--------|--------|----------|--------|
| 1 | Brute force + successful breach + passwd access | 192.168.1.105 (internal) | 🔴 Critical | Requires immediate response |
| 2 | External brute force on root | 203.0.113.42 (external) | 🟠 High | Block & monitor |
| 3 | Sara login | 10.0.0.12 (internal) | 🟢 Low | Normal — watch |

---

## Recommended Hardening Steps

```
1. ACCOUNT POLICY    Enforce lockout after 3–5 failed attempts
2. MFA               Require MFA for admin/root accounts
3. SSH HARDENING     Disable root SSH login, use key auth only
4. NETWORK           Restrict admin login to trusted IPs only
5. MONITORING        Deploy real-time alerting for failed login thresholds
6. AUDIT             Review /etc/passwd and /etc/shadow for tampering
```

> ⚠️ **Priority:** The Threat #1 chain (brute force → success → /etc/passwd) indicates an **active compromise** that should be treated as an incident response situation, not just a monitoring note.