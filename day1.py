import pandas as pd


# ============================================================
# PART 1 — BASIC FANTASY FOOTBALL EXERCISES
# ============================================================

def calculate_average(points):
    total = sum(points)
    average = total / len(points)
    return average


def count_games_above(points, threshold):
    count = 0

    for score in points:
        if score >= threshold:
            count = count + 1

    return count


def get_projection(points):
    recent_points = points[-3:]
    projection = calculate_average(recent_points)

    return projection


def get_5_game_projection(points):
    recent_points = points[-5:]
    projection = calculate_average(recent_points)

    return projection


players = {
    "Justin Jefferson": [10, 15, 20, 25, 30],
    "Ja'Marr Chase": [18, 22, 14, 20, 19],
    "Bijan Robinson": [15, 17, 21, 24, 19]
}


actual_next_week = {
    "Justin Jefferson": 18,
    "Ja'Marr Chase": 21,
    "Bijan Robinson": 17
}


# ============================================================
# PART 2 — PUT OUR TOY DATA INTO A DATAFRAME
# ============================================================

rows = []

for player, points in players.items():

    for week, score in enumerate(points, start=1):

        row = {
            "Player": player,
            "Week": week,
            "Fantasy Points": score
        }

        rows.append(row)


df = pd.DataFrame(rows)

print(df)


# ============================================================
# PART 3 — COMPARE 3-GAME VS 5-GAME PROJECTIONS
# ============================================================

errors_3_game = []
errors_5_game = []


for player, points in players.items():

    total_points = sum(points)
    average_points = calculate_average(points)

    count = count_games_above(points, 20)

    projection = get_projection(points)
    projection_5 = get_5_game_projection(points)

    actual = actual_next_week[player]

    error = projection - actual
    error_5 = projection_5 - actual

    absolute_error_3 = abs(error)
    absolute_error_5 = abs(error_5)

    errors_3_game.append(absolute_error_3)
    errors_5_game.append(absolute_error_5)

    print(f"{player} scored a total of {total_points} points.")
    print(f"{player}'s average: {average_points}")
    print(f"{player} scored 20 or more points in {count} games.")
    print(f"{player}'s 3-game projection: {projection}")
    print(f"{player}'s 5-game projection: {projection_5}")
    print(f"{player}'s 3-game prediction error: {error}")
    print(f"{player}'s 3-game absolute prediction error: {absolute_error_3}")
    print(f"{player}'s 5-game prediction error: {error_5}")
    print(f"{player}'s 5-game absolute prediction error: {absolute_error_5}")
    print()


average_error_3_game = calculate_average(errors_3_game)
average_error_5_game = calculate_average(errors_5_game)

print(f"Average Absolute Error (3-game): {average_error_3_game}")
print(f"Average Absolute Error (5-game): {average_error_5_game}")


# ============================================================
# PART 4 — LOOK AT DATA FOR ONE PLAYER
# ============================================================

print(df[df["Player"] == "Justin Jefferson"])


# ============================================================
# PART 5 — TRAINING DATA
# ============================================================

training_data = df[df["Week"] <= 3]

print(training_data)


# ============================================================
# PART 6 — JUSTIN JEFFERSON: USE WEEKS 1–3 TO
#          PREDICT WEEK 4
# ============================================================

justin_training = df[
    (df["Player"] == "Justin Jefferson") &
    (df["Week"] <= 3)
]

print(justin_training["Fantasy Points"])


projection = justin_training["Fantasy Points"].mean()

print(projection)


actual = 25

error = projection - actual
absolute_error = abs(error)

print()
print(actual)
print(error)
print(absolute_error)


# ============================================================
# PART 7 — TEST DIFFERENT AMOUNTS OF TRAINING DATA
# ============================================================

errors_3_weeks = []
errors_4_weeks = []


for training_weeks in range(3, 5):

    for player in players:

        training_data = df[
            (df["Player"] == player) &
            (df["Week"] <= training_weeks)
        ]

        projection = training_data["Fantasy Points"].mean()

        # Because Python uses zero-based indexing:
        # index 3 = Week 4
        # index 4 = Week 5

        actual = players[player][training_weeks]

        error = projection - actual

        absolute_error = abs(error)

        if training_weeks == 3:
            errors_3_weeks.append(absolute_error)

        if training_weeks == 4:
            errors_4_weeks.append(absolute_error)

        print(
            f"{player} - "
            f"projection: {projection}, "
            f"Actual: {actual}, "
            f"Error: {error}, "
            f"Absolute Error: {absolute_error}"
        )


print(errors_3_weeks)
print(errors_4_weeks)


average_errors_3_weeks = (
    sum(errors_3_weeks) / len(errors_3_weeks)
)

average_errors_4_weeks = (
    sum(errors_4_weeks) / len(errors_4_weeks)
)


print(
    f"Average Absolute Error (3 weeks): "
    f"{average_errors_3_weeks}"
)

print(
    f"Average Absolute Error (4 weeks): "
    f"{average_errors_4_weeks}"
)


