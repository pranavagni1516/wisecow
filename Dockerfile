FROM ubuntu

WORKDIR /app

RUN apt -y update
RUN apt install git netcat-openbsd -y
RUN git clone https://github.com/nyrahul/wisecow

WORKDIR /app/wisecow

RUN apt install fortune-mod cowsay -y

ENV PATH=$PATH:/usr/games

RUN chmod 755 wisecow.sh

ENTRYPOINT [ "./wisecow.sh" ]