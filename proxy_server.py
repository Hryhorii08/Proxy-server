from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL сервера времени (замени на свой)
SERVER_URL = "https://timeapi-j0xt.onrender.com/webhook"

@app.route("/proxy", methods=["POST"])
def proxy():
    data = request.json  # Получаем JSON-запрос от OpenAI
    function_call = data.get("function", {})

    # Проверяем, что функция корректная
    if not function_call or "name" not in function_call:
        return jsonify({"error": "Некорректный запрос"}), 400

    if function_call["name"] == "get_current_time":
        city = function_call["arguments"].get("city")

        if not city:
            return jsonify({"error": "Город не указан"}), 400

        # Отправляем запрос на сервер времени
        server_response = requests.post(
            SERVER_URL,
            json={"function": {"name": "get_current_time"}, "arguments": {"city": city}}
        )

        # Получаем и возвращаем ответ
        return jsonify(server_response.json()) if server_response.status_code == 200 else jsonify({"error": "Ошибка при запросе"})

    return jsonify({"error": "Неверный запрос"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
