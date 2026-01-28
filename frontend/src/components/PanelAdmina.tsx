import { useQuery } from "@tanstack/react-query";
import { listReservations } from "../services/API";
import { useEffect, useState } from "react";
import { Flex, Statistic, Table } from "antd";

export const PanelAdmina = () => {
  const [totalReservations, setTotalReservations] = useState<
    number | undefined
  >(undefined);
  const {
    data: reservations,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["list_reservations"],
    queryFn: listReservations,
  });
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Rower (Bike ID)",
      dataIndex: "bike_id",
      key: "bike_id",
    },
    {
      title: "Klient (Client ID)",
      dataIndex: "client_id",
      key: "client_id",
    },
    {
      title: "Data rozpoczęcia",
      dataIndex: "start_date",
      key: "start_date",
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: "Data zakończenia",
      dataIndex: "end_date",
      key: "end_date",
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: "Cena",
      dataIndex: "price",
      key: "price",
      render: (price: number) => `${price} PLN`,
    },
  ];
  useEffect(() => {
    const totalReservations = reservations?.length ?? 0;
    setTotalReservations(totalReservations);
  }, [reservations]);
  return (
    <>
      <Flex vertical style={{ width: "100%" }}>
        <Flex justify="center">Panel Admina</Flex>
        <Flex style={{ margin: "20px 20px" }} vertical gap={50}>
          <Flex vertical>
            <Statistic title={"Liczba rezerwacji"} value={totalReservations} />
          </Flex>
          <Flex style={{ width: "100%" }}>
            <Table
              rowKey={"id"}
              columns={columns}
              dataSource={reservations}
              pagination={false}
            />
          </Flex>
        </Flex>
      </Flex>
    </>
  );
};
