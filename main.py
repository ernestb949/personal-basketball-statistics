from drafter import *
from dataclasses import dataclass


@dataclass
class Game:
    """Stores the information and statistics from one basketball game"""
    opponent: str
    date: str
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int


@dataclass
class State:
    """Stores the information shared between the website's pages"""
    games: list[Game]
    athlete_name: str
    points_goal: int
    selected_game: int
    message: str


@route
def index(state: State) -> Page:
    """Displays the home page with links to other sections"""
    return Page(state, [
        Header("Basketball Statistics Tracker"),
        "Welcome to your personal basketball statistics tracker!",
        "Record games, track your performance, and monitor your progress.",
        Link("Dashboard", "/dashboard"),
        Link("Add a Game", "/add_game"),
        Link("Game History", "/history"),
        Link("Statistics", "/averages"),
        Link("Goals", "/goals"),
        Link("Settings", "/settings")
    ])


@route
def dashboard(state: State) -> Page:
    """Displays the player's total games, total points, and points per game"""
    total_points = 0
    total_games = 0

    # Add the points from every recorded game.
    for game in state.games:
        total_points += game.points
        total_games += 1

    # Calculate the average only if games have been recorded.
    if total_games > 0:
        average_points = total_points / total_games
    else:
        average_points = 0

    return Page(state, [
        Header("Basketball Dashboard"),
        "Player: " + state.athlete_name,
        "Games Played: " + str(total_games),
        "Total Points: " + str(total_points),
        "Points Per Game: " + str(round(average_points, 2)),
        Link("Home", "/"),
        Link("Add Game", "/add_game")
    ])


@route
def add_game(state: State) -> Page:
    """Displays input boxes for recording a new basketball game"""
    return Page(state, [
        Header("Add a Basketball Game"),
        "Enter your game statistics below:",
        TextBox("opponent", "Opponent"),
        TextBox("date", "Date"),
        NumberBox("points", 0),
        NumberBox("rebounds", 0),
        NumberBox("assists", 0),
        NumberBox("steals", 0),
        NumberBox("blocks", 0),
        Button("Save Game", "/save_game"),
        Link("Home", "/")
    ])


@route
def save_game(state: State, opponent: str, date: str,
              points: int, rebounds: int, assists: int,
              steals: int, blocks: int) -> Page:
    """Validates the user's inputs and saves a new game to the state"""

    # Make sure the required text fields are not empty.
    if opponent.strip() == "" or date.strip() == "":
        return Page(state, [
            Header("Error"),
            "Please enter an opponent and date.",
            Link("Try Again", "/add_game")
        ])

    # Prevent negative statistics.
    if (points < 0 or rebounds < 0 or assists < 0
            or steals < 0 or blocks < 0):
        return Page(state, [
            Header("Error"),
            "Statistics cannot be negative.",
            Link("Try Again", "/add_game")
        ])

    # Create a new Game object using the submitted information.
    new_game = Game(opponent, date, points, rebounds,
                    assists, steals, blocks)

    # Add the new game without changing the original list.
    new_games = state.games + [new_game]

    new_state = State(
        new_games,
        state.athlete_name,
        state.points_goal,
        state.selected_game,
        "Game successfully saved!"
    )

    return Page(new_state, [
        Header("Game Saved!"),
        "Your basketball statistics have been recorded.",
        Link("Dashboard", "/dashboard"),
        Link("Game History", "/history")
    ])


@route
def history(state: State) -> Page:
    """Displays a list of all the previously recorded basketball games"""
    game_list = []

    # Create a description for each recorded game.
    for game in state.games:
        game_list.append(
            game.date + " vs. " + game.opponent
            + " | Points: " + str(game.points)
        )

    # Display a message if there are no recorded games.
    if len(game_list) == 0:
        game_list.append("No games have been recorded yet.")

    return Page(state, [
        Header("Game History"),
        BulletedList(game_list),
        "Enter a game number to view its details (starting at 0):",
        NumberBox("game_index", 0),
        Button("View Game", "/game_details"),
        Link("Add Game", "/add_game"),
        Link("Home", "/")
    ])


