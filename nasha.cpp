/*
 * nasha.cpp — dear-my-love · encrypted memory transmission
 *
 * Compile (Windows):  g++ -o nasha.exe nasha.cpp -std=c++17 -O2
 * Compile (Linux/Mac): g++ -o nasha nasha.cpp -std=c++17 -O2
 * Run:                 nasha.exe   (or ./nasha)
 *
 * Requires a VT100-compatible terminal (Windows Terminal, iTerm2, etc.)
 */

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

#ifdef _WIN32
  #define WIN32_LEAN_AND_MEAN
  #include <windows.h>
  #include <io.h>
  #include <fcntl.h>
#else
  #include <csignal>
#endif

// ════════════════════════════════════════════════════════════════════
//  PLATFORM — VT enablement + Unicode stdout
// ════════════════════════════════════════════════════════════════════

static void enableVT() {
#ifdef _WIN32
    // Switch stdout to UTF-8 binary mode so multi-byte chars print correctly
    _setmode(_fileno(stdout), _O_BINARY);
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    // Enable virtual-terminal processing
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD mode  = 0;
    if (GetConsoleMode(hOut, &mode)) {
        SetConsoleMode(hOut, mode | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
    }
#endif
}

// ════════════════════════════════════════════════════════════════════
//  ANSI CODES
// ════════════════════════════════════════════════════════════════════

#define RESET       "\033[0m"
#define BOLD        "\033[1m"
#define DIM_        "\033[2m"
#define ITALIC_     "\033[3m"
#define ERASE_LINE  "\033[2K"
#define CURSOR_UP   "\033[1A"
#define HIDE_CURS   "\033[?25l"
#define SHOW_CURS   "\033[?25h"

// True-colour foreground — \033[38;2;R;G;Bm
#define ROSE        "\033[38;2;232;160;168m"
#define ROSE_LIGHT  "\033[38;2;245;208;214m"
#define ROSE_DARK   "\033[38;2;194;89;106m"
#define GOLD        "\033[38;2;203;167;106m"
#define GOLD_LIGHT  "\033[38;2;232;213;168m"
#define TEXT_C      "\033[38;2;212;184;190m"
#define TEXT_DIM_   "\033[38;2;122;93;101m"
#define CYAN_C      "\033[38;2;126;207;207m"
#define CYAN_DIM_   "\033[38;2;58;122;122m"
#define GREEN_C     "\033[38;2;126;207;158m"
#define GREEN_DIM_  "\033[38;2;58;122;90m"
#define GREY_C      "\033[38;2;74;63;72m"

// ════════════════════════════════════════════════════════════════════
//  HELPERS
// ════════════════════════════════════════════════════════════════════

static void ms(int n) {
    std::this_thread::sleep_for(std::chrono::milliseconds(n));
}

/* Centre a UTF-8 string within `width` visible characters.
   NOTE: each ASCII char = 1 col, each box-drawing / block char = 1 col. */
static std::string centerStr(const std::string& s, int w) {
    // Count visible columns (treat every byte < 0x80 OR leading byte as 1 col)
    int cols = 0;
    for (unsigned char c : s) {
        if ((c & 0xC0) != 0x80) ++cols;  // count only non-continuation bytes
    }
    if (cols >= w) return s;
    int pad = (w - cols) / 2;
    return std::string(pad, ' ') + s;
}

static void pline(const char* col, const std::string& s) {
    printf("%s%s%s\n", col, s.c_str(), RESET);
}
static void dim(const std::string& s) { pline(TEXT_DIM_, s); }

static std::string repeat(const std::string& s, int n) {
    std::string r;
    for (int i = 0; i < n; ++i) r += s;
    return r;
}

/* Word-wrap `text` to maxW columns with `indent` leading spaces. */
static std::vector<std::string> wordWrap(const std::string& text, int indent, int maxW) {
    std::vector<std::string> lines;
    std::istringstream iss(text);
    std::string word, line(indent, ' ');
    while (iss >> word) {
        if ((int)(line.size() + word.size() + 1) > maxW) {
            if (line.find_first_not_of(' ') != std::string::npos)
                lines.push_back(line);
            line = std::string(indent, ' ') + word + ' ';
        } else {
            line += word + ' ';
        }
    }
    if (line.find_first_not_of(' ') != std::string::npos)
        lines.push_back(line);
    return lines;
}

/* Get current time as "HH:MM:SS" string. */
static std::string nowTime() {
    auto t  = std::time(nullptr);
    auto tm = *std::localtime(&t);
    char buf[32];
    std::strftime(buf, sizeof(buf), "%H:%M:%S", &tm);
    return buf;
}
static std::string nowFull() {
    auto t  = std::time(nullptr);
    auto tm = *std::localtime(&t);
    char buf[32];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm);
    return buf;
}
static std::string nowISO() {
    auto t  = std::time(nullptr);
    auto tm = *std::localtime(&t);
    char buf[32];
    std::strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%S", &tm);
    return buf;
}