# ============================================================
# PART 8 — LOAD REAL NFL DATA
# ============================================================

real_df = pd.read_csv(
    "https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats.csv.gz"
)

print(real_df.head())


# ============================================================
# PART 9 — KEEP REGULAR SEASON ONLY
# ============================================================

regular_season = real_df[
    real_df["season_type"] == "REG"
]

print(
    "Regular season rows:",
    len(regular_season)
)


# ============================================================
# PART 10 — KEEP 2010 AND LATER
# ============================================================

model_data = regular_season[
    regular_season["season"] >= 2010
]

print(
    "2010+ regular season rows:",
    len(model_data)
)


# ============================================================
# PART 11 — LOOK AT JUSTIN JEFFERSON
# ============================================================

jefferson_regular = regular_season[
    regular_season["player_display_name"] == "Justin Jefferson"
]

print(
    jefferson_regular[[
        "season",
        "week",
        "receptions",
        "receiving_yards",
        "receiving_tds",
        "fantasy_points_ppr"
    ]]
)


# ============================================================
# PART 12 — JUSTIN JEFFERSON'S 2024 DATA
# ============================================================

jefferson_2024 = jefferson_regular[
    jefferson_regular["season"] == 2024
]

print(
    jefferson_2024[[
        "week",
        "receptions",
        "receiving_yards",
        "receiving_tds",
        "fantasy_points_ppr"
    ]]
)


print(
    "Official 2024 receptions:",
    jefferson_2024["receptions"].sum()
)


# ============================================================
# PART 13 — LOAD 2024 PLAY-BY-PLAY DATA
# ============================================================

pbp_2024 = pd.read_csv(
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2024.csv"
)

print(pbp_2024.head())


# ============================================================
# PART 14 — FIND JUSTIN JEFFERSON'S 2024 PLAYER ID
# ============================================================

print(
    jefferson_2024[[
        "player_id",
        "player_display_name"
    ]].drop_duplicates()
)


# ============================================================
# PART 15 — FIND JUSTIN JEFFERSON'S RECEIVING PLAYS
#          USING HIS UNIQUE PLAYER ID
# ============================================================

jefferson_plays = pbp_2024[
    pbp_2024["receiver_player_id"] == "00-0036322"
]

print(
    jefferson_plays[[
        "week",
        "play_type",
        "pass_attempt",
        "complete_pass",
        "receiver_player_id",
        "receiver_player_name",
        "receiving_yards"
    ]].head(30)
)


# ============================================================
# PART 16 — COUNT COMPLETED PASSES
# ============================================================

jefferson_receptions = pbp_2024[
    (pbp_2024["receiver_player_id"] == "00-0036322") &
    (pbp_2024["complete_pass"] == 1) &
    (pbp_2024["week"] <= 18)
]

print(
    "PBP receptions:",
    len(jefferson_receptions)
)


# ============================================================
# PART 17 — COMPARE PBP RECEPTIONS TO OFFICIAL STATS
# ============================================================

pbp_receptions_by_week = (
    jefferson_receptions
    .groupby("week")
    .size()
)


official_receptions_by_week = (
    jefferson_2024
    .set_index("week")["receptions"]
)


comparison = pd.DataFrame({
    "PBP Receptions": pbp_receptions_by_week,
    "Official Receptions": official_receptions_by_week
})


comparison["Difference"] = (
    comparison["PBP Receptions"] -
    comparison["Official Receptions"]
)


print(comparison)


# ============================================================
# PART 18 — FIND ANY WEEKS WHERE PBP DOESN'T MATCH
# ============================================================

print(
    comparison[
        comparison["Difference"] != 0
    ]
)


# ============================================================
# PART 19 — FIND JUSTIN JEFFERSON'S RECEIVING TDs
# ============================================================

jefferson_tds = pbp_2024[
    (pbp_2024["receiver_player_id"] == "00-0036322") &
    (pbp_2024["touchdown"] == 1) &
    (pbp_2024["week"] <= 18)
]
jefferson_receiving_yards = jefferson_receptions["receiving_yards"].sum()

print("Receiving_yards:", jefferson_receiving_yards)

print(
    jefferson_tds[[
        "game_id",
        "week",
        "receiver_player_id",
        "receiver_player_name",
        "receiving_yards",
        "touchdown",
        "pass_touchdown"
    ]]
)


# ============================================================
# PART 20 — FIND 40+ YARD RECEIVING TDs
# ============================================================

long_tds = jefferson_tds[
    jefferson_tds["receiving_yards"] >= 40
]

print(long_tds[[
    "week",
    "receiving_yards"
]])


long_td_count = len(long_tds)

print(
    "40+ yard TDs:",
    long_td_count
)


# ============================================================
# PART 21 — FIND 50+ YARD RECEIVING TDs
# ============================================================

very_long_tds = jefferson_tds[
    jefferson_tds["receiving_yards"] >= 50
]

print(very_long_tds[[
    "week",
    "receiving_yards"
]])


very_long_td_count = len(very_long_tds)

