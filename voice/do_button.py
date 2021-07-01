import logging
import platform
import sys
import threading
import subprocess
import paho.mqtt.client as mqtt

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts

def power_off_pi():
    tts.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    tts.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    tts.say('My IP address is %s' % ip_address.decode('utf-8'))

def print_message(msg):
    sender = mqtt.Client("Sender")
    #sender.connect("192.168.137.222")
    sender.connect("192.168.0.107")
    sender.publish("robot", msg)

class MyAssistant:

    def __init__(self):
        self._task = threading.Thread(target=self._run_task)
        self._can_start_conversation = False
        self._assistant = None
        self._board = Board()
        self._board.button.when_pressed = self._on_button_pressed

    def start(self):
        self._task.start()

    def _run_task(self):
        credentials = auth_helpers.get_assistant_credentials()
        with Assistant(credentials) as assistant:
            self._assistant = assistant
            for event in assistant.start():
                self._process_event(event)

    def _process_event(self, event):
        logging.info(event)
        if event.type == EventType.ON_START_FINISHED:
            self._board.led.status = Led.BEACON_DARK  # Ready.
            self._can_start_conversation = True
            # Start the voicehat button trigger.
            logging.info('Say "OK, Google" or press the button, then speak. '
                         'Press Ctrl+C to quit...')

        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self._can_start_conversation = False
            self._board.led.state = Led.ON  # Listening.

        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
                 print('You said:', event.args['text'])
                 text = event.args['text'].lower()
                 if text == 'power off':
                    self._assistant.stop_conversation()
                    power_off_pi()
                 elif text == 'reboot':
                    self._assistant.stop_conversation()
                    reboot_pi()
                 elif text == 'ip address':
                    self._assistant.stop_conversation()
                    say_ip()
                 elif text == 'robot forward':
                    self._assistant.stop_conversation()
                    print_message("forward")
                 elif text == 'robot backward':
                    self._assistant.stop_conversation()
                    print_message("backward")
                 elif text == 'robot turn clockwise':
                    self._assistant.stop_conversation()
                    print_message("counterclockwise")
                 elif text == 'robot turn counter-clockwise':
                    self._assistant.stop_conversation()
                    print_message("clockwise")
                 elif text == 'robot dance':
                    self._assistant.stop_conversation()
                    print_message("dance")
                 elif text.startswith('find'):
                    self._assistant.stop_conversation()
                    print_message(text)
        elif event.type == EventType.ON_END_OF_UTTERANCE:
            self._board.led.state = Led.PULSE_QUICK  # Thinking.

        elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
              or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
              or event.type == EventType.ON_NO_RESPONSE):
            self._board.led.state = Led.BEACON_DARK  # Ready.
            self._can_start_conversation = True

        elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
            sys.exit(1)

    def _on_button_pressed(self):
        if self._can_start_conversation:
            self._assistant.start_conversation()


def main():
    logging.basicConfig(level=logging.INFO)
    MyAssistant().start()


if __name__ == '__main__':
    main()
