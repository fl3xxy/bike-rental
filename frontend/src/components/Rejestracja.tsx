import type { FormProps } from "antd";
import { Button, Flex, Form, Input, message } from "antd";
import { type Dispatch, type SetStateAction } from "react";

type FieldType = {
  email?: string;
  password?: string;
  first_name?: string;
  last_name?: string;
};
interface RejestracjaProps {
  setSelectedView: Dispatch<
    SetStateAction<
      "oferta" | "rezerwacje" | "zaloguj" | "zarejestruj" | "panel_admina"
    >
  >;
}

export const Rejestracja = ({ setSelectedView }: RejestracjaProps) => {
  const onFinish: FormProps<FieldType>["onFinish"] = async (values) => {
    try {
      const response = await fetch("http://localhost:8000/create-client", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: values.email,
          password: values.password,
          first_name: values.first_name,
          last_name: values.last_name,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`,
        );
      }

      message.success("Pomyślnie utworzono konto");
      setSelectedView("zaloguj");
    } catch (error: any) {
      console.error("Błąd podczas rejestracji:", error);
      message.error(`Błąd podczas rejestracji: ${error.message}`);
    }
  };

  const onFinishFailed: FormProps<FieldType>["onFinishFailed"] = (
    errorInfo,
  ) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <Flex
      style={{ width: "100%", height: "100%" }}
      align="center"
      justify="center"
    >
      <Form
        name="register"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600 }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item<FieldType>
          label="Email"
          name="email"
          rules={[{ required: true, message: "Please input your email!" }]}
        >
          <Input type="email" />
        </Form.Item>

        <Form.Item<FieldType>
          label="Hasło"
          name="password"
          rules={[{ required: true, message: "Please input your password!" }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item<FieldType>
          label="Imię"
          name="first_name"
          rules={[{ required: true, message: "Please input your first name!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item<FieldType>
          label="Nazwisko"
          name="last_name"
          rules={[{ required: true, message: "Please input your last name!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item label={null}>
          <Button type="primary" htmlType="submit">
            Zarejestruj
          </Button>
        </Form.Item>
      </Form>
    </Flex>
  );
};
