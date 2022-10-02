FROM paddlepaddle/paddle:2.3.2

RUN pip install paddleocr

# Ocr test image
RUN wget http://jeroen.github.io/images/testocr.png
# Make paddle pre-download models
RUN paddleocr --image_dir ./testocr.png --use_angle_cls true --lang en --use_gpu false

COPY process_image.py process_image.py
CMD python process_image.py
