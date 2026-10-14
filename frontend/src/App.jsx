import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";


import Dashboard from "./pages/Dashboard";
import Detection from "./pages/Detection";
import Events from "./pages/Events";
import Alerts from "./pages/Alerts";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/dashboard"
                            replace
                        />
                    }
                />


                <Route
                    path="/dashboard"
                    element={<Dashboard />}
                />


                <Route
                    path="/detection"
                    element={<Detection />}
                />

                <Route
                    path="/events"
                    element={<Events />}
                />

                <Route
                    path="/alerts"
                    element={<Alerts />}
                />
                <Route
                    path="/reports"
                    element={<Reports />}
                />
                <Route
                    path="/settings"
                    element={<Settings />}
                />



            </Routes>

        </BrowserRouter>

    );

}


export default App;