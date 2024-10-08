#ifndef LEXICAL_H
#define LEXICAL_H

#include <unordered_map>
#include <stdexcept>
#include "token.h"
using namespace std;

class InvalidCharacterException : public std::exception {
public:
    explicit InvalidCharacterException(char ch)
        : message("Character not found: " + string(1, ch)) {}

    const char* what() const noexcept override {
        return message.c_str();
    }

private:
    string message;
};

class LexicalAnalyzer {
private:
    enum charType {
        LETTER,
        DIGIT,
        WS,
    };

    unordered_map<char, charType> charTypeMap;

    bool isLetter(const char c);
    bool isDigit(const char c);
    bool isWS(const char c);

    charType findOnMap(const char c);

public:
    LexicalAnalyzer();

    void sayHello();

    void getIdentifier();
    void getNumber();
    void getOther();
};

#endif