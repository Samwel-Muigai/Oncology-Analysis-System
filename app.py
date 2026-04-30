# app.py - Main Flask Application
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import jwt

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5001", "http://127.0.0.1:5001"],
)
app.config["SECRET_KEY"] = "your-secret-key-change-in-production-2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_EXPIRATION_DELTA"] = timedelta(days=7)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ==================== DATABASE MODELS ====================


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="doctor")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), default="Routine")
    expected_stay = db.Column(db.Integer, default=5)
    status = db.Column(db.String(50), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "priority": self.priority,
            "stay": self.expected_stay,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(200), default="Consultation")
    status = db.Column(db.String(50), default="Scheduled")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "patientName": self.patient_name,
            "date": self.date,
            "time": self.time,
            "reason": self.reason,
            "status": self.status,
        }


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    shift = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), default="Oncology Staff")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "doctorName": self.doctor_name,
            "date": self.date,
            "shift": self.shift,
            "role": self.role,
        }


# ==================== JWT AUTHENTICATION ====================


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + app.config["JWT_EXPIRATION_DELTA"],
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def verify_token(token):
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["user_id"]
    except Exception:
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "No token provided"}), 401
        token = token.replace("Bearer ", "")
        user_id = verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        return f(user_id, *args, **kwargs)

    return decorated_function


# ==================== API ROUTES ====================


# Health check
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


# User Registration
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if len(password) < 4:
        return jsonify({"error": "Password must be at least 4 characters"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(name=name, email=email, password_hash=password_hash)

    db.session.add(new_user)
    db.session.commit()

    token = generate_token(new_user.id)
    return (
        jsonify(
            {
                "message": "User created successfully",
                "token": token,
                "user": new_user.to_dict(),
            }
        ),
        201,
    )


# User Login
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    # Demo login for testing
    if password == "demo123" and not user:
        # Create a demo user if doesn't exist
        demo_user = User(
            name=email.split("@")[0],
            email=email,
            password_hash=bcrypt.generate_password_hash("demo123").decode("utf-8"),
        )
        db.session.add(demo_user)
        db.session.commit()
        token = generate_token(demo_user.id)
        return jsonify(
            {
                "message": "Demo login successful",
                "token": token,
                "user": demo_user.to_dict(),
            }
        )

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user.id)
    return jsonify(
        {"message": "Login successful", "token": token, "user": user.to_dict()}
    )


# Get current user
@app.route("/api/auth/me", methods=["GET"])
@login_required
def get_current_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.to_dict()})


# ==================== PATIENT CRUD ====================


@app.route("/api/patients", methods=["GET"])
@login_required
def get_patients(user_id):
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return jsonify({"patients": [p.to_dict() for p in patients]})


@app.route("/api/patients", methods=["POST"])
@login_required
def create_patient(user_id):
    data = request.json
    new_patient = Patient(
        name=data.get("name"),
        age=data.get("age"),
        diagnosis=data.get("diagnosis"),
        priority=data.get("priority", "Routine"),
        expected_stay=data.get("stay", 5),
    )
    db.session.add(new_patient)
    db.session.commit()
    return (
        jsonify(
            {
                "patient": new_patient.to_dict(),
                "message": "Patient registered successfully",
            }
        ),
        201,
    )


@app.route("/api/patients/<int:patient_id>", methods=["DELETE"])
@login_required
def delete_patient(user_id, patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"})


# ==================== APPOINTMENT CRUD ====================


@app.route("/api/appointments", methods=["GET"])
@login_required
def get_appointments(user_id):
    appointments = Appointment.query.order_by(Appointment.date).all()
    return jsonify({"appointments": [a.to_dict() for a in appointments]})


@app.route("/api/appointments", methods=["POST"])
@login_required
def create_appointment(user_id):
    data = request.json
    new_appointment = Appointment(
        patient_name=data.get("patientName"),
        date=data.get("date"),
        time=data.get("time", "12:00 PM"),
        reason=data.get("reason", "Consultation"),
        created_by=user_id,
    )
    db.session.add(new_appointment)
    db.session.commit()
    return (
        jsonify(
            {
                "appointment": new_appointment.to_dict(),
                "message": "Appointment scheduled successfully",
            }
        ),
        201,
    )


@app.route("/api/appointments/<int:appointment_id>", methods=["DELETE"])
@login_required
def delete_appointment(user_id, appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully"})


# ==================== SCHEDULE CRUD ====================


@app.route("/api/schedules", methods=["GET"])
@login_required
def get_schedules(user_id):
    schedules = Schedule.query.order_by(Schedule.date).all()
    return jsonify({"schedules": [s.to_dict() for s in schedules]})


@app.route("/api/schedules", methods=["POST"])
@login_required
def create_schedule(user_id):
    data = request.json
    new_schedule = Schedule(
        doctor_name=data.get("doctorName"),
        date=data.get("date"),
        shift=data.get("shift"),
        role=data.get("role", "Oncology Staff"),
        created_by=user_id,
    )
    db.session.add(new_schedule)
    db.session.commit()
    return (
        jsonify(
            {
                "schedule": new_schedule.to_dict(),
                "message": "Schedule added successfully",
            }
        ),
        201,
    )


@app.route("/api/schedules/<int:schedule_id>", methods=["DELETE"])
@login_required
def delete_schedule(user_id, schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({"error": "Schedule not found"}), 404
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({"message": "Schedule deleted successfully"})


# ==================== DASHBOARD STATS ====================


@app.route("/api/dashboard/stats", methods=["GET"])
@login_required
def get_dashboard_stats(user_id):
    total_patients = Patient.query.count()
    active_patients = Patient.query.filter_by(status="Active").count()
    upcoming_appointments = Appointment.query.filter(
        Appointment.date >= datetime.now().strftime("%Y-%m-%d")
    ).count()
    total_schedules = Schedule.query.filter(
        Schedule.date >= datetime.now().strftime("%Y-%m-%d")
    ).count()

    return jsonify(
        {
            "totalPatients": total_patients,
            "activePatients": active_patients,
            "upcomingAppointments": upcoming_appointments,
            "totalSchedules": total_schedules,
            "occupancy": 87,
            "predictedTrend": "+12.4%",
        }
    )


# ==================== INITIALIZE DATABASE ====================


def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
