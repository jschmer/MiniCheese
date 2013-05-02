#pragma once
#include <utility>
#include <string>

#include <Common.h>

// Pos2D coordinates begin at 1!
typedef std::pair<uint, uint> Pos2D;

class Move;

std::string posToString(Pos2D pos);
Pos2D parsePosition(std::string str);
Move parseMove(std::string str);

class Move
{
public:
    static const std::string cols, rows;

    Pos2D start, end;

    Move();
    Move(Pos2D, Pos2D);
    ~Move();

    std::string toString() const;      
    bool operator==(const Move &rhs);
};