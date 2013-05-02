#include "MiniCheese/Player/IterativeDeepening.h"

#include <algorithm>

#include "MiniCheese/Exceptions.h"
#include "MiniCheese/StringHelper.h"

using namespace std::chrono;
using std::make_pair;

IterativeDeepeningPlayer::IterativeDeepeningPlayer()
    : match_duration(295),
    time_spent(0),
    node_count(0)
{
}

IterativeDeepeningPlayer::~IterativeDeepeningPlayer()
{
}

Move IterativeDeepeningPlayer::generate_move(const Board& board) {
    //move_start_time = time()
    auto move_start_time = high_resolution_clock::now();

    //# time_left = duration - time_spent
    //time_left = self.match_duration (seconds) - self.time_spent (seconds)
    auto time_left = match_duration - time_spent;

    //max_move_time = time_left / (41 - game.move_num + 1)
    auto max_move_time = (time_left / (41 - board.get_move_num() + 1.0)) - .5;
    max_move_time *= 1000;
    milliseconds s(static_cast<int>(max_move_time));

    //self.end_time = time() + max_move_time - 0.5
    end_time = high_resolution_clock::now() + s;

    //print("time_left:", time_left)
    //print("max_move_time:", max_move_time)
    printf("time_left: %ds\n", time_left);
    printf("max_move_time: %fs\n", s.count()/1000.0);

    //# negamax could end up corrupting the board so
    //# copy the game board for every negamax iteration
    //game_copy = Board.from_other(game)
    auto game_copy = Board(board);

    //# alpha-beta values
    //a = -500000
    //b = -a
    long a = -500000;
    long b = -a;

    //depth = 2
    //self.node_count = 0
    auto depth = 2;
    node_count = 0;
    //shallow_value, shallow_move = self.negamax(game_copy, 1, a, b)
    auto res = negamax(game_copy, 1, a, b);
    auto& shallow_value = res.first;
    auto& shallow_move  = res.second;

    // dummy refs
    auto& deeper_value = res.first;
    auto& deeper_move  = res.second;

    //while True:
    while (true) {
    //    # negamax could end up corrupting the board so
    //    # copy the game board for every negamax iteration
    //    game_copy = Board.from_other(game)
        game_copy = Board(board);

    //    try:
        try {
    //        deeper_value, deeper_move = self.negamax(game_copy, depth, a, b)
            res = negamax(game_copy, depth, a, b);
            deeper_value = res.first;
            deeper_move  = res.second;
        }
    //    except TimeUpError:
        catch(TimeUpError) {
    //        # time expired
    //        # returns the shallow move
    //        break
            break;
        }
    //    if not depth > 20:
    //        print("D:", depth, "-", "Value for", deeper_move, "=", deeper_value)
        if (depth <= 20)
            printf("D: %d - Value for %s = %d\n", depth, deeper_move.toString().c_str(), deeper_value);

    //    # handle game end conditions
    //    if deeper_value >= 100000:
        if (deeper_value >= 100000) {
    //        # found win
    //        print("found win")
            printf("Found a win! \\o/\n");
    //        shallow_move = deeper_move
            shallow_move = deeper_move;
    //        break
            break;
        }

    //    # TODO: handle draw!
    //    elif deeper_value <= -100000:
        else if (deeper_value <= -100000) {
    //        # found draw or loss
    //        print("found loss")
            printf("Found a los! :'(\n");
    //        # return previous move which didn't find a loss or draw
    //        # which guarantees a loss in at least depth-1 moves
    //        # returns shallow_move
    //        break
            break;
        }

    //    shallow_move = deeper_move
    //    shallow_value = deeper_value
        shallow_move  = deeper_move;
        shallow_value = deeper_value;
    //    depth += 1
        ++depth;
    }

    //self.time_spent += time() - move_start_time
    auto spent = duration_cast<milliseconds>((high_resolution_clock::now() - move_start_time)).count();
    printf("Spent time: %fs\n", spent/1000.0);
    time_spent += spent;

    //return shallow_move
    return shallow_move;
}

std::pair<long, Move> IterativeDeepeningPlayer::negamax(Board& board, int max_depth, long alpha, long beta) {
    //# base case
    //if max_depth <= 0:
    //    return (state.score(), None)
    if (max_depth <= 0)
        return make_pair(board.score(), Move());

    //# check time
    //if self.node_count % 1000 == 0:
    //    # update time left
    //    if time() > self.end_time:
    //        raise TimeUpError()
    if (node_count % 10000 == 0) {
        if (high_resolution_clock::now() > end_time)
            throw TimeUpError();
    }

    //self.node_count += 1
    ++node_count;

    //# recursive case
    //legal_moves = state.legal_moves()
    auto legal_moves = board.legal_moves();

    //    
    //# pre sort the moves! best first!
    //sorted_moves = []
    std::vector<std::pair<int, Move>> sorted_moves;

    //for move in legal_moves:
    for (auto& move : legal_moves) {
    //    score = state.score_after(move)
        auto score = board.score_after(move);
    //    sorted_moves.append((score, move))
        sorted_moves.emplace_back(make_pair(score, move));
    }

    //# sort the moves on their score
    //sorted_moves = sorted(sorted_moves, key=lambda t: t[0])
    std::sort(sorted_moves.begin(), sorted_moves.end(), [](std::pair<int, Move>& lhs, std::pair<int, Move>& rhs) {
        return lhs.first < rhs.first;
    });

    //best_value = -sys.maxsize
    auto best_value = LONG_MIN;
    Move best_move;

    //for value, move in sorted_moves:
    for (auto& pair : sorted_moves) {
        auto& move = pair.second;
        auto value = pair.first;

    //    result = state.move(move)
        auto result = board.move(move);

    //    if result in ('W','B'):
        if (String::existIn(result, "WB")) {
    //        value = -state.score()
            value = -board.score();
        }
    //    elif result == '=':
        else if (result == '=') {
    //        value = 0
            value = 0;
        }
    //    else:
        else {
    //        value = -self.negamax(state, max_depth-1, -beta, -alpha)[0]
            value = -(negamax(board, max_depth-1, -beta, -alpha)).first;
        }

    //    state.undo_last_move()
        board.undo_last_move();

    //    if value >= beta:
        if (value >= beta)
    //        return (value, move)
            return make_pair(value, move);
    //    if value > alpha:
        if (value > alpha)
    //        alpha = value
            alpha = value;

    //    if value > best_value:
        if (value > best_value) {
    //        best_value = value
    //        best_move = move
            best_value = value;
            best_move  = move;
        }
    //    elif value == best_value:
        else if (value == best_value) {
    //        pass
        }
    }

    //return (best_value, best_move)
    return make_pair(best_value, best_move);
}