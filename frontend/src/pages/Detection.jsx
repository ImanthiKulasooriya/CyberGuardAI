import { useState } from "react";
import {
    Upload,
    ShieldAlert,
    CheckCircle,
    AlertTriangle,
    FileText
} from "lucide-react";

import api from "../services/api";
import Sidebar from "../components/Sidebar";


function Detection() {

    const [file, setFile] = useState(null);

    const [loading, setLoading] = useState(false);

    const [result, setResult] = useState(null);

    const [error, setError] = useState("");


    const handleFileChange = (event) => {

        const selectedFile = event.target.files[0];

        setResult(null);
        setError("");

        if (!selectedFile) {
            setFile(null);
            return;
        }

        if (!selectedFile.name.toLowerCase().endsWith(".csv")) {

            setError("Please select a CSV file.");

            setFile(null);

            return;
        }

        setFile(selectedFile);
    };


    const handleUpload = async () => {

        if (!file) {

            setError("Please select a CSV file first.");

            return;
        }


        const formData = new FormData();

        formData.append("file", file);


        setLoading(true);

        setError("");

        setResult(null);


        try {

            const response = await api.post(
                "/predictions/csv",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );


            console.log(
                "Prediction response:",
                response.data
            );


            setResult(response.data);

        } catch (err) {

            console.error(
                "Prediction error:",
                err
            );


            setError(
                err.response?.data?.detail ||
                "Prediction failed. Please check the backend."
            );

        } finally {

            setLoading(false);

        }
    };


    return (

        <div className="app-layout">

            <Sidebar />


            <main className="main-content">

                <div className="dashboard-content">

                    <div className="page-title">

                        <h1>
                            Threat Detection
                        </h1>

                        <p>
                            Upload network traffic data and
                            detect potential cybersecurity threats.
                        </p>

                    </div>


                    {/* Upload section */}

                    <div className="upload-card">

                        <div className="upload-icon">

                            <Upload size={30} />

                        </div>


                        <h2>
                            Upload Network Traffic CSV
                        </h2>


                        <p>
                            Upload a CSV file containing network
                            traffic features for ML-based detection.
                        </p>


                        <label className="file-input">

                            <FileText size={20} />

                            <span>
                                {file
                                    ? file.name
                                    : "Choose CSV file"}
                            </span>

                            <input
                                type="file"
                                accept=".csv"
                                onChange={handleFileChange}
                            />

                        </label>


                        {file && (

                            <button
                                className="detect-button"
                                onClick={handleUpload}
                                disabled={loading}
                            >

                                {loading
                                    ? "Analyzing..."
                                    : "Analyze Traffic"}

                            </button>

                        )}


                        {error && (

                            <div className="error-message">

                                ⚠️ {error}

                            </div>

                        )}

                    </div>


                    {/* Results */}

                    {result && (

                        <div className="results-section">

                            <div className="results-header">

                                <div>

                                    <h2>
                                        Detection Results
                                    </h2>

                                    <p>
                                        {result.filename}
                                    </p>

                                </div>

                            </div>


                            {/* Summary cards */}

                            <div className="detection-stats">

                                <div className="detection-stat">

                                    <ActivityIcon />

                                    <span>
                                        Total Records
                                    </span>

                                    <strong>
                                        {result.total_records}
                                    </strong>

                                </div>


                                <div className="detection-stat attack">

                                    <ShieldAlert size={24} />

                                    <span>
                                        Attacks
                                    </span>

                                    <strong>
                                        {result.attack_count}
                                    </strong>

                                </div>


                                <div className="detection-stat normal">

                                    <CheckCircle size={24} />

                                    <span>
                                        Normal
                                    </span>

                                    <strong>
                                        {result.normal_count}
                                    </strong>

                                </div>


                                <div className="detection-stat high">

                                    <AlertTriangle size={24} />

                                    <span>
                                        High Risk
                                    </span>

                                    <strong>
                                        {result.high_risk_count}
                                    </strong>

                                </div>

                            </div>


                            {/* Results table */}

                            <div className="results-table-card">

                                <h3>
                                    Prediction Results
                                </h3>


                                <div className="table-wrapper">

                                    <table>

                                        <thead>

                                            <tr>

                                                <th>
                                                    #
                                                </th>

                                                <th>
                                                    Prediction
                                                </th>

                                                <th>
                                                    Risk Level
                                                </th>

                                                <th>
                                                    Confidence
                                                </th>

                                            </tr>

                                        </thead>


                                        <tbody>

                                            {result.results
                                                ?.slice(0, 100)
                                                .map((item, index) => (

                                                    <tr key={index}>

                                                        <td>
                                                            {index + 1}
                                                        </td>


                                                        <td>

                                                            <span
                                                                className={
                                                                    item.prediction === "Attack"
                                                                        ? "badge attack-badge"
                                                                        : "badge normal-badge"
                                                                }
                                                            >

                                                                {item.prediction}

                                                            </span>

                                                        </td>


                                                        <td>

                                                            <span
                                                                className={
                                                                    `badge ${item.risk_level?.toLowerCase()}-badge`
                                                                }
                                                            >

                                                                {item.risk_level}

                                                            </span>

                                                        </td>


                                                        <td>

                                                            {item.confidence !== undefined
                                                                ? `${(
                                                                    item.confidence * 100
                                                                ).toFixed(2)}%`
                                                                : "N/A"}

                                                        </td>

                                                    </tr>

                                                ))}

                                        </tbody>

                                    </table>

                                </div>


                                {result.results?.length > 100 && (

                                    <p className="table-note">

                                        Showing the first 100 results
                                        out of {result.results.length} records.

                                    </p>

                                )}

                            </div>

                        </div>

                    )}

                </div>

            </main>

        </div>

    );
}


function ActivityIcon() {

    return (
        <FileText size={24} />
    );

}


export default Detection;