FROM rabbitmq:3-management
ENV TZ UTC

RUN rabbitmq-plugins enable --offline rabbitmq_shovel rabbitmq_shovel_management
