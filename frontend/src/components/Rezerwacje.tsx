import {
  deleteReservation,
  getReservations,
  type ReservationsProps,
} from "../services/API";
import type { User } from "./Zaloguj";
import { useQuery } from "@tanstack/react-query";
import { Table, Button } from "antd";
export const Rezerwacje = ({ user }: { user: User | null }) => {
  if (user === null) return;
  const { data, isLoading, error } = useQuery({
    queryKey: ["reservations", user.email],
    queryFn: () => getReservations({ user_email: user.email }),
    refetchInterval: 1000,
  });
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Rower",
      dataIndex: "bike_model",
      key: "bike_model",
    },
    {
      title: "Cena",
      dataIndex: "price",
      key: "price",
      render: (price: number) => `${price} zł`,
    },
    {
      title: "Data startu",
      dataIndex: "start_date",
      key: "start_date",
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: "Data końca",
      dataIndex: "end_date",
      key: "end_date",
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: "Anulowanie",
      render: (item: ReservationsProps) => (
        <Button
          danger
          onClick={() => {
            deleteReservation({ reservation_id: item.id });
            window.location.reload();
          }}
        >
          Anuluj rezerwacje
        </Button>
      ),
    },
  ];

  return (
    <>
      <Table
        title={() => "Rezerwacje"}
        dataSource={data}
        columns={columns}
        rowKey="id"
        style={{ width: "100%" }}
        pagination={false}
      />
    </>
  );
};
