# Pathfinding Algorithms

Navigation solutions for ZX games, from simple grids to waypoint graphs.

## Grid-Based A* Pathfinding

Best for tile-based games or levels with regular structure.

### Grid Representation

```rust
const GRID_WIDTH: usize = 32;
const GRID_HEIGHT: usize = 32;
const TILE_SIZE: f32 = 16.0;

#[derive(Clone, Copy, PartialEq)]
enum Tile {
    Floor,
    Wall,
}

struct Grid {
    tiles: [[Tile; GRID_WIDTH]; GRID_HEIGHT],
}

impl Grid {
    fn is_walkable(&self, x: usize, y: usize) -> bool {
        if x >= GRID_WIDTH || y >= GRID_HEIGHT {
            return false;
        }
        self.tiles[y][x] == Tile::Floor
    }

    fn world_to_grid(&self, wx: f32, wy: f32) -> (usize, usize) {
        ((wx / TILE_SIZE) as usize, (wy / TILE_SIZE) as usize)
    }

    fn grid_to_world(&self, gx: usize, gy: usize) -> (f32, f32) {
        (gx as f32 * TILE_SIZE + TILE_SIZE * 0.5,
         gy as f32 * TILE_SIZE + TILE_SIZE * 0.5)
    }
}
```

### A* Implementation

```rust
use core::cmp::Ordering;

#[derive(Clone, Copy, Eq, PartialEq)]
struct Node {
    x: usize,
    y: usize,
    g: u32,  // Cost from start
    f: u32,  // g + heuristic
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.f.cmp(&self.f)  // Min-heap: lower f first
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn heuristic(x1: usize, y1: usize, x2: usize, y2: usize) -> u32 {
    // Manhattan distance (works well for 4-directional movement)
    let dx = if x1 > x2 { x1 - x2 } else { x2 - x1 };
    let dy = if y1 > y2 { y1 - y2 } else { y2 - y1 };
    (dx + dy) as u32
}

const MAX_PATH_LENGTH: usize = 64;

fn find_path(
    grid: &Grid,
    start_x: usize, start_y: usize,
    goal_x: usize, goal_y: usize,
    path: &mut [(usize, usize); MAX_PATH_LENGTH],
) -> usize {
    // Fixed-size arrays for no_std compatibility
    let mut open: [Option<Node>; 256] = [None; 256];
    let mut open_count = 0;
    let mut closed: [[bool; GRID_WIDTH]; GRID_HEIGHT] = [[false; GRID_WIDTH]; GRID_HEIGHT];
    let mut came_from: [[(usize, usize); GRID_WIDTH]; GRID_HEIGHT] =
        [[(!0, !0); GRID_WIDTH]; GRID_HEIGHT];
    let mut g_score: [[u32; GRID_WIDTH]; GRID_HEIGHT] = [[u32::MAX; GRID_WIDTH]; GRID_HEIGHT];

    // Add start node
    g_score[start_y][start_x] = 0;
    open[0] = Some(Node {
        x: start_x,
        y: start_y,
        g: 0,
        f: heuristic(start_x, start_y, goal_x, goal_y),
    });
    open_count = 1;

    while open_count > 0 {
        // Find node with lowest f
        let mut best_idx = 0;
        let mut best_f = u32::MAX;
        for i in 0..open_count {
            if let Some(node) = open[i] {
                if node.f < best_f {
                    best_f = node.f;
                    best_idx = i;
                }
            }
        }

        let current = open[best_idx].unwrap();
        open[best_idx] = open[open_count - 1];
        open_count -= 1;

        if current.x == goal_x && current.y == goal_y {
            // Reconstruct path
            return reconstruct_path(came_from, goal_x, goal_y, path);
        }

        closed[current.y][current.x] = true;

        // Check neighbors (4-directional)
        let neighbors = [
            (current.x.wrapping_sub(1), current.y),
            (current.x + 1, current.y),
            (current.x, current.y.wrapping_sub(1)),
            (current.x, current.y + 1),
        ];

        for (nx, ny) in neighbors {
            if !grid.is_walkable(nx, ny) || closed[ny][nx] {
                continue;
            }

            let tentative_g = current.g + 1;

            if tentative_g < g_score[ny][nx] {
                came_from[ny][nx] = (current.x, current.y);
                g_score[ny][nx] = tentative_g;

                // Add to open if not already there
                let mut found = false;
                for i in 0..open_count {
                    if let Some(node) = &mut open[i] {
                        if node.x == nx && node.y == ny {
                            node.g = tentative_g;
                            node.f = tentative_g + heuristic(nx, ny, goal_x, goal_y);
                            found = true;
                            break;
                        }
                    }
                }

                if !found && open_count < 256 {
                    open[open_count] = Some(Node {
                        x: nx,
                        y: ny,
                        g: tentative_g,
                        f: tentative_g + heuristic(nx, ny, goal_x, goal_y),
                    });
                    open_count += 1;
                }
            }
        }
    }

    0  // No path found
}

fn reconstruct_path(
    came_from: [[(usize, usize); GRID_WIDTH]; GRID_HEIGHT],
    goal_x: usize, goal_y: usize,
    path: &mut [(usize, usize); MAX_PATH_LENGTH],
) -> usize {
    let mut count = 0;
    let mut x = goal_x;
    let mut y = goal_y;

    while came_from[y][x] != (!0, !0) && count < MAX_PATH_LENGTH {
        path[count] = (x, y);
        count += 1;
        let (px, py) = came_from[y][x];
        x = px;
        y = py;
    }

    // Reverse path (currently goal-to-start)
    for i in 0..count / 2 {
        path.swap(i, count - 1 - i);
    }

    count
}
```

