# Benchmarking

## State Snapshot Performance

For rollback netcode, state snapshot size affects performance:

| Size | Frame Budget | Status |
|------|--------------|--------|
| < 50 KB | < 1ms | Excellent |
| 50-100 KB | 1-2ms | Good |
| 100-200 KB | 2-4ms | Acceptable |
| > 200 KB | > 4ms | **Optimize** |

## Build Analysis

```bash
nether build --verbose
```

Shows:
- WASM binary size
- Asset pack size
- Individual asset sizes

## Performance Checklist

- [ ] State snapshot under 200 KB
- [ ] WASM binary under 2 MB
- [ ] Total ROM under 16 MB
- [ ] Sync test passes at 60fps
- [ ] No frame drops during gameplay

## Profiling Tips

1. **Measure state size**: Log size of your game state struct
2. **Track frame time**: Use `delta_time()` to detect spikes
3. **Asset audit**: Check largest textures/meshes in build output
