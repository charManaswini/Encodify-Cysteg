from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import tempfile
import stegano
from stegano import lsb

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        # Perform encryption here using stegano library
        image = request.files['image']
        message = request.form['message']

        # Example encryption using lsb method
        secret = lsb.hide(image, message)

        # Save the encrypted image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            encrypted_image_path = temp_file.name
            secret.save(encrypted_image_path)

        # Send the encrypted image as a file attachment in the response
        return send_file(encrypted_image_path, as_attachment=True, download_name='encrypted_image.png')

    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        # Perform decryption here using stegano library
        encrypted_image = request.files['encrypted_image']

        # Example decryption using lsb method
        decrypted_message = lsb.reveal(encrypted_image)

        return render_template('decrypt_result.html', decrypted_message=decrypted_message)

    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(debug=True)
