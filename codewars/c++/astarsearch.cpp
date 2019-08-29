#include <cmath>
#include <set>
#include <queue>

using namespace std;

class cell{
public:
    bool reachable;
    int col;
    int row;
    int g;
    int h;
    int f;
    cell parent;
    cell(int cell_collumn, int cell_row, bool cell_reachable){
        this->col = cell_collumn;
        this->row = cell_row;
        this->reachable = cell_reachable;
        this->col = 0;
        this->row = 0;
        this->g = 0;
        this->h = 0;
        this->f = 0;
    }
};

class search{
public:
    vector<vector<int>> grid;
    priority_queue<int, cell> opened;
    set<cell> closed;
    set<pair<int, int>> walls;
    queue<cell> to_be_calculated;
    set<cell> cells;
    int grid_height;
    int grid_width;
    cell start;
    cell end;

    void init_grid(string wall_character, string start_character, string end_character){
        for (int row = 0; row < this->grid_height; ++row) {
            for (int col = 0; col < this->grid_width; ++col) {
                if (to_string(grid[row][col]) == wall_character){
                    this->cells.emplace(new cell(col, row, False));
                } else {
                    this->cells.emplace(new cell(col, row, True));
                }
                if (to_string(grid[row][col]) == start_character){
                    this->start = get_cell(row, col);
                } else if (to_string(grid[row][col]) == end_character){
                    this->end = get_cell(row, col)
                }
            }
        }
    }
    void get_walls(){
        for (int row = 0; row < this->grid_height; ++row) {
            for (int col = 0; col < this->grid_width; ++col) {
                if (to_string(this->grid[row][col]) == this->wallchar){
                    this->walls.emplace(make_pair(row, col));
                }
            }
        }
    }
    cell get_cell(int row, int col){
        return this->cells[this->cells.find(make_pair(row, col))];
    }

    int get_heuristic(cell cell_to_check){
        return 10 * (abs(cell_to_check.col - this.end.col) + abs(cell_to_check.row - this.end.row))
    }

    vector<cell> get_adjacent_cells(cell center_cell){
        // center_cell is the cell to search around
        vector<cell> result;
        if (center_cell.col < this.grid_width - 1){
            result.push_back(get_cell(center_cell.col + 1, center_cell.row));
        }
        if (center_cell.row > 0){
            result.push_back(get_cell(center_cell.col, center_cell.row - 1));
        }
        if (center_cell.col > 0){
            result.push_back(get_cell(center_cell.col - 1, center_cell.row));
        }
        if (center_cell.col < this.grid_height - 1){
            result.push_back(get_cell(center_cell.col, center_cell.row + 1));
        }
        return result;
    }
    void update_cell(cell current_cell, cell adjacent_cell){
        adjacent_cell.g = current_cell.g + 10;
        adjacent_cell.h = get_heuristic(adjacent_cell);
        adjacent_cell.parent = current_cell;
        adjacent_cell.f = adjacent_cell.h + adjacent_cell.g;
    }
    vector<pair<int,int>> get_path(){
        current_cell = this.end;
        vector<pair<int,int>> path = {make_pair(this.end.col, this.end.row)};
        while(current_cell.parent != this.start){
            current_cell = current_cell.parent;
            path.push_back(make_pair(current_cell.col, current_cell.row));
        }
        path.push_back(make_pair(this.start.col, this.start.row));
        reverse(path.begin(), path.end());
        return path;
    }
    vector<int,int> solve(){
        this.opened.push(this.start.f, this.start);
        while(this.opened.size() != 0){
            pair<int,cell> current_cell = this.opened.top();
            this.opened.pop();
            this.closed.emplace(current_cell.second)
            if(current_cell == this.end){
                return this.get_path();
            }
            vector<cell> adjacent_cells = {get_adjacent_cells(current_cell)};
            for (std::vector<cell>::iterator i = adjacent_cells.begin(); i != adjacent_cells.end(); ++i){
                if((adjacent_cells[i].reachable) && (!this.closed.find(adjacent_cells[i]))){
                    if(adjacent_cells[i].g > current_cell.g + 10){
                        update_cell(current_cell, adjacent_cells[i]);
                    }
                } else {
                    update_cell(current_cell, adjacent_cells[i]);
                    this.opened.push(make_pair(adjacent_cells[i].f, adjacent_cells[i]));
                }
            }
        }
    }

    search(vector<vector<int>> grid_in, string wall_char, string startchar, string endchar){
        this->grid = grid_in;
        this->wallchar = wall;
        this->pathchar = path;
        this->grid_height = grid_in.size();
        this->grid_width = grid_in[0].size();
        this->get_walls();
        this->init_grid();
        this->get_start_end(startchar, endchar);
    }


};