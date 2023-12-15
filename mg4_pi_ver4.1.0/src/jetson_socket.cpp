#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

#include "jetson_socket.h"

// サーバーの接続
void Server::s_open(){
    createServerSocket();  // サーバーソケットの作成
    bindAndListen();       // バインドと接続待ちの設定
    acceptConnection();     // クライアントからの接続
}

// メッセージ送受信
char* Server::round_trip(const char s_msg[MAX_BUFFER_SIZE]){
    // メッセージの送信
    std::cout << "送信: " << s_msg << std::endl;
    if (send(clientsock_, s_msg, strlen(s_msg), 0) == -1) {
        perror("メッセージの送信に失敗しました");
        return nullptr;  // エラーを示す値を返す
    }

    std::cout << "クライアントの応答を待っています...\n";

    // メッセージの受信
    ssize_t bytes_received = recv(clientsock_, rcvmsg_, MAX_BUFFER_SIZE, 0);
    if (bytes_received == -1) {
        perror("メッセージの受信に失敗しました");
        return nullptr;  // エラーを示す値を返す
    }
    // 受信したデータを終端文字で終わるように調整
    rcvmsg_[bytes_received] = '\0';
    std::cout << "受信: " << rcvmsg_ << std::endl;

    return rcvmsg_;
}
// サーバーを閉じる
void Server::s_close() {
    // ソケットを閉じる
    close(clientsock_);
    close(serversock_);
}


// サーバーソケットの作成
void Server::createServerSocket() {
    serversock_ = socket(AF_INET, SOCK_STREAM, 0);
    if (serversock_ == -1) {
        perror("サーバーソケットの作成に失敗しました");
        exit(EXIT_FAILURE);
    }
}

// サーバーソケットのバインドと接続待ちの設定
void Server::bindAndListen() {
    struct sockaddr_in server_addr;
    std::memset(&server_addr, 0, sizeof(server_addr));

    // サーバーアドレスの設定
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port_);
    server_addr.sin_addr.s_addr = inet_addr(host_);

    // サーバーソケットのバインド
    if (bind(serversock_, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("サーバーソケットのバインドに失敗しました");
        exit(EXIT_FAILURE);
    }

    // 接続待ちの設定
    if (listen(serversock_, 10) == -1) {
        perror("接続待ちの設定に失敗しました");
        exit(EXIT_FAILURE);
    }

    std::cout << "クライアントの接続を待っています...\n";
}

// クライアントからの接続待ち
void Server::acceptConnection() {
    struct sockaddr_in client_addr;
    socklen_t addr_size = sizeof(struct sockaddr_in);

    // クライアントからの接続待ち
    clientsock_ = accept(serversock_, (struct sockaddr*)&client_addr, &addr_size);
    if (clientsock_ == -1) {
        perror("クライアントの接続受付に失敗しました");
        exit(EXIT_FAILURE);
    }

    std::cout << "クライアントとの接続が確立されました\n";
}
