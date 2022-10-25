from time import time
import subprocess
import logging

from paddleocr import PaddleOCR, draw_ocr
from flask import Flask, request, jsonify
import numpy as np
import psutil
import cv2

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

@app.route("/health_check", methods=["GET"])
def health_check():
    """
    Return stats about the server
    """
    # Runs the subprocess command to get the live git commit hash
    GIT_HASH = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    cpu_usage = psutil.cpu_percent()  # Gets average CPU usage since last call
    total_memory = psutil.virtual_memory().total
    available_memory = psutil.virtual_memory().available
    response = {
        "cpuPercentUsage": f"{cpu_usage}%",
        "totalMemory": f"{round(total_memory / (1024*1024))}MB",
        "availableMemory": f"{round(available_memory / (1024*1024))}MB",
        "gitCommitHash": GIT_HASH,
        "Another":"param",
    }
    return jsonify(response)

@app.route('/upload', methods=["POST"])
def upload():
    try:
        # check if the post request has the file part
        img_bytes = request.data
        app.logger.info(f"Got image ... {len(img_bytes)}")
        decoded = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        result = ocr.ocr(decoded, cls=True)
        for line in result:
            app.logger.info(line)
        blocks = []
        for line in result:
            coords = line[0]
            text, confidence = line[1]
            block = {
                "left": coords[0][0],
                "right": coords[1][0],
                "top": coords[0][1],
                "bottom": coords[-1][-1],
                "confidence": confidence,
                "text": text
            }
            blocks.append(block)
        return {"timestamp": time(), "blocks":blocks}
    except Exception as err:
        app.logger.error(f"Error occurred {err}")
        raise Exception(f"Counldn't process :( {err}")

if __name__ == "__main__":
    app.run()
