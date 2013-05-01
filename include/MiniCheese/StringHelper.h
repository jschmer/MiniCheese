/* 
 * Copyright (c) 2013 Jens Schmer
 * This file is distributed under the MIT License.
 * Consult COPYING within this package for further information. 
 */
#pragma once

#include <string>
#include <vector>
#include <sstream>
#include <algorithm> 
#include <functional> 
#include <cctype>
#include <locale>

namespace String {
    static inline std::vector<std::string> &split(const std::string &s, const char delim, std::vector<std::string> &elems){
        std::stringstream ss(s);
        std::string item;
        while(std::getline(ss, item, delim)) {
            elems.push_back(item);
        }
        return elems;
    }

    static inline std::vector<std::string> split(const std::string &s, const char delim) {
        std::vector<std::string> elems;
        return split(s, delim, elems);
    }

    static inline std::string replace(std::string s, const std::string find, const std::string replace) {
        size_t len = find.length();
        size_t pos;
        while ((pos = s.find(find)) != std::string::npos) {
            s.replace(pos, len, replace);
        }

        return s;
    }

    static inline std::string replaceExtension(std::string inp, const std::string new_ext) {
        auto point_pos = inp.find_last_of('.');
        if (point_pos == std::string::npos)
            return inp;

        return replace(inp, inp.substr(point_pos, inp.length() - 1), "." + new_ext);
    }

    static inline std::string  ToString(std::wstring wstring) {
        return std::string(begin(wstring), end(wstring));
    }

    static inline std::wstring ToWString(std::string string) {
        return std::wstring(begin(string), end(string));
    }

    static inline bool existIn(char what, std::string str) {
        auto idx = str.find(what);
        return idx != std::string::npos ? true : false;
    }

    static inline std::string& ltrim(std::string &s) {
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), std::not1(std::ptr_fun<int, int>(std::isspace))));
        return s;
    }

    // trim from end
    static inline std::string& rtrim(std::string &s) {
            s.erase(std::find_if(s.rbegin(), s.rend(), std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
            return s;
    }

    // trim from both ends
    static inline std::string& trim(std::string &s) {
            return ltrim(rtrim(s));
    }
}