### Using the Path

```rust
struct PathFollower {
    path: [(usize, usize); MAX_PATH_LENGTH],
    path_len: usize,
    current_idx: usize,
}

impl PathFollower {
    fn update(&mut self, enemy: &mut Enemy, grid: &Grid) {
        if self.current_idx >= self.path_len {
            return;  // Path complete
        }

        let (gx, gy) = self.path[self.current_idx];
        let (wx, wy) = grid.grid_to_world(gx, gy);

        let dist = enemy.distance_to(wx, wy);
        if dist < TILE_SIZE * 0.25 {
            self.current_idx += 1;
        } else {
            enemy.move_toward(wx, wy);
        }
    }

    fn repath(&mut self, grid: &Grid, enemy: &Enemy, goal_x: f32, goal_y: f32) {
        let (sx, sy) = grid.world_to_grid(enemy.x, enemy.y);
        let (gx, gy) = grid.world_to_grid(goal_x, goal_y);
        self.path_len = find_path(grid, sx, sy, gx, gy, &mut self.path);
        self.current_idx = 0;
    }
}
```

---

## Waypoint Graphs

Better for 3D levels or irregular geometry.

### Structure

```rust
const MAX_WAYPOINTS: usize = 32;
const MAX_CONNECTIONS: usize = 4;

struct Waypoint {
    x: f32, y: f32, z: f32,
    connections: [u8; MAX_CONNECTIONS],  // Indices of connected waypoints
    connection_count: u8,
}

struct WaypointGraph {
    waypoints: [Waypoint; MAX_WAYPOINTS],
    count: usize,
}
```

### Finding Nearest Waypoint

```rust
impl WaypointGraph {
    fn find_nearest(&self, x: f32, y: f32, z: f32) -> Option<usize> {
        let mut best = None;
        let mut best_dist = f32::MAX;

        for i in 0..self.count {
            let wp = &self.waypoints[i];
            let dx = wp.x - x;
            let dy = wp.y - y;
            let dz = wp.z - z;
            let dist = dx * dx + dy * dy + dz * dz;

            if dist < best_dist {
                best_dist = dist;
                best = Some(i);
            }
        }

        best
    }
}
```

### A* on Waypoint Graph

```rust
fn find_waypoint_path(
    graph: &WaypointGraph,
    start: usize,
    goal: usize,
    path: &mut [usize; MAX_WAYPOINTS],
) -> usize {
    let mut open: [Option<(usize, f32)>; MAX_WAYPOINTS] = [None; MAX_WAYPOINTS];
    let mut open_count = 0;
    let mut closed: [bool; MAX_WAYPOINTS] = [false; MAX_WAYPOINTS];
    let mut came_from: [usize; MAX_WAYPOINTS] = [!0; MAX_WAYPOINTS];
    let mut g_score: [f32; MAX_WAYPOINTS] = [f32::MAX; MAX_WAYPOINTS];

    g_score[start] = 0.0;
    open[0] = Some((start, distance(&graph.waypoints[start], &graph.waypoints[goal])));
    open_count = 1;

    while open_count > 0 {
        // Find best node
        let mut best_idx = 0;
        let mut best_f = f32::MAX;
        for i in 0..open_count {
            if let Some((_, f)) = open[i] {
                if f < best_f {
                    best_f = f;
                    best_idx = i;
                }
            }
        }

        let (current, _) = open[best_idx].unwrap();
        open[best_idx] = open[open_count - 1];
        open_count -= 1;

        if current == goal {
            return reconstruct_waypoint_path(came_from, goal, path);
        }

        closed[current] = true;

        let wp = &graph.waypoints[current];
        for i in 0..wp.connection_count as usize {
            let neighbor = wp.connections[i] as usize;
            if closed[neighbor] {
                continue;
            }

            let dist = distance(wp, &graph.waypoints[neighbor]);
            let tentative_g = g_score[current] + dist;

            if tentative_g < g_score[neighbor] {
                came_from[neighbor] = current;
                g_score[neighbor] = tentative_g;

                let h = distance(&graph.waypoints[neighbor], &graph.waypoints[goal]);
                let f = tentative_g + h;

                // Add or update in open list
                let mut found = false;
                for i in 0..open_count {
                    if let Some((idx, _)) = &mut open[i] {
                        if *idx == neighbor {
                            open[i] = Some((neighbor, f));
                            found = true;
                            break;
                        }
                    }
                }

                if !found && open_count < MAX_WAYPOINTS {
                    open[open_count] = Some((neighbor, f));
                    open_count += 1;
                }
            }
        }
    }

    0
}

fn distance(a: &Waypoint, b: &Waypoint) -> f32 {
    let dx = a.x - b.x;
    let dy = a.y - b.y;
    let dz = a.z - b.z;
    (dx * dx + dy * dy + dz * dz).sqrt()
}
```

