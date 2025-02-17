import struct
import json
from enum import Enum

class MessageType(Enum):
    PLAYER_NAME = 'player_name'
    MOVE = 'move'
    WIN = 'win'
    PLAYER_TURN = 'player_turn'
    BOARD_UPDATE = 'board_update'
    TXT = 'txt'

class MessageFactory:
    @staticmethod
    def player_name(data):
        return {'type': MessageType.PLAYER_NAME.value, 'data': data}
    @staticmethod
    def move(data):
        return {'type': MessageType.MOVE.value, 'data': data}
    @staticmethod
    def player_turn(data):
        return {'type': MessageType.PLAYER_TURN.value, 'data': data}
    @staticmethod
    def board_update(data):
        return {'type': MessageType.BOARD_UPDATE.value, 'data': data}
    @staticmethod
    def txt(data):
        return {'type': MessageType.TXT.value, 'data': data}
    
class Message:
    # 通过 socket 传输消息的工具类
    def __init__(self, sock):
        self.sock = sock
        pass
    
    def send_message(self, message):
        """
        将任意 Python 对象序列化后，通过 socket 发送
        消息格式： [4 字节消息长度][消息数据]
        """
        # 序列化数据为 JSON 字符串，再转为字节流
        data = json.dumps(message).encode('utf-8')
        # 使用 struct.pack 打包消息长度（大端方式的无符号整数）
        length = struct.pack('>I', len(data))
        self.sock.sendall(length)
        self.sock.sendall(data)

    def recv_message(self):
        """
        从 socket 接收消息，先接收长度，再接收数据
        """
        # 先接收 4 字节长的消息头
        raw_length = self.recvall(self.sock, 4)
        if not raw_length:
            return None
        msg_length = struct.unpack('>I', raw_length)[0]
        # 接收剩余的消息体
        data = self.recvall(self.sock, msg_length)
        return json.loads(data.decode('utf-8'))

    def recvall(self, sock, n):
        """
        辅助函数：接收 n 字节数据，保证全部读取
        """
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data