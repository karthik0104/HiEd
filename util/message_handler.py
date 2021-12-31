"""
Central message handler which handles and routes all application related messages, such as Web Socket, RabbitMQ,
as per the content received in the message.
"""

from config.argsparser import ArgumentsParser
from flask_socketio import send
from exception.error_code import ErrorCode
from hied.core.app_enum import MessageType
from util.kafka_producer import KafkaProducer

configs = ArgumentsParser()

class MessageHandler:

    @classmethod
    def handle_message(cls, message: str, request_id):
        pass

class SocketMessageHandler(MessageHandler):

    @classmethod
    def handle_message(cls, message: str, request_id):
        """
        Handle web socket messages by routing them as per the message type.
        @param message: The actual message in JSON format
        @param request_id: The client ID from which the message has been sent
        """

        if 'message_type' not in message:
            #raise MessageFieldMissingException(code=ErrorCode.TOKEN_MISSING, message='Message type not present')
            print('Okay')
        message_type = message['message_type']

        if message_type in [MessageType.ADD_DISCUSSION_THREAD.value, MessageType.ADD_THREAD_REPLY.value]:
            KafkaProducer.send_message(message)