print(
    "50+ yard TDs:",
    very_long_td_count
)


# ============================================================
# PART 22 — CALCULATE JEFFERSON'S 2024 RECEIVING TD BONUSES
# ============================================================

receiving_td_points = len(jefferson_tds) * 6

bonus_40_points = len(long_tds) * 2

bonus_50_points = len(very_long_tds) * 3

total_td_points = (
    receiving_td_points +
    bonus_40_points +
    bonus_50_points
)


print(
    "Receiving TD points:",
    receiving_td_points
)

print(
    "40+ yard TD bonus:",
    bonus_40_points
)

print(
    "50+ yard TD bonus:",
    bonus_50_points
)

print(
    "Total receiving TD-related points:",
    total_td_points
)

receptions_points = len(jefferson_receptions) * 1

print("Reception points:", receptions_points)

receiving_yards_points = jefferson_receiving_yards / 10

print("Receiving yards points:", receiving_yards_points)

receiving_fantasy_points = (
    receptions_points
    + receiving_yards_points
    + total_td_points
)

print("Calculated receiving fantasy points:", receiving_fantasy_points)

jefferson_two_points = pbp_2024[
    (pbp_2024["receiver_player_id"] == "00-0036322") &
    (pbp_2024["two_point_conv_result"] == "success") &
    (pbp_2024["week"] <= 18)
]

print(jefferson_two_points)

jefferson_fumbles = pbp_2024[
    (pbp_2024["fantasy_player_id"] == "00-0036322") &
    (
        (pbp_2024["fumble_lost"] == 1) |
        (pbp_2024["fumble_forced"] == 1) |
        (pbp_2024["fumble_not_forced"] == 1)
    ) &
    (pbp_2024["week"] <= 18)
]

print(
    jefferson_fumbles[[
        "week",
        "play_type",
        "desc",
        "fumble_lost",
        "fumble_forced",
        "fumble_not_forced"
    ]]
)
print(
    jefferson_fumbles[[
        "week",
        "desc",
        "fumble_lost",
        "fumble_forced",
        "fumble_not_forced"
    ]].to_string(index=False)
)
week_9 = jefferson_receptions[
    jefferson_receptions["week"] == 9
]

print(week_9[[
    "receiving_yards",
    "receiver_player_name"
]])
print("Week 9 receptions:", len(week_9))
print("Week 9 receiving yards:", week_9["receiving_yards"].sum())

jefferson_week_9 = pbp_2024[
    (pbp_2024["fantasy_player_id"] == "00-0036322") &
    (pbp_2024["week"] == 9)
]

print(
    jefferson_week_9[[
        "play_type",
        "desc",
        "receiving_yards",
        "rushing_yards",
        "fumble_lost",
        "two_point_conv_result"
    ]].to_string(index=False)
)
jefferson_passes = pbp_2024[
    (pbp_2024["passer_player_id"] == "00-0036322") &
    (pbp_2024["week"] == 9)
]

print(
    jefferson_passes[[
        "desc",
        "passing_yards",
        "pass_attempt",
        "pass_touchdown"
    ]].to_string(index=False)
)
passing_yard_points = jefferson_passes["passing_yards"].sum() / 25

print("Passing yard points:", passing_yard_points)

passing_td_points = jefferson_passes["pass_touchdown"].sum() * 4
print("Passing TD points:", passing_td_points)

interception_points = jefferson_passes["interception"].sum() * -1
print("Interception points:", interception_points)

print(
    jefferson_passes[[
        "interception",
        "return_touchdown",
        "touchdown",
        "pass_touchdown"
    ]]
)
pick_six_points = (
    jefferson_passes["interception"] *
    jefferson_passes["return_touchdown"]
).sum() * -4

print("Pick-six points:", pick_six_points)

print(
    jefferson_passes[[
        "complete_pass",
        "yards_gained",
        "pass_touchdown"
    ]]
)
completion_40_bonus = (
    (jefferson_passes["complete_pass"] == 1) &
    (jefferson_passes["yards_gained"] >= 40)
).sum() * 2

print("40+ yard completion bonus:", completion_40_bonus)

print(
    jefferson_passes[[
        "two_point_attempt",
        "two_point_conv_result"
    ]]
)
passing_2pt_points = (
    jefferson_passes["two_point_conv_result"] == "pass"
).sum() * 2

print("Passing 2-point points:", passing_2pt_points)

jefferson_rushes = pbp_2024[
    (pbp_2024["rusher_player_id"] == "00-0036322") &
    (pbp_2024["week"] == 9)
]

print(
    jefferson_rushes[[
        "rush_attempt",
        "rushing_yards",
        "rush_touchdown"
    ]]
)
jefferson_fumbles_week9 = pbp_2024[
    (pbp_2024["fantasy_player_id"] == "00-0036322") &
    (pbp_2024["week"] == 9) &
    (pbp_2024["fumble_lost"] == 1)
]

print(jefferson_fumbles_week9)

# ============================================================
# END FOR NOW
# ============================================================