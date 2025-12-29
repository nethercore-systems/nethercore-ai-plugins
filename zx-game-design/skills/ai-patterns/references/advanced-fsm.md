# Advanced State Machines

Extended patterns beyond basic FSM for complex AI behaviors.

## Hierarchical State Machines (HFSM)

Nest states within states to reduce complexity.

### Structure

```rust
#[derive(Clone, Copy, PartialEq)]
enum CombatState {
    Approach,
    Circle,
    Attack,
    Recover,
}

#[derive(Clone, Copy, PartialEq)]
enum TopState {
    Idle,
    Combat(CombatState),
    Flee,
}

struct Enemy {
    state: TopState,
    // ...
}

impl Enemy {
    fn update(&mut self, player_x: f32, player_y: f32) {
        match self.state {
            TopState::Idle => self.update_idle(player_x, player_y),
            TopState::Combat(sub) => self.update_combat(sub, player_x, player_y),
            TopState::Flee => self.update_flee(player_x, player_y),
        }
    }

    fn update_combat(&mut self, sub: CombatState, player_x: f32, player_y: f32) {
        // Check for top-level transitions first
        if self.health < FLEE_THRESHOLD {
            self.state = TopState::Flee;
            return;
        }

        // Handle sub-states
        match sub {
            CombatState::Approach => {
                let dist = self.distance_to(player_x, player_y);
                if dist < ATTACK_RANGE {
                    self.state = TopState::Combat(CombatState::Attack);
                } else if dist < CIRCLE_RANGE {
                    self.state = TopState::Combat(CombatState::Circle);
                } else {
                    self.move_toward(player_x, player_y);
                }
            }
            CombatState::Circle => {
                self.circle_player(player_x, player_y);
                if self.state_timer == 0 {
                    self.state = TopState::Combat(CombatState::Attack);
                }
            }
            CombatState::Attack => {
                self.perform_attack();
                if self.attack_complete {
                    self.state = TopState::Combat(CombatState::Recover);
                    self.state_timer = RECOVERY_FRAMES;
                }
            }
            CombatState::Recover => {
                if self.state_timer == 0 {
                    self.state = TopState::Combat(CombatState::Circle);
                    self.state_timer = random_range(60, 120);
                }
            }
        }
    }
}
```

### Benefits

