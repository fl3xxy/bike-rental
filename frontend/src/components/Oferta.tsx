import { useQuery } from "@tanstack/react-query";
import {
  getBikes,
  makeReservation,
  type Bike,
  type MakeReservationProps,
} from "../services/API";
import { Button, Card, Flex, Tooltip, Modal, DatePicker, message } from "antd";
import { useEffect, useState, type Dispatch, type SetStateAction } from "react";
import {
  MinusCircleFilled,
  CheckCircleFilled,
  CalendarOutlined,
} from "@ant-design/icons";
import type { User } from "./Zaloguj";
const { RangePicker } = DatePicker;

const { Meta } = Card;
interface OfertaProps {
  user: User | null;
  isLogged: boolean;
  setSelectedView: Dispatch<
    SetStateAction<
      "oferta" | "rezerwacje" | "zaloguj" | "zarejestruj" | "panel_admina"
    >
  >;
}

export const Oferta = ({ user, isLogged, setSelectedView }: OfertaProps) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedModel, setSelectedModel] = useState<Bike | undefined>(
    undefined,
  );
  const [selectedDate, setSelectedDate] = useState<string[] | undefined>(
    undefined,
  );
  const [totalDays, setTotalDays] = useState<number | undefined>(undefined);
  const countDaysFromStrings = (startStr: string, endStr: string): number => {
    const start = new Date(startStr);
    const end = new Date(endStr);

    const startDay = new Date(
      start.getFullYear(),
      start.getMonth(),
      start.getDate(),
    );
    const endDay = new Date(end.getFullYear(), end.getMonth(), end.getDate());

    const diffMs = endDay.getTime() - startDay.getTime();

    return Math.floor(diffMs / (1000 * 60 * 60 * 24)) + 1;
  };
  const showModal = ({ selectedModel }: { selectedModel: Bike }) => {
    setSelectedModel(selectedModel);
    setIsModalOpen(true);
  };

  const handleOk = async () => {
    if (user && selectedModel && selectedDate) {
      const params: MakeReservationProps = {
        email: user.email,
        bike_model: selectedModel.model,
        start_date: selectedDate[0], // string
        end_date: selectedDate[1], // string
      };

      try {
        const response = await makeReservation(params);
        console.log("Rezerwacja udana:", response);
      } catch (error) {
        console.error("Błąd przy rezerwacji:", error);
      }
    }

    setIsModalOpen(false);
    setSelectedModel(undefined);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
    setSelectedModel(undefined);
  };

  const { data, isLoading, error } = useQuery({
    queryKey: ["bikes"],
    queryFn: getBikes,
  });
  useEffect(() => {
    if (selectedDate) {
      const totalDays = countDaysFromStrings(selectedDate[0], selectedDate[1]);
      setTotalDays(totalDays);
    }
  }, [selectedDate]);
  if (isLoading) return <div>Ładowanie...</div>;
  if (error) return <div>Błąd 😢</div>;

  const BikeCard = ({ bike }: { bike: Bike }) => (
    <Card
      hoverable
      cover={
        <img
          draggable={false}
          alt={bike.model}
          src="/rower.jpg"
          style={{ height: 150, objectFit: "cover" }}
        />
      }
      style={{
        width: 250,
        marginBottom: 16,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <div style={{ minHeight: 60 }}>
        <Meta title={bike.model} description={bike.description ?? ""} />
      </div>

      <Flex
        style={{
          marginTop: 12,
        }}
        justify="space-between"
        align="flex-start"
        vertical
        gap={10}
      >
        <span style={{ color: "#bdbdbd" }}>
          Cena:{" "}
          <span style={{ color: "green", fontWeight: "bold" }}>
            {bike.price} zł / dzień
          </span>
        </span>
        <Flex gap={10}>
          <Tooltip
            title={
              !isLogged ? "Aby zarezerwować rower musisz być zalogowany!" : ""
            }
          >
            <Button
              icon={<CalendarOutlined />}
              size="small"
              type="primary"
              disabled={bike.is_reserved || !isLogged}
              onClick={() => showModal({ selectedModel: bike })}
            >
              Zarezerwuj
            </Button>
          </Tooltip>

          {bike.is_reserved ? (
            <Button
              icon={<MinusCircleFilled />}
              variant="solid"
              color="danger"
              size="small"
            ></Button>
          ) : (
            <Button
              icon={<CheckCircleFilled />}
              variant="solid"
              color="green"
              size="small"
            >
              Dostępny
            </Button>
          )}
        </Flex>
      </Flex>
    </Card>
  );

  return (
    <>
      <div
        style={{ display: "flex", gap: 16, flexWrap: "wrap", marginLeft: 10 }}
      >
        {data?.map((bike) => (
          <BikeCard key={bike.model} bike={bike} />
        ))}
      </div>
      <Modal
        title="Formularz rezerwacji"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        footer={[
          <Button danger onClick={handleCancel}>
            Anuluj
          </Button>,
          <Button
            type="primary"
            onClick={() => {
              handleOk();
              setSelectedView("rezerwacje");
              message.success("Rezerwacja pomyślnie utworzona");
            }}
            disabled={!selectedDate}
          >
            Zarezerwuj
          </Button>,
        ]}
      >
        <Flex vertical gap={20}>
          <Flex vertical>
            <p>
              <span style={{ color: "#bdbdbd" }}>Model:</span>{" "}
              {selectedModel?.model}
            </p>
            <p>
              <span style={{ color: "#bdbdbd" }}>Cena:</span>{" "}
              {selectedModel?.price}zł / dzień
            </p>
          </Flex>
          <Flex vertical>
            <p>Wybierz daty:</p>
            <RangePicker
              showTime
              style={{ width: "80%" }}
              onChange={(_, dateStrings) => {
                setSelectedDate(dateStrings);
              }}
            />
          </Flex>
          {selectedDate && selectedModel && totalDays && (
            <Flex vertical>
              <p style={{ color: "#bdbdbd" }}>Wybrane daty</p>
              <p>Od: {selectedDate && selectedDate[0]}</p>
              <p>Do: {selectedDate && selectedDate[1]}</p>
              <p style={{ fontWeight: "bold" }}>
                Kwota całkowita: {Number(selectedModel?.price) * totalDays}zł
              </p>
            </Flex>
          )}
        </Flex>
      </Modal>
    </>
  );
};
