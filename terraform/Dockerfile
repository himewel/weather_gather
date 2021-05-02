FROM google/cloud-sdk:alpine

ENV TF_VERSION 0.14.3

RUN curl -O https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip \
    && unzip terraform_${TF_VERSION}_linux_amd64.zip -d /usr/bin \
    && rm -rf terraform_${TF_VERSION}_linux_amd64.zip

WORKDIR /root

CMD ["tail", "-f", "/dev/null"]
