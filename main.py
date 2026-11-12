from drafter import *
from dataclasses import dataclass


set_website_title("Basketball Statistics Tracker")

set_site_information(
    author="Ernest Barnes",
    description="A website for recording basketball game statistics, tracking performance, and setting goals.",
    sources="Created using Python and the Drafter library.",
    planning="",
    links=[]
)

hide_debug_information()
set_website_framed(False)


@dataclass
class Game:
    """Stores the information and statistics from one basketball game."""
    opponent: str
    date: str
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int


@dataclass
class State:
    """Stores the information shared between the website's pages."""
    games: list[Game]
    athlete_name: str
    points_goal: int
    selected_game: int
    message: str


@route
def index(state: State) -> Page:
    """Displays the home page with links to other sections."""
    return Page(state, [
        Header("Basketball Statistics Tracker"),
        "Welcome to your personal basketball statistics tracker!",
        "Record games, track your performance, and monitor your progress.",
        "<br>",
        Link("Dashboard", "/player_dashboard"),
        "<br>",
        Link("Add a Game", "/add_game"),
        "<br>",
        Link("Game History", "/history"),
        "<br>",
        Link("Statistics", "/averages"),
        "<br>",
        Link("Goals", "/goals"),
        "<br>",
        Link("Settings", "/settings")
    ])


@route
def player_dashboard(state: State) -> Page:
    """Displays the player's total games, total points, and points per game."""
    total_points = 0
    total_games = 0

    for game in state.games:
        total_points += game.points
        total_games += 1

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
        "<br>",
        Link("Home", "/"),
        "<br>",
        Link("Add Game", "/add_game")
    ])


@route
def add_game(state: State) -> Page:
    """Displays input boxes for recording a new basketball game."""
    return Page(state, [
        Header("Add a Basketball Game"),
        "Enter the opponent:",
        TextBox("opponent", "Opponent"),
        "Enter the date:",
        TextBox("date", "Date"),
        "Enter points:",
        TextBox("points", 0, kind="number"),
        "Enter rebounds:",
        TextBox("rebounds", 0, kind="number"),
        "Enter assists:",
        TextBox("assists", 0, kind="number"),
        "Enter steals:",
        TextBox("steals", 0, kind="number"),
        "Enter blocks:",
        TextBox("blocks", 0, kind="number"),
        "<br>",
        Button("Save Game", "/save_game"),
        "<br>",
        Link("Home", "/")
    ])


@route
def save_game(state: State, opponent: str, date: str,
              points: int, rebounds: int, assists: int,
              steals: int, blocks: int) -> Page:
    """Validates the user's inputs and saves a new game."""

    if opponent.strip() == "" or date.strip() == "":
        return Page(state, [
            Header("Error"),
            "Please enter an opponent and date.",
            "<br>",
            Link("Try Again", "/add_game")
        ])

    if (points < 0 or rebounds < 0 or assists < 0
            or steals < 0 or blocks < 0):
        return Page(state, [
            Header("Error"),
            "Statistics cannot be negative.",
            "<br>",
            Link("Try Again", "/add_game")
        ])

    new_game = Game(
        opponent, date, points, rebounds,
        assists, steals, blocks
    )

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
        "<br>",
        Link("Dashboard", "/player_dashboard"),
        "<br>",
        Link("Game History", "/history")
    ])


@route
def history(state: State) -> Page:
    """Displays a list of all previously recorded basketball games."""
    game_list = []

    for game in state.games:
        game_list.append(
            game.date + " vs. " + game.opponent
            + " | Points: " + str(game.points)
        )

    if len(game_list) == 0:
        game_list.append("No games have been recorded yet.")

    return Page(state, [
        Header("Game History"),
        BulletedList(game_list),
        "Enter a game number to view its details (starting at 0):",
        TextBox("game_index", 0, kind="number"),
        "<br>",
        Button("View Game", "/game_details"),
        "<br>",
        Link("Add Game", "/add_game"),
        "<br>",
        Link("Home", "/")
    ])


@route
def game_details(state: State, game_index: int) -> Page:
    """Displays the individual statistics for a selected game."""

    if game_index < 0 or game_index >= len(state.games):
        return Page(state, [
            Header("Invalid Game"),
            "That game number does not exist.",
            "<br>",
            Link("Game History", "/history")
        ])

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
        "<br>",
        Link("Game History", "/history"),
        "<br>",
        Link("Home", "/")
    ])


@route
def averages(state: State) -> Page:
    """Calculates and displays the player's average statistics."""
    total_points = 0
    total_rebounds = 0
    total_assists = 0
    total_steals = 0
    total_blocks = 0
    total_games = 0

    for game in state.games:
        total_points += game.points
        total_rebounds += game.rebounds
        total_assists += game.assists
        total_steals += game.steals
        total_blocks += game.blocks
        total_games += 1

    if total_games > 0:
        points_average = total_points / total_games
        rebounds_average = total_rebounds / total_games
        assists_average = total_assists / total_games
        steals_average = total_steals / total_games
        blocks_average = total_blocks / total_games
    else:
        points_average = 0
        rebounds_average = 0
        assists_average = 0
        steals_average = 0
        blocks_average = 0

    return Page(state, [
        Header("Basketball Statistics"),
        "Points Per Game: " + str(round(points_average, 2)),
        "Rebounds Per Game: " + str(round(rebounds_average, 2)),
        "Assists Per Game: " + str(round(assists_average, 2)),
        "Steals Per Game: " + str(round(steals_average, 2)),
        "Blocks Per Game: " + str(round(blocks_average, 2)),
        "<br>",
        Link("Dashboard", "/player_dashboard"),
        "<br>",
        Link("Home", "/")
    ])


@route
def goals(state: State) -> Page:
    """Displays the player's current points goal."""
    return Page(state, [
        Header("Basketball Goals"),
        "Current Points Goal: " + str(state.points_goal),
        "Set a new points goal:",
        TextBox("new_goal", state.points_goal, kind="number"),
        "<br>",
        Button("Update Goal", "/update_goal"),
        "<br>",
        Link("Home", "/")
    ])


@route
def update_goal(state: State, new_goal: int) -> Page:
    """Validates and updates the player's points goal."""

    if new_goal <= 0:
        return Page(state, [
            Header("Invalid Goal"),
            "Your goal must be greater than zero.",
            "<br>",
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
        "<br>",
        Link("Goals", "/goals"),
        "<br>",
        Link("Home", "/")
    ])


@route
def settings(state: State) -> Page:
    """Displays the player's current name and allows it to be changed."""
    return Page(state, [
        Header("Settings"),
        "Current Player: " + state.athlete_name,
        TextBox("new_name", state.athlete_name),
        "<br>",
        Button("Update Name", "/update_name"),
        "<br>",
        Link("Home", "/")
    ])


@route
def update_name(state: State, new_name: str) -> Page:
    """Validates and updates the player's name."""

    if new_name.strip() == "":
        return Page(state, [
            Header("Invalid Name"),
            "Please enter a name.",
            "<br>",
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
        "<br>",
        Link("Home", "/")
    ])

start_server(State([], "Player", 20, -1, ""))
