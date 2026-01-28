import type { FormProps } from "antd";
import { Button, Flex, Form, Input } from "antd";

type FieldType = {
  username?: string;
  password?: string;
  remember?: string;
};

export interface User {
  email: string;
  type: string;
}

export const Zaloguj = () => {
  const onFinish: FormProps<FieldType>["onFinish"] = async (values) => {
    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: values.username,
          password: values.password,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: User = await response.json();
      if (data) {
        const expires = new Date();
        expires.setTime(expires.getTime() + 30 * 60 * 1000); // 30 minut

        const cookieValue = encodeURIComponent(
          JSON.stringify({ email: data.email, type: data.type }),
        );
        document.cookie = `auth=${cookieValue};expires=${expires.toUTCString()};path=/;SameSite=Lax`;

        window.location.reload();
      } else {
        console.log("Logowanie nieudane:", data);
      }
    } catch (error) {
      console.error("Błąd podczas logowania:", error);
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
        name="basic"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600 }}
        initialValues={{ remember: true }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item<FieldType>
          label="Nazwa"
          name="username"
          rules={[{ required: true, message: "Please input your username!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item<FieldType>
          label="Hasło"
          name="password"
          rules={[{ required: true, message: "Please input your password!" }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item label={null}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </Flex>
  );
};
