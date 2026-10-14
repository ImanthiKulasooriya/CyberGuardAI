import {
    useEffect,
    useState
} from "react";


import {
    FileText,
    ShieldAlert,
    CheckCircle,
    AlertTriangle,
    Activity,
    Download
} from "lucide-react";


import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer
} from "recharts";


import api from "../services/api";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";


function Reports() {

    const [report, setReport] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);


    // ======================================================
    // LOAD REPORT
    // ======================================================

    useEffect(() => {

        fetchReport();

    }, []);

    const downloadReport = async () => {

    try {

        const response = await api.get(
            "/reports/download",
            {
                responseType: "blob"
            }
        );

        const url = window.URL.createObjectURL(
            new Blob(
                [response.data],
                {
                    type: "text/csv"
                }
            )
        );

        const link =
            document.createElement("a");

        link.href = url;

        link.setAttribute(
            "download",
            "cyberguard_security_report.csv"
        );

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {

        console.error(
            "Report download error:",
            error
        );

        alert(
            "Unable to download the security report."
        );

    }
};


    const fetchReport = async () => {

        setLoading(true);

        setError(null);

        try {

            const response = await api.get(
                "/reports/summary"
            );

            console.log(
                "Reports API:",
                response.data
            );

            setReport(response.data);

        } catch (err) {

            console.error(
                "Reports error:",
                err
            );

            setError(
                "Unable to load security report."
            );

        } finally {

            setLoading(false);

        }

    };


    // ======================================================
    // LOADING
    // ======================================================

    if (loading && !report) {

        return (

            <div className="loading-screen">

                <div className="loading-spinner"></div>

                <h2>
                    Generating Security Report...
                </h2>

                <p>
                    Analyzing stored security events
                </p>

            </div>

        );

    }


    // ======================================================
    // ERROR
    // ======================================================

    if (error && !report) {

        return (

            <div className="error-screen">

                <h2>
                    ⚠️ Report unavailable
                </h2>

                <p>
                    {error}
                </p>

                <button
                    onClick={fetchReport}
                    className="retry-button"
                >
                    Try Again
                </button>

            </div>

        );

    }


    // ======================================================
    // REPORT DATA
    // ======================================================

    const eventSummary =
        report?.event_summary ?? {};


    const riskDistribution =
        report?.risk_distribution ?? {};


    const alertSummary =
        report?.alert_summary ?? {};


    const detectionSummary =
        report?.detection_summary ?? {};


    // ======================================================
    // TRAFFIC CHART DATA
    // ======================================================

    const trafficData = [

        {
            name: "Attacks",
            value:
                eventSummary.total_attacks ?? 0
        },

        {
            name: "Normal",
            value:
                eventSummary.total_normal ?? 0
        }

    ];


    // ======================================================
    // RISK CHART DATA
    // ======================================================

    const riskData = [

        {
            name: "High",
            value:
                riskDistribution.high ?? 0
        },

        {
            name: "Medium",
            value:
                riskDistribution.medium ?? 0
        },

        {
            name: "Low",
            value:
                riskDistribution.low ?? 0
        }

    ];


    // ======================================================
    // GENERATE / DOWNLOAD REPORT
    // ======================================================

    const generateReport = () => {

        const reportDate =
            new Date().toLocaleString();


        const totalEvents =
            eventSummary.total_events ?? 0;


        const totalAttacks =
            eventSummary.total_attacks ?? 0;


        const totalNormal =
            eventSummary.total_normal ?? 0;


        const openAlerts =
            alertSummary.open_alerts ?? 0;


        const totalAlerts =
            alertSummary.total_alerts ?? 0;


        const attackPercentage =
            eventSummary.attack_percentage ?? 0;


        const normalPercentage =
            eventSummary.normal_percentage ?? 0;


        const highRisk =
            riskDistribution.high ?? 0;


        const mediumRisk =
            riskDistribution.medium ?? 0;


        const lowRisk =
            riskDistribution.low ?? 0;


        const model =
            detectionSummary.model
            ?? "Random Forest";


        const dataset =
            detectionSummary.dataset
            ?? "UNSW-NB15";


        const averageConfidence =
            detectionSummary.average_confidence
            ?? 0;


        const averageAttackProbability =
            detectionSummary.average_attack_probability
            ?? 0;


        const reportContent = `

============================================================
                     CYBERGUARD AI
                  SECURITY REPORT
============================================================

Generated: ${reportDate}


------------------------------------------------------------
SECURITY OVERVIEW
------------------------------------------------------------

Total Events        : ${totalEvents}
Detected Attacks    : ${totalAttacks}
Normal Traffic      : ${totalNormal}
Open Alerts         : ${openAlerts}
Total Alerts        : ${totalAlerts}


------------------------------------------------------------
TRAFFIC CLASSIFICATION
------------------------------------------------------------

Attack Rate         : ${attackPercentage}%
Normal Rate         : ${normalPercentage}%

Attacks             : ${totalAttacks}
Normal              : ${totalNormal}


------------------------------------------------------------
RISK DISTRIBUTION
------------------------------------------------------------

High Risk           : ${highRisk}
Medium Risk         : ${mediumRisk}
Low Risk            : ${lowRisk}


------------------------------------------------------------
DETECTION SUMMARY
------------------------------------------------------------

Machine Learning Model : ${model}
Dataset                 : ${dataset}
Average Confidence     : ${averageConfidence}%
Average Attack         : ${averageAttackProbability}%


------------------------------------------------------------
SECURITY STATUS
------------------------------------------------------------

System Status       : Monitoring Active


------------------------------------------------------------
REPORT SUMMARY
------------------------------------------------------------

CyberGuard AI analyzed ${totalEvents} security events.

${totalAttacks} potential attacks were detected,
representing ${attackPercentage}% of all recorded events.

${totalNormal} normal network events were identified,
representing ${normalPercentage}% of all recorded events.

There are currently ${openAlerts} open security alerts
requiring investigation.


============================================================
                 END OF SECURITY REPORT
============================================================
`;


        // --------------------------------------------------
        // Create downloadable file
        // --------------------------------------------------

        const blob = new Blob(
            [reportContent],
            {
                type: "text/plain;charset=utf-8"
            }
        );


        const url =
            window.URL.createObjectURL(blob);


        const link =
            document.createElement("a");


        link.href = url;


        const date =
            new Date()
                .toISOString()
                .slice(0, 10);


        link.download =
            `CyberGuard_Security_Report_${date}.txt`;


        document.body.appendChild(link);


        link.click();


        document.body.removeChild(link);


        window.URL.revokeObjectURL(url);

    };


    // ======================================================
    // PAGE
    // ======================================================

    return (

        <div className="app-layout">

            <Sidebar />


            <main className="main-content">

                <Header
                    onRefresh={fetchReport}
                    loading={loading}
                />


                <section className="dashboard-content">


                    {/* ==================================================
                        REPORT HEADER
                    ================================================== */}

                    <div className="page-header">

                        <div>

                            <div className="report-title-row">

                                <div className="report-title-icon">

                                    <FileText
                                        size={25}
                                    />

                                </div>

                                <div>

                                    <h1>
                                        Security Reports
                                    </h1>

                                    <p>
                                        CyberGuard AI security analysis
                                        and detection summary
                                    </p>

                                </div>

                            </div>

                        </div>
                        <div className="report-actions">

                            <button
                                className="download-report-button"
                                onClick={downloadReport}
                            >

                                <Download size={18} />

                                <span>
                                    Download Report
                                </span>

                            </button>

                        </div>

                    </div>


                    {/* ==================================================
                        EVENT SUMMARY
                    ================================================== */}

                    <div className="report-stats-grid">


                        {/* TOTAL EVENTS */}

                        <div className="report-stat-card">

                            <div className="report-stat-icon blue">

                                <Activity
                                    size={22}
                                />

                            </div>

                            <div className="report-stat-content">

                                <span>
                                    Total Events
                                </span>

                                <strong>
                                    {
                                        eventSummary.total_events
                                        ?? 0
                                    }
                                </strong>

                            </div>

                        </div>


                        {/* ATTACKS */}

                        <div className="report-stat-card">

                            <div className="report-stat-icon red">

                                <ShieldAlert
                                    size={22}
                                />

                            </div>

                            <div className="report-stat-content">

                                <span>
                                    Attacks
                                </span>

                                <strong>
                                    {
                                        eventSummary.total_attacks
                                        ?? 0
                                    }
                                </strong>

                            </div>

                        </div>


                        {/* NORMAL TRAFFIC */}

                        <div className="report-stat-card">

                            <div className="report-stat-icon green">

                                <CheckCircle
                                    size={22}
                                />

                            </div>

                            <div className="report-stat-content">

                                <span>
                                    Normal Traffic
                                </span>

                                <strong>
                                    {
                                        eventSummary.total_normal
                                        ?? 0
                                    }
                                </strong>

                            </div>

                        </div>


                        {/* OPEN ALERTS */}

                        <div className="report-stat-card">

                            <div className="report-stat-icon orange">

                                <AlertTriangle
                                    size={22}
                                />

                            </div>

                            <div className="report-stat-content">

                                <span>
                                    Open Alerts
                                </span>

                                <strong>
                                    {
                                        alertSummary.open_alerts
                                        ?? 0
                                    }
                                </strong>

                            </div>

                        </div>


                    </div>


                    {/* ==================================================
                        RATES
                    ================================================== */}

                    <div className="report-rate-grid">


                        {/* ATTACK RATE */}

                        <div className="report-rate-card attack-rate">

                            <div className="rate-content">

                                <span>
                                    Attack Rate
                                </span>

                                <strong>
                                    {
                                        eventSummary.attack_percentage
                                        ?? 0
                                    }%
                                </strong>

                            </div>

                            <div className="rate-description">

                                Percentage of detected attacks

                            </div>

                        </div>


                        {/* NORMAL RATE */}

                        <div className="report-rate-card normal-rate">

                            <div className="rate-content">

                                <span>
                                    Normal Rate
                                </span>

                                <strong>
                                    {
                                        eventSummary.normal_percentage
                                        ?? 0
                                    }%
                                </strong>

                            </div>

                            <div className="rate-description">

                                Percentage of normal traffic

                            </div>

                        </div>


                        {/* TOTAL ALERTS */}

                        <div className="report-rate-card alerts-rate">

                            <div className="rate-content">

                                <span>
                                    Total Alerts
                                </span>

                                <strong>
                                    {
                                        alertSummary.total_alerts
                                        ?? 0
                                    }
                                </strong>

                            </div>

                            <div className="rate-description">

                                Security alerts generated

                            </div>

                        </div>


                    </div>


                    {/* ==================================================
                        CHARTS
                    ================================================== */}

                    <div className="report-charts-grid">


                        {/* ==================================================
                            TRAFFIC CLASSIFICATION
                        ================================================== */}

                        <div className="report-chart-card">

                            <div className="report-chart-header">

                                <div>

                                    <h3>
                                        Traffic Classification
                                    </h3>

                                    <p>
                                        Attack versus normal traffic
                                    </p>

                                </div>

                            </div>


                            <div className="report-chart-container">

                                <ResponsiveContainer
                                    width="100%"
                                    height={300}
                                >

                                    <PieChart>

                                        <Pie
                                            data={trafficData}
                                            dataKey="value"
                                            nameKey="name"
                                            cx="50%"
                                            cy="48%"
                                            outerRadius={100}
                                            label
                                        >

                                            <Cell
                                                fill="#dc2626"
                                            />

                                            <Cell
                                                fill="#16a34a"
                                            />

                                        </Pie>


                                        <Tooltip
                                            formatter={(value) => [
                                                value,
                                                "Events"
                                            ]}
                                        />


                                        <Legend
                                            verticalAlign="bottom"
                                            height={36}
                                        />

                                    </PieChart>

                                </ResponsiveContainer>

                            </div>

                        </div>


                        {/* ==================================================
                            RISK DISTRIBUTION
                        ================================================== */}

                        <div className="report-chart-card">

                            <div className="report-chart-header">

                                <div>

                                    <h3>
                                        Risk Distribution
                                    </h3>

                                    <p>
                                        Security risk levels
                                    </p>

                                </div>

                            </div>


                            <div className="report-chart-container">

                                <ResponsiveContainer
                                    width="100%"
                                    height={300}
                                >

                                    <PieChart>

                                        <Pie
                                            data={riskData}
                                            dataKey="value"
                                            nameKey="name"
                                            cx="50%"
                                            cy="48%"
                                            outerRadius={100}
                                            label
                                        >

                                            <Cell
                                                fill="#dc2626"
                                            />

                                            <Cell
                                                fill="#ea580c"
                                            />

                                            <Cell
                                                fill="#16a34a"
                                            />

                                        </Pie>


                                        <Tooltip
                                            formatter={(value) => [
                                                value,
                                                "Events"
                                            ]}
                                        />


                                        <Legend
                                            verticalAlign="bottom"
                                            height={36}
                                        />

                                    </PieChart>

                                </ResponsiveContainer>

                            </div>

                        </div>


                    </div>


                    {/* ==================================================
                        DETECTION SUMMARY
                    ================================================== */}

                    <div className="detection-summary-card">


                        <div className="detection-summary-header">

                            <div className="detection-summary-icon">

                                <ShieldAlert
                                    size={24}
                                />

                            </div>

                            <div>

                                <h3>
                                    Detection Summary
                                </h3>

                                <p>
                                    Machine learning model information
                                </p>

                            </div>

                        </div>


                        <div className="detection-summary-grid">


                            <div className="detection-info">

                                <span>
                                    Model
                                </span>

                                <strong>
                                    {
                                        detectionSummary.model
                                        ?? "Random Forest"
                                    }
                                </strong>

                            </div>


                            <div className="detection-info">

                                <span>
                                    Dataset
                                </span>

                                <strong>
                                    {
                                        detectionSummary.dataset
                                        ?? "UNSW-NB15"
                                    }
                                </strong>

                            </div>


                            <div className="detection-info">

                                <span>
                                    Average Confidence
                                </span>

                                <strong>
                                    {
                                        detectionSummary.average_confidence
                                        ?? 0
                                    }%
                                </strong>

                            </div>


                            <div className="detection-info">

                                <span>
                                    Average Attack Probability
                                </span>

                                <strong>
                                    {
                                        detectionSummary.average_attack_probability
                                        ?? 0
                                    }%
                                </strong>

                            </div>


                        </div>

                    </div>


                </section>

            </main>

        </div>

    );

}


export default Reports;