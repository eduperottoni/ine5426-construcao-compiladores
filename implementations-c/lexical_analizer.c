#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

typedef enum {
    IDENT,
    OUTRO,
    NI,
    NPF
} TokenType;

typedef struct {
    TokenType type;
} Token;

const char LETTERS[53] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";
const char DIGITS[10] = "0123456789";
const char WS[3] = {'\t', ' ', '\n'};

unsigned int TOKEN_LIST_SIZE = 0;
unsigned int LEXIC_ANALYSIS_STAGE = 0;
Token *tokenList = NULL;
// char WS[3] = "\t"

unsigned int IDENTIFIER_CURRENT_STATE = 0;
unsigned int OTHER_CURRENT_STATE = 0;
unsigned int NUM_CURRENT_STATE = 17;


bool isLetter(char c) {
    for(int i = 0; i < 53; i++)
        if(c == LETTERS[i]) return true;
    return false;
}

bool isDigit(char c) {
    for(int i = 0; i < 10; i++)
        if(c == DIGITS[i]) return true;
    return false;
}

bool isWS(char c) {
    for(int i = 0; i < 3; i++)
        if(c == WS[i]) return true;
    return false;
}

void generateToken(TokenType type) {
    Token *t = realloc(tokenList, (TOKEN_LIST_SIZE + 1) * sizeof(Token));
    if (t == NULL) {
        // printf("Memory allocation failed\n");
        free(tokenList); // Free previously allocated memory if realloc fails
    }
    tokenList = t;
    // printf("COLOCANDO TOKEN DO TIPO %d\n", type);
    tokenList[TOKEN_LIST_SIZE].type = type;
    TOKEN_LIST_SIZE++;
}

/**
 * Função chamada em caso de falha em algum diagrama
 */
void fail(FILE* ptr) {
    // printf("fail\n");
    // Temos que voltar um caractere na entrada (vai ser lido pelo próximo diagrama)
    // fseek(ptr, -1, SEEK_CUR);
    LEXIC_ANALYSIS_STAGE++;
}


void getIdentifier(FILE* ptr) {
    // Lemos o próximo caractere de entrada
    char c;
    while(true) {
        if(IDENTIFIER_CURRENT_STATE != 2) c = fgetc(ptr);
        // printf("id-CHAR: %c\n", c);
        switch (IDENTIFIER_CURRENT_STATE) {
            case 0:
                if(isLetter(c)) IDENTIFIER_CURRENT_STATE = 1;
                else {
                    fseek(ptr, -1, SEEK_CUR);
                    return fail(ptr);
                }
                break;
            case 1:
                if(!isLetter(c) && !isDigit(c)) IDENTIFIER_CURRENT_STATE = 2;
                break;
            case 2:
                fseek(ptr, -1, SEEK_CUR);
                IDENTIFIER_CURRENT_STATE = 0;
                return generateToken(IDENT);
            default:
                break;
        }
    }
    // printf("Saimos");
}

void getNumber(FILE* ptr) {
    // Lemos o próximo caractere de entrada
    char c;
    NUM_CURRENT_STATE = 17;
    while(true) {
        // printf("1num-CHAR: %c\n", c);
        // printf("num-STATE: %d\n", NUM_CURRENT_STATE);
        if(NUM_CURRENT_STATE != 19 && NUM_CURRENT_STATE != 22 && NUM_CURRENT_STATE != 26) c = fgetc(ptr);
        // printf("2num-CHAR: %c\n", c);
        switch (NUM_CURRENT_STATE) {
            case 17:
                if(isDigit(c)) NUM_CURRENT_STATE = 18;
                else {
                    fseek(ptr, -1, SEEK_CUR);
                    return fail(ptr);
                }
                break;
            case 18:
                if(isDigit(c)) NUM_CURRENT_STATE = 18;
                else if (c == '.') NUM_CURRENT_STATE = 20;
                else if (c == 'E') NUM_CURRENT_STATE = 23;
                else NUM_CURRENT_STATE = 19;
                break;
            case 19:
                fseek(ptr, -1, SEEK_CUR);
                return generateToken(NI);
                break;
            case 20:
                if(isDigit(c)) NUM_CURRENT_STATE = 21;
                else return fail(ptr);
                break;
            case 21:
                if(isDigit(c)) NUM_CURRENT_STATE = 21;
                else if(c == 'E') NUM_CURRENT_STATE = 23;
                else NUM_CURRENT_STATE = 22;
                break;
            case 22:
                fseek(ptr, -1, SEEK_CUR);
                return generateToken(NPF);
                break;
            case 23:
                if(c == '+' || c == '-') NUM_CURRENT_STATE = 24;
                else if(isDigit(c)) NUM_CURRENT_STATE = 25;
                else return fail(ptr);
                break;
            case 24:
                if(isDigit(c)) NUM_CURRENT_STATE = 25;
                else return fail(ptr);
                break;
            case 25:
                if(isDigit(25)) NUM_CURRENT_STATE = 25;
                else NUM_CURRENT_STATE = 26;
                break;
            case 26:
                fseek(ptr, -1, SEEK_CUR);
                return generateToken(NPF);
                break;
            default:
                break;
        }
    }
    // printf("Saimos");
}

void getOther(FILE * ptr) {
    OTHER_CURRENT_STATE = 0;
    char c;
    while(true) {
        if(OTHER_CURRENT_STATE != 2) c = fgetc(ptr);
        // printf("other-CHAR: %d\n", c);
        // printf("other-state: %d", OTHER_CURRENT_STATE);
        switch (OTHER_CURRENT_STATE) {
            case 0:
                if(isLetter(c) || isDigit(c) || isWS(c)) {
                    fseek(ptr, -1, SEEK_CUR);
                    return fail(ptr);
                } else
                    OTHER_CURRENT_STATE = 1;
                break;
            case 1:
                fseek(ptr, -1, SEEK_CUR);
                return generateToken(OUTRO);
                break;
            default:
                break;
        }
    }
    // printf("Saimos");
}


void (*function_list[])(FILE*) = {getIdentifier};

int main() {
    FILE* ptr;
    ptr = fopen("input2.txt", "r");

    unsigned int numTokens = TOKEN_LIST_SIZE;
    while(true) {
        char c = fgetc(ptr);
        // printf("char: %c\n",c);
        if(c == EOF) break;
        // Ignoramos qualquer ocorrência de \b, \t ou \n
        if(isWS(c)) continue;

        fseek(ptr, -1, SEEK_CUR);
        // printf("VAMOS PESQUISAR POR: %c\n", c);
        getIdentifier(ptr);

        if(TOKEN_LIST_SIZE > numTokens) {
            // printf("Número de tokens: %u", TOKEN_LIST_SIZE);
            numTokens = TOKEN_LIST_SIZE;
            continue;
        }

        getNumber(ptr);

        if(TOKEN_LIST_SIZE > numTokens) {
            // printf("Número de tokens: %u", TOKEN_LIST_SIZE);
            numTokens = TOKEN_LIST_SIZE;
            continue;
        }

        // printf("OTHER\n");
        getOther(ptr);
    }

    // printf("TOKEN LIST %u\n", TOKEN_LIST_SIZE);

    for(int i = 0; i < TOKEN_LIST_SIZE; i++) {
        switch (tokenList[i].type) {
            case IDENT: 
                printf("%s\t", "IDENT");
                break;
            case OUTRO: 
                printf("%s\t", "OUTRO");
                break;
            case NI:
                printf("%s\t", "NI");
                break;
            case NPF:
                printf("%s\t", "NPF");
                break;
        }
    }
    printf("\n");

    fclose(ptr);
    return 0;
}