#include <iostream>
using std::cout;
using std::endl;

#include "MiniCheese/Board.h"
#include "MiniCheese/Player/IterativeDeepening.h"

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
    cout << "\nScore after move: " << b.score_after(m) << endl << endl;

    cout << "move: " << b.move(m) << endl << endl;

    cout << b.toString() << endl;
    cout << "score: " + std::to_string(b.score()) << endl << endl;

    b.undo_last_move();

    cout << b.toString() << endl;
    cout << "score: " + std::to_string(b.score()) << endl;


    Board game;
    IterativeDeepeningPlayer p;

    auto moveasd = p.generate_move(game);
    printf("Best move: %s\n", moveasd.toString().c_str());

    getchar();
    return 0;
}