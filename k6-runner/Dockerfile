# note: image runs with k6 user, which plays weird with the WORKDIR
FROM grafana/k6:latest
WORKDIR /app
COPY . /app

USER root
RUN apk add --no-cache jq

USER k6
RUN /app/build.sh

CMD ["run","uptime-check.js"]
