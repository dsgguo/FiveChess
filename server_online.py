import socket
from source.message import Message, MessageFactory, MessageType
from source.chess import Chess, Player

ROOM_KEY = "123"

def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', 12345))
    server_sock.listen(2)
    print('服务器启动，等待连接...')
    
    # 接收两个客户端连接
    conn1, addr1 = server_sock.accept()
    print('客户端1已连接:', addr1)
    conn2, addr2 = server_sock.accept()
    print('客户端2已连接:', addr2)
    
    # 创建消息处理工具类
    msg1 = Message(conn1)
    msg2 = Message(conn2)
    
    # 两个客户端在初始化阶段发送玩家信息，其中data为 "name;room_key"
    handshake1 = msg1.recv_message()
    handshake2 = msg2.recv_message()
    
    if handshake1['type'] == MessageType.PLAYER_NAME.value and handshake2['type'] == MessageType.PLAYER_NAME.value:
        # 简单解析提交的数据
        try:
            name1, key1 = handshake1["data"].split(",")
            name2, key2 = handshake2["data"].split(",")
        except Exception as e:
            print("握手数据格式错误", e)
            conn1.close()
            conn2.close()
            server_sock.close()
            return
        # 校验密钥 
        if key1 != ROOM_KEY or key2 != ROOM_KEY:
            error_msg = MessageFactory.txt("房间密钥错误，连接拒绝！")
            msg1.send_message(error_msg)
            msg2.send_message(error_msg)
            conn1.close()
            conn2.close()
            server_sock.close()
            return

    # 分配玩家角色
    player1 = Player.BLACK
    player2 = Player.WHITE
    # 发送玩家信息
    player1info = MessageFactory.txt('玩家f{name1},执黑子，玩家f{name2},执白子')
    player2info = MessageFactory.txt('玩家f{name1},执黑子，玩家f{name2},执白子')
    msg1.send_message(player1info)
    msg2.send_message(player2info)
    
    board = Chess()
    board.drawbord()
    
    # 初始回合设为服务器（白棋）下棋
    current_player = player2
    
    msg1.send_message(MessageFactory.player_turn(player2.value))
    msg2.send_message(MessageFactory.player_turn(player1.value))
    
    while True:
        if current_player == player1:
            # 轮到客户端下棋，等待接收客户端落子
            data = msg1.recv_message()
            if not data:
                print("玩家1断开连接")
                break
            if data['type'] == MessageType.MOVE.value:
                print(f"玩家 {name1} 落子: {data['data']}")
                # 客户端落子
                brand_board, check_result = board.move(data['data'], player1)
                # 向客户端发送棋盘信息
                update = MessageFactory.board_update(brand_board)
                msg1.send_message(update)
                msg2.send_message(update)
            
                if check_result:
                    win_msg = MessageFactory.txt(f"{name1} 获胜！")
                    # 向客户端发送胜利结果
                    msg1.send_message(win_msg)
                    msg2.send_message(win_msg)
                    break
            # 变更回合至服务器
            current_player = player2
        else:
            data = msg2.recv_message()
            if not data:
                print("玩家2断开连接")
                break
            
            if data['type'] == MessageType.MOVE.value:
                print(f"玩家 {name2} 落子: {data['data']}")
                # 客户端落子
                brand_board, check_result = board.move(data['data'], player2)
                update = MessageFactory.board_update(brand_board)
                msg1.send_message(update)
                msg2.send_message(update)
           
                if check_result:
                    win_msg = MessageFactory.txt(f"{name2} 获胜！")
                    msg1.send_message(win_msg)
                    msg2.send_message(win_msg)
                    break
                current_player = player1

        turn_msg = MessageFactory.player_turn(current_player.value)
        msg1.send_message(turn_msg)
        msg2.send_message(turn_msg)
        
    conn1.close()
    conn2.close()
    server_sock.close()

if __name__ == "__main__":
#    server_thread =  threading.Thread(target=server).start()
    server()
    