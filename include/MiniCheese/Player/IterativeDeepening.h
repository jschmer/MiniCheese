#pragma once

#include <utility>
#include <chrono>

#include "MiniCheese/Move.h"
#include "MiniCheese/Board.h"

class IterativeDeepeningPlayer
{
public:
    IterativeDeepeningPlayer();
    ~IterativeDeepeningPlayer();

    Move generate_move(const Board& board);

private:
    std::pair<long, Move> negamax(Board& board, int max_depth, long alpha, long beta);

private:
    long long node_count;
    long long match_duration, time_spent;
    std::chrono::high_resolution_clock::time_point end_time;
};

