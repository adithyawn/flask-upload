from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)


# engine = create_engine('mysql://stratekc_root:E0r6Quq20Fmg@localhost/stratekc_test')
# con = engine.connect()
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/coba'
app.config['SQLALCHEMNY_TRACK_MODIFICATIONS'] =False #ini buat alert kalo ada perubahan tapi gak perlu jadi di off
app.config['SQLALCHEMNY_TRACK_ECHO'] =False

db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)     #sqlalchemy butuh promary key di setiap tabel untuk relation ke table lain
    username = db.Column(db.String(30) , unique = True) #30 karakter batasnya, dan sifatnya unique
    password = db.Column(db.String(30))
    email = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)

    orders = db.relationship('Order', backref='member', lazy='dynamic') #Order itu dari class Order, backref = 'member' adalah Pseudo Column bisa menghubungkan antara username, email, etc di class Member ke member_id 

    courses = db.relationship('Course', secondary='user_courses', backref='member', lazy = 'dynamic')

    def __repr__(self): #return representation from object, anggap aja random string
        return '<Member %r>' % self.username

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id')) #member.id itu dari class Member.id

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

#Gabungin semua dari class Course dengan Class Member.
#courses = db.relationship('Course') ini ngacu ke Course yang diambil member, secondary = 'user_courses' itu untuk nyimpen data course id dan member idnya
#backref = member itu untuk jadi pseudo coloum, menghubungkan antara user_courses dan class Member
db.Table('user_courses',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
    )

############## PENGAPLIKASIAN #########################
# >>> from app import db, Member, Order, Course
# >>> course1 = Course(name='Course One')
# >>> course2 = Course(name='Course Two')
# >>> course3 = Course(name='Course Three')
# >>> db.session(course1)
# >>> db.session.add(course1)
# >>> db.session.add(course2)
# >>> db.session.add(course3)
# >>> db.commit()

# >>> Course.member
# <sqlalchemy.orm.attributes.InstrumentedAttribute object at 0x0000029BC14C4830>
# >>> course1.member
# [] -> JADI LIST BEGINI
# >>> course2.member
# []
# >>> adithya = Member.query.filter(Member.username == 'adithya').first()
# >>> adithya
# <Member 'adithya'>

# >>> course1.member.append(adithya)

# >>> michele = Member.query.filter(Member.username == 'michele').first()

# >>> michele
# <Member 'michele'>

# >>> course1.member.append(michele)

# >>> course1.member
# [<Member 'adithya'>, <Member 'michele'>]
# >>> db.session.commit() -> Menambahkan list member ke course 1

#### Bisa cek dari sudut pandang Member, course apa aja yg diambil tuh ####
# >>> adithya
# <Member 'adithya'>
# >>> adithya.courses
# <sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x000001F6892D1CC0>
# >>> adithya.courses.all()
# [<Course 1>]

# >>> michele
# <Member 'michele'>
# >>> michele.courses
# <sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x000001F68B196240>
# >>> michele.courses.all()
# [<Course 1>]

### Bisa juga dari sudut pandang Course ###
# >>> course1.member
# <Member 'adithya'>, <Member 'michele'>




if __name__ == '__main__':
    app.run(debug=True)

