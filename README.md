# CHECK24-BEST-COMBINATION-CHALLENGE

## Approach
1. I conceptualized the entire problem as a **set-cover problem** to leverage Integer Linear Programming (ILP) for finding the best possible solution quickly.
2. In the file `algorithms_comparison.ipynb`, I tested both a heuristic approach and the optimal ILP approach to observe the time differences between the two methods.
3. Since the time difference was minimal, I opted for the fastest solution for the user. The program is designed to first use the greedy algorithm to quickly provide the user with a possible solution. The user can review whether this matches their expectations while being informed that the optimal solution is still being computed — a behavior commonly seen in comparison portals.
4. If the optimal solution differs from the heuristic one, the new table is displayed to the user.
5. After both calculations, the program generates additional useful information, such as uncovered games, leagues fully/partially/not covered by the selected streaming providers, and a comprehensive list of all games offered by the streaming providers.
- **Technologies**: The user interface was created using Streamlit.
- **Optimazation**: The primary optimization opportunity lies in improving the presentation of information. Using graphs and a better layout can significantly enhance readability and clarity. Additionally, implementing a calculation based on the monthly price would be a valuable step to explore whether there are more cost-effective options for watching the games.

## How to run locally
Follow these steps to run the project locally:

### Prerequisites
- **Python 3.8 or higher** installed.
- **Pip** installed (usually bundled with Python).
- **Optional dependencies**: Docker (if desired).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sebus1208/check24-best-combination-challenge.git
   cd https://github.com/sebus1208/check24-best-combination-challenge.git
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run the application
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the application in your browser:
   - By default, the app will be available at [http://localhost:8501](http://localhost:8501).

## Project Structure
Describe the structure of the project:
```
project/
├── app.py                # Main file for the Streamlit app
├── algorithmen_comparison.ipynb  # Compare greedy and ILP solution
├── calc.py               # Logic for project calculations
├── present.py            # Presentation logic (tables and outputs)
├── data/                 # Folder containing CSV files
│   ├── bc_game.csv
│   ├── bc_streaming_offer.csv
│   └── bc_streaming_package.csv
├── assets/               # Additional resources
├── requirements.txt      # List of dependencies
└── README.md             # Project description
```

## Features
- Select favorite teams through a user-friendly interface.
- Calculate the optimal combination of streaming providers.
- Display uncovered games.
- Detailed cost coverage information.
