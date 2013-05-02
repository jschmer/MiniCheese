#include "MiniCheese/Board.h"

#include <cctype> // isupper / islower

#include "MiniCheese/ScanArguments.h"
#include "MiniCheese/StringHelper.h"
#include "MiniCheese/Exceptions.h"

using std::string;
using std::vector;

using std::make_tuple;
using std::make_pair;
using std::get;

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
    for (int x = 1; x < 6; ++x)
        for (int y = 1; y < 7; ++y)
            tmp.emplace_back(x, y);
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

void Board::set(const Pos2D& pos, char piece) {
    assert(is_within_bounds(pos));

    auto& x = pos.first;
    auto& y = pos.second;

    //if piece in Board.pieces:
    //    self.board[pos[1]-1][pos[0]-1] = piece
    if (String::existIn(piece, Board::pieces))
        board[y-1][x-1] = piece;
}

char Board::at(const Pos2D& pos) const {
    assert(is_within_bounds(pos));
    
    auto& x = pos.first;
    auto& y = pos.second;
    
    // y is row index!
    return board[y-1][x-1] ;
}

char Board::move(const Move& move) {
    //old_piece_end = self.at(move.end)
    //new_piece_end = piece_start = self.at(move.start)
    //new_score = self.cur_score

    auto old_piece_end = at(move.end);
    auto new_piece_end = at(move.start);
    auto piece_start = new_piece_end;
    auto new_score = cur_score;

    //# pawn promotion
    //if new_piece_end == 'p' and move.end[1] == 1:
    if (new_piece_end == 'p' && move.end.second == 1) {
    //    assert self.turn == 'B'
        assert(turn == 'B');

    //    new_piece_end = 'q'
    //    new_score -= Board.piece_values['p']
    //    new_score += Board.piece_values['q']
        new_piece_end = 'q';
        new_score -= Board::piece_values.at('p');
        new_score += Board::piece_values.at('q');
    }
    //elif new_piece_end == 'P' and move.end[1] == 6:
    else if (new_piece_end == 'P' && move.end.second == 6) {
    //    assert self.turn == 'W'
        assert(turn == 'W');
    //    new_piece_end = 'Q'
    //    new_score -= Board.piece_values['P']
    //    new_score += Board.piece_values['Q']
        new_piece_end = 'Q';
        new_score -= Board::piece_values.at('P');
        new_score += Board::piece_values.at('Q');
    }

    //new_score -= Board.piece_values[old_piece_end]
    new_score -= Board::piece_values.at(old_piece_end);
    //self.set(move.end, new_piece_end)
    //self.set(move.start, '.')
    set(move.end, new_piece_end);
    set(move.start, '.');

    //# remove bonus score of start piece
    //new_score -= self._bonus_score(move.start, piece_start)
    new_score -= _bonus_score(move.start, piece_start);

    //# remove bonus score of captured piece
    //new_score -= self._bonus_score(move.end, old_piece_end)
    new_score -= _bonus_score(move.end, old_piece_end);

    //# add bonus score of end piece
    //new_score += self._bonus_score(move.end, new_piece_end)
    new_score += _bonus_score(move.end, new_piece_end);

    //if self.turn == "W":
    //    self.turn = "B"
    if (turn == 'W') {
        turn = 'B';
    }
    //else:
    else {
    //    self.move_num += 1
    //    self.turn = "W"
        ++move_num;
        turn = 'W';
    }

    char result = '?';

    //# king capture and result
    //if old_piece_end == 'k':
    if (old_piece_end == 'k') {
    //    result = 'W'
    //    new_score = 100000
        result = 'W';
        new_score = 100000;
    }
    //elif old_piece_end == 'K':
    else if (old_piece_end == 'K') {
    //    result = 'B'
    //    new_score = -100000
        result = 'B';
        new_score = -100000;
    }
    //elif self.move_num == 41:
    else if (move_num == 41) {
    //    result = '='
    //    new_score = 0
        result = '=';
        new_score = 0;
    }

    //# save old state to be able to undo it later
    //# ((startpos, startpiece), (endpos, endpiece), score)
    //# if self._calc_score() != new_score:
    //#     print("calc_score:", self._calc_score(), "new_score:")
    //#     print("Wtf")
    //self.history.append(((move.start, piece_start), (move.end, old_piece_end), self.cur_score))
    history.emplace(make_tuple(make_pair(move.start, piece_start), make_pair(move.end, old_piece_end), cur_score));

    //self.cur_score = new_score
    cur_score = new_score;
    //return result
    return result;
}

