#include "MiniCheese/Move.h"

#include "MiniCheese/Exceptions.h"
#include "MiniCheese/StringHelper.h"

using std::string;

//
// free standing functions
std::string posToString(Pos2D pos) {
    char buf[32];
    sprintf_s(buf, "%d", pos.second);

    return Move::cols.at(pos.first-1) + string(buf);
}

Pos2D parsePosition(std::string str) {
    using String::existIn;

    if (str.length() > 2) throw ValueError("Too much position information");
    if (!existIn(str[0], Move::cols)) throw ValueError("Wrong column index");
    if (!existIn(str[1], Move::rows)) throw ValueError("Wrong row index");

    auto x = Move::cols.find(str[0]) + 1;
    auto y = atoi(&str[1]);
    return Pos2D(x, y);
}

Move parseMove(std::string str) {
    auto idx = str.find("-");
    if (str.length() != 5 || idx == std::string::npos)
        throw ValueError(str + " is not a valid move string!");

    return Move(parsePosition(str.substr(0, 2)), parsePosition(str.substr(3, 2)));
}

//
// class Move
const string Move::cols = "abcde",
             Move::rows = "123456";

Move::Move(Pos2D start, Pos2D end)
    : start(start), end(end)
{
}

Move::~Move()
{
}

std::string Move::toString() const {
    return posToString(start) + "-" + posToString(end);
}

bool Move::operator==(const Move &rhs) {
    return start == rhs.start && end == rhs.end;
}