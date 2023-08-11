# Level creation guide 🛠️🎮

## General Structure 

Your level file should be a JSON file with the following main sections:

- **floors**: Platforms your agent can walk on.
- **walls**: Obstructions that can block your agent's path.
- **spikes**: Dangerous hazards your agent should avoid.
- **enemies**: TODO.
- **finish**: The goal your agent aims to reach.

## Sections Breakdown

### 1. Floors & Walls 🧱

Platforms and obstructions have similar properties:

- **shape**: The shape of the object. For this example, it's `"rect"`.
- **type**: The type of the object (can be `"platform"` for floors or `"wall"` for walls).
- **x, y**: The starting coordinates of the object.
- **width, height**: Dimensions of the object.

**Example**:

```json
{
  "shape": "rect",
  "type": "platform",
  "x": 0,
  "y": 650,
  "width": 150,
  "height": 10
}
```

### 2. Spikes ⚠️

Hazardous objects with properties:

- **shape**: "triangle" for this example.
- **type**: "spike" to denote hazard.
- **scale**: The size factor of the spike.
- **internal_angle**: The interior angle of the spike (45° is common).
- **rotation**: The orientation of the spike. A rotation of 0 means the spike points upwards.
- **x, y**: The starting coordinates of the spike.
- **rotor**: A boolean that specifies if the spike rotates (true or false).
- **angle**: The degree of rotation per time span if the spike is a rotor.

**Example**:
```json
{
  "shape": "triangle",
  "type": "spike",
  "scale": 25,
  "internal_angle": 45,
  "rotation": 0,
  "x": 150,
  "y": 575,
  "rotor": true,
  "angle": 5
}
```

### 3. Finish 🏁

The endpoint your agent should reach:

- **shape**: "rect" denotes the shape.
- **type**: "finish" denotes the end goal.
- **x, y**: Starting coordinates.
- **width, height**: Dimensions of the finish platform.

**Example**:
```json
{
  "shape": "rect",
  "type": "finish",
  "x": 950,
  "y": 650,
  "width": 100,
  "height": 10
}
```
## Wrapping Up 💾 🎯
Once you've defined your custom level, save it as a .json file, put under `levels` directory and in config specify the name of your level: `"start_level": "<name>"`. Then load it into the game. Happy designing and playing!