// ════════════════════════════════════════════════════════════════════
//  ASCII ART
// ════════════════════════════════════════════════════════════════════

static const char* BANNER[] = {
    "  \u2588\u2588\u2588\u2588\u2588\u2588\u2557     \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557    \u2588\u2588\u2588\u2588\u2588\u2557     \u2588\u2588\u2588\u2588\u2588\u2588\u2557  ",
    "  \u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557    \u2588\u2588\u2554\u2550\u2550\u2550\u2550\u255d   \u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557    \u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557 ",
    "  \u2588\u2588\u2551  \u2588\u2588\u2551    \u2588\u2588\u2588\u2588\u2588\u2557     \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2551    \u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d ",
    "  \u2588\u2588\u2551  \u2588\u2588\u2551    \u2588\u2588\u2554\u2550\u2550\u255d     \u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2551    \u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557 ",
    "  \u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d    \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557   \u2588\u2588\u2551  \u2588\u2588\u2551    \u2588\u2588\u2551  \u2588\u2588\u2551 ",
    "  \u255a\u2550\u2550\u2550\u2550\u2550\u255d     \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u255d   \u255a\u2550\u255d  \u255a\u2550\u255d    \u255a\u2550\u255d  \u255a\u2550\u255d ",
};
static const int BANNER_ROWS = 6;

// Full-block heart shapes (UTF-8 U+2588 = █)
static const char* HEART_BIG[] = {
    " \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588  \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588 ",
    "\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588",
    "\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588",
    " \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588 ",
    " \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588",
    "  \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588  ",
    "   \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588   ",
    "     \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588     ",
    "       \u2588\u2588\u2588\u2588\u2588\u2588       ",
    "         \u2588\u2588         ",
};
static const int HEART_BIG_ROWS = 10;

static const char* HEART_SMALL[] = {
    "  \u2588\u2588\u2588\u2588  \u2588\u2588\u2588\u2588  ",
    " \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588 ",
    " \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588 ",
    "  \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588  ",
    "   \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588   ",
    "    \u2588\u2588\u2588\u2588\u2588\u2588    ",
    "      \u2588\u2588      ",
};
static const int HEART_SMALL_ROWS = 7;

// ════════════════════════════════════════════════════════════════════
//  BOOT SEQUENCE
// ════════════════════════════════════════════════════════════════════

static void bootSequence() {
    printf(HIDE_CURS "\n");
    const char* grad[] = {ROSE_DARK, ROSE, ROSE_LIGHT, GOLD_LIGHT, ROSE_LIGHT, ROSE};
    for (int i = 0; i < BANNER_ROWS; ++i) {
        printf("%s%s%s%s\n", BOLD, grad[i % 6], centerStr(BANNER[i], 60).c_str(), RESET);
        ms(80);
    }
    printf("\n");
    dim("  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510");
    dim("  \u2502  DEAR-MY-LOVE  \u00b7  v2.0  \u00b7  encrypted transmission   \u2502");
    dim("  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518");
    printf("\n");
    ms(300);

    struct { const char* col; const char* msg; } logs[] = {
        {GREEN_DIM_,  "[boot]   initializing memory encoder ..."},
        {GREEN_DIM_,  "[sys]    loading cryptographic identity module ..."},
        {CYAN_DIM_,   "[io]     mounting memory filesystem ..."},
        {CYAN_DIM_,   "[net]    establishing secure channel ..."},
        {GOLD,        "[crypto] verifying recipient signature ..."},
        {ROSE_DARK,   "[mem]    allocating heart buffer ..."},
        {ROSE,        "[enc]    compiling emotional payload ..."},
        {GREEN_C,     "[sys]    all systems nominal \u2014 transmission authorized"},
    };
    for (auto& l : logs) {
        printf("%s%s%s\n", l.col, l.msg, RESET);
        ms(110);
    }
    printf("\n");

    const char* stages[] = {"BOOT", "LOAD", "INIT", "LINK"};
    for (auto s : stages) {
        for (int i = 0; i <= 32; ++i) {
            std::string bar = repeat("\u2588", i) + repeat("\u2591", 32 - i);
            printf("\r%s  [%s]%s  [%s%s%s]  %3d%%",
                CYAN_DIM_, s, RESET, ROSE, bar.c_str(), RESET, i * 100 / 32);
            fflush(stdout);
            ms(14);
        }
        printf("  %s\u2713%s\n", GREEN_C, RESET);
    }
    printf("\n");
    ms(400);
}

