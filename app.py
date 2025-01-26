from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import datetime

app = Flask(__name__)
api = Api(app)

DATABASE_URL = "sqlite:///hospital.db"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False, unique=True)
    phone = Column(String(length=15), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}')"
    
class Doctor(Base):
    __tablename__ = 'doctor'
    doctor_id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False, unique=True)
    phone = Column(String(length=15), nullable=False, unique=True)
    specialization = Column(String(length=100))
    created_at = Column(DateTime, default=func.now())
    def __repr__(self):
        return f"Doctor('{self.name}', '{self.email}', '{self.phone}', '{self.specialization}'"
    
class Appointment(Base):
    __tablename__ = 'appointment'
    apt_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    doctor_id = Column(Integer, ForeignKey('doctor.doctor_id', ondelete='CASCADE'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    def __repr__(self):
        return f"Appointment('{self.user_id}', '{self.doctor_id}', '{self.start_time}', '{self.end_time}'"
    
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class UserAppointments(Resource):
    def get(self, user_id):
        return {"msg":"UserAppointments", "user":user_id}

class DoctorAppointments(Resource):
    def get(self, doctor_id):
        return {"msg":"DoctorAppointments", "doctor":doctor_id}

class CreateAppointment(Resource):
    def post(self):
        return {"msg":"Appointment Created"}, 201

class UpdateAppointment(Resource):
    def put(self):
        return {"msg":"Appointment Updated"}, 200

class DeleteAppointment(Resource):
    def delete(self, apt_id):
        return {"msg":"Appointment Deleted"}, 200

api.add_resource(UserAppointments, '/appointments/user/<int:user_id>')
api.add_resource(DoctorAppointments, '/appointments/doctor/<int:doctor_id>')
api.add_resource(CreateAppointment, '/appointments')
api.add_resource(UpdateAppointment, '/appointments/<int:apt_id>')
api.add_resource(DeleteAppointment, '/appointments/<int:apt_id>')

if __name__ == '__main__':
    app.run(debug=True)
