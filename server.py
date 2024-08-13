import socket
import threading

rooms = {}
usernames = {}
def broadcast(message, client_socket, room):
    for client in rooms[room]:
        if client != client_socket:
            try:
                client.send(message)
            except:
                rooms[room].remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("/join"):
                _, room, username = message.split()
                if room not in rooms:
                    rooms[room] = []
                rooms[room].append(client_socket)
                usernames[client_socket] = username
                broadcast(f"{username} joined the room!".encode("utf-8"), client_socket, room)
                update_participants_list(room)  # Notify all users about the updated participant list
            elif message.startswith("/create"):
                _, room, username = message.split()
                rooms[room] = [client_socket]
                usernames[client_socket] = username
                update_participants_list(room)  # Notify all users about the updated participant list
            else:
                room, msg = message.split(' ', 1)
                if msg.startswith("/remove"):
                    _, user_to_remove = msg.split()
                    usernames_to_remove = [key for key, value in usernames.items() if value == user_to_remove]
                    for user_socket in usernames_to_remove:
                        if user_socket in rooms[room]:
                            rooms[room].remove(user_socket)
                            del usernames[user_socket]  # Remove user from the usernames dictionary
                    broadcast(f"/remove {user_to_remove}".encode('utf-8'), client_socket, room)
                    update_participants_list(room)  # Notify remaining users about the updated participant list
                else:
                    broadcast(msg.encode('utf-8'), client_socket, room)
        except:
            for room in rooms.values():
                if client_socket in room:
                    room.remove(client_socket)
                    update_participants_list(room)  # Notify remaining users about the updated participant list
            client_socket.close()
            break

def update_participants_list(room):
    participants = [usernames[client] for client in rooms[room] if client in usernames]
    participants_message = f"/participants {','.join(participants)}"
    for client in rooms[room]:
        client.send(participants_message.encode('utf-8'))


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345))
    server.listen()
    print("Server is listening on port 12345")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