// ════════════════════════════════════════════════════════════════════
//  SYSTEM DASHBOARD
// ════════════════════════════════════════════════════════════════════

static void systemDashboard() {
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    pline(BOLD GOLD, "  SYSTEM REPORT");
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    printf("\n");

    struct { const char* kc; const char* k; const char* v; } rows[] = {
#ifdef _WIN32
        {CYAN_DIM_, "OS",        "windows"},
#elif __APPLE__
        {CYAN_DIM_, "OS",        "macos"},
#else
        {CYAN_DIM_, "OS",        "linux"},
#endif
        {CYAN_DIM_, "RUNTIME",   "C++17"},
        {CYAN_DIM_, "SESSION",   nowFull().c_str()},
        {ROSE,      "RECIPIENT", "Nasha Putri Zaqirah"},
        {ROSE,      "SENDER",    "Afra Fadma Dinata"},
        {GOLD,      "ENCODING",  "UTF-8 / emotional-256"},
        {GREEN_C,   "STATUS",    "AUTHORIZED  \u2713"},
    };
    for (auto& r : rows) {
        printf("  %s%-14s%s  %s\u2502%s  %s%s%s\n",
            r.kc, r.k, RESET, TEXT_DIM_, RESET, TEXT_C, r.v, RESET);
        ms(65);
    }
    printf("\n");
    ms(400);
}

// ════════════════════════════════════════════════════════════════════
//  DECODE ANIMATION
// ════════════════════════════════════════════════════════════════════

static void decodeAnimation() {
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    pline(BOLD ROSE_DARK, "  DECODING RECIPIENT SIGNATURE");
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    printf("\n");

    const char* name    = "Nasha Putri Zaqirah";
    size_t nameLen      = std::strlen(name);

    // Hex dump
    printf("%s  HEX_DUMP  \u00bb%s  ", CYAN_DIM_, RESET);
    for (size_t i = 0; i < nameLen; ++i) {
        printf("%s%02X %s", CYAN_C, (unsigned char)name[i], RESET);
        fflush(stdout);
        ms(38);
    }
    printf("\n");

    // Binary (first 6 bytes)
    printf("%s  BINARY    \u00bb%s  ", CYAN_DIM_, RESET);
    for (size_t i = 0; i < 6; ++i) {
        for (int b = 7; b >= 0; --b)
            printf("%s%c%s", GREEN_DIM_, ((name[i] >> b) & 1) ? '1' : '0', RESET);
        printf(" ");
        fflush(stdout);
        ms(48);
    }
    printf("%s ...%s\n\n", TEXT_DIM_, RESET);

    // Glitch reveal (works on ASCII part of the name)
    const char* noise = "\u2588\u2593\u2592\u2591\u2592\u2593\u2588"; // "█▓▒░▒▓█"
    // Count rune-length of noise (each block = 3 bytes in UTF-8)
    int noiseCount = 7;
    for (int step = 0; step <= (int)nameLen; ++step) {
        printf("\r  %s", BOLD ROSE);
        fwrite(name, 1, step, stdout);
        printf("%s%s", RESET, TEXT_DIM_);
        // print some noise chars
        for (int i = 0; i < std::min((int)nameLen - step, 7); ++i) {
            // Each block char is 3 UTF-8 bytes; pick which noise char cyclically
            int ni = i % noiseCount;
            // noise char index: 3 bytes per char
            fwrite(noise + ni * 3, 1, 3, stdout);
        }
        printf("%s    ", RESET);
        fflush(stdout);
        ms(58);
    }
    printf("\r  %s%s%s\n\n", BOLD ROSE_LIGHT, name, RESET);
    ms(500);
}

