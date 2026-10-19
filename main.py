import cv2
import numpy as np

# --- Project Configuration ---
OUTPUT_IMAGE_PATH = "output_perforations.png"
TEXT_COLOR = (0, 255, 0) # Green in BGR
BLOB_COLOR = (255, 0, 0) # Blue in BGR
HOLE_COLOR = (0, 0, 255) # Red in BGR
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_SCALE = 0.5
TEXT_THICKNESS = 1
BORDER_MARGIN = 10 # Margin for overall summary text

def create_synthetic_image(width=600, height=400):
    """
    Generates a synthetic binary image with distinct white blobs, some with holes.
    """
    img = np.zeros((height, width), dtype=np.uint8)

    # Blob 1: Rectangle without holes
    cv2.rectangle(img, (50, 50), (150, 150), 255, -1)

    # Blob 2: Circle with one hole
    cv2.circle(img, (250, 100), 70, 255, -1) # Outer circle
    cv2.circle(img, (250, 100), 30, 0, -1)   # Inner black circle (hole)

    # Blob 3: Larger rectangle with two holes
    cv2.rectangle(img, (350, 50), (550, 200), 255, -1)
    cv2.circle(img, (400, 100), 20, 0, -1) # Hole 1
    cv2.circle(img, (500, 150), 25, 0, -1) # Hole 2

    # Blob 4: Irregular shape (union of two circles) with one hole
    # Create an initial blob by combining two circles
    temp_mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(temp_mask, (100, 300), 60, 255, -1)
    cv2.circle(temp_mask, (150, 300), 50, 255, -1)
    img = cv2.bitwise_or(img, temp_mask)
    # Add a hole to it
    cv2.circle(img, (120, 300), 30, 0, -1)

    # Blob 5: Rectangle with a large, somewhat irregular hole
    cv2.rectangle(img, (300, 250), (500, 350), 255, -1)
    # Draw a black star-like shape for an irregular hole
    pts = np.array([[350, 300], [380, 280], [400, 320], [370, 340], [330, 310]], np.int32)
    pts = pts.reshape((-1, 1, 2)) # Reshape for fillPoly
    cv2.fillPoly(img, [pts], 0)

    return img

def main():
    """
    Main function to generate image, identify blobs/holes,
    calculate average holes, and save output.
    """
    print("Generating synthetic binary image...")
    synthetic_img = create_synthetic_image()

    # Prepare a color image for visualization
    output_img_display = cv2.cvtColor(synthetic_img, cv2.COLOR_GRAY2BGR)

    print("Finding contours (blobs and holes)...")
    # Use RETR_CCOMP to retrieve all contours and organize them into a two-level hierarchy.
    # Level 1 contours are external boundaries, and Level 2 contours are holes.
    contours, hierarchy = cv2.findContours(synthetic_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    blob_hole_counts = []
    total_blobs_found = 0

    if contours and hierarchy is not None:
        # hierarchy is a numpy array of shape (1, N, 4)
        # For each contour i, hierarchy[0, i] = [next, previous, child, parent]
        # parent == -1 indicates an external contour (a distinct white blob)
        print(f"Found {len(contours)} raw contours in total (including holes).")

        for i in range(len(contours)):
            # Check if it's an external contour (parent is -1)
            if hierarchy[0][i][3] == -1:
                total_blobs_found += 1
                num_holes = 0
                
                # Get the index of the first child contour (which is a hole)
                child_idx = hierarchy[0][i][2]
                
                # Iterate through all children (holes) of this blob
                while child_idx != -1:
                    num_holes += 1
                    # Draw the hole contour on the display image
                    cv2.drawContours(output_img_display, contours, child_idx, HOLE_COLOR, 1)
                    # Move to the next sibling child
                    child_idx = hierarchy[0][child_idx][0]
                
                blob_hole_counts.append(num_holes)

                # Draw the external blob contour on the display image
                cv2.drawContours(output_img_display, contours, i, BLOB_COLOR, 2)

                # Place text indicating hole count near the blob's centroid
                M = cv2.moments(contours[i])
                if M["m00"] != 0: # Avoid division by zero for very small or degenerate contours
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # Ensure text stays within image bounds (simple clipping)
                    cX = max(BORDER_MARGIN, min(output_img_display.shape[1] - BORDER_MARGIN, cX))
                    cY = max(BORDER_MARGIN + int(TEXT_SCALE * 20), min(output_img_display.shape[0] - BORDER_MARGIN, cY))
                    
                    cv2.putText(output_img_display, f"Holes: {num_holes}", (cX - 40, cY),
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
    else:
        print("No contours found. Ensure the image has white blobs.")

    average_holes_per_blob = np.mean(blob_hole_counts) if blob_hole_counts else 0

    # Add global summary text at the top-left
    summary_text = f"Total Blobs: {total_blobs_found}, Avg. Holes per Blob: {average_holes_per_blob:.2f}"
    cv2.putText(output_img_display, summary_text, (BORDER_MARGIN, BORDER_MARGIN + 15), # Adjusted Y position for visibility
                TEXT_FONT, TEXT_SCALE * 1.2, TEXT_COLOR, TEXT_THICKNESS + 1)

    print(f"\n--- Analysis Summary ---")
    print(f"Total distinct white blobs found: {total_blobs_found}")
    print(f"Holes found per blob: {blob_hole_counts}")
    print(f"Average number of holes per blob: {average_holes_per_blob:.2f}")

    print(f"\nSaving visual output to {OUTPUT_IMAGE_PATH}")
    cv2.imwrite(OUTPUT_IMAGE_PATH, output_img_display)
    print("Script finished. Check the output image and console for results.")

if __name__ == "__main__":
    main()