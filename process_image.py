import cv2
from time import time
import logging
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
from flask import Flask, request

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

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
    app.run(debug=True, host="0.0.0.0", port=80)
