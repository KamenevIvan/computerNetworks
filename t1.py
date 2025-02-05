import csv

from pythonping import ping

sites = {
    "google.com":'74.125.195.100',
    "youtube.com":'142.250.217.78',
    "facebook.com":'157.240.3.35',
    "instagram.com":'157.240.3.174',
    "whatsapp.com":'157.240.3.54',
    "x.com":'104.244.42.65',
    "wikipedia.org":'208.80.153.224',
    "chatgpt.com":'104.18.32.47',
    "reddit.com":'151.101.129.140',
    "yahoo.com":'74.6.231.20'
}

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Site", " Ping (ms)"])
    for site, ip in sites.items():
        writer.writerow([site, ping(ip, count=1).rtt_avg_ms]) 

print("Done!")