# ClearPath - Basic Intersection Simulation

Simulation of ClearPath's Traffic Safety Systems, including the Emergency Response Traffic System (ERTS) and the Pursuit 
Activated Traffic System (PATS).

## Background

ClearPath aims to enhance public safety by automatically converting traffic signals into 4-way blinking red stop lights in the path of emergency vehicles and police pursuits, reducing the risk of intersection accidents. 

The Pursuit Activated Traffic System (PATS) will utilize real-time GPS data from emergency vehicles, traffic signal status from city management systems, and voice inputs from dispatchers to continuously track vehicle locations and predict their paths. AI will monitor dispatch communications for critical updates and extend the safety zone to include schools and public events when necessary. 

The Emergency Response Traffic System (ERTS) on the other hand, is a more general system and will itself be a part of PATS. ERTS will be activated by different means depending on existing infrastructure. If possible, ERTS will automatically be activated anytime an emergency vehicle is dispatched and has lights/sirens on. The system will track the vehicle GPS coordinates along with the destination and queue up all the traffic signals that the vehicle will pass through. The system will then automatically convert these signals to 4-way blinking red lights to clear the path for the emergency vehicle. If the infrastructure does not support this, the system will rely on dispatchers to activate ERTS manually. 

In either situation, an AI "listener" is added to each event. The listener's job is to monitor the dispatch communications for critical updates. If the dispatcher mentions that the emergency vehicle is responding to a critical event, the listener will extend the safety zone to include schools and public events.

By automating these safety measures, ClearPath seeks to create a safer environment for both responders and the public, minimizing accidents and ensuring efficient emergency responses. This project will demonstrate the system's basic functionality through a Python simulation, providing a foundation for real-world application and highlighting the system's potential benefits.

For further information or to see the status of the main ClearPath project, feel free to visit the [ClearPath GitHub repository](https://github.com/MyPetLobster/clearpath).

** As of the time of writing (8/19/2024), I've only just added some notes and research links to that repo. I just began working toward my degree, so won't have too much time for side projects. But I really want to turn this idea in to a real proposal that I can bring to a company or a city eventually, so I'll be working on it as much as I can.


### About this project

I've had this idea to build ClearPath as a personal project for a while now, but only recently started taking notes, researching statistics, and brainstorming ideas. I'm currently taking Sophia Learning's Introduction to Python Programming course. Prior to beginning this course, I already had some prior experience with Python. So instead of doing the bare minimum for this final project, I decided to actually build something that, will help me toward building a full prototype for ClearPath. 

Initially, I planned to simulate an entire city on a grid, but I realized that would be too much for this project. So I decided
to simulate a single intersection instead. This simulation models an intersection with traffic lights, civilian vehicles, and emergency vehicles. The sim allows you to toggle between two modes: ERTS Active and ERTS Inactive. In ERTS Active mode, the traffic light will turn into a 4-way blinking red light. In ERTS Inactive mode, the traffic light will operate as normal. You can toggle between the two modes by pressing the 'e' key when the sim is running. 

The simulation also has an analysis mode. Beginning an analysis will run the simulation for a set duration (defined in config.py) 
and display the results on the screen. The analysis will split its run time between ERTS Active and ERTS Inactive modes and track the statistics separately. Before the results are displayed, a weighted collision frequency is calculated based on the number of vehicles and emergency vehicles generated during each mode and the number of collisions that occurred.


## Getting Started

To run the simulation, you will need Python installed on your computer. You can download Python from the [official website](https://www.python.org/downloads/).

**Note: This project was built using Python 3.12.1, but should work with any version of Python 3.**

1. Clone the repository to your local machine.
2. Open a terminal window and navigate to the project directory.
3. Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```
**Note: The only dependency required for this project is `pygame`.**
**Note: Gonna be honest, I did all my development on a Mac and when I tried using the sim on my Windows machine, I couldn't get PyGame installed. That's likely an issue with my old Windows machine, but just a heads up that this README will not be able to help you with any Windows-specific issues.**

4. Run the simulation by executing the following command:

```bash
python main.py
```

5. Follow the on-screen instructions to interact with the simulation.


## Simulation Overview

The simulation consists of the following components:

1. **Intersection**: The main intersection where vehicles interact with traffic lights.
2. **Traffic Light**: Controls the flow of traffic at the intersection.
3. **Vehicle**: Represents a civilian vehicle that follows traffic rules.
4. **Emergency Vehicle**: Represents a vehicle responding to an emergency.
5. **Simulation**: Manages the simulation and its components.
6. **Analysis**: Runs the simulation for a set duration and displays the results.

The simulation allows you to toggle between ERTS Active and ERTS Inactive modes, as well as run an analysis to compare the collision rates of each mode. 

## Simulation Controls

The simulation can be controlled using the following keys:

- **e**: Toggle between ERTS Active and ERTS Inactive modes.
- **a**: Begin an analysis of the simulation.
- **q/esc**: Quit the simulation.
- **p/space**: Pause/unpause the simulation.
- **r**: Reset the simulation.

## Simulation Results

The analysis mode will display the following results for each mode:

- Total number of civilian vehicles generated.
- Total number of emergency vehicles generated.
- Total number of collisions that occurred.
- Collision frequency per vehicle.
- Weighted collision frequency based on the number of vehicles and emergency vehicles generated.

The weighted collision frequency is calculated as follows:

```
erts_weighted_collision_rate = erts_collision_rate * weighting_factor
```

