import os
import json
from flask import Flask, request, jsonify
from db import get_client
from bson.objectid import ObjectId
from mistral_api import describe_scan_and_verify

db_client = get_client()
db = db_client.sana

app = Flask(__name__)

UPLOAD_LOCATION = "files"
os.makedirs(UPLOAD_LOCATION, exist_ok=True)


@app.route("/")
def index():
    return "Hello, world"


@app.route("/upload-scan", methods=["POST"])
def upload_scan():
    if "file" not in request.files:
        return jsonify({"error": "No file received"}), 400

    scan = request.files["file"]

    if not scan:
        return jsonify({"error": "Error processing the file"}), 400

    try:
        file_path = os.path.join(UPLOAD_LOCATION, scan.filename)
        scan.save(file_path)

        diagnosis, diagnosis_verification = describe_scan_and_verify(file_path)

        print(diagnosis_verification[7:-3], "truncated") 
        diagnosis_verification = json.loads(diagnosis_verification[7:-3])
        print(diagnosis_verification, "verification")

        os.remove(file_path)

        patients_collection = db.patients
        patient_diagnosis = None
        patient_severity = None 
        if diagnosis_verification["match_condition"]: 
            try:
                patients_collection.update_one(
                    {"_id": ObjectId("67023fd4abe9faf12a432bc2")}, {"$set": {"severity": diagnosis_verification["severity"]}}
                )

            except Exception as e:
                return jsonify({"error": "Could not edit the severity"}), 400


    except Exception as e:
        print(str(e))
        return jsonify({"error": "Could not get information about the file"}), 500

    return (
        jsonify(
            {"diagnosis": diagnosis, "diagnosis_verification": diagnosis_verification}
        ),
        200,
    )


@app.route("/get-patients/<doctor_id>")
def get_doctor_patients(doctor_id):
    doctors_collection = db.doctors
    try:
        target_doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    except Exception as e:
        return jsonify({"error": "Could not find the provided doctor"}), 403
    patients = target_doctor["patient_ids"]

    return patients


@app.route("/add-doctor-note/<patient_id>", methods=["POST"])
def add_doctor_note(patient_id):
    payload = request.get_json()

    patients_collection = db.patients
    try:
        patients_collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$push": {"doctors_notes": payload["message"]}},
        )
    except Exception as e:
        return jsonify({"error": "Could not add a doctor note"}), 400

    return jsonify({"success": "Doctors note successfully added"}), 200


@app.route("/get-patient-data/<patient_id>")
def get_patient_data(patient_id):
    patients_collection = db.patients

    try:
        target_patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
        if target_patient:
            target_patient["id"] = str(target_patient["_id"])
            del target_patient["_id"]
    except Exception as e:
        return jsonify({"error": "Could not find the patient"}), 400

    return jsonify(target_patient), 200


@app.route("/update-patient-severity/<patient_id>", methods=["POST"])
def update_patient_severity(patient_id):
    payload = request.get_json()

    patients_collection = db.patients

    try:
        patients_collection.update_one(
            {"_id": ObjectId(patient_id)}, {"$set": {"severity": payload["severity"]}}
        )

    except Exception as e:
        return jsonify({"error": "Could not edit the severity"}), 400

    return jsonify({"success": "Patient severity successfully updated"}), 200


# app.run('localhost',5555)
