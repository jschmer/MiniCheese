#include <tuple>
#include <map>
#include <vector>

typedef std::tuple<int, int, bool, bool, bool> scan_args;
typedef std::map<char, std::vector<scan_args>> ScanArgsMap;

// scan_args(dx, dy, only_capture, no_capture, one_step)
scan_args _k[] = {
     scan_args(0, 1, false, false, true),
     scan_args(0, -1, false, false, true), 
     scan_args(1, 0, false, false, true), 
     scan_args(1, 1, false, false, true), 
     scan_args(1, -1, false, false, true), 
     scan_args(-1, 0, false, false, true), 
     scan_args(-1, 1, false, false, true), 
     scan_args(-1, -1, false, false, true)
};
std::vector<scan_args> k(&_k[0], &_k[8]);
auto& K = k;


scan_args _q[] = {
    scan_args(0, 1, false, false, false), 
     scan_args(0, -1, false, false, false), 
     scan_args(1, 0, false, false, false), 
     scan_args(1, 1, false, false, false), 
     scan_args(1, -1, false, false, false), 
     scan_args(-1, 0, false, false, false), 
     scan_args(-1, 1, false, false, false), 
     scan_args(-1, -1, false, false, false)
};
std::vector<scan_args> q(&_q[0], &_q[8]);
auto& Q = q;

scan_args _b[] = {
    scan_args(1, 1, false, false, false), 
     scan_args(1, -1, false, false, false), 
     scan_args(-1, 1, false, false, false), 
     scan_args(-1, -1, false, false, false),
     scan_args(0, 1, false, true, true), 
     scan_args(0, -1, false, true, true), 
     scan_args(1, 0, false, true, true), 
     scan_args(-1, 0, false, true, true)
};
std::vector<scan_args> b(&_b[0], &_b[8]);
auto& B = b;

// .n.n.
// n...n
// ..N..
// n...n
// .n.n.

// first row
scan_args _n[] = {
    scan_args(-1, 2, false, false, true),
     scan_args(1, 2, false, false, true),
// second row
     scan_args(-2, 1, false, false, true),
     scan_args(2, 1, false, false, true),
// forth row
     scan_args(-2, -1, false, false, true),
     scan_args(2, -1, false, false, true),
// fifth
     scan_args(-1, -2, false, false, true),
     scan_args(1, -2, false, false, true)
};
std::vector<scan_args> n(&_n[0], &_n[8]);
auto& N = n;

scan_args _r[] = {
    scan_args(0, 1, false, false, false), 
     scan_args(0, -1, false, false, false), 
     scan_args(1, 0, false, false, false), 
     scan_args(-1, 0, false, false, false)
};
std::vector<scan_args> r(&_r[0], &_r[4]);
auto& R = r;

// black pawn can only move down
scan_args _p[] = {
    scan_args(0, -1, false, true, true), 
     scan_args(-1, -1, true, false, true), 
     scan_args(1, -1, true, false, true)
};
std::vector<scan_args> p(&_p[0], &_p[3]);

// white pawn can only move up
scan_args _P[] = {
    scan_args(0, 1, false, true, true), 
     scan_args(-1, 1, true, false, true), 
     scan_args(1, 1, true, false, true)
};
std::vector<scan_args> P(&_P[0], &_P[3]);

// initialize map
ScanArgsMap scan_arguments = [&](){
    ScanArgsMap tmp;
    tmp['k'] = k;
    tmp['q'] = q;
    tmp['b'] = b;
    tmp['n'] = n;
    tmp['r'] = r;
    tmp['p'] = p;
    tmp['K'] = K;
    tmp['Q'] = Q;
    tmp['B'] = B;
    tmp['N'] = N;
    tmp['R'] = R;
    tmp['P'] = P;
    return tmp;
}();

//auto scan_arguments = {
//    'k': k,
//    'q': q,
//    'b': b,
//    'n': n,
//    'r': r,
//    'p': p,
//    'K': K,
//    'Q': Q,
//    'B': B,
//    'N': N,
//    'R': R,
//    'P': P
//}