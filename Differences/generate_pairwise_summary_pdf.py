import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib.backends.backend_pdf import PdfPages
import os

def load_data_and_names(data_type):
    """Load interpolated data and sample names for given data type."""
    if data_type == 'dsc':
        interpolated_data = np.load('processed_data/dsc/interpolated_dsc_data.npy')
        sample_names_file = 'processed_data/dsc/dsc_sample_names.txt'
        y_label = 'DSC Signal'
    elif data_type == 'tga':
        interpolated_data = np.load('processed_data/tga/interpolated_tga_data.npy')
        sample_names_file = 'processed_data/tga/tga_sample_names.txt'
        y_label = 'Weight Retention'
    else:
        raise ValueError("data_type must be 'dsc' or 'tga'")
    
    sample_names = []
    with open(sample_names_file, 'r') as f:
        for line in f:
            if ':' in line:
                sample_names.append(line.split(': ')[1].strip())
    
    return interpolated_data, sample_names, y_label

def create_pairwise_summary_pdf():
    """Generate a comprehensive PDF summary of pairwise differences for both DSC and TGA."""
    
    # Create output directory if it doesn't exist
    os.makedirs('Differences/summary_pdfs', exist_ok=True)
    
    # Generate summary for both DSC and TGA
    for data_type in ['dsc', 'tga']:
        print(f"Generating {data_type.upper()} pairwise summary...")
        
        # Load data
        interpolated_data, sample_names, y_label = load_data_and_names(data_type)
        
        # Generate all pairs
        sample_indices = list(range(len(sample_names)))
        sample_pairs = list(itertools.combinations(sample_indices, 2))
        
        # Calculate global limits
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
        
        # Create PDF
        pdf_filename = f'Differences/summary_pdfs/{data_type.upper()}_pairwise_summary.pdf'
        with PdfPages(pdf_filename) as pdf:
            
            # Title page
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.7, f'{data_type.upper()} Pairwise Difference Analysis', 
                   transform=ax.transAxes, fontsize=24, ha='center', va='center', fontweight='bold')
            ax.text(0.5, 0.5, f'Total Samples: {len(sample_names)}', 
                   transform=ax.transAxes, fontsize=16, ha='center', va='center')
            ax.text(0.5, 0.4, f'Total Pairs: {len(sample_pairs)}', 
                   transform=ax.transAxes, fontsize=16, ha='center', va='center')
            ax.text(0.5, 0.3, f'Data Points per Sample: {interpolated_data.shape[1]}', 
                   transform=ax.transAxes, fontsize=16, ha='center', va='center')
            ax.text(0.5, 0.2, f'Global Difference Range: [{diff_min:.6f}, {diff_max:.6f}]', 
                   transform=ax.transAxes, fontsize=12, ha='center', va='center')
            ax.text(0.5, 0.1, f'Max Absolute Difference: {abs_diff_max:.6f}', 
                   transform=ax.transAxes, fontsize=12, ha='center', va='center')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            pdf.savefig(fig)
            plt.close()
            
            # Average difference curve page
            print("  Creating average difference curve page...")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
            fig.suptitle(f'{data_type.upper()} Average Difference Analysis Across All Sample Pairs', fontsize=16, fontweight='bold')
            
            # Calculate average difference and standard deviation at each data point
            data_length = interpolated_data.shape[1]
            all_diffs_array = np.zeros((len(sample_pairs), data_length))
            all_abs_diffs_array = np.zeros((len(sample_pairs), data_length))
            
            for i, (idx1, idx2) in enumerate(sample_pairs):
                y1, y2 = interpolated_data[idx1], interpolated_data[idx2]
                all_diffs_array[i, :] = y1 - y2
                all_abs_diffs_array[i, :] = np.abs(y1 - y2)
            
            # Calculate mean and std at each data point for differences
            mean_diff_curve = np.mean(all_diffs_array, axis=0)
            std_diff_curve = np.std(all_diffs_array, axis=0)
            
            # Calculate mean and std at each data point for absolute differences
            mean_abs_diff_curve = np.mean(all_abs_diffs_array, axis=0)
            std_abs_diff_curve = np.std(all_abs_diffs_array, axis=0)
            
            # Create x-axis
            x_points = range(data_length)
            
            # Top plot: Mean difference curve
            ax1.plot(x_points, mean_diff_curve, color='blue', linewidth=2, label='Mean Difference')
            ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            
            # Shade the range (mean ± std)
            ax1.fill_between(x_points, 
                          mean_diff_curve - std_diff_curve, 
                          mean_diff_curve + std_diff_curve, 
                          alpha=0.3, color='blue', label='±1 Standard Deviation')
            
            # Shade the range (mean ± 2*std)
            ax1.fill_between(x_points, 
                          mean_diff_curve - 2*std_diff_curve, 
                          mean_diff_curve + 2*std_diff_curve, 
                          alpha=0.1, color='blue', label='±2 Standard Deviations')
            
            ax1.set_xlabel('Data Point Index (0-2999)')
            ax1.set_ylabel(f'{y_label} Difference')
            ax1.set_title('Average Difference Curve')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Add statistics for difference curve
            overall_mean = np.mean(mean_diff_curve)
            overall_std = np.std(mean_diff_curve)
            max_abs_mean = np.max(np.abs(mean_diff_curve))
            
            stats_text_diff = f'Overall Mean: {overall_mean:.6f}\nOverall Std: {overall_std:.6f}\nMax Abs Mean: {max_abs_mean:.6f}'
            ax1.text(0.02, 0.98, stats_text_diff, transform=ax1.transAxes, fontsize=10,
                   verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
                   facecolor="lightblue", alpha=0.8))
            
            # Bottom plot: Mean absolute difference curve
            ax2.plot(x_points, mean_abs_diff_curve, color='red', linewidth=2, label='Mean Absolute Difference')
            
            # Shade the range (mean ± std)
            ax2.fill_between(x_points, 
                          mean_abs_diff_curve - std_abs_diff_curve, 
                          mean_abs_diff_curve + std_abs_diff_curve, 
                          alpha=0.3, color='red', label='±1 Standard Deviation')
            
            # Shade the range (mean ± 2*std)
            ax2.fill_between(x_points, 
                          mean_abs_diff_curve - 2*std_abs_diff_curve, 
                          mean_abs_diff_curve + 2*std_abs_diff_curve, 
                          alpha=0.1, color='red', label='±2 Standard Deviations')
            
            ax2.set_xlabel('Data Point Index (0-2999)')
            ax2.set_ylabel(f'Absolute {y_label} Difference')
            ax2.set_title('Average Absolute Difference Curve')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Add statistics for absolute difference curve
            overall_mean_abs = np.mean(mean_abs_diff_curve)
            overall_std_abs = np.std(mean_abs_diff_curve)
            max_mean_abs = np.max(mean_abs_diff_curve)
            
            stats_text_abs = f'Overall Mean: {overall_mean_abs:.6f}\nOverall Std: {overall_std_abs:.6f}\nMax Mean: {max_mean_abs:.6f}'
            ax2.text(0.02, 0.98, stats_text_abs, transform=ax2.transAxes, fontsize=10,
                   verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
                   facecolor="lightcoral", alpha=0.8))
            
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            pdf.savefig(fig)
            plt.close()
            
            # Process pairs - show interpolated data and difference plots on same page
            colors = plt.cm.tab10(np.linspace(0, 1, len(sample_names)))
            
            for pair_idx, (idx1, idx2) in enumerate(sample_pairs):
                name1, name2 = sample_names[idx1], sample_names[idx2]
                y1, y2 = interpolated_data[idx1], interpolated_data[idx2]
                y_diff = y1 - y2
                
                # Create figure with two subplots
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
                fig.suptitle(f'{data_type.upper()}: {name1} vs {name2}', fontsize=16, fontweight='bold')
                
                # Top plot: Interpolated data comparison
                ax1.plot(range(len(y1)), y1, color=colors[idx1], label=name1, linewidth=2)
                ax1.plot(range(len(y2)), y2, color=colors[idx2], label=name2, linewidth=2)
                ax1.set_xlabel('Data Point Index (0-2999)')
                ax1.set_ylabel(y_label)
                ax1.set_title('Interpolated Data Comparison')
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                
                # Bottom plot: Difference analysis
                ax2.plot(range(len(y_diff)), y_diff, color='red', linewidth=2, label='Difference')
                ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
                ax2.set_xlabel('Data Point Index (0-2999)')
                ax2.set_ylabel(f'{y_label} Difference ({name1} - {name2})')
                ax2.set_title('Difference Analysis')
                ax2.set_ylim(diff_min, diff_max)
                ax2.legend()
                ax2.grid(True, alpha=0.3)
                
                # Add statistics to both plots
                mean_diff = np.mean(y_diff)
                std_diff = np.std(y_diff)
                max_abs_diff = np.max(np.abs(y_diff))
                avg_abs_diff = np.mean(np.abs(y_diff))
                
                stats_text = f'Mean diff: {mean_diff:.6f}\nStd diff: {std_diff:.6f}\nMax abs diff: {max_abs_diff:.6f}\nAvg abs diff: {avg_abs_diff:.6f}'
                
                ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=10,
                        verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
                        facecolor="lightblue", alpha=0.8))
                
                ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, fontsize=10,
                        verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
                        facecolor="lightgreen", alpha=0.8))
                
                plt.tight_layout(rect=[0, 0, 1, 0.95])
                pdf.savefig(fig)
                plt.close()
                
                print(f"  Processed pair {pair_idx+1}/{len(sample_pairs)}: {name1} vs {name2}")
        
        print(f"  Saved {pdf_filename}")

if __name__ == "__main__":
    print("Generating pairwise difference summary PDFs...")
    create_pairwise_summary_pdf()
    print("Summary PDF generation complete!")
    print("\nGenerated files:")
    print("- Differences/summary_pdfs/DSC_pairwise_summary.pdf")
    print("- Differences/summary_pdfs/TGA_pairwise_summary.pdf") 