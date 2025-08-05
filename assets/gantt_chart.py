import matplotlib.pyplot as plt
import matplotlib.animation as animation


import tempfile

def draw_gantt_chart(execution_log, title="Gantt Chart"):
    if not execution_log:
        return None

    fig, ax = plt.subplots(figsize=(10, 3))
    y = 10
    height = 9

    pids = list(sorted(set(entry['pid'] for entry in execution_log)))
    colors = plt.cm.tab20.colors
    color_map = {pid: colors[i % len(colors)] for i, pid in enumerate(pids)}

    def animate(i):
        ax.clear()
        ax.set_ylim(5, 25)
        ax.set_xlim(0, max(entry['end'] for entry in execution_log) + 2)
        ax.set_yticks([])
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.grid(True, axis='x', linestyle='--', alpha=0.6)

        for j in range(i + 1):
            entry = execution_log[j]
            start = entry['start']
            duration = entry['end'] - entry['start']
            pid = entry['pid']
            ax.broken_barh([(start, duration)], (y, height),
                           facecolors=color_map[pid], edgecolors='black')
            ax.text(start + duration / 2, y + height / 2, pid,
                    ha='center', va='center', fontsize=10, fontweight='bold')
            ax.text(start, y - 2, str(start), ha='center', va='top', fontsize=8)

        if i == len(execution_log) - 1:
            ax.text(execution_log[-1]['end'], y - 2, str(execution_log[-1]['end']),
                    ha='center', va='top', fontsize=8)

    ani = animation.FuncAnimation(fig, animate, frames=len(execution_log),
                                  interval=1000, repeat=False)

    temp_file = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
    ani.save(temp_file.name, writer='pillow')

    plt.close(fig)
    return temp_file.name
 
 
