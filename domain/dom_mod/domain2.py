import requests, logging, datetime, json, sqlite3, time



def domain_list():
    return ["d13579.com", "kingbaly.com", "xdl5566.com", "xindeli015.com", "bzj55.com",
            "f13579.com", "a1628.net", "deli2828.com", "xindeli099.com", "xindeli789.com", "xindeli168.com","animater.cn", "xylintai.cn", "osmtv.cn", "weik.me", "rzkangyuan.cn", "jiusheng.tv", "kbonlive.cn", "yixiuxian.cn", "drbear.shop", "fotric.org.cn", "hqlzx.com", "yay567.com"]

def domain_status(specific_domain, domain_timeout=10, domain_delay=5):
    try:
        r = requests.get(
        "http://v.juhe.cn/siteTools/app/NewDomain/query.php?key=0066ee95da11143ef165f348ccd105a8&domainName={0}".format(
           specific_domain), timeout=domain_timeout)
        r = json.loads(r.text)
        time.sleep(domain_delay)
        if not r["result"]:
            msg = "ERROR"
            return msg
        else:
            msg = "OK"
            return msg
    except:
        msg = "TIMEOUT"
        return msg

def domain_store():
    db_table = "domainlist"
    db_columid = "domain_id"
    db_column1 = "domains"
    db_column2 = "status"
    db_column3 = "lastcheck"
    db_column4 = "forcecheck"
    db_conn = sqlite3.connect('domain.db')
    cursor = db_conn.cursor()
#    db_conn.execute("DROP TABLE IF EXISTS {0}".format(db_table))
    try:
        db_conn.execute("CREATE TABLE {}({} TEXT, {} TEXT, {} TEXT, {} TEXT, {} INTEGER PRIMARY KEY)".format(db_table, db_column1, db_column2, db_column3, db_column4, str(db_columid)))
        db_conn.commit()
        for list in domain_list():
            d_status = domain_status(list, domain_timeout=10, domain_delay=4)
            params = (list, d_status, datetime.datetime.now(),"---")
            db_conn.execute("INSERT INTO {}({},{},{},{}) VALUES (?, ?, ?, ?)".format(db_table,db_column1,db_column2,db_column3,db_column4), params)
#            db_conn.execute("INSERT INTO {} VALUES (?, ?, ?, ?)".format(db_table), params)
            db_conn.commit()
        db_conn.close()
    except Exception as e:
        cursor.execute("SELECT {0} FROM {1}".format(db_column1,db_table))
        d_list_tuple = cursor.fetchall()
        for d_list in d_list_tuple:
            d_status = domain_status(d_list[0], domain_timeout=10, domain_delay=4)
            params = (str(d_status), str(datetime.datetime.now()),str(d_list[0]))
            cursor.execute("UPDATE {0} SET {1}=?, {2}=? WHERE {3}=? ".format(db_table,db_column2,db_column3,db_column1), params)
            db_conn.commit()
        db_conn.close()
        return e


def domain_forcecheck(f_domain,f_domain_column1="domains",f_table="domainlist",f_domain_column4="forcecheck"):
    db_conn = sqlite3.connect('domain.db')
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM {} WHERE domains=?".format(f_table),(str(f_domain),))
    d_list_tuple = cursor.fetchall()[0]
    f_check_str = domain_status(d_list_tuple[0]) + " - " + str(datetime.datetime.now())
    cursor.execute("UPDATE {0} SET {1}=? WHERE {2}=? ".format(f_table, f_domain_column4, f_domain_column1),(f_check_str,str(f_domain)))
    db_conn.commit()
    db_conn.close()
    return f_check_str





if __name__ == "__main__":
    print(domain_store())






