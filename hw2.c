#include <iostream>
using namespace std;

int main() {

    int Nk = 4;
    int Nr = 10;

    char plaintext[] = "00112233445566778899aabbccddeeff";
    char keyone[] = "000102030405060708090a0b0c0d0e0f";

    cipher(key, plaintext);


    Nk = 6;
    Nr = 12;

    char keytwo[] = "000102030405060708090a0b0c0d0e0f1011121314151617";

    cipher(key, plaintext);

    Nk = 8;
    Nr = 14;

    char keythree[] = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f";

    cipher(key, plaintext);
    return 0;
}

void Cipher (uint8_t[] in[], uint8_t out[], uint16_t w[]) {
    uint8_t state[4][Nb];
    state = in;
    AddRoundKey(state, uint16_t[0, Nb-1]);
    for (int round = 0; round < Nr-1; round++) {
        SubBytes(state);
        ShiftRows(state);
        MixColumns(state);
        AddRoundKey(state, uint16_t[round* Nb][(round+1)*(Nb-1)]);
    }

    SubBytes(state);
    ShiftRows(state);
    AddRoundKey(state, uint16_t[Nr*Nb][(Nr+1)*(Nb-1)]);
    return out;
}

void KeyExpansion(uint8_t key[], uint16_t w[], unsigned Nk) {
    uint16_t temp;
    int i = 0;
    while(i < Nk) {
        w[i] = uint16_t(key[4*i], key[4*i+2], key[4*i+3]);
        i++;
    }

    i = Nk;
    while( i < Nb * (Nr + 1)){
        temp = w[i-1];
        if ( i % Nk == 0) {
            temp = SubWord(RotWord(temp)) ^ Rcon[i/Nk];
        } else if (Nk > 6 && i % Nk == 4) {
            temp = SubWord(temp);
        } else {
            w[i] == w[i-Nk] ^ temp
        }
        i++;
    }
}

uint8_t xtime(word) {
    if (word & 0x80) {
        return ffAdd((word << 1), 0x11b);
    }
    return word << 1;
}

uint8_t ffAdd(a, b) {
    return a ^ b;
}

uint8_t ffMultiply(a, b) {
    uint8_t answer = 0;
    
}