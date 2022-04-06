FROM python:3

# 導入packageはrequirements.txtを変更のこと
WORKDIR /work/
COPY ./requirements.lock /work/
RUN pip install -r requirements.lock

ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]