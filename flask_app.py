from flask import Flask, request, render_template, jsonify, send_from_directory, session
import os
from datetime import datetime
import dongsooAI as ds
from langchain.document_loaders import TextLoader

app = Flask(__name__)
app.secret_key = 'GTalkStory'
# loader = WebBaseLoader(web_path="https://jeju-s.jje.hs.kr/jeju-s/0102/history")

# 이미지가 저장될 디렉토리를 설정합니다.
UPLOAD_FOLDER = 'saved_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
 
      return send_from_directory("templates", "start.html")


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('templates/files', filename, as_attachment=True)

@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory("templates/audio", filename)

@app.route('/images/<filename>')
def images(filename):
    return send_from_directory("templates/images", filename)

@app.route('/chat_audio/<filename>')
def chat_audio(filename):
    return send_from_directory("templates/chat_audio", filename)

@app.route('/<path:page>')
def pathpage(page):
        print(page)
        return send_from_directory("templates", page)

@app.route('/<page>')
def page(page):
    if 'token' not in session:
        session['token'] = ds.rnd_str(n=20, type="s")
    if ".html" in page:
        return render_template(page, token=session['token'])
    else:
        return send_from_directory("templates", page)

@app.route("/vision", methods=["POST"])
def vision():
    prompt = request.json.get("prompt")
    image_infor = request.json.get("image_infor")
    print("vision prompt=", prompt)
    print("image_infor=", image_infor[:50])
    re = ds.vision_talk(prompt=prompt, image_infor=image_infor)

    print(re)

    return jsonify(re)

@app.route("/dalle3", methods=["POST"])
def dalle3():
    prompt = request.json.get("prompt")
    print("dalle3 prompt=", prompt)
    re = ds.image_create(prompt=prompt)
    print(re)

    # 이미지 URL을 파일에 저장
    if 'url' in re:
        image_url = re['url']
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_images.txt')

        with open(save_path, 'a') as file:
            file.write(image_url + '\n')

    return jsonify(re)

@app.route("/chatGPT_tts", methods=["POST"])
def chatGPT_tts():
    prompt = request.json.get("prompt")
    voice = request.json.get("voice")
    chat_id = request.json.get("chat_id")
    print("prompt= ", prompt)
    global chat_story
    re = ds.chatGPT_tts(query=prompt, voice=voice, chat_id=chat_id, chat_story=chat_story, token=session['token'])
    return jsonify(re)

@app.route('/일기', methods=['GET', 'POST'])
def 일기():
    if request.method == 'GET':
        # 일기 작성 폼을 보여주기 위한 GET 요청 처리
        return render_template('일기.html', token=session['token'])
    elif request.method == 'POST':
        # 일기 항목을 저장하기 위한 POST 요청 처리
        오늘날짜 = datetime.now().strftime("%Y-%m-%d")
        일기내용 = request.form.get('일기_항목')

        # 현재 날짜로 파일을 만들어 일기 내용을 저장
        파일명 = f"diaries/{오늘날짜}.txt"
        with open(파일명, 'w', encoding='utf-8') as 파일:
            파일.write(일기내용)

        return render_template('일기.html', token=session['token'])

@app.route('/save_image', methods=['POST'])
def save_image():
    # 이미지 저장 버튼을 눌렀을 때 호출되는 함수
    # 여기서는 이미지 URL을 파일에 저장
    image_url = request.json.get("url")
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_images.txt')

    with open(save_path, 'a') as file:
        file.write(image_url + '\n')

    return jsonify({"message": f"Image URL saved successfully. URL: {image_url}"})

if __name__ == '__main__':
    app.run(ssl_context=('openSSL/cert.pem', 'openSSL/key.pem'), debug=True, port=5001, host='0.0.0.0')
