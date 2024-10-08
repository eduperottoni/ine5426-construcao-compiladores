#ifndef LEXICAL_H
#define LEXICAL_H

#include <iostream>
using namespace std;

class Token{
public:
    enum TokenType{
        IDENT,
        NI,
        NPF,
        OTHER
    };

    string value;
    TokenType type;
};

#endif