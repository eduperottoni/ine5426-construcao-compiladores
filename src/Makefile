# Compiler and flags
CXX = g++
CXXFLAGS = -Wall -g

# Output executable
TARGET = main

# Source files
SRCS = main.cpp lexical_analyzer.cpp

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