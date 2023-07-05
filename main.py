import os
import argparse
from google.cloud import pubsub_v1
from graceful_shutdown import ExitSignalHandler
from time import sleep

print("VERSION - v0.1")

PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
TOPIC_NAME = os.environ.get('GCP_PUBSUB_TOPIC', 'pubsubtopic-test')
SUBSCRIPTION_ID = os.environ.get('GCP_PUBSUB_TOPIC_SUB', 'pubsubsubscription-test-a')

SEND_INTERVAL = 5


def publisher(shutdown: ExitSignalHandler):
  print('PUBLISHER WORKER ')
    
  message_index = 0
  with pubsub_v1.PublisherClient() as publisher:
    full_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    print(f'TOPIC {full_path}')

    while not shutdown.triggered:
      msg = f'#{message_index} Process Me Harder!'
      print(f'Send {msg}')
      future = publisher.publish(full_path, msg.encode('ascii') )
      future.result()

      message_index += 1

      sleep(SEND_INTERVAL)


def subscriber(shutdown: ExitSignalHandler):
  print('SUBSCRIBER WORKER')

  def message_callback(message):
      print(f"Message receieved: {message.data}")
      message.ack()

  with pubsub_v1.SubscriberClient() as subscriber:
      subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
      print(f'USE SUBSCRIPTION {subscription_path}')    

      future = subscriber.subscribe(subscription_path, message_callback)
      future.result()


def main():
  parser = argparse.ArgumentParser(prog='PubSub Dummy Worker',
                                   description='Allow to publish or subscribe dummy message to PubSub')
  
  parser.add_argument('--publisher', dest='worker', action='store_const', default=publisher,
                      const=publisher,
                      help='run dummy publisher')
  parser.add_argument('--subscriber', dest='worker', action='store_const',
                      const=subscriber,
                      help='run dummy subscriber')

  args = parser.parse_args()

  shutdown = ExitSignalHandler()
  # Do To exit from process in order to make keep pod running
  # It will make it possible to exec bash inside pod and debug
  # For example, make http request to metadada
  while not shutdown.triggered:
    try:
      args.worker(shutdown)
    except Exception as e:
      print(e)
      sleep(SEND_INTERVAL)


if __name__ == "__main__":
  main()
