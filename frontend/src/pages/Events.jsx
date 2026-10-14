import { useEffect, useState } from "react";

import {
    Activity,
    ShieldAlert,
    CheckCircle,
    RefreshCw,
    ChevronLeft,
    ChevronRight
} from "lucide-react";

import api from "../services/api";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";


function Events() {

    const [events, setEvents] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);


    // =====================================================
    // Pagination
    // =====================================================

    const [page, setPage] = useState(1);

    const [totalEvents, setTotalEvents] = useState(0);

    const [totalPages, setTotalPages] = useState(1);

    const eventsPerPage = 50;


    // =====================================================
    // Fetch events
    // =====================================================

    const fetchEvents = async (pageNumber = page) => {

        setLoading(true);

        setError(null);

        try {

            const response = await api.get(
                `/events/?page=${pageNumber}&limit=${eventsPerPage}`
            );

            console.log(
                "Events API:",
                response.data
            );

            setEvents(
                response.data.events || []
            );

            setTotalEvents(
                response.data.total || 0
            );

            setTotalPages(
                response.data.total_pages || 1
            );

        } catch (err) {

            console.error(
                "Events error:",
                err
            );

            setError(
                "Unable to load security events."
            );

        } finally {

            setLoading(false);

        }
    };


    useEffect(() => {

        fetchEvents(page);

    }, [page]);


    // =====================================================
    // Refresh
    // =====================================================

    const handleRefresh = () => {

        fetchEvents(page);

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
    // Risk badge
    // =====================================================

    const getRiskClass = (risk) => {

        if (risk === "HIGH") {

            return "risk-badge high";

        }

        if (risk === "MEDIUM") {

            return "risk-badge medium";

        }

        return "risk-badge low";
    };


    // =====================================================
    // Prediction badge
    // =====================================================

    const getPredictionClass = (prediction) => {

        if (prediction === "Attack") {

            return "prediction-badge attack";

        }

        return "prediction-badge normal";
    };


    // =====================================================
    // Statistics for CURRENT PAGE
    // =====================================================

    const attackCount = events.filter(
        event =>
            event.prediction === "Attack"
    ).length;

    const normalCount = events.filter(
        event =>
            event.prediction === "Normal"
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
                                Security Events
                            </h1>

                            <p>
                                View all network security events
                                detected by CyberGuard AI.
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
                        SUMMARY
                    ====================================== */}

                    <div className="events-summary">


                        <div className="event-summary-card">

                            <Activity
                                size={22}
                                className="event-icon total"
                            />

                            <div>

                                <span>
                                    Total Events
                                </span>

                                <strong>
                                    {totalEvents}
                                </strong>

                            </div>

                        </div>


                        <div className="event-summary-card">

                            <ShieldAlert
                                size={22}
                                className="event-icon attack"
                            />

                            <div>

                                <span>
                                    Attacks
                                </span>

                                <strong>
                                    {attackCount}
                                </strong>

                            </div>

                        </div>


                        <div className="event-summary-card">

                            <CheckCircle
                                size={22}
                                className="event-icon normal"
                            />

                            <div>

                                <span>
                                    Normal
                                </span>

                                <strong>
                                    {normalCount}
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
                        EVENTS TABLE
                    ====================================== */}

                    <div className="events-card">


                        <div className="events-card-header">

                            <div>

                                <h2>
                                    All Security Events
                                </h2>

                                <p>
                                    Events are ordered from newest
                                    to oldest.
                                </p>

                            </div>

                        </div>


                        {loading ? (

                            <div className="table-loading">

                                Loading security events...

                            </div>

                        ) : events.length === 0 ? (

                            <div className="empty-events">

                                <Activity
                                    size={40}
                                    className="event-icon total"
                                />

                                <h3>
                                    No security events
                                </h3>

                                <p>
                                    Run a detection to generate
                                    security events.
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
                                                    Timestamp
                                                </th>

                                                <th>
                                                    Prediction
                                                </th>

                                                <th>
                                                    Confidence
                                                </th>

                                                <th>
                                                    Attack Probability
                                                </th>

                                                <th>
                                                    Risk Level
                                                </th>

                                                <th>
                                                    Source
                                                </th>

                                            </tr>

                                        </thead>


                                        <tbody>

                                            {events.map(
                                                (event) => (

                                                    <tr
                                                        key={event.id}
                                                    >

                                                        <td>
                                                            #{event.id}
                                                        </td>


                                                        <td>

                                                            {
                                                                event.timestamp
                                                                    ? new Date(
                                                                        event.timestamp
                                                                    ).toLocaleString()
                                                                    : "-"
                                                            }

                                                        </td>


                                                        <td>

                                                            <span
                                                                className={
                                                                    getPredictionClass(
                                                                        event.prediction
                                                                    )
                                                                }
                                                            >

                                                                {event.prediction}

                                                            </span>

                                                        </td>


                                                        <td>
                                                            {event.confidence}%
                                                        </td>


                                                        <td>
                                                            {
                                                                event.attack_probability
                                                            }%
                                                        </td>


                                                        <td>

                                                            <span
                                                                className={
                                                                    getRiskClass(
                                                                        event.risk_level
                                                                    )
                                                                }
                                                            >

                                                                {event.risk_level}

                                                            </span>

                                                        </td>


                                                        <td>
                                                            {
                                                                event.source || "-"
                                                            }
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


export default Events;