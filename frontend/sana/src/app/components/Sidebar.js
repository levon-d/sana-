import Image from "next/image";
import { useState } from "react";

export default function Sidebar({
  patients,
  selectedPatient,
  onPatientSelect,
}) {
  const [search, setSearch] = useState("");

  const filteredPatients = patients.filter((patient) =>
    patient.name.toLowerCase().includes(search.toLowerCase())
  );

  

  return (
    <div className="drawer-side">
      <label
        htmlFor="my-drawer-2"
        aria-label="close sidebar"
        className="drawer-overlay"
      ></label>

      <ul className="menu bg-base-200 text-base-content min-h-full w-80 p-4">
      <div className="mb-4">
        <Image src="/sana.jpeg" alt="Logo" width={100} height={50} style={{'borderRadius':'20px'}} />
      </div>
        <input
          type="text"
          placeholder="Search patients"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="input input-bordered w-full mb-4"
        />
        {filteredPatients.map((patient, index) => (
          <li key={index} className="flex p-2">
          <div className={`bg-white rounded-lg shadow-md p-4 w-full hover:bg-gray-100 cursor-pointer border ${patient.condition === "Healthy" ? "border-green-500" : patient.condition === "Moderate" ? "border-yellow-500" : "border-red-500"}`}>
            <a
              onClick={() => onPatientSelect(patient)}
              className={`block ${patient === selectedPatient ? "bg-gray-300" : ""}`}
            >
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Image
                    src={patient.image || "/image.png"} // Assuming you have a default avatar image
                    alt={patient.name}
                    width={50}
                    height={50}
                    className="rounded-full"
                  />
                </div>
                <div className="ml-4">
                  <div className="font-bold text-lg">{patient.name}</div>
                  <div className={`text-sm ${patient.condition === "Healthy" ? "text-green-500" : patient.condition === "Moderate" ? "text-yellow-500" : "text-red-500"}`}>
                    {patient.condition}
                  </div>
                </div>
              </div>
            </a>
          </div>
        </li>
        ))}
      </ul>
    </div>
  );
}
