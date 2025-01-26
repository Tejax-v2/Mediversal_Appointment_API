from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from flasgger import Swagger
import datetime

app = Flask(__name__)
api = Api(app)

swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Mediversal Appointment API",
    "description": "API for managing appointments",
    "contact": {
      "responsibleOrganization": "Tejax-v2",
      "responsibleDeveloper": "Tejax-v2",
      "email": "tejastupke74@gmail.com",
      "url": "https://github.com/Tejax-v2"
    }
}
}

swagger = Swagger(app, template=swagger_template)

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
        """
        Retrieve all appointments for a specific user.
        ---
        parameters:
          - in: path
            name: user_id
            type: integer
            example: 1
            required: true
            description: The ID of the user.
        responses:
          200:
            description: A list of appointments for the user.
            schema:
              type: array
              items:
                type: object
                properties:
                  apt_id:
                    type: integer
                    example: 3
                    description: The ID of the appointment.
                  doctor_id:
                    type: integer
                    description: The ID of the doctor.
                    example: 2
                  start_time:
                    type: string
                    format: date-time
                    example: '2025-01-01T13:00:00'
                    description: The start time of the appointment.
                  end_time:
                    type: string
                    format: date-time
                    example: '2025-01-01T14:00:00'
                    description: The end time of the appointment.
                  created_at:
                    type: string
                    format: date-time
                    example: '2025-01-01T12:00:00'
                    description: The time the appointment was created.
          404:
            description: The user was not found.
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: User not found
        """
        user = session.query(User).filter_by(user_id=user_id).all()
        if not user:
          return {"error": "User not found"}, 404
        appointments = session.query(Appointment).filter_by(user_id=user_id).all()
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
        """
        Retrieve all appointments for a specific doctor.
        ---
        parameters:
          - in: path
            name: doctor_id
            type: integer
            required: true
            example: 2
            description: The ID of the doctor.
        responses:
          200:
            description: A list of appointments for the doctor.
            schema:
              type: array
              items:
                type: object
                properties:
                  apt_id:
                    type: integer
                    example: 3
                    description: The ID of the appointment.
                  doctor_id:
                    type: integer
                    example: 2
                    description: The ID of the doctor.
                  start_time:
                    type: string
                    format: date-time
                    example: '2025-01-01T13:00:00'
                    description: The start time of the appointment.
                  end_time:
                    type: string
                    format: date-time
                    example: '2025-01-01T14:00:00'
                    description: The end time of the appointment.
                  created_at:
                    type: string
                    format: date-time
                    example: '2025-01-01T12:00:00'
                    description: The time the appointment was created.
          404:
            description:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Doctor not found
        """
        doctor = session.query(Doctor).filter_by(doctor_id=doctor_id).all()
        if not doctor:
          return jsonify({"error": "Doctor not found"}), 404
        appointments = session.query(Appointment).filter_by(doctor_id=doctor_id).all()
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
        """
        Create a new appointment.
        ---
        parameters:
          - in: body
            name: body
            required: true
            description: The details of the appointment to be created.
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  description: The ID of the user creating the appointment.
                  example: 1
                doctor_id:
                  type: integer
                  example: 2
                  description: The ID of the doctor for the appointment.
                start_time:
                  type: string
                  format: date-time
                  example: '2025-01-01T13:00:00'
                  description: The start time of the appointment (ISO 8601 format).
                end_time:
                  type: string
                  format: date-time
                  example: '2025-01-01T14:00:00'
                  description: The end time of the appointment (ISO 8601 format).
        responses:
          201:
            description: Appointment successfully created.
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Appointment Created
                  description: Confirmation message.
                apt_id:
                  type: integer
                  example: 3
                  description: The ID of the newly created appointment.
          400:
            description: Missing required fields in the request.
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Missing required fields
                  description: Error message indicating missing fields.
        """
        data = request.get_json()
        user_id = data.get('user_id')
        doctor_id = data.get('doctor_id')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if not (user_id and doctor_id and start_time and end_time):
            return {"msg": "Missing required fields."}, 400
          
        user = session.query(User).filter_by(user_id=user_id).all()
        if not user:
            return {"msg": "User not found."}, 404
          
        doctor = session.query(Doctor).filter_by(doctor_id=doctor_id).all()
        if not doctor:
            return {"msg": "Doctor not found."}, 404

        new_appointment = Appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            start_time=datetime.datetime.fromisoformat(start_time),
            end_time=datetime.datetime.fromisoformat(end_time),
        )

        session.add(new_appointment)
        session.commit()
        return {"msg": "Appointment Created", "apt_id": new_appointment.apt_id}, 201

class UpdateAppointment(Resource):
    def put(self, apt_id):
        """
        Update an existing appointment.
        ---
        parameters:
          - in: path
            name: apt_id
            type: integer
            required: true
            description: The ID of the appointment to update.
          - in: body
            name: body
            required: true
            description: The updated details of the appointment.
            schema:
              type: object
              properties:
                start_time:
                  type: string
                  format: date-time
                  example: 2022-01-01T16:00:00
                  description: The new start time of the appointment
                end_time:
                  type: string
                  format: date-time
                  example: 2022-01-01T17:00:00
                  description: The new end time of the appointment
        responses:
          200:
            description: Appointment successfully updated.
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Appointment Updated
                  description: Confirmation message.
                apt_id:
                  type: integer
                  description: The ID of the updated appointment.
          404:
            description: Appointment not found.
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Appointment not found
                  description: Error message indicating the appointment was not found.
        """
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
        """
        Delete an existing appointment.
        ---
        parameters:
          - in: path
            name: apt_id
            type: integer
            example: 3
            required: true
            description: The ID of the appointment to delete.
        responses:
          200:
            description: Appointment successfully deleted.
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Appointment Deleted
                  description: Confirmation message.
                apt_id:
                  type: integer
                  example: 3
                  description: The ID of the deleted appointment.
          404:
            description: Appointment not found.
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Appointment not found
                  description: Error message indicating the appointment was not found.
        """
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
