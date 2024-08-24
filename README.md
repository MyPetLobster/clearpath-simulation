<div id="readme-top">

# ClearPath - Basic Intersection Simulation
### **By Cory Suzuki**
#### Sophia Learning: Introduction to Python Programming - Touchstone 4
#### Submitted on 8/24/2024

#### **Youtube Demo:** [ClearPath - Basic Intersection Simulation](https://youtu.be/-gR9btnFwes)
#### **Replit Link:** [ClearPath - Basic Intersection Simulation](https://replit.com/@CorySuzuki2/clearpath-simulation)

<img src="https://i.imgur.com/W6qoe6J.jpeg" width="300px">

</br>

This project is a simple simulation of ClearPath's Emergency Response Traffic System (ERTS) at a single intersection. The program will simulate traffic flow, emergency vehicle response, and the activation of 4-way blinking red lights to clear the path for emergency vehicles. The simulation allows you to toggle between ERTS Active and ERTS Inactive modes, as well as run an analysis to compare the collision rates of each mode. Built using Python and Pygame, this simulation provides a foundation for the development of ClearPath's real-world application.

</br>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
        <a href="#about-the-project">About the Project</a>
        <ul>
            <li><a href="#background">Background</a></li>
            <li><a href="#what-issues-does-clearpath-aim-to-solve">What Issues Does ClearPath Aim to Solve?</a></li>
            <li><a href="#what-is-clearpath-what-about-pats-and-erts">What is ClearPath? What about PATS and ERTS?</a></li>
            <li><a href="#why-i-built-this-simulation-how-it-works-what-it-does">Why I Built This Simulation, How It Works, What It Does</a></li>
        </ul>
    <li>
        <a href="#getting-started">Getting Started</a>
    </li>
    <li>
        <a href="#using-the-simulation">Using the Simulation</a>
        <ul>
            <li><a href="#simulation-overview">Simulation Overview</a></li>
            <li><a href="#simulation-controls">Simulation Controls</a></li>
            <li><a href="#analysis-mode">Analysis Mode</a></li>
            <ul>
                <li><a href="#weight-calculations-explained">Weight Calculations Explained</a></li>
                <li><a href="#extrapolated-collision-count">Extrapolated Collision Count</a></li>
            </ul>
        </ul>
    </li>
    <li>
        <a href="#screenshots">Screenshots</a>
    </li>
    <li>
        <a href="#conclusion">Conclusion</a>
    </li>
  </ol>
</details>

</br>
</br>

# About the Project 

### Background

I watch too many police pursuit videos and I'm always gritting my teeth every time I watch a suspect and pursuing officer fly through red lights. I've seen too many accidents happen at intersections during police pursuits. I've also seen too many videos of emergency vehicles getting stuck in traffic near congested intersections. I've always thought there must be a better way to handle these situations. And one day I had a really simple idea. Why not just turn all the lights to blinking red lights whenever an emergency vehicle is approaching? Or in the case of a pursuit, calculate a cone ahead of the chase and turn all the lights in that cone to blinking red? 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### What Issues Does ClearPath Aim to Solve?
 - **Emergency vehicles getting stuck in traffic** At a four-way stop, by nature there is a mostly open lane for emergency vehicles to use in every direction, making approaching, entering, and exiting the intersection much easier. This is especially important when the emergency vehicle is responding to a critical event where every second counts.

 -  **Accidents that occur at intersections during police pursuits/emergency responses** By automatically converting a standard red/yellow/green intersection into a blinking 4-way red, we can reduce the risk of accidents at intersections during police pursuits and emergency responses. The first clear benefit of this approach is that it requires no new physical infrastructure. It also doesn't require any kind of mass education campaign, as anyone with a drivers license should already know what to do at a blinking red light. The stop light also forces drivers to look both ways before entering the intersection, something most never think to do when a light is green. 
 
 **Note:** Although, not strictly necessary, a campaign to notify the public of the change would be beneficial and keep drivers on high alert when they approach a familiar intersection and see the lights blinking red.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### What is ClearPath? What about PATS and ERTS? 

So ClearPath is the overarching name of the project. Any research I do goes in the ClearPath directory. Any tools I build will be in the ClearPath directory, etc. PATS and ERTS are two tools that will be a part of ClearPath.

The Pursuit Activated Traffic System (PATS) will utilize real-time GPS data from emergency vehicles, traffic signal status from city management systems, and voice inputs from dispatchers to continuously track vehicle locations and predict their paths. AI will monitor dispatch communications for critical updates and extend the safety zone to include schools and public events when necessary. 

The Emergency Response Traffic System (ERTS) on the other hand, is a more general system and will itself be a part of PATS. ERTS will be implemented/activated by different means depending on existing infrastructure. If possible, ERTS will automatically be activated anytime an emergency vehicle is dispatched and has lights/sirens on (Code 3). The system will track the vehicle GPS coordinates along with the destination and queue up all the traffic signals that the vehicle will pass through. The system will then automatically convert these signals to 4-way blinking red lights to clear the path for the emergency vehicle. If the infrastructure does not support this, the system will rely on dispatchers to activate ERTS manually. 

