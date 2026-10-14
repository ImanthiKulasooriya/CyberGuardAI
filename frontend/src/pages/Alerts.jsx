import { useEffect, useState } from "react";

import {
    Bell,
    AlertTriangle,
    CheckCircle,
    RefreshCw,
    ChevronLeft,
    ChevronRight
} from "lucide-react";

import api from "../services/api";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";


function Alerts() {

    const [alerts, setAlerts] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    // =====================================================
    // Pagination
    // =====================================================

    const [page, setPage] = useState(1);

    const [totalAlerts, setTotalAlerts] = useState(0);

    const [totalPages, setTotalPages] = useState(1);

    const alertsPerPage = 50;


    // =====================================================
    // Fetch alerts
    // =====================================================

    const fetchAlerts = async (pageNumber = page) => {

        setLoading(true);

        setError(null);

        try {

            const response = await api.get(
                `/alerts/?page=${pageNumber}&limit=${alertsPerPage}`
            );

            console.log(
                "Alerts API:",
                response.data
            );

            setAlerts(
                response.data.alerts || []
            );

            setTotalAlerts(
                response.data.total || 0
            );

            setTotalPages(
                response.data.total_pages || 1
            );

        } catch (err) {

            console.error(
                "Alerts error:",
                err
            );

            setError(
                "Unable to load security alerts."
            );

        } finally {

            setLoading(false);

        }
    };


    useEffect(() => {

        fetchAlerts(page);

    }, [page]);


    // =====================================================
    // Refresh
    // =====================================================

    const handleRefresh = () => {

        fetchAlerts(page);

    };


    // =====================================================
    // Resolve alert
    // =====================================================

    const resolveAlert = async (alertId) => {

        try {

            await api.put(
                `/alerts/${alertId}/resolve`
            );

            await fetchAlerts(page);

        } catch (err) {

            console.error(
                "Resolve alert error:",
                err
            );

            setError(
                "Unable to resolve the alert."
            );

        }
    };


    // =====================================================
    // Pagination controls
    // =====================================================

    const goToPreviousPage = () => {

        if (page > 1) {

            setPage(
                page - 1
            );

        }

    };


    const goToNextPage = () => {

        if (page < totalPages) {

            setPage(
                page + 1
            );

        }

    };


    // =====================================================
    // Severity class
    // =====================================================

    const getSeverityClass = (severity) => {

        if (severity === "HIGH") {

            return "severity-badge high";

        }

        if (severity === "MEDIUM") {

            return "severity-badge medium";

        }

        return "severity-badge low";
    };


    // =====================================================
    // Status class
    // =====================================================

    const getStatusClass = (status) => {

        if (status === "RESOLVED") {

            return "status-badge resolved";

        }

        return "status-badge open";
    };


    // =====================================================
    // Statistics for CURRENT PAGE
    // =====================================================

    const openAlerts = alerts.filter(
        alert =>
            alert.status === "OPEN"
    ).length;

    const resolvedAlerts = alerts.filter(
        alert =>
            alert.status === "RESOLVED"
    ).length;

    const highAlerts = alerts.filter(
        alert =>
            alert.severity === "HIGH"
    ).length;


    return (

        <div className="app-layout">

            <Sidebar />

            <main className="main-content">

                <Header
                    onRefresh={handleRefresh}
                    loading={loading}
                />


                <section className="dashboard-content">


                    {/* =====================================
                        PAGE HEADER
                    ====================================== */}

                    <div className="page-header">

                        <div>

                            <h1>
                                Security Alerts
                            </h1>

                            <p>
                                Monitor and manage detected
                                cybersecurity threats.
                            </p>

                        </div>


                        <button
                            className="refresh-button"
                            onClick={handleRefresh}
                            disabled={loading}
                        >

                            <RefreshCw size={18} />

                            Refresh

                        </button>

                    </div>


                    {/* =====================================
                        SUMMARY CARDS
                    ====================================== */}

                    <div className="events-summary">


                        <div className="event-summary-card">

                            <Bell
                                size={22}
                                className="alert-icon total"
                            />

                            <div>

                                <span>
                                    Total Alerts
                                </span>

                                <strong>
                                    {totalAlerts}
                                </strong>

                            </div>

                        </div>


                        <div className="event-summary-card">

                            <AlertTriangle
                                size={22}
                                className="alert-icon open"
                            />

                            <div>

                                <span>
                                    Open Alerts
                                </span>

                                <strong>
                                    {openAlerts}
                                </strong>

                            </div>

                        </div>


                        <div className="event-summary-card">

                            <CheckCircle
                                size={22}
                                className="alert-icon resolved"
                            />

                            <div>

                                <span>
                                    Resolved
                                </span>

                                <strong>
                                    {resolvedAlerts}
                                </strong>

                            </div>

                        </div>


                        <div className="event-summary-card">

                            <AlertTriangle
                                size={22}
                                className="alert-icon high"
                            />

                            <div>

                                <span>
                                    High Severity
                                </span>

                                <strong>
                                    {highAlerts}
                                </strong>

                            </div>

                        </div>


                    </div>


                    {/* =====================================
                        ERROR
                    ====================================== */}

                    {error && (

                        <div className="error-message">

                            ⚠️ {error}

                        </div>

                    )}


                    {/* =====================================
                        ALERTS TABLE
                    ====================================== */}

                    <div className="events-card">


                        <div className="events-card-header">

                            <div>

                                <h2>
                                    Security Alerts
                                </h2>

                                <p>
                                    Potential threats detected
                                    by CyberGuard AI.
                                </p>

                            </div>

                        </div>


                        {loading ? (

                            <div className="table-loading">

                                Loading alerts...

                            </div>

                        ) : alerts.length === 0 ? (

                            <div className="empty-events">

                                <CheckCircle
                                    size={40}
                                    className="alert-icon resolved"
                                />

                                <h3>
                                    No alerts
                                </h3>

                                <p>
                                    No cybersecurity threats
                                    have been detected.
                                </p>

                            </div>

                        ) : (

                            <>

                                <div className="table-wrapper">

                                    <table className="events-table">

                                        <thead>

                                            <tr>

                                                <th>
                                                    ID
                                                </th>

                                                <th>
                                                    Time
                                                </th>

                                                <th>
                                                    Severity
                                                </th>

                                                <th>
                                                    Alert
                                                </th>

                                                <th>
                                                    Message
                                                </th>

                                                <th>
                                                    Status
                                                </th>

                                                <th>
                                                    Action
                                                </th>

                                            </tr>

                                        </thead>


                                        <tbody>

                                            {alerts.map(
                                                (alert) => (

                                                    <tr
                                                        key={alert.id}
                                                    >

                                                        <td>
                                                            #{alert.id}
                                                        </td>


                                                        <td>

                                                            {
                                                                alert.timestamp
                                                                    ? new Date(
                                                                        alert.timestamp
                                                                    ).toLocaleString()
                                                                    : "-"
                                                            }

                                                        </td>


                                                        <td>

                                                            <span
                                                                className={
                                                                    getSeverityClass(
                                                                        alert.severity
                                                                    )
                                                                }
                                                            >

                                                                {alert.severity}

                                                            </span>

                                                        </td>


                                                        <td>

                                                            <strong>
                                                                {alert.title}
                                                            </strong>

                                                        </td>


                                                        <td>
                                                            {alert.message}
                                                        </td>


                                                        <td>

                                                            <span
                                                                className={
                                                                    getStatusClass(
                                                                        alert.status
                                                                    )
                                                                }
                                                            >

                                                                {alert.status}

                                                            </span>

                                                        </td>


                                                        <td>

                                                            {alert.status !== "RESOLVED" ? (

                                                                <button
                                                                    className="resolve-button"
                                                                    onClick={() =>
                                                                        resolveAlert(
                                                                            alert.id
                                                                        )
                                                                    }
                                                                >

                                                                    <CheckCircle
                                                                        size={16}
                                                                    />

                                                                    Resolve

                                                                </button>

                                                            ) : (

                                                                <span className="resolved-text">

                                                                    ✓ Resolved

                                                                </span>

                                                            )}

                                                        </td>

                                                    </tr>

                                                )
                                            )}

                                        </tbody>

                                    </table>

                                </div>


                                {/* =====================================
                                    PAGINATION
                                ====================================== */}

                                <div className="pagination">

                                    <button
                                        className="pagination-button"
                                        onClick={goToPreviousPage}
                                        disabled={
                                            page === 1 || loading
                                        }
                                    >

                                        <ChevronLeft size={18} />

                                        Previous

                                    </button>


                                    <span className="pagination-info">

                                        Page{" "}
                                        <strong>
                                            {page}
                                        </strong>
                                        {" "}of{" "}
                                        <strong>
                                            {totalPages}
                                        </strong>

                                    </span>


                                    <button
                                        className="pagination-button"
                                        onClick={goToNextPage}
                                        disabled={
                                            page === totalPages || loading
                                        }
                                    >

                                        Next

                                        <ChevronRight size={18} />

                                    </button>

                                </div>

                            </>

                        )}

                    </div>

                </section>

            </main>

        </div>

    );

}


export default Alerts;