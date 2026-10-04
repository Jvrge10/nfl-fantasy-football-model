import pandas as pd


# ==========================================
# 1. BASIC PRACTICE FUNCTIONS
# ==========================================

def calculate_average(points):
    return sum(points) / len(points)


def get_recent_average(points, games=3):
    recent_points = points[-games:]
    return sum(recent_points) / len(recent_points)


# ==========================================
# 2. TOY PRACTICE DATA
# ==========================================

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


# ==========================================
# 3. TOY PROJECTIONS
# ==========================================

print("===== TOY PROJECTIONS =====")

for player, points in players.items():

    average = calculate_average(points)
    recent_average = get_recent_average(points, 3)

    print("\nPlayer:", player)
    print("Average:", average)
    print("Last 3 games:", recent_average)


# ==========================================
# 4. TOY DATAFRAME
# ==========================================

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

print("\n===== TOY DATAFRAME =====")
print(df)


# ==========================================
# 5. LOAD REAL NFL WEEKLY DATA
# ==========================================

real_df = pd.read_csv(
    "https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats.csv.gz"
)


# ==========================================
# 6. KEEP REGULAR SEASON
# ==========================================

real_df = real_df[
    real_df["season_type"] == "REG"
]


# ==========================================
# 7. KEEP 2010 AND LATER
# ==========================================

real_df = real_df[
    real_df["season"] >= 2010
]


print("\n===== REAL NFL DATA =====")
print("Rows:", len(real_df))
print(
    "Seasons:",
    real_df["season"].min(),
    "-",
    real_df["season"].max()
)


# ==========================================
# 8. LOAD 2024 PLAY-BY-PLAY DATA
# ==========================================

pbp_2024 = pd.read_csv(
    "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2024.csv"
)


print("\n===== 2024 PBP DATA =====")
print("Rows:", len(pbp_2024))
print("Columns:", len(pbp_2024.columns))


# ==========================================
# 9. REGULAR SEASON PBP
# ==========================================

regular_season_pbp = pbp_2024[
    pbp_2024["week"] <= 18
]


# ==========================================
# 10. PLAYER IDS
# ==========================================

jefferson_id = "00-0036322"
lamar_id = "00-0034796"
bijan_id = "00-0038542"


print("\n===== PLAYER IDS =====")
print("Justin Jefferson:", jefferson_id)
print("Lamar Jackson:", lamar_id)
print("Bijan Robinson:", bijan_id)


# ==========================================
# 11. CUSTOM FANTASY SCORING ENGINE
# ==========================================

def calculate_fantasy_points(player_id, pbp):

    # =========================
    # RECEIVING
    # =========================

    receiving_plays = pbp[
        pbp["receiver_player_id"] == player_id
    ]

    receptions = receiving_plays["complete_pass"].sum()
    receiving_yards = receiving_plays["receiving_yards"].sum()
    receiving_tds = receiving_plays["pass_touchdown"].sum()

    receiving_40_plus_tds = receiving_plays[
        (receiving_plays["pass_touchdown"] == 1) &
        (receiving_plays["receiving_yards"] >= 40)
    ]

    receiving_50_plus_tds = receiving_plays[
        (receiving_plays["pass_touchdown"] == 1) &
        (receiving_plays["receiving_yards"] >= 50)
    ]

    receiving_points = (
        receptions * 1
        + receiving_yards / 10
        + receiving_tds * 6
        + len(receiving_40_plus_tds) * 2
        + len(receiving_50_plus_tds) * 3
    )


    # =========================
    # RUSHING
    # =========================

    rushing_plays = pbp[
        pbp["rusher_player_id"] == player_id
    ]

    rushing_yards = rushing_plays["rushing_yards"].sum()
    rushing_tds = rushing_plays["rush_touchdown"].sum()

    rushing_40_plus_tds = rushing_plays[
        (rushing_plays["rush_touchdown"] == 1) &
        (rushing_plays["rushing_yards"] >= 40)
    ]

    rushing_50_plus_tds = rushing_plays[
        (rushing_plays["rush_touchdown"] == 1) &
        (rushing_plays["rushing_yards"] >= 50)
    ]

    rushing_points = (
        rushing_yards / 10
        + rushing_tds * 6
        + len(rushing_40_plus_tds) * 2
        + len(rushing_50_plus_tds) * 3
    )


    # =========================
    # PASSING
    # =========================

    passing_plays = pbp[
        pbp["passer_player_id"] == player_id
    ]

    passing_yards = passing_plays["passing_yards"].sum()
    passing_tds = passing_plays["pass_touchdown"].sum()
    interceptions = passing_plays["interception"].sum()

    passing_40_plus_completions = passing_plays[
        (passing_plays["complete_pass"] == 1) &
        (passing_plays["passing_yards"] >= 40)
    ]

    passing_40_plus_td = passing_plays[
        (passing_plays["pass_touchdown"] == 1) &
        (passing_plays["passing_yards"] >= 40)
    ]

    passing_50_plus_td = passing_plays[
        (passing_plays["pass_touchdown"] == 1) &
        (passing_plays["passing_yards"] >= 50)
    ]

    pick_sixes_thrown = passing_plays[
        (passing_plays["interception"] == 1) &
        (passing_plays["return_touchdown"] == 1)
    ]

    passing_points = (
        passing_yards / 25
        + passing_tds * 4
        - interceptions * 1
        - len(pick_sixes_thrown) * 4
        + len(passing_40_plus_completions) * 2
        + len(passing_40_plus_td) * 3
        + len(passing_50_plus_td) * 4
    )


    # =========================
    # 2-POINT CONVERSIONS
    # =========================

    passing_2pt = passing_plays[
        passing_plays["two_point_conv_result"] == "success"
    ]

    rushing_2pt = rushing_plays[
        rushing_plays["two_point_conv_result"] == "success"
    ]

    receiving_2pt = receiving_plays[
        receiving_plays["two_point_conv_result"] == "success"
    ]

    two_point_points = (
        len(passing_2pt) * 2
        + len(rushing_2pt) * 2
        + len(receiving_2pt) * 2
    )


    # =========================
    # FUMBLES
    # =========================
    #
    # IMPORTANT:
    # Use fumbled_1_player_id to identify
    # the actual player who fumbled.
    # =========================

    player_fumbles = pbp[
        (pbp["fumbled_1_player_id"] == player_id) &
        (pbp["fumble_lost"] == 1)
    ]

    fumbles_lost = player_fumbles["fumble_lost"].sum()

    fumble_points = fumbles_lost * -2


    # =========================
    # TOTAL
    # =========================

    total_points = (
        receiving_points
        + rushing_points
        + passing_points
        + two_point_points
        + fumble_points
    )

    return total_points


