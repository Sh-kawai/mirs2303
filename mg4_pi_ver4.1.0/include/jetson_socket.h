#ifndef __JETSON_SOCKET__
#define __JETSON_SOCKET__

#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

//#define HOST "172.25.19.3"
//#define HOST "localhost"
#define HOST "192.168.1.2"
#define PORT 8080
#define MAX_BUFFER_SIZE 1024

class Server {
public:
  Server(const char* host, int port) : host_(host), port_(port) {}

  // サーバーの接続
  int s_open();
  // メッセージ送受信
  char* round_trip(const char s_msg[MAX_BUFFER_SIZE]);
  // サーバーを閉じる
  void s_close();

private:
  const char* host_;
  int port_;
  int serversock_;
  int clientsock_;
  char s_msg_[MAX_BUFFER_SIZE];
  char rcvmsg_[MAX_BUFFER_SIZE];

  // サーバーソケットの作成
  int createServerSocket();
  // サーバーソケットのバインドと接続待ちの設定
  int bindAndListen();
  // クライアントからの接続待ち
  int acceptConnection();
};


#endif