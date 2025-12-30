# Soft Materials (Fabrics, Leather, Plastic)

```python
from dataclasses import dataclass

@dataclass
class PbrParams:
    base_color: tuple[float, float, float]
    metallic: float
    roughness: float
    normal_strength: float
    ao_strength: float
    emission: float
    ior: float
```

## Fabrics

### fabric.cotton
Plain cotton fabric.
```python
MATERIALS = {
    "fabric.cotton": PbrParams(
        base_color=(0.85, 0.83, 0.8), metallic=0.0, roughness=0.9,
        normal_strength=0.4, ao_strength=0.5, emission=0.0, ior=1.5,
    ),
}
```

### fabric.silk
Smooth, shiny silk.
```python
MATERIALS = {
    "fabric.silk": PbrParams(
        base_color=(0.9, 0.85, 0.8), metallic=0.0, roughness=0.25,
        normal_strength=0.3, ao_strength=0.3, emission=0.0, ior=1.5,
    ),
}
```

### fabric.velvet
Soft velvet with sheen.
```python
MATERIALS = {
    "fabric.velvet": PbrParams(
        base_color=(0.3, 0.1, 0.15), metallic=0.0, roughness=0.7,
        normal_strength=0.5, ao_strength=0.6, emission=0.0, ior=1.5,
    ),
}
```

### fabric.wool / fabric.burlap / fabric.synthetic
```python
FABRIC_VARIANTS = {
    "fabric.wool": {"roughness": 0.95, "normal_strength": 0.6},
    "fabric.burlap": {"roughness": 0.95, "normal_strength": 0.9},
    "fabric.synthetic": {"roughness": 0.6, "normal_strength": 0.3},
}
```

---

## Leathers

### leather.brown
Classic brown leather.
```python
MATERIALS = {
    "leather.brown": PbrParams(
        base_color=(0.45, 0.3, 0.2), metallic=0.0, roughness=0.55,
        normal_strength=0.7, ao_strength=0.5, emission=0.0, ior=1.5,
    ),
}
```

### leather.worn
Aged, worn leather.
```python
MATERIALS = {
    "leather.worn": PbrParams(
        base_color=(0.4, 0.32, 0.25), metallic=0.0, roughness=0.75,
        normal_strength=0.9, ao_strength=0.7, emission=0.0, ior=1.5,
    ),
}
```

### leather.fine
High-quality polished leather.
```python
MATERIALS = {
    "leather.fine": PbrParams(
        base_color=(0.25, 0.15, 0.1), metallic=0.0, roughness=0.35,
        normal_strength=0.5, ao_strength=0.4, emission=0.0, ior=1.5,
    ),
}
```

---

## Plastics

### plastic.glossy
Shiny plastic.
```python
MATERIALS = {
    "plastic.glossy": PbrParams(
        base_color=(0.8, 0.2, 0.2), metallic=0.0, roughness=0.15,
        normal_strength=0.2, ao_strength=0.3, emission=0.0, ior=1.5,
    ),
}
```

### plastic.matte
Matte plastic finish.
```python
MATERIALS = {
    "plastic.matte": PbrParams(
        base_color=(0.5, 0.5, 0.5), metallic=0.0, roughness=0.7,
        normal_strength=0.2, ao_strength=0.4, emission=0.0, ior=1.5,
    ),
}
```

### plastic.rubber
Rubber material.
```python
MATERIALS = {
    "plastic.rubber": PbrParams(
        base_color=(0.15, 0.15, 0.15), metallic=0.0, roughness=0.9,
        normal_strength=0.4, ao_strength=0.5, emission=0.0, ior=1.5,
    ),
}
```

### plastic.translucent
Semi-transparent plastic.
```python
MATERIALS = {
    "plastic.translucent": PbrParams(
        base_color=(0.9, 0.9, 0.95), metallic=0.0, roughness=0.2,
        normal_strength=0.1, ao_strength=0.2, emission=0.0, ior=1.45,
    ),
}
```
