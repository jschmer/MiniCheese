#pragma once
#include <string>

inline bool existIn(char what, std::string str) {
    auto idx = str.find(what);
    return idx != std::string::npos ? true : false;
}