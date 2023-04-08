#FROM continuumio/anaconda3
FROM python:2.7

#RUN conda install pip
RUN pip install neuron && pip install termcolor && pip install scipy && pip install matplotlib && pip install seaborn
COPY . . 


RUN apt update
RUN apt install build-essential -y
