#include <iostream>
#include <array>
#include <string>

using std::cout, std::cin, std::endl;

class Piece;

class Table;

class Game;

int Game(Table table);


void fillRows(Table table, int rows, int displacement);

void printTable(Table table);

// Color = 0 (white), 1 (black), 2 (empty)
class Piece {
public:
    int color;
};

//
//class Cell {
//public:
//    int x, y;
//};

class Game {
public:
    int turn;

    Game() {}
};

class Table {
public:

    int table[10][10];

    Table() {
        for (int i = 0; i < 10; i++)
            for (int j = 0; j < 10; j++)
                table[i][j] = 0;
    }
};

Table fillRows(Table table, int fromColumn, int toColumn, int fromRow, int cellType) {
    for (int i = fromColumn - 1; i < toColumn; i++) {
        table.table[fromRow - 1][i] = cellType;
    }
    return table;
}


void printTable(Table table) {
    std::string colors[3] = {"\e[0;31m", "\e[0;32m", "\e[0m"};
    std::cout << "Created game as: " << std::endl;
    std::cout << "     0 1 2 3 4 5 6 7 8 9" << std::endl;
    std::cout << "     ====================";

    for (int i = 0; i < 10; i++) {
        std::cout << std::endl << 9 - i << " || ";
        for (int j = 9; j >= 0; j--) {
            int color = 2;
            if (table.table[j][i] == 1) color = 0;
            if (table.table[j][i] == 2) color = 1;
            std::cout << colors[color] << table.table[j][i] << colors[2] << " ";
        }
    }
}

Table createBoard() {
    Table top;
    for (int i = 5; i >= 1; i--) {
        top = fillRows(top, 1, i, i + 5, 1);
        top = fillRows(top, i + 5, 10, i, 2);
    }
    return top;
}

int Game(Table table) {
    bool running = true;
    int x = -1, y = -1;
    char changeTurn = 'N';
    while (running) {
        try {
            std::cout << "\nX coordinate: ";
            std::cin >> x;
            std::cout << "\nY coordinate: ";
            std::cin >> y;
            std::cout << "\nChange coords? (Y/N)";
            std::cin >> changeTurn;
            changeTurn = putchar(toupper(changeTurn));

            if (changeTurn == 'Y') throw 'Change turn';


        } catch (std::string myError) {
            // Do nothing
        }
        running = !running;
    }
}

int main() {
    Table top = Table();
    /**
     * How it should start:
     *      1 1 1 1 1 0 0 0 0 0
     *      1 1 1 1 0 0 0 0 0 0
     *      1 1 1 0 0 0 0 0 0 0
     *      1 1 0 0 0 0 0 0 0 0
     *      1 0 0 0 0 0 0 0 0 0
     *      0 0 0 0 0 0 0 0 0 2
     *      0 0 0 0 0 0 0 0 2 2
     *      0 0 0 0 0 0 0 2 2 2
     *      0 0 0 0 0 0 2 2 2 2
     *      0 0 0 0 0 2 2 2 2 2
     *
     *      [ 0, 10 ]----[ 10, 10 ]
     *         |            |
     *      [ 0, 0 ]----[ 10, 0 ]
     */

    // Create the game

    top = createBoard();
    printTable(top);
    Game(top);
    return 0;

}