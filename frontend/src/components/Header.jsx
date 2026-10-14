import {
    Bell,
    RefreshCw
} from "lucide-react";


function Header({ onRefresh, loading }) {

    return (

        <header className="top-header">

            <div>

                <h1>
                    Security Dashboard
                </h1>

                <p>
                    Monitor and analyze network security threats
                </p>

            </div>


            <div className="header-actions">

                <button
                    className="refresh-button"
                    onClick={onRefresh}
                    disabled={loading}
                >

                    <RefreshCw
                        size={18}
                        className={loading ? "spinning" : ""}
                    />

                    Refresh

                </button>


                <button className="notification-button">

                    <Bell size={20} />

                    <span className="notification-dot"></span>

                </button>


                <div className="user-profile">

                    <div className="avatar">
                        A
                    </div>

                    <div>

                        <strong>
                            Administrator
                        </strong>

                        <small>
                            Security Admin
                        </small>

                    </div>

                </div>

            </div>

        </header>

    );
}


export default Header;