import os
import lightkurve as lk
import matplotlib.pyplot as plt
import random
from astroquery.mast import Catalogs

def generate_random_color():
    """Generate a random color in RGB format."""
    return [random.random(), random.random(), random.random()]

def fetch_star_temperature(tic_id):
    """Fetch the star's surface temperature (Teff) from the TESS Input Catalog."""
    try:
        star_info = Catalogs.query_object(f"TIC {tic_id}", catalog="TIC")
        if len(star_info) > 0 and 'Teff' in star_info.columns:
            return star_info[0]['Teff']
        return "Unknown"
    except Exception as e:
        print(f"Error fetching temperature for TIC {tic_id}: {e}")
        return "Unknown"

def filter_numeric_lightcurve(lc):
    """
    Ensures that the LightCurve object contains only numeric columns before binning.
    
    Parameters:
    - lc: LightCurve object to filter.
    
    Returns:
    - A filtered LightCurve object with only numeric columns.
    """
    try:
        lc = lc["time", "flux", "flux_err"]  # Retain only essential numeric columns
        return lc
    except KeyError as e:
        print(f"Error filtering light curve: {e}")
        return None

def plot_individual_sectors_with_time_binning(tic_id, bin_time_minutes=15):
    """
    Downloads all available light curves for the TIC ID, bins them based on a time interval, 
    and plots both the unbinned and binned light curves for each sector, using a random color for each plot.
    
    Parameters:
    - tic_id: The TIC ID to query.
    - bin_time_minutes: Time interval for binning, in minutes (default: 15 minutes).
    """
    # Convert binning time to days (Lightkurve uses days as the time unit)
    bin_time_days = bin_time_minutes / 24 / 60

    # Fetch star temperature
    temperature = fetch_star_temperature(tic_id)

    # Search for light curves
    search_result = lk.search_lightcurve(f"TIC {tic_id}")  # , author="SPOC"
    if len(search_result) == 0:
        print(f"No light curves found for TIC {tic_id}.")
        return
    
    # Create a folder for the TIC ID if it doesn't exist
    if not os.path.exists(str(tic_id)):
        os.makedirs(str(tic_id))
    
    # Iterate over each sector and plot individually, then save to the folder
    for i, lc_file in enumerate(search_result, start=1):
        # Download the light curve and filter numeric columns
        lc = lc_file.download()
        if lc is None:
            continue
        
        lc = filter_numeric_lightcurve(lc)
        if lc is None:
            print(f"Skipping sector {i} for TIC {tic_id} due to invalid data.")
            continue
        
        # Remove outliers
        lc = lc.remove_outliers(sigma=5)
        
        # Bin the light curve based on the specified time interval
        lc_binned = lc.bin(bin_time_days)
        
        # Generate a random color for the plot
        random_color = generate_random_color()
        
        # Plot the unbinned and binned light curves
        plt.figure(figsize=(10, 5))
        lc_binned.plot(marker='o', linewidth=0, color=random_color, alpha=0.8, markersize=5, label='Binned')
        
        # Add plot labels and legend
        plt.title(
            f"Light Curve for TIC {tic_id} (Sector {lc.sector})\n"
            f"Stellar Temperature: {temperature} K | Binned Interval: {bin_time_minutes} minutes"
        )
        plt.xlabel("Time [BTJD days]")
        plt.ylabel("Normalized Flux")
        plt.legend()

        # Save the plot with the correct file name inside the corresponding folder
        plt.savefig(f"{tic_id}/Sector{i}.png", format='png')
        plt.close()  # Close the plot to avoid display

# Function to process a list of TIC IDs
def process_tic_ids(tic_ids, bin_time_minutes=15):
    for tic_id in tic_ids:
        plot_individual_sectors_with_time_binning(tic_id, bin_time_minutes)

# List of TIC IDs to process
tic_ids = [
    "50365310", "65212867", "88863718", "106997505", "124709665", 
    "156115721", "169904935", "238597883", "277039287", "57299130", 
    "21720215", "263723967", "284300833", "269343479", "345724317", 
    "210904767", "329981856", "201175570"
]
process_tic_ids(tic_ids, bin_time_minutes=15)