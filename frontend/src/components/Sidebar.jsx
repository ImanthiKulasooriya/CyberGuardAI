import {
    LayoutDashboard,
    ShieldAlert,
    Activity,
    Bell,
    FileText,
    Settings
} from "lucide-react";

import { NavLink } from "react-router-dom";


function Sidebar() {

    const menuItems = [
        {
            name: "Dashboard",
            path: "/dashboard",
            icon: LayoutDashboard
        },
        {
            name: "Detection",
            path: "/detection",
            icon: ShieldAlert
        },
        {
            name: "Events",
            path: "/events",
            icon: Activity
        },
        {
            name: "Alerts",
            path: "/alerts",
            icon: Bell
        },
        {
            name: "Reports",
            path: "/reports",
            icon: FileText
        }
    ];


    return (

        <aside className="sidebar">

            <div className="logo">

                <div className="logo-icon">
                    🛡️
                </div>

                <div>
                    <h2>CyberGuard</h2>
                    <span>AI Security</span>
                </div>

            </div>


            <nav className="sidebar-menu">

                {menuItems.map((item) => {

                    const Icon = item.icon;

                    return (

                        <NavLink
                            key={item.name}
                            to={item.path}
                            className={({ isActive }) =>
                                isActive
                                    ? "menu-item active"
                                    : "menu-item"
                            }
                        >

                            <Icon size={20} />

                            <span>
                                {item.name}
                            </span>

                        </NavLink>

                    );

                })}

            </nav>


            <div className="sidebar-bottom">

                <NavLink
                    to="/settings"
                    className="menu-item"
                >

                    <Settings size={20} />

                    <span>
                        Settings
                    </span>
                    

                </NavLink>
                
                <div className="system-status">

                    <span className="status-dot"></span>

                    <div>
                        <strong>System Online</strong>
                        <small>ML engine active</small>
                    </div>

                </div>

            </div>

        </aside>

    );
}


export default Sidebar;