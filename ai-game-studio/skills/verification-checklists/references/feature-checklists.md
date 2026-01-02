# Feature Verification Checklists

## Game Feature (General)

- [ ] Module file exists: `src/[feature].rs`
- [ ] Module declared in lib.rs: `mod [feature];`
- [ ] No incomplete code markers (TODO/FIXME/unimplemented!)
- [ ] All match arms implemented
- [ ] Build succeeds
- [ ] State struct defined
- [ ] State initialized in init()
- [ ] Update logic called in update()
- [ ] Render logic called in render()

## Visual Feature

All of Game Feature PLUS:

- [ ] draw_* function called (mesh/sprite/text/etc)
- [ ] Correct texture bound before drawing
- [ ] Camera/viewport correct
- [ ] Render order correct (not hidden)
- [ ] Player would see it

## Interactive Feature

All of Game Feature PLUS:

- [ ] Input is read (input_*/button_*/gamepad_*)
- [ ] Input affects state
- [ ] State change is visible
- [ ] Feedback is immediate

## Audio Feature

All of Game Feature PLUS:

- [ ] Sound file exists and integrated
- [ ] Trigger event occurs
- [ ] sound_play() called at trigger
- [ ] Sound actually plays in game

## After Implementation

- [ ] Module exists and declared
- [ ] No TODO/FIXME markers
- [ ] Init/Update/Render hooked up
- [ ] Build succeeds
- [ ] Feature works in running game
- [ ] Player would notice feature

## After Bug Fix

- [ ] Original issue no longer occurs
- [ ] No new issues introduced
- [ ] Build still succeeds
- [ ] Sync test still passes (if multiplayer)
