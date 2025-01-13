CXX = clang++
CXXFLAGS = -std=c++20 -O3 -Wall
DEBUG = -DDEBUG

BIN_DIR = ./bin
SRC = main.cpp
OUT = $(BIN_DIR)/main

build:
	@mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $(OUT) $(SRC)

debug:
	@mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $(OUT) $(SRC)

run:
	@$(OUT)

clean:
	@rm -rf $(BIN_DIR)
