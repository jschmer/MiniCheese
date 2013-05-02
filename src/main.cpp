#include <iostream>
using std::cout;
using std::endl;

#include "MiniCheese/Board.h"

int main() {
    auto str_rep = \
    "1 W\n"
    "kqbn.\n"
    ".pppP\n"
    ".....\n"
    ".....\n"
    "pPPP.\n"
    ".NBQK\n";

    Board b(str_rep);

    cout << b.toString() << endl;
    cout << "score: " + std::to_string(b.score()) << endl;

    auto move = b.legal_moves();

    Move m = parseMove("e5-e6");
    cout << "move: " << b.move(m) << endl << endl;

    cout << b.toString() << endl;
    cout << "score: " + std::to_string(b.score()) << endl << endl;

    b.undo_last_move();

    cout << b.toString() << endl;
    cout << "score: " + std::to_string(b.score()) << endl;

    getchar();
    return 0;
}