---

## Path Smoothing

Raw A* paths follow grid cells exactly. Smooth them for natural movement:

```rust
fn smooth_path(
    path: &[(usize, usize)],
    path_len: usize,
    grid: &Grid,
    smoothed: &mut [(f32, f32); MAX_PATH_LENGTH],
) -> usize {
    if path_len == 0 {
        return 0;
    }

    let mut count = 0;
    let (x, y) = grid.grid_to_world(path[0].0, path[0].1);
    smoothed[0] = (x, y);
    count = 1;

    let mut anchor = 0;

    for i in 2..path_len {
        // Check if we can skip intermediate nodes
        let (ax, ay) = path[anchor];
        let (ix, iy) = path[i];

        if !has_line_of_sight(grid, ax, ay, ix, iy) {
            // Can't skip, add previous point
            let (px, py) = path[i - 1];
            let (wx, wy) = grid.grid_to_world(px, py);
            smoothed[count] = (wx, wy);
            count += 1;
            anchor = i - 1;
        }
    }

    // Add final point
    let (fx, fy) = path[path_len - 1];
    let (wx, wy) = grid.grid_to_world(fx, fy);
    smoothed[count] = (wx, wy);
    count += 1;

    count
}

fn has_line_of_sight(grid: &Grid, x1: usize, y1: usize, x2: usize, y2: usize) -> bool {
    // Bresenham's line algorithm
    let dx = (x2 as i32 - x1 as i32).abs();
    let dy = (y2 as i32 - y1 as i32).abs();
    let sx = if x1 < x2 { 1i32 } else { -1 };
    let sy = if y1 < y2 { 1i32 } else { -1 };
    let mut err = dx - dy;

    let mut x = x1 as i32;
    let mut y = y1 as i32;

    while x != x2 as i32 || y != y2 as i32 {
        if !grid.is_walkable(x as usize, y as usize) {
            return false;
        }

        let e2 = 2 * err;
        if e2 > -dy {
            err -= dy;
            x += sx;
        }
        if e2 < dx {
            err += dx;
            y += sy;
        }
    }

    true
}
```

---

## Performance Tips

### Limit Repath Frequency

```rust
const REPATH_INTERVAL: u32 = 30;  // Every half second

impl Enemy {
    fn update_pathfinding(&mut self, player_x: f32, player_y: f32) {
        self.repath_timer = self.repath_timer.saturating_sub(1);

        if self.repath_timer == 0 {
            self.path_follower.repath(&GRID, self, player_x, player_y);
            self.repath_timer = REPATH_INTERVAL;
        }

        self.path_follower.update(self, &GRID);
    }
}
```

### Stagger Enemy Pathfinding

Don't update all enemies on the same frame:

```rust
fn update_enemies(enemies: &mut [Enemy], player_x: f32, player_y: f32, frame: u32) {
    for (i, enemy) in enemies.iter_mut().enumerate() {
        // Each enemy pathfinds on a different frame
        if (frame + i as u32) % REPATH_INTERVAL == 0 {
            enemy.path_follower.repath(&GRID, enemy, player_x, player_y);
        }
        enemy.path_follower.update(enemy, &GRID);
    }
}
```

### Precompute Static Paths

For patrol routes that never change:

```rust
static PATROL_ROUTES: [[usize; 8]; 4] = [
    [0, 1, 2, 3, 2, 1, 0, 0],  // Route 0
    [4, 5, 6, 7, 6, 5, 4, 4],  // Route 1
    // ...
];
```
