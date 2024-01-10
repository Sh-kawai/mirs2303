#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

#include "jetson_socket.h"

int main() {
    char s_msg[MAX_BUFFER_SIZE];
    char* r_msg;

    Server server(HOST, PORT);
    server.s_open();

    while (true) {
        std::cout << "end-socket:q, get_img:1, get_img[auto]:2, upload:3, message:[string]\n";
        std::cin.getline(s_msg, MAX_BUFFER_SIZE);

        // メッセージの送受信
        r_msg = server.round_trip(s_msg);

        // 終了条件の確認
        if (strcmp(s_msg, "q") == 0) {
            break;
        }
    }
    server.s_close();

    return 0;
}