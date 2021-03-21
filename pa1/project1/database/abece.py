import db

a = db.DB()

a.connectDB()
a.createTables()
value = a.insertSite('dsadasd', 'ime na fajlot', 'sodrzina')
print(value)
value2 = a.insertPage(value, 'HTML', 'fsdfds', 'dasdada', '200', None)
print(value2)

