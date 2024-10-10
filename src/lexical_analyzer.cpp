#include "lexical_analizer.h"
#include <iostream>

using namespace std;

void LexicalAnalyzer::sayHello() {
    cout << "Hello from LexicalAnalyser" << endl;
    cout << findOnMap('\t') << endl;
}

LexicalAnalyzer::LexicalAnalyzer() {
    // Fill map with letters (A-Z, a-z)
    for (char c = 'A'; c <= 'Z'; ++c) {
        charTypeMap[c] = LETTER;
        charTypeMap[c + 32] = LETTER;  // add lowercase letters
    }
    // Fill map with digits
    for (char c = '0'; c <= 9; ++c) {
        charTypeMap[c] = DIGIT;
    }

    charTypeMap[' '] = WS;
    charTypeMap['\t'] = WS;
    charTypeMap['\n'] = WS;
}

bool LexicalAnalyzer::isLetter(const char c) {
    return findOnMap(c) == LETTER;
}

bool LexicalAnalyzer::isDigit(const char c) {
    return findOnMap(c) == DIGIT;
}

bool LexicalAnalyzer::isWS(const char c) {
    return isWS(c) == WS;
}

LexicalAnalyzer::charType LexicalAnalyzer::findOnMap(const char c) {
    auto it = charTypeMap.find(c);
    cout << "Tamanho do mapa: " << charTypeMap.size() << endl;
    if (it != charTypeMap.end())
        return it->second;
    else
        throw InvalidCharacterException(c);
}