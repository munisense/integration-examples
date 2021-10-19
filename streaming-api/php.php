<?php

// We use the PHP compiled module "ext-amqp", but libs like https://github.com/php-amqplib/php-amqplib work as well

// Create the connection to our AMQP(S) endpoint
$conn = new AMQPConnection(['host' => "", "port" => 5671, "login" => "yourusername", "password" => "yourpassword", "vhost" => "yourvhost"]);
$conn->setCACert(openssl_get_cert_locations()["default_cert_file"]);
$conn->connect();

// Each consuming thread gets its own channel
$chan = new AMQPChannel($conn);

// Bit weird API, but this loads an existing queue
$queue = new AMQPQueue($chan);
$queue->setName("yourqueuename");

// Either use get() for a single message, or consume() block until the next message. Usually in a for loop.
$msg = $queue->get();

echo "Found msg: " . $msg->getRoutingKey() . " with contents " . $msg->getBody() . PHP_EOL;

$queue->ack($msg->getDeliveryTag());