from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
