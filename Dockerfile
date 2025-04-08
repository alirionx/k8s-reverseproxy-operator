# Stage 1: Build Environment
FROM python:3.13-alpine AS build-env
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev
COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt
RUN pip install pyinstaller
COPY ./src /app
WORKDIR /app
RUN pyinstaller --onefile reverse-proxy.py

# Stage 2: Runtime Environment
FROM alpine:latest AS runner
RUN apk add --no-cache libffi
COPY --from=build-env /app/dist/reverse-proxy /app/
WORKDIR /app
CMD ["./reverse-proxy", "run", "--verbose"]


# docker run -d \
#   --name some-krpo \
#   -v <PATH_TO_YOUR_KUBECONFIG>:/opt/kubeconfig.yaml \
#   -e KUBECONFIG=/opt/kubeconfig.yaml \
#   ghcr.io/alirionx/k8s-reverseproxy-operator:latest