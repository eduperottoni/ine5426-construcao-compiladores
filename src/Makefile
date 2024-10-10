# Compiler and flags
CXX = g++
CXXFLAGS = -Wall -g -std=c++11

# Output executable
TARGET = main
TEST_TARGET = test_lexical_analyzer
GTEST_LIBS = -lgtest -lgtest_main -pthread

# Source files
SRCS = main.cpp lexical_analyzer.cpp
TEST_SRCS =  lexical_analyzer.cpp lexical_analyzer_test.cpp

# Object files (replace .cpp with .o)
OBJS = $(SRCS:.cpp=.o)

# Default target to build the executable
all: $(TARGET)

# Rule to link the object files and create the executable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Rule to compile the .cpp files into .o object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean target to remove the executable and object files
clean:
	rm -f $(OBJS) $(TARGET)

# Run the program after building it
run: all
	./$(TARGET)

# Build the tests
$(TEST_TARGET): $(TEST_SRCS)
	$(CXX) $(CXXFLAGS) $(TEST_SRCS) $(GTEST_LIBS) -o $(TEST_TARGET)

# Run tests
tests: $(TEST_TARGET)
	./$(TEST_TARGET)
