import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "@/pages/Home";
import FourOFour from "@/pages/404";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route index element={<Home />} />
                <Route path="*" element={<FourOFour />} />
            </Routes>
        </BrowserRouter>
      );
}

export default App;
