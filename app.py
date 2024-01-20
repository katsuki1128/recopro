# app.py
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import speech_recognition as sr
import csv
from datetime import datetime

app = Flask(__name__)

# APIキー
YOUR_API_KEY = "AIzaSyDcZ9vKsgSuml2lHUF9EV7sHO9v-w4v7G8"
genai.configure(api_key=YOUR_API_KEY)

# モデルの選択
model = genai.GenerativeModel("gemini-pro")

# Speech Recognition インスタンスの初期化
r = sr.Recognizer()
mic = sr.Microphone()


def append_to_csv(summary_text, file_name="summaries.csv"):
    with open(file_name, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), summary_text])


@app.route("/")
def index():
    return render_template("index.html")


# while True:
# print("話しかけてください")


@app.route("/process_audio", methods=["POST"])
def process_audio():
    # クライアントから送信されたデータを取得
    data = request.get_json()
    speech_text = data.get("text")

    try:
        # テキスト要約のためのプロンプトを作成
        prompt = f"以下のテキストを30文字に要約してください: {speech_text}"

        # Geminiを使用してテキスト推論
        response = model.generate_content(prompt)

        # CSVファイルに要約テキストと日時を追記
        append_to_csv(response.text)

        return jsonify({"text": response.text})

    except Exception as e:
        # 何らかのエラーが発生した場合
        return jsonify({"error": str(e)})

    # with mic as source:
    #     r.adjust_for_ambient_noise(source)  # 雑音対策
    #     audio = r.listen(source)

    #     # オーディオデータをWAVファイルとして保存
    #     with open("recorded_audio.wav", "wb") as audio_file:
    #         audio_file.write(audio.get_wav_data())

    # print("Now to recognize it...")

    # try:
    #     # 音声をテキストに変換
    #     speech_text = r.recognize_google(audio, language="ja-JP")
    #     print("speech_text", speech_text)

    #     # "ストップ" と言ったら音声認識を止める
    #     # if speech_text == "ストップ":
    #     #     print("End of Speech Recognition")
    #     #     break

    #     # Geminiを使用してテキスト推論
    #     response = model.generate_content(speech_text)
    #     print(response.text)
    #     return jsonify({"text": response.text})

    # except sr.UnknownValueError:
    #     return jsonify({"error": "Could not understand audio"})
    # except sr.RequestError as e:
    #     return jsonify(
    #         {
    #             "error": f"Could not request results from Google Speech Recognition service; {e}"
    #         }
    #     )


if __name__ == "__main__":
    app.run(debug=True)
