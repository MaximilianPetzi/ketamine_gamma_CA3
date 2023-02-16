#FROM continuumio/anaconda3
FROM python:2.7

#RUN conda install pip
RUN pip install neuron
#COPY . .

RUN pip install termcolor


RUN apt update
RUN apt install build-essential -y

