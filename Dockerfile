FROM nodejs as nodejsbuilder
FROM python:3.8.17-bookworm

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    apt update && \
    apt install -y libgl1 && \
    apt clean && \
    wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1-1ubuntu2.1~18.04.23_amd64.deb && \
    dpkg -i libssl1.1_1.1.1-1ubuntu2.1~18.04.23_amd64.deb

WORKDIR /app

COPY requirements.txt requirements.txt
COPY paddlewebocr paddlewebocr
COPY inference inference
COPY --from=nodejsbuilder /app/dist webui/dist
COPY docker-entrypoint.sh /usr/local/bin/
RUN wget https://paddle-wheel.bj.bcebos.com/2.4.2/linux/linux-cpu-mkl-noavx/paddlepaddle-2.4.2-cp38-cp38-linux_x86_64.whl
RUN pip install paddlepaddle-2.4.2-cp38-cp38-linux_x86_64.whl -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple \
        --no-cache-dir \
        -r requirements.txt

RUN python paddlewebocr/pkg/ocr.py

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8080

VOLUME /app/logs

CMD ["uvicorn", "paddlewebocr.main:app", "--host", "0.0.0.0", "--port", "8080"]
