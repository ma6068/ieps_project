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
        if self.cur:
            self.cur.close()

    def createTables(self):
        code = open("database/crawldb.sql", "r").read()
        try:
            self.cur.execute(code)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()

    # ------------------------------  INSERT FUNCTIONS  ------------------------------

    def insertSite(self, domain=None, robots_content=None, sitemap_content=None):
        sql = "INSERT INTO crawldb.site(domain, robots_content, sitemap_content) VALUES (%s, %s, %s) RETURNING id"
        values = (domain, robots_content, sitemap_content)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
            result = self.cur.fetchone()
            return result[0]
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()
        return None

    def insertImage(self, page_id=None, filename=None, content_type=None, data=None, accessed_time=None):
        sql = "INSERT INTO crawldb.image(page_id, filename, content_type, data, accessed_time) " \
              "VALUES (%s, %s, %s, %s, %s) RETURNING id"
        values = (page_id, filename, content_type, data, accessed_time)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
            result = self.cur.fetchone()
            return result[0]
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()
        return None

    def insertPage(self, site_id=None, page_type_code=None, url=None, html_content=None, http_status_code=None,
                   accessed_time=None):
        if not page_type_code == 'DUPLICATE':
            sql = "INSERT INTO crawldb.page" \
                  "(site_id, page_type_code, url, html_content, http_status_code, accessed_time)" \
                  "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
            values = (site_id, page_type_code, url, html_content, http_status_code, accessed_time)
        else:
            sql = "INSERT INTO crawldb.page" \
                  "(site_id, page_type_code, url, http_status_code, accessed_time)" \
                  "VALUES (%s, %s, %s, %s, %s) RETURNING id"
            values = (site_id, page_type_code, url, http_status_code, accessed_time)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
            result = self.cur.fetchone()
            return result[0]
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()
        return None

    def insertPageData(self, page_id=None, data_type_code=None, data=None):
        sql = "INSERT INTO crawldb.page_data(page_id, data_type_code, data) VALUES (%s, %s, %s)"
        values = (page_id, data_type_code, data)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()

    def insertLink(self, from_page, to_page):
        sql = "INSERT INTO crawldb.link(from_page, to_page) VALUES (%s, %s)"
        values = (from_page, to_page)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()

    # ------------------------------  SELECT FUNCTIONS  ------------------------------
    def getSiteByDomain(self, domain=None):
        sql = "SELECT id FROM crawldb.site WHERE domain = %s"
        values = (domain, )
        try:
            self.cur.execute(sql, values)
            result = self.cur.fetchone()
            if result:
                return result
        except psycopg2.IntegrityError as error:
            raise error
        except (Exception, psycopg2.DatabaseError):
            self.conn.rollback()
        return None
