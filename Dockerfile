FROM ubuntu:latest
LABEL authors="anhtu"

ENTRYPOINT ["top", "-b"]