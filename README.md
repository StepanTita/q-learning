# Q-Learning game with epsilon-greedy algorithm 🎮 🧠

This is a university project.
The game with basic level editing. One can add obstacles, enemies, and bonuses on the level by putting those in the JSON file. That way creating and editing test environments is as easy as adding a couple of rows to the JSON file. After the level is built, one should initialize some basic parameters and see the model performance. Based on that, one may consider updating or keeping the parameters. The game itself is just a set of primitives. The objects can either be static or moving.
We also introduce the concept of **reward backpropagation** in this project. 

More precise description of the solution and full report please find in the [REPORT](report.pdf)

## Demo:
![Game Demo](path_to_game_demo_gif_or_screenshot)

## Features 🚀
- **Q-Learning Powered**: Experience a game environment influenced by Q-Learning.
- **Epsilon-Greedy Strategy**: Watch the game evolve and adapt its strategy over time.
- **Custom Levels**: Design and play on your very own levels using straightforward JSON structures:

_*.json level file_
```json
{
  "floors": [
    {
      "shape": "rect",
      "type": "platform",
      "x": 0,
      "y": 650,
      "width": 150,
      "height": 10
    }
  ],
  "walls": [
    {
      "shape": "rect",
      "type": "wall",
      "x": 800,
      "y": 400,
      "width": 10,
      "height": 300
    }
  ],
  "spikes": [
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
  ],
  "finish": {
    "shape": "rect",
    "type": "finish",
    "x": 950,
    "y": 650,
    "width": 100,
    "height": 10
  }
}
```

## Tech Stack 📚
- [Python](https://www.python.org/)
- Reinforcement Learning: Q-Learning with epsilon-greedy algorithm
- Reward backpropagation concept. Please find detailed description in the [REPORT](report.pdf)

## Getting Started 🏁

### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository:
```bash
git clone https://github.com/StepanTita/q-learning.git
```
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Run the game:
```bash
python main.py
```

or

4. Run the game in reinforcement learning mode:
```bash
cd reiforcement # make sure you are in the correct direction
python main.py
```

## Level Creation 🌍
Create custom levels using JSON files. Refer to the [level creation guide](level-creation-guide.md) to learn about the structure and possibilities!

## License 📄

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.

## TODO:
- enemies