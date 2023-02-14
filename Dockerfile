FROM continuumio/anaconda3

RUN conda install pip
RUN pip install neuron
#COPY . .

RUN pip install termcolor

#RUN apt-get update -y
RUN apt update
RUN apt install build-essential -y

