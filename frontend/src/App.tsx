import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar";
import { Oferta } from "./components/Oferta";
import { Rezerwacje } from "./components/Rezerwacje";
import { Zaloguj, type User } from "./components/Zaloguj";
import { Rejestracja } from "./components/Rejestracja";
import { Flex } from "antd";
import { PanelAdmina } from "./components/PanelAdmina";
function App() {
  const [selectedView, setSeletctedView] = useState<
    "oferta" | "rezerwacje" | "zaloguj" | "zarejestruj" | "panel_admina"
  >("oferta");
  const [isLogged, setIsLogged] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);

  const getAuthCookie = () => {
    const match = document.cookie
      .split("; ")
      .find((cookie) => cookie.startsWith("auth="));
    if (!match) return null;
    try {
      return JSON.parse(decodeURIComponent(match.split("=")[1]));
    } catch {
      return null;
    }
  };
  useEffect(() => {
    const authData = getAuthCookie();
    setUser(authData);
  }, []);
  useEffect(() => {
    if (user !== null) {
      setIsLogged(true);
    }
  }, [user]);
  console.log(user);
  return (
    <>
      <Flex style={{ width: "100%", height: "100vh" }}>
        <Flex style={{ width: "100%", height: "100%" }} vertical gap={20}>
          <Navbar
            setSeletctedView={setSeletctedView}
            isLogged={isLogged}
            user={user}
          />
          <Flex>
            {selectedView === "oferta" && (
              <Oferta
                user={user}
                isLogged={isLogged}
                setSelectedView={setSeletctedView}
              />
            )}
            {selectedView === "rezerwacje" && <Rezerwacje user={user} />}
            {selectedView === "zaloguj" && <Zaloguj />}
            {selectedView === "zarejestruj" && (
              <Rejestracja setSelectedView={setSeletctedView} />
            )}
            {selectedView === "panel_admina" && user?.type == "admin" && (
              <PanelAdmina />
            )}
          </Flex>
        </Flex>
      </Flex>
    </>
  );
}

export default App;