int Board::score_after(Move move) const {
    //score = self.cur_score
    //turn = self.turn
    //move_num = self.move_num

    auto t_score = cur_score;
    auto t_turn = turn;
    auto t_move_num = move_num;

    //old_piece_end = self.at(move.end)
    //new_piece_end = piece_start = self.at(move.start)
    auto old_piece_end = at(move.end);
    auto new_piece_end = at(move.start);
    auto piece_start = new_piece_end;

    //# pawn promotion
    //if new_piece_end == 'p' and move.end[1] == 1:
    if (new_piece_end == 'p' && move.end.second == 1) {
    //    assert self.turn == 'B'
        assert(turn == 'B');

    //    new_piece_end = 'q'
    //    new_score -= Board.piece_values['p']
    //    new_score += Board.piece_values['q']
        new_piece_end = 'q';
        t_score -= Board::piece_values.at('p');
        t_score += Board::piece_values.at('q');
    }
    //elif new_piece_end == 'P' and move.end[1] == 6:
    else if (new_piece_end == 'P' && move.end.second == 6) {
    //    assert self.turn == 'W'
        assert(turn == 'W');
    //    new_piece_end = 'Q'
    //    new_score -= Board.piece_values['P']
    //    new_score += Board.piece_values['Q']
        new_piece_end = 'Q';
        t_score -= Board::piece_values.at('P');
        t_score += Board::piece_values.at('Q');
    }

    //new_score -= Board.piece_values[old_piece_end]
    t_score -= Board::piece_values.at(old_piece_end);

    //# remove bonus score of start piece
    //new_score -= self._bonus_score(move.start, piece_start)
    t_score -= _bonus_score(move.start, piece_start);

    //# remove bonus score of captured piece
    //new_score -= self._bonus_score(move.end, old_piece_end)
    t_score -= _bonus_score(move.end, old_piece_end);

    //# add bonus score of end piece
    //new_score += self._bonus_score(move.end, new_piece_end)
    t_score += _bonus_score(move.end, new_piece_end);

    //if turn == "W":
    if (t_turn == 'W')
    //    turn = "B"
        t_turn = 'B';
    //else:
    else {
    //    move_num += 1
    //    turn = "W"
        ++t_move_num;
        t_turn = 'W';
    }

    //# king capture and result
    //if old_piece_end == 'k':
    if (old_piece_end == 'k') {
    //    new_score = 100000
        t_score = 100000;
    }
    //elif old_piece_end == 'K':
    else if (old_piece_end == 'K') {
    //    new_score = -100000
        t_score = -100000;
    }
    //elif self.move_num == 41:
    else if (move_num == 41) {
    //    new_score = 0
        t_score = 0;
    }

    //return score if turn == "W" else -score
    return t_turn == 'W' ? t_score : -t_score;
}

void Board::undo_last_move() {
    //# change turn and move_num
    //if self.turn == "W":
    if (turn == 'W') {
    //    self.move_num -= 1
    //    self.turn = "B"
        move_num -= 1;
        turn = 'B';
    }
    //else:
    else {
    //    self.turn = "W"
        turn = 'W';
    }

    //assert self.history
    //last_move = self.history.pop()
    auto last_move = history.top();
    history.pop();

    auto& start = get<0>(last_move);
    auto& end   = get<1>(last_move);
    auto& score = get<2>(last_move);

    //# ((startpos, startpiece), (endpos, endpiece), score)
    //self.set(last_move[0][0], last_move[0][1])
    set(start.first, start.second);
    //self.set(last_move[1][0], last_move[1][1])
    set(end.first, end.second);
    //self.cur_score = last_move[2]
    cur_score = score;
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

bool Board::is_within_bounds(const Pos2D& pos) const {
    auto& col = pos.first;
    auto& row = pos.second;

    // if pos[0] < 1 or pos[0] > 5:
    //   return False
    if (col < 1 || col > 5)
        return false;
    // if pos[1] < 1 or pos[1] > 6:
    //   return False
    if (row < 1 || row > 6)
        return false;

    // return True
    return true;
}

// void fields() const {}

int Board::_bonus_score(const Pos2D& pos, char piece) const {
    auto& x = pos.first;  // col index
    auto& y = pos.second; // row index

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
            const Pos2D pos, short dx, short dy,
            bool only_capture,
            bool no_capture,
            bool one_step) const
{
    //assert isinstance(pos, tuple)
    //newpos = pos
    auto newpos = pos;

    //while True:
    while (true) {
    //    newpos = (newpos[0] + dx, newpos[1] + dy)
        newpos.first  += dx;
        newpos.second += dy;
    //    if not self.is_within_bounds(newpos):
    //        break

        if (!is_within_bounds(newpos))
            break;

    //    piece = self.at(newpos)
        auto piece = at(newpos);

    //    if only_capture:
        if (only_capture) {
    //        # pawn bastard
    //        if piece == '.': break
            if (piece == '.') break;
    //        elif self.is_own_piece(piece): break
            else if (is_own_piece(piece)) break;
    //        else: 
    //            move_list.append(Move(pos, newpos))
    //            break
            else {
                move_list.emplace_back(pos, newpos);
                break;
            }
        }
    //    else:
        else {
    //        # everything else
    //        if piece == '.':
    //            # legal move
    //            move_list.append(Move(pos, newpos))
            if (piece == '.')
                move_list.emplace_back(pos, newpos);
    //        elif self.is_own_piece(piece):
    //            # collision with own piece
    //            break
            else if (is_own_piece(piece))
                break;
    //        else:
            else {
    //            if no_capture == False:
    //                # capture enemy piece
    //                move_list.append(Move(pos, newpos))
                if (no_capture == false)
                    move_list.emplace_back(pos, newpos);
    //            break
                break;
            }
        }

    //    if one_step:
    //        break
        if (one_step)
            break;
    }
}

std::vector<Move> Board::legal_moves() const {
    //legal_moves = []
    std::vector<Move> legal_moves;

    for (auto& pos : Board::positions) {
    //for row in range(1, 7):
    //    for col in range(1, 6):
    //        position = (col, row)
    //        field = self.at(position)
        auto piece = at(pos);
    //        if not field in ['#', '.'] and self.is_own_piece(field):
        if (!String::existIn(piece, "#.") && is_own_piece(piece)) {
    //            possible_piece_moves = moves_for[field]
            auto& possible_piece_moves = scan_arguments_for[piece];
    //            for move in possible_piece_moves:
            for (auto& sa : possible_piece_moves) {
    //                self.scan(legal_moves, position, *move)
                scan(legal_moves, pos, get<0>(sa), get<1>(sa), get<2>(sa), get<3>(sa), get<4>(sa));
            }
        }
    }

    //return legal_moves
    return legal_moves;
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