@route
def game_details(state: State, game_index: int) -> Page:
    """Displays the individual statistics for a selected game"""

    # Check whether the selected game number is valid.
    if game_index < 0 or game_index >= len(state.games):
        return Page(state, [
            Header("Invalid Game"),
            "That game number does not exist.",
            Link("Game History", "/history")
        ])

    # Retrieve the selected game.
    game = state.games[game_index]

    new_state = State(
        state.games,
        state.athlete_name,
        state.points_goal,
        game_index,
        state.message
    )

    return Page(new_state, [
        Header("Game Details"),
        "Opponent: " + game.opponent,
        "Date: " + game.date,
        "Points: " + str(game.points),
        "Rebounds: " + str(game.rebounds),
        "Assists: " + str(game.assists),
        "Steals: " + str(game.steals),
        "Blocks: " + str(game.blocks),
        Link("Game History", "/history"),
        Link("Home", "/")
    ])


@route
def averages(state: State) -> Page:
    """Calculates and displays the player's average statistics for their games"""
    total_points = 0
    total_rebounds = 0
    total_assists = 0
    total_games = 0

    # Add together the statistics from every game.
    for game in state.games:
        total_points += game.points
        total_rebounds += game.rebounds
        total_assists += game.assists
        total_games += 1

    # Calculate averages if at least one game exists.
    if total_games > 0:
        points_average = total_points / total_games
        rebounds_average = total_rebounds / total_games
        assists_average = total_assists / total_games
    else:
        points_average = 0
        rebounds_average = 0
        assists_average = 0

    return Page(state, [
        Header("Basketball Statistics"),
        "Points Per Game: " + str(round(points_average, 2)),
        "Rebounds Per Game: " + str(round(rebounds_average, 2)),
        "Assists Per Game: " + str(round(assists_average, 2)),
        Link("Dashboard", "/dashboard"),
        Link("Home", "/")
    ])


@route
def goals(state: State) -> Page:
    """Displays the player's current points goal with an input to change it"""
    return Page(state, [
        Header("Basketball Goals"),
        "Current Points Goal: " + str(state.points_goal),
        "Set a new points goal:",
        NumberBox("new_goal", state.points_goal),
        Button("Update Goal", "/update_goal"),
        Link("Home", "/")
    ])


@route
def update_goal(state: State, new_goal: int) -> Page:
    """Validates and updates the player's points goal"""

    # Goals must be positive numbers.
    if new_goal <= 0:
        return Page(state, [
            Header("Invalid Goal"),
            "Your goal must be greater than zero.",
            Link("Try Again", "/goals")
        ])

    new_state = State(
        state.games,
        state.athlete_name,
        new_goal,
        state.selected_game,
        state.message
    )

    return Page(new_state, [
        Header("Goal Updated"),
        "Your new points goal is " + str(new_goal),
        Link("Goals", "/goals"),
        Link("Home", "/")
    ])


@route
def settings(state: State) -> Page:
    """Displays the player's current name and gives an option to change it"""
    return Page(state, [
        Header("Settings"),
        "Current Player: " + state.athlete_name,
        TextBox("new_name", state.athlete_name),
        Button("Update Name", "/update_name"),
        Link("Home", "/")
    ])


@route
def update_name(state: State, new_name: str) -> Page:
    """Validates and updates the player's name"""

    # Make sure the name is not empty.
    if new_name.strip() == "":
        return Page(state, [
            Header("Invalid Name"),
            "Please enter a name.",
            Link("Try Again", "/settings")
        ])

    new_state = State(
        state.games,
        new_name,
        state.points_goal,
        state.selected_game,
        state.message
    )

    return Page(new_state, [
        Header("Name Updated"),
        "Your player name is now " + new_name,
        Link("Home", "/")
    ])


set_website_title("Basketball Statistics Tracker")

set_site_information(
    author="Ernest Barnes",
    description="A website for recording basketball game statistics, tracking performance, and setting goals.",
    sources="Created using Python and the Drafter library.",
    planning=[],
    links=[]
)

hide_debug_information()
set_website_framed(False)

start_server(State([], "Player", 20, -1, ""))
