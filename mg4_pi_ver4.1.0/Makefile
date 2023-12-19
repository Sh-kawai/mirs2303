# 各種ファイルの保存ディレクトリ
DIR_SRC  := ./src
DIR_HEAD := ./include
DIR_OBJ  := ./build
DIR_IMG  := ./img

# 生成するプログラム
PRGS := 
PRGS += test_io test_uss test_request test_direction
PRGS += test_capture test_number test_dir_num test_camera
PRGS += test_server test_position test_socket
PRGS += test_keyboard
PRGS += pilot

# オブジェクト
OBJS_RUN := $(addprefix $(DIR_OBJ)/, io.o uss.o arduino.o request.o direction.o)
OBJS_CAP := $(addprefix $(DIR_OBJ)/, get_img.o)
OBJS_NUM := $(addprefix $(DIR_OBJ)/, number_search.o number_detect.o)
OBJS_SVR := $(addprefix $(DIR_OBJ)/, server.o)
OBJS_POS := $(addprefix $(DIR_OBJ)/, position.o)
OBJS_SOC := $(addprefix $(DIR_OBJ)/, jetson_socket.o)
OBJS_KEY := $(addprefix $(DIR_OBJ)/, keyboard.o)

# コンパイルオプション
CC      := g++
G++      := g++
CFLAGS  := -O2 -Wall -MMD -MP `pkg-config --cflags opencv`
LDFLAGS := -lm -lpthread -lwiringPi `pkg-config --libs opencv` -lncurses
INCLUDE := -I $(DIR_HEAD)

# 全コンパイル・ファイル削除用ターゲット
.PHONY: all clean

all: $(PRGS)

clean:
	$(RM) $(PRGS)
	$(RM) $(DIR_OBJ)/*.o $(DIR_OBJ)/*.d
	$(RM) $(DIR_IMG)/*.jpg

# パターンルール
$(DIR_OBJ)/%.o: $(DIR_SRC)/%.c
	@if [ ! -d $(DIR_OBJ) ]; then echo "mkdir $(DIR_OBJ)"; mkdir $(DIR_OBJ); fi
	$(CC) -c $(CFLAGS) $(INCLUDE) $< -o $@

$(DIR_OBJ)/%.o: $(DIR_SRC)/%.cpp
	@if [ ! -d $(DIR_OBJ) ]; then echo "mkdir $(DIR_OBJ)"; mkdir $(DIR_OBJ); fi
	$(G++) -c $(CFLAGS) $(INCLUDE) $< -o $@

# 依存関係ファイルの読み込み
-include $(DIR_OBJ)/*.d

# プログラム毎に生成ルールを記述
pilot: $(OBJS_RUN) $(OBJS_CAP) $(OBJS_NUM) $(OBJS_SVR) $(OBJS_POS) $(OBJS_SOC) $(DIR_OBJ)/pilot.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_io: $(OBJS_RUN) $(DIR_OBJ)/test_io.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_uss: $(OBJS_RUN) $(DIR_OBJ)/test_uss.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_request: $(OBJS_RUN) $(DIR_OBJ)/test_request.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_direction: $(OBJS_RUN) $(DIR_OBJ)/test_direction.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_capture: $(OBJS_CAP) $(DIR_OBJ)/test_capture.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_number: $(OBJS_CAP) $(OBJS_NUM) $(DIR_OBJ)/test_number.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_dir_num: $(OBJS_RUN) $(OBJS_CAP) $(OBJS_NUM) $(DIR_OBJ)/test_dir_num.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_server: $(OBJS_SVR) $(DIR_OBJ)/test_server.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_position: $(OBJS_POS) $(DIR_OBJ)/test_position.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_camera: $(DIR_OBJ)/test_camera.o
	$(CC) $^ -o $@ $(LDFLAGS)

test_socket: $(OBJS_SOC) $(DIR_OBJ)/test_socket.o
	$(CC) $^ -o $@

test_keyboard: $(OBJS_RUN) $(OBJS_KEY) $(OBJS_SOC) $(DIR_OBJ)/test_keyboard.o
	$(CC) $^ -o $@ $(LDFLAGS)