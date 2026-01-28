import axios from "axios";

export interface Bike {
  id: number;
  description: string;
  is_reserved: boolean;
  model: string;
  price: number;
  type: string;
}
export interface MakeReservationProps {
  email: string;
  bike_model: string;
  start_date: string;
  end_date: string;
}
export interface ReservationsProps {
  id: number;
  bike_model: string;
  price: number;
  start_date: string;
  end_date: string;
}
export const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const getBikes = async (): Promise<Bike[]> => {
  const res = await api.get("/bikes");
  return res.data;
};

export const makeReservation = async (params: MakeReservationProps) => {
  try {
    const res = await api.post("/create-reservation", params);
    return res.data;
  } catch (error) {
    console.error("Błąd przy rezerwacji:", error);
    throw error;
  }
};

export const getReservations = async ({
  user_email,
}: {
  user_email: string;
}): Promise<ReservationsProps[]> => {
  const res = await api.get(`/list-reservations/${user_email}`);
  return res.data;
};

export const deleteReservation = async ({
  reservation_id,
}: {
  reservation_id: number;
}) => {
  try {
    const res = await api.delete(`/remove-reservation/${reservation_id}`);
    return res.data;
  } catch (error) {
    console.error("Błąd przy usuwaniu rezerwacji:", error);
    throw error;
  }
};

export const listReservations = async (): Promise<string[]> => {
  const res = await api.get("/list-reservation");
  return res.data;
};
