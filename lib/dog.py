import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []

    def __init__(self, name, breed, id = None):
        self.name = name
        self.breed = breed
        self.id = id
    
    @classmethod
    def create_table(self):
        sql = f"CREATE TABLE IF NOT EXISTS {self.__name__.lower()}s (id INTEGER PRIMARY KEY, name TEXT, breed TEXT);"
        CURSOR.execute(sql)
    
    @classmethod
    def drop_table(self):
        sql = f"DROP TABLE IF EXISTS {self.__name__.lower()}s;"
        CURSOR.execute(sql)
    
    @classmethod
    def create(self, name, breed):
        sql = f"INSERT INTO {self.__name__.lower()}s (name, breed) VALUES (?, ?);"
        CURSOR.execute(sql, (name, breed))
        id = CURSOR.execute(f"SELECT last_insert_rowid() from {self.__name__.lower()}s;").fetchone()[0]
        dog = Dog(name, breed, id)
        self.all.append(dog)
        return dog
    
    @classmethod
    def new_from_db(self, row):
        id, name, breed = row
        return Dog(name, breed, id)
    
    @classmethod
    def get_all(self):
        sql = f"SELECT * FROM {self.__name__.lower()}s"
        rows = CONN.execute(sql).fetchall()
        self.all = [self.new_from_db(row) for row in rows]
        return self.all
    
    @classmethod
    def find_by_name(self, name):
        sql = f"SELECT name FROM {self.__name__.lower()}s WHERE name == ?"
        row = CONN.execute(sql, (name,)).fetchone()
        for dog in self.all:
            if row and dog.name == row[0]:
                return dog
        return None
        # return next((x for x in self.all if x.name == row[1]), [None])
    
    @classmethod
    def find_by_id(self, id):
        sql = f"SELECT id FROM {self.__name__.lower()}s WHERE id == ?"
        row = CONN.execute(sql, (id,)).fetchone()
        for dog in self.all:
            if row and dog.id == row[0]:
                return dog
        return None
        # return next((x for x in self.all if x.id == row[0]), [None])
    
    @classmethod
    def find_or_create_by(self, name, breed):
        return self.find_by_name(name) or self.create(name, breed)

    def save(self):
        sql = f"INSERT INTO {self.__class__.__name__.lower()}s (name, breed) VALUES (?, ?);"
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute(f"SELECT last_insert_rowid() from {self.__class__.__name__.lower()}s;").fetchone()[0]
        self.__class__.all.append(self)
        return self

    def update(self):
        sql = f"UPDATE {self.__class__.__name__.lower()}s SET name = ?, breed = ? WHERE id = ?;"
        CONN.execute(sql, (self.name, self.breed, self.id,))
        # import ipdb; ipdb.set_trace()

Dog.drop_table()
Dog.create_table()
joey = Dog.create("joey", "cocker spaniel")
joey.name = "joseph"
joey.update()