import { Button, Flex } from "antd";
import type { Dispatch, SetStateAction } from "react";
import type { User } from "./Zaloguj";

interface NavbarProps {
  setSeletctedView: Dispatch<
    SetStateAction<
      "oferta" | "rezerwacje" | "zaloguj" | "zarejestruj" | "panel_admina"
    >
  >;
  isLogged: boolean;
  user: User | null;
}

export const Navbar = ({ setSeletctedView, isLogged, user }: NavbarProps) => {
  return (
    <>
      <Flex
        style={{
          width: "100%",
          height: 80,
          background: "rgba(34, 34, 34, 0.77)",
        }}
      >
        <Flex
          align="center"
          justify="space-between"
          style={{ width: "100%", margin: "0px 10px" }}
        >
          <Flex>
            <span style={{ color: "white", fontSize: 20, fontWeight: "bold" }}>
              ROWEROWNIA
            </span>
          </Flex>
          <Flex gap={10}>
            <Button type="primary" onClick={() => setSeletctedView("oferta")}>
              Oferta
            </Button>

            {isLogged && (
              <>
                <Button
                  type="primary"
                  onClick={() => setSeletctedView("rezerwacje")}
                >
                  Rezerwacje
                </Button>
                {isLogged && user?.type == "admin" && (
                  <Button
                    type="primary"
                    onClick={() => setSeletctedView("panel_admina")}
                  >
                    Panel Admina
                  </Button>
                )}
                <Button
                  danger
                  onClick={() => {
                    document.cookie =
                      "auth=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                    console.log("Wylogowano");
                    window.location.reload();
                  }}
                >
                  Wyloguj
                </Button>
              </>
            )}
            {!isLogged && (
              <>
                <Button
                  type="primary"
                  onClick={() => setSeletctedView("zaloguj")}
                >
                  Zaloguj
                </Button>
                <Button
                  type="primary"
                  onClick={() => setSeletctedView("zarejestruj")}
                >
                  Zarejestruj
                </Button>
              </>
            )}
          </Flex>
        </Flex>
      </Flex>
    </>
  );
};
