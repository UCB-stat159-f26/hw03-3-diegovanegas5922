import matplotlib.pyplot as plt

COLORS = {"Win": "#2B5C8F", "Loss": "#D95F02"}

def plot_age_difference(matches):
    fig, ax = plt.subplots(figsize=(12, 7))

    for result in ("Win", "Loss"):
        subset = matches[matches["Result"] == result]
        ax.scatter(subset["Player_Age"], subset["Age_Difference"], color=COLORS[result], alpha=0.7,
                   label=result, s=25, edgecolors="none")

    ax.axhline(0, color="gray", linewidth=1)
    ax.set_xlabel("Player Age")
    ax.set_ylabel("Player Age - Opponent Age")
    ax.set_title("Career Matches by Age Difference")
    ax.grid(alpha=0.15)
    ax.legend()

    return fig, ax


