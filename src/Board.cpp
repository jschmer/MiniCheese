#include "MiniCheese/Board.h"

#include <cctype> // isupper / islower

#include "MiniCheese/ScanArguments.h"
#include "MiniCheese/StringHelper.h"
#include "MiniCheese/Exceptions.h"

using std::string;
using std::vector;

//
// Board statics
const string Board::colors = "BW",
             Board::pieces = "kqbnrpKQBNRP.";

const int Board::bonus_score_per_step_pawn = 20;
const int Board::bonus_score_rest_pieces   = 10;
const std::locale Board::locale;

// init piece values
const std::map<char, int> Board::piece_values = [](){
    std::map<char, int> tmp;
    tmp['k'] = -100000;
    tmp['q'] = -800;
    tmp['b'] = -300;
    tmp['n'] = -250;
    tmp['r'] = -400;
    tmp['p'] = -125;
    tmp['K'] = 100000;
    tmp['Q'] = 800;
    tmp['B'] = 300;
    tmp['N'] = 250;
    tmp['R'] = 400;
    tmp['P'] = 125;
    tmp['.'] = 0;
    return tmp;
}();

const std::vector<Pos2D> Board::positions = []() {
    std::vector<Pos2D> tmp;
    for (int x = 1; x < 7; ++x)
        for (int y = 1; y < 6; ++y)
            tmp.push_back(Pos2D(x, y));
    return tmp;
}();

//
// Board class
Board::Board(string str_rep)
    : move_num(1),
      turn('W'),
      cur_score(0),
      board(),
      history()
{
    if (str_rep.length() == 0) {
        str_rep = \
            "1 W\n"
            "kqbnr\n"
            "ppppp\n"
            ".....\n"
            ".....\n"
            "PPPPP\n"
            "RNBQK\n";
    }

    _load_board(str_rep);
    cur_score = _calc_score();
}

Board::~Board()
{
}

void Board::_load_board(std::string str_rep) {
    //# strip newlines at beginning and end
    //lines = str_rep.strip().split("\n")
    auto lines = String::split(String::trim(str_rep), '\n');

    //if len(lines) != 7:
    //    raise ValueError("Invalid board size")
    if (lines.size() != 7)
        throw ValueError("Invalid board size");

    auto spl = String::split(lines[0], ' ');
    //move_num, turn = lines[0].split(" ")
    //self.move_num = int(move_num)
    //self.turn = turn
    move_num = std::atoi(spl[0].c_str());
    turn = spl[1].c_str()[0];

    //if self.turn not in Board.colors:
    //    raise ValueError("Invalid turn")
    if (!String::existIn(turn, Board::colors))
        throw ValueError("Invalid turn");

    //for line in lines[1:]:
    for (auto& line : vector<string>(lines.begin()+1, lines.end())) {
        // line = line.strip()
        line = String::trim(line);

        // if len(line) != 5:
        // raise ValueError("Invalid line size")
        if (line.length() != 5)
            throw ValueError("Invalid line size");

        // for char in line:
        for (auto& c : line) {
            // if char not in self.pieces:
                // raise ValueError("Invalid piece")
            if (!String::existIn(c, Board::pieces))
                throw ValueError("Invalid piece");
        }
        // self.board.append(list(line))
        // void insert (iterator position, InputIterator first, InputIterator last);
        board.push_back(line);
    }

    //self.board.reverse()
    std::reverse(board.begin(),board.end()); 
}

void Board::set(Pos2D pos, char piece) {
    assert(is_within_bounds(pos));

    auto& x = pos.first;
    auto& y = pos.second;

    //if piece in Board.pieces:
    //    self.board[pos[1]-1][pos[0]-1] = piece
    if (String::existIn(piece, Board::pieces))
        board[x-1][y-1] = piece;
}

char Board::at(Pos2D pos) const {
    assert(is_within_bounds(pos));
    
    auto& x = pos.first;
    auto& y = pos.second;
    
    return board[x-1][y-1] ;
}

char Board::move(Move move) {
    assert(false);
    return 'c';
}