# ==========================================
# 12. JUSTIN JEFFERSON TEST
# ==========================================

jefferson_points = calculate_fantasy_points(
    jefferson_id,
    regular_season_pbp
)

print("\n===== SCORING ENGINE TEST =====")
print(
    "Justin Jefferson calculated points:",
    round(jefferson_points, 2)
)


# ==========================================
# 13. WEEK 19 CHECK
# ==========================================

week_19_pbp = pbp_2024[
    pbp_2024["week"] == 19
]

week_19_points = calculate_fantasy_points(
    jefferson_id,
    week_19_pbp
)

print("\n===== WEEK 19 CHECK =====")
print(
    "Justin Jefferson Week 19 points:",
    round(week_19_points, 2)
)


# ==========================================
# 14. MULTIPLE PLAYER TEST
# ==========================================

test_players = {
    "Justin Jefferson": jefferson_id,
    "Lamar Jackson": lamar_id,
    "Bijan Robinson": bijan_id
}

print("\n===== MULTIPLE PLAYER TEST =====")

for player_name, player_id in test_players.items():

    points = calculate_fantasy_points(
        player_id,
        regular_season_pbp
    )

    print(
        player_name,
        ":",
        round(points, 2)
    )


# ==========================================
# 15. BIJAN ID CHECK
# ==========================================

print("\n===== BIJAN ID CHECK =====")

bijan_rows = real_df[
    real_df["player_display_name"].str.contains(
        "Bijan Robinson",
        case=False,
        na=False
    )
]

print(
    bijan_rows[
        ["player_id", "player_display_name", "season"]
    ].tail(10).to_string(index=False)
)


# ==========================================
# 16. LAMAR 2-POINT CHECK
# ==========================================

print("\n===== LAMAR 2-POINT CHECK =====")

lamar_2pt = regular_season_pbp[
    (regular_season_pbp["fantasy_player_id"] == lamar_id) &
    (regular_season_pbp["two_point_conv_result"] == "success")
]

print(
    lamar_2pt[
        ["week", "desc", "two_point_conv_result"]
    ].to_string(index=False)
)


# ==========================================
# 17. LAMAR WEEKLY COMPARISON
# ==========================================

print("\n===== LAMAR WEEKLY COMPARISON =====")

for week in range(1, 19):

    week_pbp = regular_season_pbp[
        regular_season_pbp["week"] == week
    ]

    model_points = calculate_fantasy_points(
        lamar_id,
        week_pbp
    )

    official_points = real_df[
        (real_df["season"] == 2024) &
        (real_df["week"] == week) &
        (real_df["player_id"] == lamar_id)
    ]["fantasy_points_ppr"].sum()

    difference = model_points - official_points

    print(
        f"Week {week}: "
        f"Model = {model_points:.2f}, "
        f"Sleeper = {official_points:.2f}, "
        f"Difference = {difference:.2f}"
    )


# ==========================================
# 18. LAMAR WEEKLY SCORES
# ==========================================

print("\n===== LAMAR WEEKLY SCORES =====")

for week in range(1, 19):

    week_data = regular_season_pbp[
        regular_season_pbp["week"] == week
    ]

    score = calculate_fantasy_points(
        lamar_id,
        week_data
    )

    print(
        "Week",
        week,
        ":",
        round(score, 2)
    )


# ==========================================
# 19. LAMAR WEEK 11 VALIDATION
# ==========================================

print("\n===== LAMAR WEEK 11 VALIDATION =====")

lamar_week11 = regular_season_pbp[
    regular_season_pbp["week"] == 11
]

week11_points = calculate_fantasy_points(
    lamar_id,
    lamar_week11
)

official_week11 = 17.88

print("Week 11 model:", round(week11_points, 2))
print("Sleeper:", official_week11)
print(
    "Difference:",
    round(week11_points - official_week11, 2)
)


# ==========================================
# 20. LAMAR WEEK 11 40+ PASS CHECK
# ==========================================

lamar_40_plus = regular_season_pbp[
    (regular_season_pbp["week"] == 11) &
    (regular_season_pbp["passer_player_id"] == lamar_id) &
    (regular_season_pbp["passing_yards"] >= 40)
]

print("\n===== LAMAR WEEK 11 40+ PASS CHECK =====")

print(
    lamar_40_plus[
        [
            "desc",
            "complete_pass",
            "passing_yards",
            "pass_touchdown"
        ]
    ].to_string(index=False)
)