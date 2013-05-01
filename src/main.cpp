#include <iostream>
using std::cout;
using std::endl;

#include "MiniCheese/Board.h"

int main() {
    auto str_rep = \
    "1 W\n"
    "kqbnr\n"
    "ppppp\n"
    ".....\n"
    "..P..\n"
    "PP.PP\n"
    "RNBQK\n";

    Board b(str_rep);

    cout << b.toString() << endl;
    cout << "score: " + std::to_string(b.score()) << endl;

    getchar();
    return 0;
}