In either situation, an AI "listener" is added to each event. The listener's job is to monitor the dispatch communications for critical updates. If the dispatcher mentions that the emergency vehicle is responding to a critical event, the listener will extend the safety zone to include schools and public events.

Many of these features are still only ideas. But this simulation is a proof of concept for the basic idea that less accidents will occur between civilians and emergency vehicles at intersections if all the lights are blinking red.

For further information or to see the status of the main ClearPath project, feel free to visit the [ClearPath GitHub repository](https://github.com/MyPetLobster/clearpath).

** As of the time of writing (8/19/2024), I've only just added some notes and research links to that repo. I just began working toward my degree, so won't have too much time for side projects. But I really want to turn this idea in to a real proposal that I can bring to a company or a city eventually, so I'll be working on it as much as I can.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Why I Built This Simulation, How It Works, What It Does

I've had this idea to build ClearPath as a personal project for a while now, but only recently started taking notes, researching statistics, and brainstorming ideas. I'm currently taking Sophia Learning's Introduction to Python Programming course. Prior to beginning this course, I already had some experience with Python. So I had two personal goals for this project. First, learn something new involving Python. I opted to learn the basics of PyGame. And two, actually build something that will help me toward building a full prototype for ClearPath.

Initially, I planned to simulate an entire city on a grid, but I realized that would be too much for this project. So I decided
to simulate a single intersection instead. This simulation models an intersection with traffic lights, civilian vehicles, and emergency vehicles. The sim allows you to toggle between two modes: ERTS Active and ERTS Inactive. In ERTS Active mode, the traffic light will turn into a 4-way blinking red light. In ERTS Inactive mode, the traffic light will operate as normal. You can toggle between the two modes by pressing the 'e' key when the sim is running. Each time you switch modes, the collision counter will reset to zero.

The simulation also has an analysis mode. When a user starts analysis mode (with 'a'), they can set the duration of the analysis and set whether or not they want the results to be exported to a JSON file. The analysis will split its run time between ERTS Active and ERTS Inactive modes and track the statistics separately. Before the results are displayed, some weighted calculations are performed to provide a fair comparison between the two modes. For more information on the weighted calculations, see the "Weight Calculations Explained" section below.

The analysis will then display the total number of civilian and emergency vehicles generated, the total number of collisions that occurred, the collision frequency per vehicle, the average weighted collision frequency, and the base weighted collision frequency.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>

# Getting Started

To run the simulation, you will need Python installed on your computer. You can download Python from the [official website](https://www.python.org/downloads/).

**Note: This project was built using Python 3.12.1, but should work with any version of Python 3.**

1. Clone the repository to your local machine.
2. Open a terminal window and navigate to the project directory.
3. Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```
**Note:**  The only dependency required for this project is `pygame`.  

**Note:** Gonna be honest, I did all my development on a Mac and when I tried using the sim on my Windows machine, I couldn't get PyGame installed. That's likely an issue with my old Windows machine, but just a heads up that this README will not be able to help you with any Windows-specific issues.

4. Run the simulation by executing the following command:

```bash
python main.py
```

5. Follow the on-screen instructions to interact with the simulation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>

# Using the Simulation

### Simulation Overview

The simulation consists of the following components:

1. **Intersection**: The main intersection where vehicles interact with traffic lights.
2. **Traffic Light**: Controls the flow of traffic at the intersection.
3. **Vehicle**: Represents a civilian vehicle that follows traffic rules.
4. **Emergency Vehicle**: Represents a vehicle responding to an emergency.
5. **Simulation**: Manages the simulation and its components.
6. **Analysis**: Runs the simulation for a set duration and displays/exports the results.

The simulation allows you to toggle between ERTS Active and ERTS Inactive modes, as well as run an analysis to compare the collision rates of each mode. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Simulation Controls

The simulation can be controlled using the following keys:

- **e**: Toggle between ERTS Active and ERTS Inactive modes.
- **a**: Begin an analysis of the simulation.
- **q/esc**: Quit the simulation.
- **p/space**: Pause/unpause the simulation.
- **r**: Reset the simulation.

- **Analysis Mode**: 
    - **up/down arrow keys**: Increase/decrease the duration of the analysis in increments of 60 seconds.
    - **left/right arrow keys**: Increase/decrease the duration of the analysis in increments of 5 seconds.
    - **e**: Toggle boolean to export results to a JSON file.
    - **a**: Reset the analysis settings.
    - **Enter or s**: Start the analysis with the current settings.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Analysis Mode

When activated, the user must set the duration of the analysis and choose whether to export the results to a JSON file. The analysis will then run for the specified duration, splitting the time between ERTS Active and ERTS Inactive modes. The simulation will track the number of civilian and emergency vehicles generated, as well as the number of collisions that occur in each mode.

The analysis mode will display the following results for each mode:

- Total number of civilian vehicles generated.
- Total number of emergency vehicles generated.
- Total number of collisions that occurred.
- Collision frequency per vehicle.
- Average Weighted Collision Frequency.
- Extrapolated Collision Count (ERTS Active only)
- Base Weighted Collision Frequency (ERTS Active only)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Weight Calculations Explained 

The weighting calculations in this analysis aim to provide a fair comparison between ERTS and no-ERTS scenarios by accounting for differences in vehicle distributions. The base weighted collision rate for ERTS adjusts for differences in the ratio of emergency vehicles to cars between the two phases. This is accomplished by comparing the ratio of emergency vehicles to civilian vehicles in the no-ERTS phase to the ratio in the ERTS phase. The base weighted collision rate for ERTS is then calculated by multiplying the ERTS collision rate by this ratio.

The average weighted collision rates for both ERTS and no-ERTS use the mean number of vehicles across both phases as a baseline. Each phase's collision rate is then adjusted based on how its specific vehicle counts deviate from this average. This method ensures that both phases are compared against a common standard, accounting for any variations in overall traffic volume or emergency vehicle frequency. These weighted rates provide a more nuanced view of the effectiveness of the ERTS system by normalizing the data and reducing the impact of random variations in vehicle generation between the two phases.

The formulas for calculating the weighted collision rates are as follows: 

```
base_weight_factor = (no_erts_emergency_ct / erts_emergency_ct) / (no_erts_civilian_ct / erts_civilian_ct)
erts_base_weighted_rate = ERTSCollisionRate * BaseWeightFactor

average_civilian_ct = (no_erts_civilian_ct + erts_civilian_ct) / 2
average_emergency_ct = (no_erts_emergency_ct + erts_emergency_ct) / 2

no_erts_weight_factor = (average_emergency_ct / no_erts_emergency_ct) / (average_civilian_ct / no_erts_civilian_ct)
erts_weight_factor = (average_emergency_ct / erts_emergency_ct) / (average_civilian_ct / erts_civilian_ct)

no_erts_avg_weighted_rate = no_erts_collision_rate * no_erts_weight_factor
erts_avg_weighted_rate = erts_collision_rate * erts_weight_factor
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Extrapolated Collision Count
After running the analysis while testing, the first thing that stood out to me was that the ERTS phase allowed much fewer cars to pass through the intersection in the same amount of time as the no-ERTS phase. While I believe that this is an acceptable downside to make intersections safer, it did make me realize that the collision rates were not directly comparable between the two phases. To address this issue, I added an extrapolated collision count to the analysis results.

The extrapolated collision count is a theoretical estimate of the total number of ERTS collisions that would occur if the sim was allowed to run long enough to generate the same number of vehicles as the no-ERTS phase. The extrapolation factor is calculated based on the number of cars generated in the no-ERTS phase compared to the ERTS phase. This factor is then used to adjust the ERTS collision count to account for the difference in vehicle volume between the two phases. The extrapolated collision count provides a more accurate representation of the potential impact of ERTS on collision rates by normalizing the data based on vehicle generation rates.

The formula for calculating the extrapolated collision count is as follows:

```
        extrapolation_factor = self.no_erts_car_count / self.erts_car_count
        self.erts_extrapolated_collisions = self.erts_collision_count * extrapolation_factor
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>

# Screenshots
<p>Basic Simulation Mode</p>
<img src="https://i.imgur.com/W6qoe6J.jpeg" width="500px">
<hr>
<p>Analysis Settings</p>
<img src="https://i.imgur.com/id1hvSi.jpeg" width="500px">
<hr>
<p>Analysis Mode - ERTS Inactive</p>
<img src="https://i.imgur.com/IfWG3mt.jpeg" width="500px">
<hr>
<p>Analysis Mode - ERTS Active</p>
<img src="https://i.imgur.com/5Sdplue.jpeg" width="500px">
<hr>
<p>Analysis Results - Pygame Window</p>
<img src="https://i.imgur.com/HJywVgq.jpeg" width="500px">
<hr>
<p>Analysis Results - JSON File</p>
<img src="https://i.imgur.com/BrHlI07.png" width="500px">



# Conclusion
This simulation provides a basic demonstration of ClearPath's Emergency Response Traffic System (ERTS) at a single intersection. By toggling between ERTS Active and ERTS Inactive modes, users can observe the impact of the system on collision rates and traffic flow. The analysis mode offers a detailed comparison of the two modes, including collision frequencies, weighted rates, and extrapolated collision counts. These results provide valuable insights into the potential benefits of implementing ERTS in real-world scenarios, highlighting the system's ability to enhance public safety and reduce intersection accidents.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
</br>