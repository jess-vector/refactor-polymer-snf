import numpy as np
import matplotlib.pyplot as plt
import itertools

# Load data
interpolated_data = np.load('processed_data/tga/interpolated_tga_data.npy')
sample_names = []
with open('processed_data/tga/tga_sample_names.txt', 'r') as f:
    for line in f:
        if ':' in line:
            sample_names.append(line.split(': ')[1].strip())

# Verify we have the right number of samples
assert len(sample_names) == interpolated_data.shape[0], f"Sample count mismatch: {len(sample_names)} names vs {interpolated_data.shape[0]} data samples"

print(f"Loaded {len(sample_names)} TGA samples with {interpolated_data.shape[1]} data points each")

# Create color map for samples
colors = plt.cm.tab10(np.linspace(0, 1, len(sample_names)))

# Generate all possible pairs
sample_indices = list(range(len(sample_names)))
sample_pairs = list(itertools.combinations(sample_indices, 2))

print(f"Total number of sample pairs: {len(sample_pairs)}")

# Calculate global y-axis limits for difference plots
all_diffs = []
all_abs_diffs = []
for idx1, idx2 in sample_pairs:
    y1, y2 = interpolated_data[idx1], interpolated_data[idx2]
    y_diff = y1 - y2
    abs_diff = np.abs(y_diff)
    all_diffs.extend(y_diff)
    all_abs_diffs.extend(abs_diff)

diff_min, diff_max = min(all_diffs), max(all_diffs)
abs_diff_max = max(all_abs_diffs)

print(f"Global difference range: [{diff_min:.6f}, {diff_max:.6f}]")
print(f"Global max absolute difference: {abs_diff_max:.6f}")

pair_idx = 0
while 0 <= pair_idx < len(sample_pairs):
    idx1, idx2 = sample_pairs[pair_idx]
    name1, name2 = sample_names[idx1], sample_names[idx2]
    y1, y2 = interpolated_data[idx1], interpolated_data[idx2]

    nav = {'direction': 1}
    def on_key(event):
        if event.key in ['right', 'enter', 'return']:
            nav['direction'] = 1
            plt.close()
        elif event.key == 'left':
            nav['direction'] = -1
            plt.close()

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(f'TGA: {name1} vs {name2} - Difference Analysis', fontsize=16, fontweight='bold')

    # Plot 1: Vector representations (interpolated) - top left
    ax = axes[0, 0]
    ax.plot(range(len(y1)), y1, color=colors[idx1], label=f'{name1} (interpolated)', linewidth=1.5)
    ax.plot(range(len(y2)), y2, color=colors[idx2], label=f'{name2} (interpolated)', linewidth=1.5)
    ax.set_xlabel('Data Point Index (0-2999)')
    ax.set_ylabel('Weight Retention')
    ax.set_title('3000-dimensional Interpolated TGA Vectors')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    # Plot 2: Sample information - top right
    ax = axes[0, 1]
    ax.text(0.5, 0.5, f'Sample Pair:\n{name1}\nvs\n{name2}', 
            transform=ax.transAxes, fontsize=14, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Plot 3: Difference between y-values vs data point index - bottom left
    ax = axes[1, 0]
    y_diff = y1 - y2
    ax.plot(range(len(y_diff)), y_diff, color='red', linewidth=1.5, label='Difference')
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax.set_xlabel('Data Point Index (0-2999)')
    ax.set_ylabel(f'Weight Retention Difference ({name1} - {name2})')
    ax.set_title('Difference Between Weight Retention vs Data Point Index')
    ax.set_ylim(diff_min, diff_max)
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    
    # Add statistics
    mean_diff = np.mean(y_diff)
    std_diff = np.std(y_diff)
    max_diff = np.max(np.abs(y_diff))
    ax.text(0.05, 0.95, f'Mean diff: {mean_diff:.6f}\nStd diff: {std_diff:.6f}\nMax abs diff: {max_diff:.6f}', 
            transform=ax.transAxes, fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
            verticalalignment='top')

    # Plot 4: Absolute difference vs data point index - bottom right
    ax = axes[1, 1]
    abs_diff = np.abs(y_diff)
    ax.plot(range(len(abs_diff)), abs_diff, color='purple', linewidth=1.5, label='Absolute Difference')
    ax.set_xlabel('Data Point Index (0-2999)')
    ax.set_ylabel(f'Absolute Weight Retention Difference |{name1} - {name2}|')
    ax.set_title('Absolute Difference vs Data Point Index')
    ax.set_ylim(0, abs_diff_max)
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    
    # Add statistics
    mean_abs_diff = np.mean(abs_diff)
    max_abs_diff = np.max(abs_diff)
    ax.text(0.05, 0.95, f'Mean abs diff: {mean_abs_diff:.6f}\nMax abs diff: {max_abs_diff:.6f}', 
            transform=ax.transAxes, fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.8),
            verticalalignment='top')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()

    pair_idx += nav['direction']
    if pair_idx < 0:
        pair_idx = 0
    elif pair_idx >= len(sample_pairs):
        print("Reached the end of all sample pairs.")
        break 