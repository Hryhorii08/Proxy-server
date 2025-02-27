from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL сервера времени (замени на свой)
SERVER_URL = "https://timeapi-j0xt.onrender.com/webhook"

@app.route("/proxy", methods=["POST"])
def proxy():
    data = request.json  # Получаем JSON-запрос от OpenAI
    function_call = data.get("function")

    if function_call and function_call["name"] == "get_current_time":
        city = function_call["arguments"]["city"]

        # Отправляем запрос на сервер времени
        server_response = requests.post(
            SERVER_URL,
            json={"function": {"name": "get_current_time"}, "arguments": {"city": city}}
        )

        # Получаем и возвращаем ответ
        return jsonify(server_response.json() if server_response.status_code == 200 else {"error": "Ошибка при запросе"})

    return jsonify({"error": "Неверный запрос"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
