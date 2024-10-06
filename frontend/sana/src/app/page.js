"use client";
import { useState } from "react";
import Sidebar from "./components/Sidebar";

export default function Home() {
  const [isExpanded, setIsExpanded] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    
    fetch('https://localhost:5000/upload-scan', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        console.log('File uploaded successfully:', data);
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      });
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };
  const [selectedPatient, setSelectedPatient] = useState(null);
  const patients = [{name:"Levon",condition:"Moderate"}, {name:"Marwan",condition:"Critical"}, {name:"Lenart",condition:"Healthy"}, {name:"Raghav",condition:"Critical"}];
  
  return (
    <div className="drawer lg:drawer-open bg-white">
      <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content flex flex-col items-center justify-center">
        <label
          htmlFor="my-drawer-2"
          className="btn btn-primary drawer-button lg:hidden"
        >
          Open drawer
        </label>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 p-4">
        <div className="stack" onClick={toggleExpand}>
          <div className="card bg-base-100 w-full shadow-xl text-black hover:bg-gray-100 hover:shadow-2xl transition duration-300 ease-in-out cursor-pointer">
            <figure>
              <img
                src="http://www.mychox.net/cf/mod_CXR.jpg"
                alt="Lung X-Ray"
              />
            </figure>
            <div className="card-body">
              <h2 className="card-title">Patient Scans</h2>
              <p>Lung condition improved from last scan</p>
              
            </div>
          </div>
        </div>
        <div className="stack" onClick={toggleExpand}>
          <div className="card bg-base-100 w-full shadow-xl text-black hover:bg-gray-100 hover:shadow-2xl transition duration-300 ease-in-out cursor-pointer">
            <div className="card-body">
              <h2 className="card-title">Patient Analytics</h2>
              <p>Overall normal ranges with a slight deficiency in Vitamin D</p>
              <h3 className="text-lg font-semibold mt-4">Last Blood Test Results</h3>
              <ul className="list-disc list-inside">
              <li>
                <span className="font-bold text-lg">Hemoglobin:</span> 13.5 g/dL
              </li>
              <li>
                <span className="font-bold text-lg">White Blood Cells:</span> 6,000 per microliter
              </li>
              <li>
                <span className="font-bold text-lg">Platelets:</span> 250,000 per microliter
              </li>
              <li>
                <span className="font-bold text-lg">Vitamin D:</span> 20 ng/mL (Deficient)
              </li>
              <li>
                <span className="font-bold text-lg">Cholesterol:</span> 180 mg/dL
              </li>
              </ul>

            </div>
          </div>
        </div>
        <div className="stack" onClick={toggleExpand}>
          <div className="card bg-base-100 w-full shadow-xl text-black hover:bg-gray-100 hover:shadow-2xl transition duration-300 ease-in-out cursor-pointer">
            <div className="card-body">
              <h2 className="card-title">Patient Context/Doctor's Notes</h2>
              <p>Last Note: Patient had the symptoms of a very bad cold - runny nose, fever, headaches.</p>
            </div>
          </div>
        </div>
              
        </div>
        <div className="mt-4">
          <input
            type="text"
            placeholder="Input any notes"
            className="input input-bordered w-full h-10 p-4"
          />
        </div>
        <div className="mt-4">
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleFileUpload}>Upload File</button>
        </div>

      </div>
      <Sidebar
        patients={patients}
        selectedPatient={selectedPatient}
        onPatientSelect={setSelectedPatient}
      />
    </div>
  );
}
