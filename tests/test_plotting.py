import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from tennis_age import plot_age_difference
def test_plot_age_difference():
    matches = pd.DataFrame({"Player_Age": [20, 21, 22], "Age_Difference": [-3, 2, 0],
                            "Result": ["Win", "Loss", "Win"],})
    fig, ax = plot_age_difference(matches)
    assert fig is not None
    assert ax is not None
    assert len(ax.collections) == 2

    plt.close(fig)

