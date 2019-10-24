import json, sqlite3

class SslMonitor():
    def toQueryDom(self):
        conn = sqlite3.connect('/root/zabbix/db.sqlite3')
        cur = conn.cursor()
        cur.execute("SELECT domain FROM SSLDOMAINS_ssldomain")
        b = cur.fetchall()
        d = {"data":[]}
        for new_b in b:
            d["data"].append({"{#DOMAINSSL}":new_b[0]})
        return json.dumps(d)


if __name__=="__main__":
    a = SslMonitor()
    print(a.toQueryDom())
