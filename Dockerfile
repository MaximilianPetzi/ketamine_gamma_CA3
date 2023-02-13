FROM continuumio/anaconda2

#RUN git clone https://MaximilianPetzi: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@github.com/MaximilianPetzi/my_neymotin.git

RUN conda install pip
RUN pip install neuron
COPY . .

#RUN git checkout LTP_fullmodel

#RUN pip install termcolor

#RUN apt-get update
#RUN apt update
#RUN apt install build-essential

