#pragma once
#include <exception>
#include <string>

struct MiniCheeseException : public std::exception {
public:
    MiniCheeseException(const char* m = "MiniCheeseException")
        : msg(m)
    {}
    ~MiniCheeseException() {}

    const char* what(){
        return msg.c_str();
    }

    std::string msg;
};

struct ValueError : public MiniCheeseException {
    ValueError(const std::string m = "ValueError")
        : MiniCheeseException(m.c_str())
    {}
    ~ValueError() {}
};