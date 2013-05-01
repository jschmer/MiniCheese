#include <iostream>
using std::cout;
using std::endl;

#include <MiniCheese/Move.h>
#include <MiniCheese/Exceptions.h>

#include <MiniCheese/ScanArguments.h>

int main() {
    scan_arguments;

    Move m(Pos2D(1, 1), Pos2D(2, 2));
    Move m2(Pos2D(1, 1), Pos2D(2, 2));

    try {
        cout << m.toString() << endl;
        cout << parseMove("a1-e6").toString() << endl;
        cout << ((m == m2) ? "true" : "false") << endl;
    } catch (ValueError &e) {
        cout << e.what() << endl;
    }

    getchar();
    return 0;
}