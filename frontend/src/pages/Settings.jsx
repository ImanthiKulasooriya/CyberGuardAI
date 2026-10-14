import {
    useEffect,
    useState
} from "react";

import {
    Settings as SettingsIcon,
    ShieldAlert,
    Database,
    Server,
    Bell,
    RefreshCw,
    Info
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";


function Settings() {

    // ======================================================
    // SETTINGS STATE
    // ======================================================

    const [autoRefresh, setAutoRefresh] = useState(
        () => {
            const saved =
                localStorage.getItem(
                    "cyberguard_auto_refresh"
                );

            return saved !== "false";
        }
    );


    const [notifications, setNotifications] = useState(
        () => {
            const saved =
                localStorage.getItem(
                    "cyberguard_notifications"
                );

            return saved !== "false";
        }
    );


    // ======================================================
    // SAVE AUTO REFRESH SETTING
    // ======================================================

    useEffect(() => {

        localStorage.setItem(
            "cyberguard_auto_refresh",
            autoRefresh
        );

    }, [autoRefresh]);


    // ======================================================
    // SAVE NOTIFICATION SETTING
    // ======================================================

    useEffect(() => {

        localStorage.setItem(
            "cyberguard_notifications",
            notifications
        );

    }, [notifications]);


    return (

        <div className="app-layout">

            <Sidebar />


            <main className="main-content">

                <Header />


                <section className="dashboard-content">


                    {/* ==================================================
                        PAGE HEADER
                    ================================================== */}

                    <div className="settings-page-header">

                        <div className="settings-title-row">

                            <div className="settings-title-icon">

                                <SettingsIcon
                                    size={25}
                                />

                            </div>

                            <div>

                                <h1>
                                    Settings
                                </h1>

                                <p>
                                    Manage CyberGuard AI
                                    system and interface settings
                                </p>

                            </div>

                        </div>

                    </div>


                    {/* ==================================================
                        DETECTION SETTINGS
                    ================================================== */}

                    <div className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon blue">

                                <ShieldAlert
                                    size={21}
                                />

                            </div>

                            <div>

                                <h3>
                                    Detection Settings
                                </h3>

                                <p>
                                    Machine learning detection
                                    configuration
                                </p>

                            </div>

                        </div>


                        <div className="settings-info-grid">

                            <div className="settings-info-card">

                                <span>
                                    Machine Learning Model
                                </span>

                                <strong>
                                    Random Forest
                                </strong>

                            </div>


                            <div className="settings-info-card">

                                <span>
                                    Dataset
                                </span>

                                <strong>
                                    UNSW-NB15
                                </strong>

                            </div>


                            <div className="settings-info-card">

                                <span>
                                    Detection Type
                                </span>

                                <strong>
                                    Binary Network Attack Detection
                                </strong>

                            </div>

                        </div>

                    </div>


                    {/* ==================================================
                        RISK THRESHOLDS
                    ================================================== */}

                    <div className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon red">

                                <ShieldAlert
                                    size={21}
                                />

                            </div>

                            <div>

                                <h3>
                                    Risk Thresholds
                                </h3>

                                <p>
                                    Current attack probability
                                    classification
                                </p>

                            </div>

                        </div>


                        <div className="threshold-list">


                            <div className="threshold-item">

                                <div className="threshold-left">

                                    <span className="threshold-dot high"></span>

                                    <div>

                                        <strong>
                                            High Risk
                                        </strong>

                                        <small>
                                            Attack probability is
                                            80% or higher
                                        </small>

                                    </div>

                                </div>


                                <span className="threshold-value high">
                                    ≥ 80%
                                </span>

                            </div>


                            <div className="threshold-item">

                                <div className="threshold-left">

                                    <span className="threshold-dot medium"></span>

                                    <div>

                                        <strong>
                                            Medium Risk
                                        </strong>

                                        <small>
                                            Attack probability is
                                            between 50% and 79.99%
                                        </small>

                                    </div>

                                </div>


                                <span className="threshold-value medium">
                                    ≥ 50%
                                </span>

                            </div>


                            <div className="threshold-item">

                                <div className="threshold-left">

                                    <span className="threshold-dot low"></span>

                                    <div>

                                        <strong>
                                            Low Risk
                                        </strong>

                                        <small>
                                            Normal traffic or attack
                                            probability below 50%
                                        </small>

                                    </div>

                                </div>


                                <span className="threshold-value low">
                                    &lt; 50%
                                </span>

                            </div>

                        </div>

                    </div>


                    {/* ==================================================
                        INTERFACE SETTINGS
                    ================================================== */}

                    <div className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon green">

                                <RefreshCw
                                    size={21}
                                />

                            </div>

                            <div>

                                <h3>
                                    Interface Settings
                                </h3>

                                <p>
                                    Customize dashboard behaviour
                                </p>

                            </div>

                        </div>


                        <div className="settings-options">


                            {/* AUTO REFRESH */}

                            <div className="settings-option">

                                <div className="settings-option-info">

                                    <div className="option-icon">

                                        <RefreshCw
                                            size={18}
                                        />

                                    </div>

                                    <div>

                                        <strong>
                                            Automatic Refresh
                                        </strong>

                                        <small>
                                            Automatically refresh
                                            dashboard data
                                        </small>

                                    </div>

                                </div>


                                <label className="toggle">

                                    <input
                                        type="checkbox"
                                        checked={autoRefresh}
                                        onChange={(event) =>
                                            setAutoRefresh(
                                                event.target.checked
                                            )
                                        }
                                    />

                                    <span className="toggle-slider"></span>

                                </label>

                            </div>


                            {/* NOTIFICATIONS */}

                            <div className="settings-option">

                                <div className="settings-option-info">

                                    <div className="option-icon">

                                        <Bell
                                            size={18}
                                        />

                                    </div>

                                    <div>

                                        <strong>
                                            Security Notifications
                                        </strong>

                                        <small>
                                            Show notifications for
                                            security alerts
                                        </small>

                                    </div>

                                </div>


                                <label className="toggle">

                                    <input
                                        type="checkbox"
                                        checked={notifications}
                                        onChange={(event) =>
                                            setNotifications(
                                                event.target.checked
                                            )
                                        }
                                    />

                                    <span className="toggle-slider"></span>

                                </label>

                            </div>

                        </div>

                    </div>


                    {/* ==================================================
                        SYSTEM INFORMATION
                    ================================================== */}

                    <div className="settings-section">

                        <div className="settings-section-header">

                            <div className="settings-section-icon purple">

                                <Info
                                    size={21}
                                />

                            </div>

                            <div>

                                <h3>
                                    System Information
                                </h3>

                                <p>
                                    CyberGuard AI system details
                                </p>

                            </div>

                        </div>


                        <div className="system-info-grid">


                            <div className="system-info-item">

                                <Server
                                    size={18}
                                />

                                <div>

                                    <span>
                                        Application
                                    </span>

                                    <strong>
                                        CyberGuard AI
                                    </strong>

                                </div>

                            </div>


                            <div className="system-info-item">

                                <ShieldAlert
                                    size={18}
                                />

                                <div>

                                    <span>
                                        ML Model
                                    </span>

                                    <strong>
                                        Random Forest
                                    </strong>

                                </div>

                            </div>


                            <div className="system-info-item">

                                <Database
                                    size={18}
                                />

                                <div>

                                    <span>
                                        Database
                                    </span>

                                    <strong>
                                        SQLite
                                    </strong>

                                </div>

                            </div>


                            <div className="system-info-item">

                                <Server
                                    size={18}
                                />

                                <div>

                                    <span>
                                        Backend
                                    </span>

                                    <strong>
                                        FastAPI
                                    </strong>

                                </div>

                            </div>

                        </div>

                    </div>


                    {/* ==================================================
                        SYSTEM STATUS
                    ================================================== */}

                    <div className="settings-status-card">

                        <div>

                            <h3>
                                System Status
                            </h3>

                            <p>
                                CyberGuard AI security monitoring
                                system is currently operational.
                            </p>

                        </div>


                        <div className="settings-online-status">

                            <span className="status-dot"></span>

                            <strong>
                                System Online
                            </strong>

                        </div>

                    </div>


                </section>

            </main>

        </div>

    );

}


export default Settings;