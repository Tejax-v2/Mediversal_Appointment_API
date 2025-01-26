from flask import Flask, request, jsonify
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
        return f"Doctor('{self.name}', '{self.email}', '{self.phone}', '{self.specialization}')"

class Appointment(Base):
    __tablename__ = 'appointment'
    apt_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    doctor_id = Column(Integer, ForeignKey('doctor.doctor_id', ondelete='CASCADE'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    def __repr__(self):
        return f"Appointment('{self.user_id}', '{self.doctor_id}', '{self.start_time}', '{self.end_time}')"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class UserAppointments(Resource):
    def get(self, user_id):
        appointments = session.query(Appointment).filter_by(user_id=user_id).all()
        if not appointments:
            return {"msg": "No appointments found for the user."}, 404

        result = [
            {
                "apt_id": apt.apt_id,
                "doctor_id": apt.doctor_id,
                "start_time": apt.start_time,
                "end_time": apt.end_time,
                "created_at": apt.created_at
            } for apt in appointments
        ]
        return jsonify(result)

class DoctorAppointments(Resource):
    def get(self, doctor_id):
        appointments = session.query(Appointment).filter_by(doctor_id=doctor_id).all()
        if not appointments:
            return {"msg": "No appointments found for the doctor."}, 404

        result = [
            {
                "apt_id": apt.apt_id,
                "user_id": apt.user_id,
                "start_time": apt.start_time,
                "end_time": apt.end_time,
                "created_at": apt.created_at
            } for apt in appointments
        ]
        return jsonify(result)

class CreateAppointment(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        doctor_id = data.get('doctor_id')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if not (user_id and doctor_id and start_time and end_time):
            return {"msg": "Missing required fields."}, 400

        new_appointment = Appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            start_time=datetime.datetime.fromisoformat(start_time),
            end_time=datetime.datetime.fromisoformat(end_time)
        )

        session.add(new_appointment)
        session.commit()
        return {"msg": "Appointment Created", "apt_id": new_appointment.apt_id}, 201

class UpdateAppointment(Resource):
    def put(self, apt_id):
        data = request.get_json()
        appointment = session.query(Appointment).filter_by(apt_id=apt_id).first()

        if not appointment:
            return {"msg": "Appointment not found."}, 404

        appointment.start_time = datetime.datetime.fromisoformat(data.get('start_time', appointment.start_time.isoformat()))
        appointment.end_time = datetime.datetime.fromisoformat(data.get('end_time', appointment.end_time.isoformat()))

        session.commit()
        return {"msg": "Appointment Updated", "apt_id": apt_id}, 200

class DeleteAppointment(Resource):
    def delete(self, apt_id):
        appointment = session.query(Appointment).filter_by(apt_id=apt_id).first()

        if not appointment:
            return {"msg": "Appointment not found."}, 404

        session.delete(appointment)
        session.commit()
        return {"msg": "Appointment Deleted", "apt_id": apt_id}, 200

api.add_resource(UserAppointments, '/appointments/user/<int:user_id>')
api.add_resource(DoctorAppointments, '/appointments/doctor/<int:doctor_id>')
api.add_resource(CreateAppointment, '/appointments')
api.add_resource(UpdateAppointment, '/appointments/<int:apt_id>')
api.add_resource(DeleteAppointment, '/appointments/<int:apt_id>')

if __name__ == '__main__':
    app.run(debug=True)
