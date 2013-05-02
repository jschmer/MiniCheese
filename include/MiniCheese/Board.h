#pragma once

#include <string>
#include <map>
#include <vector>
#include <tuple>
#include <stack>

#include "MiniCheese/Move.h"

class Board
{
public:
    static const std::string colors, pieces;
    static const std::map<char, int> piece_values;
    static const int bonus_score_per_step_pawn, bonus_score_rest_pieces;
    static const std::vector<Pos2D>  positions;
    static const std::locale locale; // for isupper function

public:
    Board(std::string str_rep = "");
    ~Board();

    std::string toString() const;
    int score() const;

    std::vector<Move> legal_moves() const;
    char move(Move move);
    void undo_last_move();

private:
    void _load_board(std::string str_rep);
    void set(Pos2D pos, char piece);
    char at(Pos2D pos) const;


    bool is_own_piece(char piece) const;
    bool is_within_bounds(Pos2D pos) const;
    // void fields() const;

    int _bonus_score(Pos2D pos, char piece) const;
    int _calc_score() const;
    
    // scanner
    void scan(std::vector<Move>& move_list,
              const Pos2D pos, short dx, short dy,
              bool only_capture = false,
              bool no_capture = false,
              bool one_step = false) const;

private:
    int  move_num;
    char turn;
    int  cur_score;
    std::vector<std::string> board;

    typedef std::tuple<std::pair<Pos2D, char>, std::pair<Pos2D, char>, int> HistoryEntry;
    // make_tuple(make_pair(Pos2D, char), make_pair(Pos2D, char), int)
    std::stack<HistoryEntry> history;
};

