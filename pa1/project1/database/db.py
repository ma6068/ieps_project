import psycopg2


class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connectDB()

    # ------------------------------  CONNECT DB, DISCONNECT DB AND CREATE TABLES   ------------------------------
    def connectDB(self):
        try:
            self.conn = psycopg2.connect(
                database="crawler",
                host="localhost",
                user="postgres",
                password="password"
            )
            self.cur = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnectDB(self):
        if self.conn:
            self.conn.close()

    def createTables(self):
        code = open("crawldb.sql", "r").read()
        try:
            self.cur.execute(code)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()

    # ------------------------------  INSERT FUNCTIONS  ------------------------------

    def insertSite(self, domain=None, robots_content=None, sitemap_content=None):
        sql = "INSERT INTO crawldb.site(domain, robots_content, sitemap_content) VALUES (%s, %s, %s)"
        values = (domain, robots_content, sitemap_content)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()

    def insertImage(self, page_id=None, filename=None, content_type=None, data=None, accessed_time=None):
        sql = "INSERT INTO crawldb.image(page_id, filename, content_type, data, accessed_time) " \
              "VALUES (%s, %s, %s, %s, %s)"
        values = (page_id, filename, content_type, data, accessed_time)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()



    '''
    def insertPage(self, site_id=None, page_type_code=None, url=None, html_content=None, http_status_code=None,
                   accessed_time=None):
        if page_type_code == 'HTML':
            sql = "INSERT INTO page(site_id, page_type_code, url, html_content, http_status_code, accessed_time) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            values = (site_id, page_type_code, url, html_content, http_status_code, accessed_time)
        else:
    '''