- Reduces transition complexity (combat sub-states don't need flee checks)
- Groups related behaviors
- Easier to add new combat moves without touching flee logic

---

## State with Entry/Exit Actions

Execute code when entering or leaving a state.

```rust
impl Enemy {
    fn transition(&mut self, new_state: EnemyState) {
        // Exit action for old state
        match self.state {
            EnemyState::Attack => {
                self.attack_frame = 0;  // Cancel attack animation
            }
            EnemyState::Chase => {
                // Play "lost target" sound
            }
            _ => {}
        }

        // Enter action for new state
        match new_state {
            EnemyState::Idle => {
                self.state_timer = random_range(60, 180);
            }
            EnemyState::Alert => {
                self.state_timer = ALERT_DURATION;
                // Play alert sound
            }
            EnemyState::Attack => {
                self.attack_frame = ATTACK_WINDUP;
                // Face player
            }
            _ => {}
        }

        self.state = new_state;
    }
}
```

---

## Behavior Trees (Simplified)

For more complex decision-making, behavior trees provide better modularity.

### Node Types

```rust
#[derive(Clone, Copy)]
enum NodeStatus {
    Success,
    Failure,
    Running,
}

trait BehaviorNode {
    fn tick(&mut self, enemy: &mut Enemy, ctx: &BehaviorContext) -> NodeStatus;
}

struct BehaviorContext {
    player_x: f32,
    player_y: f32,
    player_visible: bool,
    dt: f32,
}
```

### Selector (OR logic)

Tries children in order until one succeeds:

```rust
struct Selector {
    children: Vec<Box<dyn BehaviorNode>>,
    current: usize,
}

impl BehaviorNode for Selector {
    fn tick(&mut self, enemy: &mut Enemy, ctx: &BehaviorContext) -> NodeStatus {
        for i in self.current..self.children.len() {
            match self.children[i].tick(enemy, ctx) {
                NodeStatus::Success => {
                    self.current = 0;
                    return NodeStatus::Success;
                }
                NodeStatus::Running => {
                    self.current = i;
                    return NodeStatus::Running;
                }
                NodeStatus::Failure => continue,
            }
        }
        self.current = 0;
        NodeStatus::Failure
    }
}
```

### Sequence (AND logic)

Runs children in order, all must succeed:

```rust
struct Sequence {
    children: Vec<Box<dyn BehaviorNode>>,
    current: usize,
}

impl BehaviorNode for Sequence {
    fn tick(&mut self, enemy: &mut Enemy, ctx: &BehaviorContext) -> NodeStatus {
        for i in self.current..self.children.len() {
            match self.children[i].tick(enemy, ctx) {
                NodeStatus::Failure => {
                    self.current = 0;
                    return NodeStatus::Failure;
                }
                NodeStatus::Running => {
                    self.current = i;
                    return NodeStatus::Running;
                }
                NodeStatus::Success => continue,
            }
        }
        self.current = 0;
        NodeStatus::Success
    }
}
```

### Leaf Nodes (Actions and Conditions)

```rust
struct IsPlayerVisible;
impl BehaviorNode for IsPlayerVisible {
    fn tick(&mut self, _enemy: &mut Enemy, ctx: &BehaviorContext) -> NodeStatus {
        if ctx.player_visible { NodeStatus::Success } else { NodeStatus::Failure }
    }
}

struct ChasePlayer;
impl BehaviorNode for ChasePlayer {
    fn tick(&mut self, enemy: &mut Enemy, ctx: &BehaviorContext) -> NodeStatus {
        enemy.move_toward(ctx.player_x, ctx.player_y);
        if enemy.distance_to(ctx.player_x, ctx.player_y) < ATTACK_RANGE {
            NodeStatus::Success
        } else {
            NodeStatus::Running
        }
    }
}

struct AttackPlayer;
impl BehaviorNode for AttackPlayer {
    fn tick(&mut self, enemy: &mut Enemy, _ctx: &BehaviorContext) -> NodeStatus {
        if enemy.attack_frame == 0 {
            enemy.attack_frame = ATTACK_DURATION;
        }
        if enemy.attack_frame > 0 {
            enemy.attack_frame -= 1;
            NodeStatus::Running
        } else {
            NodeStatus::Success
        }
    }
}
```

### Building a Tree

```rust
fn create_enemy_behavior() -> Box<dyn BehaviorNode> {
    Box::new(Selector {
        children: vec![
            // Priority 1: Flee if low health
            Box::new(Sequence {
                children: vec![
                    Box::new(IsLowHealth),
                    Box::new(FleeFromPlayer),
                ],
                current: 0,
            }),
            // Priority 2: Attack if player visible
            Box::new(Sequence {
                children: vec![
                    Box::new(IsPlayerVisible),
                    Box::new(ChasePlayer),
                    Box::new(AttackPlayer),
                ],
                current: 0,
            }),
            // Priority 3: Patrol
            Box::new(Patrol),
        ],
        current: 0,
    })
}
```

---

## FSM vs Behavior Tree

| Aspect | FSM | Behavior Tree |
|--------|-----|---------------|
| Simplicity | Better for < 5 states | Better for complex AI |
| Reusability | States are monolithic | Nodes are composable |
| Debugging | Easy to visualize | Harder to trace |
| Memory | Minimal | More allocations |
| Recommendation | Most ZX games | Boss fights, complex NPCs |

For most ZX games, a well-structured FSM or HFSM is sufficient. Behavior trees add overhead but provide flexibility for complex enemy AI.

---

## Rollback Considerations

Both FSM and behavior tree state must be deterministic:

```rust
// All state must be serializable for rollback
#[derive(Clone)]
struct EnemyAI {
    state: EnemyState,
    state_timer: u32,
    attack_frame: u32,
    last_known_player: (f32, f32),
    memory_timer: u32,
    // For behavior trees: current node indices
    bt_current_child: [usize; MAX_BT_DEPTH],
}

impl EnemyAI {
    fn save_state(&self) -> EnemyAIState {
        // Clone all AI state for rollback
    }

    fn restore_state(&mut self, state: &EnemyAIState) {
        // Restore from saved state
    }
}
```