// ════════════════════════════════════════════════════════════════════
//  LETTER
// ════════════════════════════════════════════════════════════════════

static void renderLetter() {
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    pline(BOLD ROSE, "  TRANSMISSION PAYLOAD  \u00b7  10 BLOCKS");
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    printf("\n");

    struct { const char* tag; const char* col; const char* text; } blocks[] = {
        {"INIT", CYAN_DIM_,   "Aku ingin memulai ini dengan jujur \u2014 bukan dengan kata yang dipoles, bukan dengan kalimat yang dilatih. Hanya aku, dan apa yang aku rasakan."},
        {"ADDR", ROSE_DARK,   "Nasha. Namamu sendiri sudah terasa seperti sebuah baris kode yang, setiap kali aku baca, mengembalikan sesuatu yang hangat."},
        {"DATA", ROSE,        "Aku tidak tahu persis kapan mulainya. Tapi aku tahu \u2014 ada momen-momen kecil bersamamu yang diam-diam aku simpan, seperti file yang tidak bisa aku hapus."},
        {"MEM_", GOLD,        "Cara kamu tertawa. Cara kamu serius dengan hal-hal yang kamu pedulikan. Cara kamu hadir \u2014 bukan hanya secara fisik, tapi benar-benar hadir."},
        {"PROC", ROSE_LIGHT,  "Dan aku, yang biasanya lebih nyaman dengan logika daripada perasaan, tiba-tiba mendapati diriku memikirkanmu lebih dari yang seharusnya."},
        {"SYNC", CYAN_C,      "Bersamamu, aku tidak merasa perlu menjadi versi terbaik dari diriku. Aku cukup menjadi aku \u2014 dan itu rasanya seperti kebebasan."},
        {"EXEC", GREEN_C,     "Aku tidak punya banyak janji besar. Yang aku punya hanyalah ini: aku ingin ada. Aku ingin mendengar. Aku ingin menjadi tempat yang aman bagimu."},
        {"SEND", GOLD_LIGHT,  "Kalau kamu pernah merasa sendirian di tengah keramaian \u2014 aku ingin kamu tahu bahwa aku di sini. Dan aku tidak ke mana-mana."},
        {"RECV", ROSE,        "Mungkin ini bukan waktu yang sempurna. Mungkin aku bukan orang yang sempurna. Tapi perasaan ini \u2014 ini nyata. Dan itu cukup bagiku untuk mengatakannya."},
        {"DONE", ROSE_DARK,   "Jadi ini dia. Bukan akhir dari sesuatu, tapi awal \u2014 kalau kamu mau. Aku di sini, Nasha. Dan aku sangat ingin berada di sini, bersamamu."},
    };

    for (int i = 0; i < 10; ++i) {
        auto& b = blocks[i];
        printf("%s  [%s] BLOCK_%02d%s\n", b.col, b.tag, i + 1, RESET);
        for (auto& line : wordWrap(b.text, 4, 70)) {
            printf("%s%s%s\n", TEXT_C, line.c_str(), RESET);
            ms(7);
        }
        printf("\n");
        ms(90);
    }
}

// ════════════════════════════════════════════════════════════════════
//  POEM
// ════════════════════════════════════════════════════════════════════

static void renderPoem() {
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    pline(BOLD GOLD, "  POEM  \u00b7  encoded in rose");
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    printf("\n");

    struct { const char* col; const char* text; } poem[] = {
        {ROSE_LIGHT, "Namamu  \u00b7  tiga suku kata"},
        {ROSE,       "yang selalu aku ucapkan pelan-pelan"},
        {ROSE_LIGHT, "seolah kalau terlalu keras"},
        {GOLD_LIGHT, "ia akan hilang."},
        {nullptr,    ""},
        {GOLD,       "Kamu adalah jeda di antara baris kode"},
        {GOLD_LIGHT, "yang membuatnya masuk akal."},
        {nullptr,    ""},
        {ROSE_LIGHT, "Dan aku \u2014 hanyalah seseorang"},
        {ROSE,       "yang perlahan belajar"},
        {GOLD_LIGHT, "bahwa beberapa hal"},
        {ROSE_LIGHT, "tidak perlu dijelaskan."},
        {nullptr,    ""},
        {ROSE,       "Mereka cukup dirasakan."},
    };

    for (auto& l : poem) {
        if (!l.col) { printf("\n"); }
        else         { pline(l.col, std::string("    ") + l.text); }
        ms(85);
    }
    printf("\n");
    ms(300);
}