void Board::undo_last_move() {
    assert(false);
}

bool Board::is_own_piece(char piece) const {
    //if not c in Board.pieces:
    //    assert False
    assert(String::existIn(piece, Board::pieces));

    //if c.isupper():
    //    return self.turn == "W"
    if (isupper(piece))
        return turn == 'W';
    //elif c.islower():
    //    return self.turn == "B"
    else if (islower(piece))
        return turn == 'B';
    //else:
    //    assert False
    assert(false);
    return false;
}

bool Board::is_within_bounds(Pos2D pos) const {
    auto& x = pos.first;
    auto& y = pos.second;

    // if pos[0] < 1 or pos[0] > 5:
    //   return False
    if (x < 1 || x > 5)
        return false;
    // if pos[1] < 1 or pos[1] > 6:
    //   return False
    if (y < 1 || y > 6)
        return false;

    // return True
    return true;
}

// void fields() const {}

int Board::_bonus_score(Pos2D pos, char piece) const {
    auto& y = pos.first;  // row index
    auto& x = pos.second; // column index

    //if piece == '.': return 0
    if (piece == '.')
        return 0;

    //whites_piece = piece.isupper()
    bool whites_piece = std::isupper(piece, Board::locale);

    int distance = 0;
    //if whites_piece:
    //    # how far is this piece from its baseline?
    //    distance = pos[1] - 1
    if (whites_piece)
        distance = y - 1;
    //else:
    //    distance = 6 - pos[1]
    else
        distance = 6 - y;

    //bonus = 0
    int bonus = 0;

    //p = piece.lower()
    char p = tolower(piece);

    //if p == 'p':
    //    # pawn
    //    bonus = distance * 20
    if (p == 'p')
        bonus = distance * Board::bonus_score_per_step_pawn;
    //else:
    //    # everything except king
    //    if distance > 0:
    //        bonus = 10
    else
        if (distance > 0)
            bonus = Board::bonus_score_rest_pieces;

    //if whites_piece: return bonus
    //else: return -bonus
    if (whites_piece)
        return bonus;
    else
        return -bonus;
}

int Board::_calc_score() const {
    //score = 0
    int score = 0;
    //black_king_found = False
    //white_king_found = False
    bool black_king_found = false, white_king_found = false;

    //for pos in self.positions():
    for (auto& pos : Board::positions) {
    //    piece = self.at(pos)
        auto piece = at(pos);

    //    if piece == 'k':
    //        black_king_found = True
        if (piece == 'k')
            black_king_found = true;
    //    elif piece == 'K':
    //        white_king_found = True
        if (piece == 'K')
            white_king_found = true;

    //    score += Board.piece_values[piece]
    //    score += self._bonus_score(pos, piece)
        score += Board::piece_values.at(piece);
        score += _bonus_score(pos, piece);
    }

    //if not black_king_found:
    //    score = 100000
    if (!black_king_found)
        score = 100000;
    //if not white_king_found:
    //    score = -100000
    if (!white_king_found)
        score = -100000;
    //if self.move_num == 41:
    //    score = 0
    if (move_num == 41)
        score = 0;

    //return score
    return score;
}

int Board::score() const {
    return turn == 'W' ? cur_score : -cur_score;
}


// scanner
void Board::scan(std::vector<Move>& move_list,
            Pos2D pos, short dx, short dy,
            bool only_capture,
            bool no_capture,
            bool one_step) const
{
    assert(false);
}

std::vector<Move> Board::legal_moves() const {
    assert(false);
    return std::vector<Move>();
}

    
std::string Board::toString() const {
    //result = []
    //result.append("{} {}".format(self.move_num, self.turn))
    string result;
    result += (std::to_string(move_num) + ' ' + turn + '\n');

    //for line in reversed(self.board):
    //    result.append("".join(line))
    auto reversed_board = board;
    std::reverse(reversed_board.begin(), reversed_board.end()); 

    for (auto& line : reversed_board) {
        result += line + "\n";
    }

    //return "\n".join(result)
    return result;
}
