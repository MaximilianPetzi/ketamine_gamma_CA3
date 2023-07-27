#FROM continuumio/anaconda3
FROM python:2.7
#RUN ECHO pip --version
#RUN conda install pip
RUN pip install neuron && pip install termcolor && pip install scipy && pip install matplotlib && pip install statsmodels==0.10
RUN pip install pandas
RUN pip install seaborn 
COPY . . 
#WTF it doesnt know all the new modules from seaborn, statsmodels and pandas???

RUN apt update
RUN apt install build-essential -y
RUN apt install vim -y
RUN git config --global user.email maximilianpetzi@gmx.de
RUN git config --global user.name MaximilianPetzi

