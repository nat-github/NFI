import re


def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract rectangle coordinates
    rectangle_match = re.search(r"Rectangle\s*\((-?\d+,\s*-?\d+)\)", content)
    if not rectangle_match:
        raise ValueError("Invalid input file format: Rectangle not found.")

    rectangle = [tuple(map(float, coord.split(','))) for coord in re.findall(r"\((-?\d+,\s*-?\d+)\)", content)]

    # Extract points
    points_match = re.search(r"Points\s*\((-?\d+,\s*-?\d+)\)", content)
    if not points_match:
        raise ValueError("Invalid input file format: Points not found.")

    points = [tuple(map(float, coord.split(','))) for coord in re.findall(r"\((-?\d+,\s*-?\d+)\)", content)]

    return rectangle, points


def parse_output_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Extract visited points
    visited_points = []
    for line in content:
        match = re.match(r"\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)", line.strip())
        if match:
            visited_points.append((float(match.group(1)), float(match.group(2))))

    return visited_points


def is_point_in_rectangle(point, rectangle):
    x, y = point
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = rectangle
    return min(x1, x2, x3, x4) <= x <= max(x1, x2, x3, x4) and min(y1, y2, y3, y4) <= y <= max(y1, y2, y3, y4)


def verify_system(input_file, output_file, results_file):
    rectangle, expected_points = parse_input_file(input_file)
    actual_points = parse_output_file(output_file)

    results = []
    all_pass = True

    for i, (expected, actual) in enumerate(zip(expected_points, actual_points)):
        if expected == actual and is_point_in_rectangle(actual, rectangle):
            results.append(f"{expected} {actual} PASS")
        else:
            results.append(f"{expected} {actual} FAIL")
            all_pass = False
            print(f"Failure: Point {i + 1} - Expected {expected}, Actual {actual}")

    with open(results_file, 'w') as file:
        file.write("\n".join(results))

    if all_pass:
        print("All tests PASSED.")
    else:
        print("Some tests FAILED.")


input_file = "data/input_file.txt"
output_file = "data/output_file.txt"
results_file = "output/test_results.txt"

verify_system(input_file, output_file, results_file)