// ════════════════════════════════════════════════════════════════════
//  TRANSMISSION REPORT
// ════════════════════════════════════════════════════════════════════

static void transmissionReport() {
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    pline(BOLD GREEN_C, "  TRANSMISSION REPORT");
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    printf("\n");

    struct { const char* k; const char* v; } rows[] = {
        {"BLOCKS_SENT",  "10 / 10"},
        {"POEM_LINES",   "14"},
        {"RECIPIENT",    "Nasha Putri Zaqirah"},
        {"SENDER",       "Afra Fadma Dinata"},
        {"TIMESTAMP",    nowISO().c_str()},
        {"LANG",         "C++17"},
        {"STATUS",       "DELIVERED  \u2713"},
    };
    for (auto& r : rows) {
        printf("  %s%-16s%s  %s%s%s\n", CYAN_DIM_, r.k, RESET, GREEN_C, r.v, RESET);
        ms(80);
    }
    printf("\n");
    ms(400);
}

// ════════════════════════════════════════════════════════════════════
//  OUTRO
// ════════════════════════════════════════════════════════════════════

static void outro() {
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    pline(BOLD ROSE, "  END OF TRANSMISSION");
    dim("  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
    printf("\n");
    pline(BOLD ITALIC_ ROSE_LIGHT, centerStr("Nasha Putri Zaqirah", 60));
    pline(TEXT_DIM_, centerStr("[ " + nowFull() + " ]", 60));
    printf("\n");
    ms(600);
}

// ════════════════════════════════════════════════════════════════════
//  FINAL LOOP ANIMATION
// ════════════════════════════════════════════════════════════════════

// The orbit and wave strings as UTF-8 C string literals.
static const char* ORBIT_STR  = "\u00b7  \u2736  \u00b7  \u2665  \u00b7  \u2736  \u00b7  \u2665  ";
static const char* WAVES[]    = {
    "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581",
    "\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581\u2582",
    "\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581\u2582\u2583",
    "\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581\u2582\u2583\u2584",
};
static const char* ROSE_COLS[] = {ROSE_DARK, ROSE, ROSE_LIGHT, GOLD_LIGHT, GOLD, ROSE_LIGHT, ROSE};

static volatile bool g_running = true;

#ifdef _WIN32
static BOOL WINAPI ctrlHandler(DWORD type) {
    if (type == CTRL_C_EVENT || type == CTRL_BREAK_EVENT) {
        g_running = false;
        return TRUE;
    }
    return FALSE;
}
#else
static void sigHandler(int) { g_running = false; }
#endif

static void finalLoop() {
    pline(TEXT_DIM_, centerStr("[ animation loop started \u2014 ctrl+c to exit ]", 60));
    printf("\n");
    ms(600);

#ifdef _WIN32
    SetConsoleCtrlHandler(ctrlHandler, TRUE);
#else
    std::signal(SIGINT,  sigHandler);
    std::signal(SIGTERM, sigHandler);
#endif

    // We'll use cursor-up redraws.
    // Pre-compute max heart rows (big = 10).
    const int FPS       = 18;
    const int W         = 64;
    const int ORBIT_LEN = 48;  // visible chars in orbit strip

    // Count UTF-8 "runes" (non-continuation bytes) in orbit string
    // We need to index into it by rune, not byte.
    // Build a vector of byte-offsets for each rune in ORBIT_STR repeated.
    std::string orbitBase = ORBIT_STR;
    // Repeat orbit base a few times for cycling
    std::string orbitPool = orbitBase + orbitBase + orbitBase + orbitBase;

    // Build wave pool
    std::string wavePool[4];
    for (int i = 0; i < 4; ++i) {
        for (int r = 0; r < 4; ++r) wavePool[i] += WAVES[i];
    }

    auto start = std::chrono::steady_clock::now();
    int tick       = 0;
    int frameLines = 0;
    bool firstFrame= true;

    while (g_running) {
        bool big  = (tick / FPS) % 2 == 0;
        const char** heart     = big ? HEART_BIG   : HEART_SMALL;
        int          heartRows = big ? HEART_BIG_ROWS : HEART_SMALL_ROWS;

        const char* hue  = ROSE_COLS[tick % 7];
        const char* gCol = ROSE_COLS[tick % 7];
        const char* rCol = ROSE_COLS[tick % 7];
        const char* wCols[]= {CYAN_DIM_, CYAN_DIM_, ROSE_DARK, ROSE_DARK};
        const char* wCol   = wCols[tick % 4];

        // Elapsed
        auto now     = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - start).count();
        int  mins    = (int)(elapsed / 60000);
        int  secs    = (int)((elapsed / 1000) % 60);
        int  ms_part = (int)(elapsed % 1000);

        // Build frame in a buffer
        std::string frame;
        int lc = 0;  // line count

        frame += "\n"; ++lc;
        for (int i = 0; i < heartRows; ++i) {
            frame += BOLD;
            frame += hue;
            frame += centerStr(heart[i], W);
            frame += RESET "\n";
            ++lc;
        }
        frame += "\n"; ++lc;

        // Name glow
        frame += BOLD ITALIC_;
        frame += gCol;
        frame += centerStr("Nasha Putri Zaqirah", W);
        frame += RESET "\n"; ++lc;

        // Orbit ring — slice orbitPool at rune-offset tick
        // Count rune columns in orbitPool up to ORBIT_LEN
        frame += "\n"; ++lc;
        {
            // Build a sub-string of orbitPool starting from rune #tick, length ORBIT_LEN
            std::string ring;
            int rune_idx = 0;
            int start_rune = tick % (int)orbitBase.size();
            bool inSlice = false;
            int collected = 0;
            for (size_t bi = 0; bi < orbitPool.size() && collected < ORBIT_LEN; ) {
                unsigned char c = (unsigned char)orbitPool[bi];
                int char_bytes = 1;
                if      ((c & 0xF8) == 0xF0) char_bytes = 4;
                else if ((c & 0xF0) == 0xE0) char_bytes = 3;
                else if ((c & 0xE0) == 0xC0) char_bytes = 2;

                if (rune_idx >= start_rune && collected < ORBIT_LEN) {
                    ring.append(orbitPool, bi, char_bytes);
                    ++collected;
                }
                ++rune_idx;
                bi += char_bytes;
                if (rune_idx >= (int)orbitPool.size()) rune_idx = 0;
            }
            frame += DIM_;
            frame += rCol;
            frame += centerStr(ring, W);
            frame += RESET "\n"; ++lc;
        }

        // Wave bar
        frame += "\n"; ++lc;
        {
            const std::string& wp = wavePool[tick % 4];
            // slice 40 runes
            std::string waveSeg;
            int col = 0;
            for (size_t bi = tick % 15 * 3; bi < wp.size() && col < 40; ) {
                unsigned char c = (unsigned char)wp[bi];
                int cb = 1;
                if      ((c & 0xF8) == 0xF0) cb = 4;
                else if ((c & 0xF0) == 0xE0) cb = 3;
                else if ((c & 0xE0) == 0xC0) cb = 2;
                waveSeg.append(wp, bi, cb);
                bi += cb; ++col;
            }
            frame += DIM_;
            frame += wCol;
            frame += centerStr(waveSeg, W);
            frame += RESET "\n"; ++lc;
        }

        // Status footer
        frame += "\n"; ++lc;
        char status[128];
        snprintf(status, sizeof(status),
            "%s  looping  \u00b7  %02d:%02d.%03d  \u00b7  ctrl+c to exit",
            nowTime().c_str(), mins, secs, ms_part);
        frame += DIM_;
        frame += GREY_C;
        frame += centerStr(status, W);
        frame += RESET "\n"; ++lc;

        // Move cursor up past previous frame, then print new frame
        if (!firstFrame) {
            for (int i = 0; i < frameLines; ++i)
                printf(CURSOR_UP ERASE_LINE);
        }
        firstFrame  = false;
        frameLines  = lc;

        fwrite(frame.data(), 1, frame.size(), stdout);
        fflush(stdout);

        ++tick;
        ms(1000 / FPS);
    }

    printf(SHOW_CURS);
    printf("\n%s  [ loop exited \u2736 farewell, Nasha ]%s\n\n", TEXT_DIM_, RESET);
}

// ════════════════════════════════════════════════════════════════════
//  MAIN
// ════════════════════════════════════════════════════════════════════

int main() {
    enableVT();

    bootSequence();
    systemDashboard();
    decodeAnimation();
    renderLetter();
    renderPoem();
    transmissionReport();
    outro();
    finalLoop();

    printf(SHOW_CURS);
    return 0;
}
