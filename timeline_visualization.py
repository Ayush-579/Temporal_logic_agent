import matplotlib.pyplot as plt

def build_timeline():
    labels = [
        "Presidential Certification",
        "Topic 12 (upon cert)",
        "Topic 22 (12 + 45d)",
        "Protocol (cert + 45d)",
    ]
    # Since cert is pending, show everything as pending blocks, no concrete dates
    y = range(len(labels))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(y, [1]*len(labels), left=[0]*len(labels), color="orange", alpha=0.5)

    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Relative timeline (certification not yet occurred)")
    ax.set_title("Rule Lifecycles (All Pending Certification)")

    plt.tight_layout()
    plt.savefig("timeline_visualization.pdf")

if __name__ == "__main__":
    build_timeline()
    print("Wrote timeline_visualization.pdf")
