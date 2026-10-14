import {
    useEffect,
    useState
} from "react";


import {
    ShieldAlert,
    Activity,
    CheckCircle,
    AlertTriangle,
    AlertCircle
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
import StatCard from "../components/StatCard";

const TRAFFIC_COLORS = [
    "#ef4444", // Attack - red
    "#22c55e"  // Normal - green
];

const RISK_COLORS = [
    "#ef4444", // High - red
    "#f97316", // Medium - orange
    "#22c55e"  // Low - green
];


function Dashboard() {

    const [stats, setStats] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);


    useEffect(() => {

        fetchStats();

    }, []);


    const fetchStats = async () => {

        setLoading(true);

        setError(null);

        try {

            const response = await api.get(
                "/dashboard/stats"
            );

            console.log(
                "Dashboard API:",
                response.data
            );

            setStats(response.data);

        } catch (err) {

            console.error(
                "Dashboard error:",
                err
            );

            setError(
                "Unable to connect to the CyberGuard AI backend."
            );

        } finally {

            setLoading(false);

        }

    };


    if (loading && !stats) {

        return (

            <div className="loading-screen">

                <div className="loading-spinner"></div>

                <h2>
                    Loading CyberGuard AI...
                </h2>

                <p>
                    Connecting to security engine
                </p>

            </div>

        );

    }


    if (error && !stats) {

        return (

            <div className="error-screen">

                <h2>
                    ⚠️ Dashboard unavailable
                </h2>

                <p>
                    {error}
                </p>

                <button
                    onClick={fetchStats}
                    className="retry-button"
                >
                    Try Again
                </button>

            </div>

        );

    }


    /*
     * These values match the dashboard API
     * we created in the backend.
     */

    const totalEvents =
        stats?.total_events ?? 0;


    const totalAttacks =
        stats?.total_attacks ?? 0;


    const totalNormal =
        stats?.total_normal ?? 0;


    const highRisk =
        stats?.risk_distribution?.high ?? 0;


    const mediumRisk =
        stats?.risk_distribution?.medium ?? 0;


    const lowRisk =
        stats?.risk_distribution?.low ?? 0;


    const openAlerts =
        stats?.alerts?.open ?? 0;


    const trafficData = [

        {
            name: "Attacks",
            value: totalAttacks
        },

        {
            name: "Normal",
            value: totalNormal
        }

    ];


    const riskData = [

        {
            name: "High",
            value: highRisk
        },

        {
            name: "Medium",
            value: mediumRisk
        },

        {
            name: "Low",
            value: lowRisk
        }

    ];


    return (

        <div className="app-layout">

            <Sidebar />


            <main className="main-content">

                <Header
                    onRefresh={fetchStats}
                    loading={loading}
                />


                <section className="dashboard-content">

                    {/* =========================
                        STATISTICS
                    ========================== */}

                    <div className="stats-grid">

                        <StatCard
                            title="Total Events"
                            value={totalEvents}
                            subtitle="Security events recorded"
                            icon={<Activity size={24} />}
                            type="blue"
                        />


                        <StatCard
                            title="Detected Attacks"
                            value={totalAttacks}
                            subtitle="Potential threats detected"
                            icon={<ShieldAlert size={24} />}
                            type="red"
                        />


                        <StatCard
                            title="Normal Traffic"
                            value={totalNormal}
                            subtitle="Safe network activity"
                            icon={<CheckCircle size={24} />}
                            type="green"
                        />


                        <StatCard
                            title="Open Alerts"
                            value={openAlerts}
                            subtitle="Requires investigation"
                            icon={<AlertTriangle size={24} />}
                            type="orange"
                        />

                    </div>


                    {/* =========================
                        RISK CARDS
                    ========================== */}

                    <div className="risk-grid">

                        <div className="risk-card high">

                            <AlertCircle size={22} />

                            <div>

                                <span>
                                    High Risk
                                </span>

                                <strong>
                                    {highRisk}
                                </strong>

                            </div>

                        </div>


                        <div className="risk-card medium">

                            <AlertTriangle size={22} />

                            <div>

                                <span>
                                    Medium Risk
                                </span>

                                <strong>
                                    {mediumRisk}
                                </strong>

                            </div>

                        </div>


                        <div className="risk-card low">

                            <CheckCircle size={22} />

                            <div>

                                <span>
                                    Low Risk
                                </span>

                                <strong>
                                    {lowRisk}
                                </strong>

                            </div>

                        </div>

                    </div>


                    {/* =========================
                        CHARTS
                    ========================== */}

                    <div className="charts-grid">


                        {/* Traffic Chart */}

                        <div className="chart-card">

                            <div className="chart-header">

                                <div>

                                    <h3>
                                        Traffic Classification
                                    </h3>

                                    <p>
                                        Attack vs normal traffic
                                    </p>

                                </div>

                            </div>


                            <div className="chart-container">

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
                                            cy="50%"
                                            outerRadius={100}
                                            label={({ name, value }) =>
                                                value > 0 ? `${name}: ${value}` : ""
                                            }


                                        >
                                            {trafficData.map((entry, index) => (
                                                <Cell
                                                   key={`traffic-cell-${index}`}
                                                   fill={TRAFFIC_COLORS[index]}
                                                /> 
                                            ))}      

                                          

                                        </Pie>


                                        <Tooltip />

                                        <Legend />

                                    </PieChart>

                                </ResponsiveContainer>

                            </div>

                        </div>


                        {/* Risk Chart */}

                        <div className="chart-card">

                            <div className="chart-header">

                                <div>

                                    <h3>
                                        Risk Distribution
                                    </h3>

                                    <p>
                                        Security risk levels
                                    </p>

                                </div>

                            </div>


                            <div className="chart-container">

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
                                            cy="50%"
                                            outerRadius={100}
                                            label={({ name, value }) =>
                                                value > 0 ? `${name}: ${value}` : ""
                                            }
                                        >
                                            {riskData.map((entry, index) => (
                                               <Cell 
                                                  key={`risk-cell-${index}`}
                                                  fill={RISK_COLORS[index]}
                                                />
                                            ))}       
                                            

                                        </Pie>


                                        <Tooltip />

                                        <Legend />

                                    </PieChart>

                                </ResponsiveContainer>

                            </div>

                        </div>

                    </div>


                    {/* =========================
                        SECURITY SUMMARY
                    ========================== */}

                    <div className="summary-card">

                        <div>

                            <h3>
                                Security Status
                            </h3>

                            <p>
                                Current CyberGuard AI
                                monitoring status
                            </p>

                        </div>


                        <div className="security-status">

                            <span className="status-dot"></span>

                            <strong>
                                Monitoring Active
                            </strong>

                        </div>

                    </div>


                </section>

            </main>

        </div>

    );

}


export default Dashboard;