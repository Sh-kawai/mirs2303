#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

#include "arduino.h"
#include "request.h"

int kbhit(void)
{
	struct termios oldt, newt;
	int ch;
	int oldf;

	tcgetattr(STDIN_FILENO, &oldt);
	newt = oldt;
	newt.c_lflag &= ~(ICANON | ECHO);
	tcsetattr(STDIN_FILENO, TCSANOW, &newt);
	oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
	fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

	ch = getchar();

	tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
	fcntl(STDIN_FILENO, F_SETFL, oldf);

	if (ch != EOF) {
		//ungetc(ch, stdin);
		return ch;
	}
	return 0;
}

int main() {
    if(arduino_open() != 0) return -1;

    int input;
    int speed_str = 30;
    int dist_str = speed_str/2;
    int speed_rot = 45;
    int dist_rot = speed_rot/2;
    int sv_angle = 90;

    printf("program start\n");

    while (1) {
        // 入力に基づいてロボットの走行を制御
        input = kbhit();
        switch (input) {
            case 'w':
            case 'A':
                printf("[key_ctrl]forward\n");
                request_set_runmode(STR, speed_str, dist_str);
                break;
            case 'a':
            case 'D':
                printf("[key_ctrl]left\n");
                request_set_runmode(ROT, speed_rot, dist_rot);
                break;
            case 's':
            case 'B':
                printf("[key_ctrl]backward\n");
                request_set_runmode(STR, speed_str, -dist_str);
                break;
            case 'd':
            case 'C':
                printf("[key_ctrl]right\n");
                request_set_runmode(ROT, speed_rot, -dist_rot);
                break;
            case ' ':
                printf("[key_ctrl]stop\n");
                request_set_runmode(STP, 0, 0);
                break;
            case 'u':
                sv_angle++;
                if(sv_angle > 180) sv_angle = 180;
                printf("[key_ctrl]servo:%d[deg]\n", sv_angle);
                request_set_runmode(SER, sv_angle, sv_angle);
                break;
            case 'j':
                sv_angle--;
                if(sv_angle < 0) sv_angle = 0;
                printf("[key_ctrl]servo:%d[deg]\n", sv_angle);
                request_set_runmode(SER, sv_angle, sv_angle);
                break;
            case 27: // escapeキー
                request_set_runmode(STP, 0, 0);
                printf("[key_ctrl]setting\n");
                printf("change speed: [str] [rot]\n");
                scanf("%d %d",&speed_str, &speed_rot);
                dist_str = speed_str/2;
                dist_rot = speed_rot/2;
                printf("setted str:%d, rot:%d\n", speed_str, speed_rot);
                break;
            case 'q':
                request_set_runmode(STP, 0, 0);
                printf("[key_ctrl]Exiting the program\n");
                return 1;
            default:
                break;
        }
    }
    return 0;
}
