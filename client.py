from source.message import Message, MessageFactory, MessageType
import socket
from pprint import pprint
import time


def client():
    time.sleep(1)  # 等待服务器启动
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('20.2.217.120', 12345))
    Client_message = Message(client)
    
    name = input("请输入玩家昵称和房间密码(格式：张三,123): ")
    handshake_msg = MessageFactory.player_name(name)
    Client_message.send_message(handshake_msg)
    time.sleep(1)
    
    while True:
        data = Client_message.recv_message()
        if not data:
            print("服务器断开连接")
            break
        if data['type'] == MessageType.TXT.value:
            print(data['data'])
            
        if data['type'] == MessageType.PLAYER_TURN.value:
            if data['data'] == 1:
                print("轮到黑子下棋")
                move_str = input("请输入你的落子位置'x,y': ")
                message = MessageFactory.move(move_str)
                Client_message.send_message(message)
            else:
                print("轮到白子下棋")
                data = Client_message.recv_message()
                if data['type'] == MessageType.BOARD_UPDATE.value:
                    pprint(data['data'])
                elif data['type'] == MessageType.WIN.value:
                    print(data['data'])
                    break
        
        if data['type'] == MessageType.WIN.value:
            print(data['data'])
            break

if __name__ == '__main__':
    client()