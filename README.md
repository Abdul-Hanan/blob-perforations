# Blob Perforations

Analyzes white blobs in a binary image to report the average number of internal holes per blob.

## Description

This project identifies distinct white regions (blobs) in a generated binary image and then counts the number of internal contours, referred to as "holes," within each identified blob. Finally, it calculates and displays the average number of holes found across all blobs. The process includes generating a synthetic test image, performing contour analysis using OpenCV, and saving a visual output with annotations.

## How to Run

1.  **Clone the repository** (or save `main.py`, `requirements.txt` to a local directory).
    ```bash
    # git clone <repo-url>
    # cd blob-perforations
    ```

2.  **Install dependencies:**
    Ensure you have `pip` installed. Then install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    Execute the `main.py` script. It will generate a synthetic image, perform the analysis, print a summary to the console, and save the annotated image.
    ```bash
    python main.py
    ```

## Output

After running, the script will:
-   Print a summary to the console detailing the total blobs found, the hole count for each blob, and the overall average number of holes per blob.
-   Save an image file named `output_perforations.png` in the same directory. This image will visually represent the analyzed blobs (outlined in blue), their internal holes (outlined in red), and text annotations indicating the hole count for each blob, as well as the overall average.