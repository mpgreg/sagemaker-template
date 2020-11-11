FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.6.0-cpu-py36-ubuntu16.04
  WORKDIR /tmp
  COPY ./dashboard.py ./umap_embedding.joblib /tmp/
  RUN pip install dash dash-ui matplotlib
  ENTRYPOINT python /tmp/dashboard.py
